import os
from uuid import uuid4

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.deepseek import DeepSeek
from rich.pretty import pprint

# 使用 SQLite 数据库，无需安装 PostgreSQL
db = SqliteDb(db_file="tmp/agents.db")

#db.clear_memories()

session_id = str(uuid4())
john_doe_id = "john_doe@example.com"

agent = Agent(
    model=DeepSeek(  # 使用 DeepSeek 官方聊天模型
            api_key=os.getenv("DEEPSEEK_API_KEY")
        ),
    db=db,
    enable_user_memories=True,
)

agent.print_response(
    "My name is John Doe and I like to hike in the mountains on weekends.",
    stream=True,
    user_id=john_doe_id,
    session_id=session_id,
)

agent.print_response(
    "What are my hobbies?", stream=True, user_id=john_doe_id, session_id=session_id
)

memories = agent.get_user_memories(user_id=john_doe_id)
print("John Doe's memories:")
pprint(memories)

agent.print_response(
    "Ok i dont like hiking anymore, i like to play soccer instead.",
    stream=True,
    user_id=john_doe_id,
    session_id=session_id,
)

# You can also get the user memories from the agent
memories = agent.get_user_memories(user_id=john_doe_id)
print("John Doe's memories:")
pprint(memories)