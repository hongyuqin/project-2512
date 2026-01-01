"""
使用 agno 库创建 Agent 示例
优先学习 Agent 开发
"""
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.run.agent import RunEvent
from agno.tools.duckduckgo import DuckDuckGoTools


def main():
    # 初始化 Agent，使用 DeepSeek 的聊天模型
    agent = Agent(
        model=DeepSeek( # 使用 DeepSeek 官方聊天模型
            api_key="sk-a19832c6da69445d9f05d04116e0636c"
        ),
        tools=[DuckDuckGoTools()],
        instructions="你是一个简洁明了、适合初学者的技术助手"
    )

    ################ STREAM RESPONSE #################
    stream = agent.run("What are the latest news in AI?",stream=True)
    # Consume the streaming response
    for chunk in stream:
        if chunk.event == RunEvent.run_content:
            print(chunk.content)


if __name__ == '__main__':
    main()
