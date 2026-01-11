from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=DeepSeek(  # 使用 DeepSeek 官方聊天模型
            api_key="sk-a19832c6da69445d9f05d04116e0636c"
        ),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
    debug_mode=True,
    # debug_level=2, # Uncomment to get more detailed logs
)

# Run agent and print response to the terminal
agent.print_response("Trending startups and products.")