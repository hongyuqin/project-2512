"""
直接调用 DeepSeek API，查看返回结果
用于理解 Tool Calling 的完整流程
"""
import json
import requests

# DeepSeek API 配置
API_KEY = "sk-a19832c6da69445d9f05d04116e0636c"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 构建请求消息（与 agno 框架发送的格式相同）
request_data = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "system",
            "content": "<instructions>\nWrite a report on the topic. Output only the report.\n</instructions>\n\n<additional_information>\n- Use markdown to format your answers.\n</additional_information>"
        },
        {
            "role": "user",
            "content": "Trending startups and products."
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_top_hackernews_stories",
                "description": "获取 Hacker News 热门故事",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "num_stories": {
                            "type": "integer",
                            "description": "要获取的故事数量"
                        }
                    },
                    "required": ["num_stories"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_user_details",
                "description": "获取 Hacker News 用户详情",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "用户名"
                        }
                    },
                    "required": ["username"]
                }
            }
        }
    ]
}

def main():
    print("=" * 80)
    print("发送给 DeepSeek API 的请求：")
    print("=" * 80)
    print(json.dumps(request_data, indent=2, ensure_ascii=False))
    print("\n")
    
    # 发送请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("=" * 80)
    print("正在调用 DeepSeek API...")
    print("=" * 80)
    
    try:
        response = requests.post(API_URL, json=request_data, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        print("\n")
        print("=" * 80)
        print("DeepSeek API 返回的完整响应：")
        print("=" * 80)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        print("\n")
        print("=" * 80)
        print("解析后的关键信息：")
        print("=" * 80)
        
        # 解析响应
        if "choices" in result and len(result["choices"]) > 0:
            choice = result["choices"][0]
            message = choice["message"]
            
            print(f"\n1. 角色 (role): {message.get('role')}")
            
            print(f"\n2. 文本内容 (content):")
            print(f"   {message.get('content', 'None')}")
            
            print(f"\n3. 工具调用 (tool_calls):")
            if "tool_calls" in message:
                for i, tool_call in enumerate(message["tool_calls"], 1):
                    print(f"\n   工具调用 {i}:")
                    print(f"   - ID: {tool_call.get('id')}")
                    print(f"   - Type: {tool_call.get('type')}")
                    print(f"   - Function Name: {tool_call.get('function', {}).get('name')}")
                    print(f"   - Function Arguments: {tool_call.get('function', {}).get('arguments')}")
            else:
                print("   (无工具调用)")
            
            print(f"\n4. Token 使用情况:")
            if "usage" in result:
                usage = result["usage"]
                print(f"   - Prompt Tokens: {usage.get('prompt_tokens')}")
                print(f"   - Completion Tokens: {usage.get('completion_tokens')}")
                print(f"   - Total Tokens: {usage.get('total_tokens')}")
        
        print("\n")
        print("=" * 80)
        print("总结：")
        print("=" * 80)
        print("DeepSeek 返回了一个包含工具调用的响应。")
        print("Agent 框架会解析这个响应，执行工具，然后将工具结果再次发送给 DeepSeek。")
        
    except requests.exceptions.RequestException as e:
        print(f"\n错误：API 调用失败")
        print(f"错误信息：{e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码：{e.response.status_code}")
            print(f"响应内容：{e.response.text}")

if __name__ == "__main__":
    main()
