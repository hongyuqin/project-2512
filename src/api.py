"""
简单的 FastAPI demo - 提供 HTTP 接口给 App 调用
"""
import os
from fastapi import FastAPI
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools

# 创建 FastAPI 应用
app = FastAPI(title="AI Agent API", version="0.1.0")

# 请求模型
class ChatRequest(BaseModel):
    message: str

# 响应模型
class ChatResponse(BaseModel):
    response: str

@app.get("/")
def root():
    """健康检查"""
    return {"message": "AI Agent API is running"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    简单的聊天接口
    """
    # 创建 Agent 实例
    agent = Agent(
        model=DeepSeek(api_key=os.getenv("DEEPSEEK_API_KEY")),
        tools=[DuckDuckGoTools()],
        instructions="你是一个简洁明了、适合初学者的技术助手"
    )
    
    # 调用 Agent
    result = agent.run(request.message)
    
    return ChatResponse(response=result.content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
