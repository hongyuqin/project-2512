# Project 2512 - AI Agent Development

AI Agent 开发项目，使用 Agno 框架构建智能代理应用。

## 项目结构

```
project-2512/
├── src/                    # 源代码目录
│   └── agents/            # Agent 核心代码
│       ├── __init__.py
│       ├── main.py
│       ├── agent_with_memory.py
│       ├── agent_with_knowledge.py
│       ├── agent_with_storage.py
│       ├── active_conversation_agent.py
│       ├── news_weather_team.py
│       └── agent_run_metadata.py
├── tests/                 # 测试代码
│   ├── test_deepseek_api.py
│   ├── test_deepseek_api_simple.py
│   ├── debug_agent1.py
│   ├── debug_agent2.py
│   ├── minimax_test.py
│   ├── minimax_test_t2a.py
│   ├── tts_test.py
│   └── bgm_test.py
├── examples/              # 示例代码
│   ├── minimax_tts_example.py
│   └── run_response_events.py
├── docs/                  # 文档
├── scripts/               # 脚本工具
├── tmp/                   # 临时文件和数据库
│   ├── agents.db
│   ├── data.db
│   └── lancedb/
├── pyproject.toml         # 项目配置
├── requirements.txt       # 依赖列表
├── .gitignore            # Git 忽略文件
└── README.md             # 项目说明
```

## 安装

1. 克隆项目：
```bash
git clone <repository-url>
cd project-2512
```

2. 创建虚拟环境：
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/Mac
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件，填入你的 API key
# DEEPSEEK_API_KEY=your_deepseek_api_key
# MINIMAX_API_KEY=your_minimax_api_key
```

## 主要功能

### 基础 Agent
- **agent_with_memory.py**: 带记忆功能的 Agent
- **agent_with_knowledge.py**: 带知识库的 RAG Agent
- **agent_with_storage.py**: 支持持久化存储的 Agent
- **active_conversation_agent.py**: 主动对话 Agent

### 团队协作
- **news_weather_team.py**: 新闻和天气信息团队

### 工具集成
- MiniMax TTS 语音合成
- DuckDuckGo 搜索工具
- DeepSeek API 集成

## 使用示例

### 运行基础 Agent
```bash
cd src/agents
python main.py
```

### 运行示例
```bash
cd examples
python minimax_tts_example.py
```

### 运行测试
```bash
python -m pytest tests/
```

### 启动 API 服务器
```bash
# 方式1：使用启动脚本
python scripts/start_api.py

# 方式2：直接使用 uvicorn
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

启动后访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/

### API 调用示例
```bash
# 聊天接口
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

## 开发

### 代码规范
项目使用以下工具保证代码质量：
- **Black**: 代码格式化
- **isort**: 导入排序
- **mypy**: 类型检查
- **flake8**: 代码检查

### 运行代码检查
```bash
# 格式化代码
black src/ tests/ examples/

# 排序导入
isort src/ tests/ examples/

# 类型检查
mypy src/

# 代码检查
flake8 src/ tests/ examples/
```

## 配置

项目使用以下 API 服务，请配置相应的环境变量：

```bash
# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key

# MiniMax API
MINIMAX_API_KEY=your_minimax_api_key

# OpenAI API (可选)
OPENAI_API_KEY=your_openai_api_key
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
