"""
主动对话 Agent - 用于冥想App的对话收集功能
AI会主动提问，通过5轮对话收集用户情绪和状态信息
"""
import os
from uuid import uuid4
from enum import Enum
from typing import Dict, List, Optional
from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.deepseek import DeepSeek


class ConversationState(Enum):
    """对话状态"""
    START = "start"           # 开始，AI主动打招呼
    COLLECTING = "collecting" # 收集信息中
    READY = "ready"           # 信息收集完成，准备生成
    COMPLETED = "completed"   # 对话完成


class ActiveConversationAgent:
    """主动对话Agent - 负责主动提问和收集信息"""
    
    def __init__(self, api_key: str, max_turns: int = 5):
        """
        初始化主动对话Agent
        
        Args:
            api_key: DeepSeek API Key
            max_turns: 最大对话轮数，默认5轮
        """
        self.db = SqliteDb(db_file="tmp/meditation_agents.db")
        self.max_turns = max_turns
        
        # 主动对话Agent - 负责提问
        self.conversation_agent = Agent(
            model=DeepSeek(api_key=api_key),
            db=self.db,
            instructions="""
            你是一位温柔的冥想引导师。你的任务是：
            1. 主动、温和地询问用户的情绪和状态
            2. 通过5-5轮对话了解用户当前的心理状态
            3. 每次只问一个问题，不要连续问多个问题
            4. 根据用户的回答，深入询问相关细节
            5. 当收集到足够信息时，用"好的，我了解了"来结束对话
            
            提问策略：
            - 第1轮：询问用户今天的心情或状态
            - 第2-3轮：深入了解情绪的具体表现（身体感受、想法等）
            - 第4-5轮：询问压力来源或困扰的事情
            - 第6-7轮：了解用户希望如何改善或放松
            - 第8-5轮：补充细节，确认理解
            
            语气要求：
            - 温柔、耐心、不催促
            - 使用"你感觉..."、"能告诉我..."等引导性语言
            - 避免说教，只是倾听和了解
            - 不要一次性问多个问题
            """,
            markdown=True
        )
        
        # 冥想生成Agent - 负责生成冥想引导文字
        self.meditation_generator_agent = Agent(
            model=DeepSeek(api_key=api_key),
            db=self.db,
            instructions="""
            你是一位专业的冥想内容创作者。你的任务是：
            1. 根据用户的情绪状态和对话内容，生成个性化的冥想引导文本
            2. 生成适合5分钟左右的冥想引导（约500-800字）
            3. 语速慢、句子短、温柔平静
            4. 没有说教、不做心理诊断
            5. 包含呼吸引导、身体放松、情绪接纳等内容
            
            冥想引导结构：
            - 开场：引导用户找到舒适的姿势，闭上眼睛
            - 呼吸引导：引导用户关注呼吸，自然呼吸
            - 身体扫描：引导用户放松身体各个部位
            - 情绪接纳：引导用户接纳当前的情绪状态
            - 正念练习：引导用户观察当下的感受，不评判
            - 结束：引导用户慢慢回到当下，睁开眼睛
            
            语气要求：
            - 温柔、平静、有节奏感
            - 使用"现在"、"请"、"慢慢"等引导词
            - 避免命令式，使用建议式
            - 句子简短，每句话后可以停顿
            """,
            markdown=True
        )
        
        # 对话状态
        self.state = ConversationState.START
        self.conversation_count = 0
        self.conversation_history: List[Dict] = []
        self.user_id: Optional[str] = None
        self.session_id: Optional[str] = None
    
    def start_conversation(self, user_id: str, session_id: Optional[str] = None) -> Dict:
        """
        开始主动对话
        
        Args:
            user_id: 用户ID
            session_id: 会话ID，如果不提供会自动生成
            
        Returns:
            包含AI主动问候消息的字典
        """
        self.user_id = user_id
        self.session_id = session_id or str(uuid4())
        self.state = ConversationState.START
        self.conversation_count = 0
        self.conversation_history = []
        
        # AI主动开始第一句话
        first_message = self._generate_first_message()
        
        # 记录AI的第一句话
        self.conversation_history.append({
            "role": "assistant",
            "content": first_message,
            "turn": 0
        })
        
        return {
            "message": first_message,
            "state": self.state.value,
            "turn": self.conversation_count,
            "session_id": self.session_id
        }
    
    def _generate_first_message(self) -> str:
        """生成第一句主动问候"""
        prompt = """
        作为冥想引导师，请主动向用户打招呼，并询问他们今天的心情或状态。
        要求：
        1. 温柔、自然，一句话即可
        2. 不要问多个问题
        3. 语气要温暖、耐心
        
        示例："你好，今天感觉怎么样？" 或 "你好，想聊聊你现在的状态吗？"
        """
        response = self.conversation_agent.run(
            prompt,
            user_id=self.user_id,
            session_id=self.session_id
        )
        return response.content.strip()
    
    def continue_conversation(self, user_input: str) -> Dict:
        """
        继续对话 - 用户回复后，AI主动提问
        
        Args:
            user_input: 用户的输入
            
        Returns:
            包含AI回复和对话状态的字典
        """
        # 更新状态
        if self.state == ConversationState.START:
            self.state = ConversationState.COLLECTING
        
        # 记录用户输入
        self.conversation_count += 1
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "turn": self.conversation_count
        })
        
        # 判断是否达到最大轮数
        if self.conversation_count >= self.max_turns:
            self.state = ConversationState.READY
            return self._finish_collection()
        
        # AI主动提问
        ai_response = self._generate_next_question()
        
        # 记录AI回复
        self.conversation_history.append({
            "role": "assistant",
            "content": ai_response,
            "turn": self.conversation_count
        })
        
        return {
            "message": ai_response,
            "state": self.state.value,
            "turn": self.conversation_count,
            "remaining_turns": self.max_turns - self.conversation_count,
            "total_turns": self.max_turns
        }
    
    def _generate_next_question(self) -> str:
        """生成下一个主动提问"""
        # 构建对话历史上下文（最近6轮对话）
        recent_history = self.conversation_history[-6:] if len(self.conversation_history) > 6 else self.conversation_history
        history_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in recent_history
        ])
        
        prompt = f"""
        基于以下对话历史，请主动提出下一个问题，深入了解用户的情绪和状态。
        
        对话历史：
        {history_text}
        
        要求：
        1. 根据用户刚才的回答，提出一个相关的深入问题
        2. 如果用户提到情绪，询问身体感受或具体表现
        3. 如果用户提到压力，询问来源或影响
        4. 如果已经了解较多信息，可以询问用户希望如何改善
        5. 只问一个问题，语气温柔自然
        6. 不要重复之前问过的问题
        
        当前对话轮数：{self.conversation_count}/{self.max_turns}
        
        请只输出你的问题，不要有其他解释。
        """
        
        response = self.conversation_agent.run(
            prompt,
            user_id=self.user_id,
            session_id=self.session_id
        )
        return response.content.strip()
    
    def _finish_collection(self) -> Dict:
        """完成信息收集"""
        self.state = ConversationState.READY
        
        # 总结对话内容
        summary = self._summarize_conversation()
        
        return {
            "message": "好的，我了解了。让我为你生成一段个性化的冥想引导。",
            "state": self.state.value,
            "summary": summary,
            "ready_to_generate": True,
            "turn": self.conversation_count,
            "conversation_history": self.conversation_history
        }
    
    def _summarize_conversation(self) -> str:
        """总结对话内容"""
        history_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history
        ])
        
        prompt = f"""
        请总结以下对话，提取用户的情绪状态和关键信息：
        
        {history_text}
        
        要求：
        1. 总结用户的情绪状态
        2. 提取关键问题和困扰
        3. 简洁明了，便于后续生成冥想内容
        """
        
        response = self.conversation_agent.run(
            prompt,
            user_id=self.user_id,
            session_id=self.session_id
        )
        return response.content.strip()
    
    def get_conversation_history(self) -> List[Dict]:
        """获取完整的对话历史"""
        return self.conversation_history.copy()
    
    def get_state(self) -> ConversationState:
        """获取当前状态"""
        return self.state
    
    def generate_meditation_text(self, summary: Optional[str] = None) -> Dict:
        """
        生成5分钟的冥想引导文字
        
        Args:
            summary: 对话总结，如果不提供则使用内部总结
            
        Returns:
            包含冥想引导文字的字典
        """
        if self.state != ConversationState.READY:
            raise ValueError("对话尚未完成，无法生成冥想内容。请先完成对话收集。")
        
        # 如果没有提供总结，使用内部总结
        if summary is None:
            summary = self._summarize_conversation()
        
        # 构建对话历史上下文
        history_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history
        ])
        
        prompt = f"""
        基于以下对话历史和总结，生成一段5分钟左右的个性化冥想引导文字。
        
        对话总结：
        {summary}
        
        完整对话历史：
        {history_text}
        
        要求：
        1. 生成适合5分钟左右的冥想引导（约500-800字）
        2. 根据用户的情绪状态和困扰，定制冥想内容
        3. 语速慢、句子短、温柔平静
        4. 包含以下部分：
           - 开场：引导找到舒适姿势，闭上眼睛
           - 呼吸引导：关注自然呼吸
           - 身体放松：引导放松身体各个部位
           - 情绪接纳：接纳当前的情绪状态
           - 正念练习：观察当下感受，不评判
           - 结束：慢慢回到当下，睁开眼睛
        
        5. 语气温柔、平静，使用"现在"、"请"、"慢慢"等引导词
        6. 每句话简短，适合慢速朗读
        7. 不要有说教，不要做心理诊断
        8. 直接输出冥想引导文字，不要有其他解释
        
        请开始生成冥想引导文字：
        """
        
        response = self.meditation_generator_agent.run(
            prompt,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        meditation_text = response.content.strip()
        
        # 更新状态
        self.state = ConversationState.COMPLETED
        
        return {
            "meditation_text": meditation_text,
            "summary": summary,
            "word_count": len(meditation_text),
            "estimated_duration": "约5分钟",
            "state": self.state.value
        }


def main():
    """测试主动对话Agent"""
    # 配置API Key（使用项目中的DeepSeek API Key）
    API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    # 创建Agent实例
    agent = ActiveConversationAgent(api_key=API_KEY, max_turns=5)
    
    print("=" * 60)
    print("冥想引导 - 主动对话测试")
    print("=" * 60)
    print()
    
    # 1. 开始对话 - AI主动打招呼
    user_id = "test_user_001"
    result = agent.start_conversation(user_id=user_id)
    
    print(f"AI: {result['message']}")
    print(f"[状态: {result['state']}, 轮数: {result['turn']}/{result.get('total_turns', 5)}]")
    print()
    
    # 2. 循环对话直到达到最大轮数
    while agent.get_state() != ConversationState.READY:
        # 获取用户输入
        user_input = input("你: ").strip()
        
        if not user_input:
            print("请输入你的回复...")
            continue
        
        # AI继续提问
        result = agent.continue_conversation(user_input)
        
        print(f"AI: {result['message']}")
#        print(f"[状态: {result['state']}, 轮数: {result['turn']}/{result['total_turns']}, 剩余: {result['remaining_turns']}轮]")

    
    # 3. 显示对话总结
    print("=" * 60)
    print("对话收集完成！")
    print("=" * 60)
    print(f"\n对话总结：\n{result['summary']}")
    print()
    
    # 4. 显示完整对话历史
    print("=" * 60)
    print("完整对话历史：")
    print("=" * 60)
    for msg in result['conversation_history']:
        role = "AI" if msg['role'] == 'assistant' else "用户"
        print(f"[{role}] (第{msg['turn']}轮): {msg['content']}")
    
    # 5. 生成冥想引导文字
    print("\n" + "=" * 60)
    print("正在生成冥想引导文字...")
    print("=" * 60)
    
    meditation_result = agent.generate_meditation_text(summary=result['summary'])
    
    print(f"\n✅ 冥想引导生成完成！")
    print(f"字数: {meditation_result['word_count']} 字")
    print(f"预计时长: {meditation_result['estimated_duration']}")
    print("\n" + "-" * 60)
    print("冥想引导文字：")
    print("-" * 60)
    print(meditation_result['meditation_text'])
    print("-" * 60)
    
    print("\n✅ 测试完成！")


if __name__ == "__main__":
    main()

