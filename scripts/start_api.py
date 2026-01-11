#!/usr/bin/env python3
"""
启动 API 服务器
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式，代码变更自动重载
    )
