from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.deepseek import DeepSeek
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=DeepSeek(  # 使用 DeepSeek 官方聊天模型
            api_key="sk-a19832c6da69445d9f05d04116e0636c"
        ),
    tools=[HackerNewsTools()],
    db=SqliteDb(db_file="tmp/data.db"),
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

# Run agent as an interactive CLI app
agent.cli_app(stream=True)
