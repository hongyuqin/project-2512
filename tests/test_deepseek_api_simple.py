"""
简化版：直接调用 DeepSeek API，查看返回结果
"""
import json
import requests

API_KEY = "sk-a19832c6da69445d9f05d04116e0636c"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 请求数据
data = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "system",
            "content": "你是一个有用的助手，可以使用工具来回答问题。"
        },
        {
            "role": "user",
            "content": "帮我查一下 Hacker News 的热门故事"
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
                            "description": "要获取的故事数量，默认20"
                        }
                    },
                    "required": []
                }
            }
        }
    ]
}

# 发送请求
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

print("发送请求...")
response = requests.post(API_URL, json=data, headers=headers)
result = response.json()

print("\n返回结果：")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 解析工具调用
if "choices" in result:
    message = result["choices"][0]["message"]
    print("\n文本内容：", message.get("content"))
    
    if "tool_calls" in message:
        print("\n工具调用：")
        for tool_call in message["tool_calls"]:
            func = tool_call["function"]
            print(f"  - {func['name']}({func['arguments']})")

