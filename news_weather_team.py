from agno.models.deepseek import DeepSeek
from agno.team import Team
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

# Create specialized agents
news_agent = Agent(
    id="news-agent",
    name="News Agent",
    role="Get the latest news and provide summaries",
    tools=[DuckDuckGoTools()]
)

weather_agent = Agent(
    id="weather-agent",
    name="Weather Agent",
    role="Get weather information and forecasts",
    tools=[DuckDuckGoTools()]
)

# Create the team
team = Team(
    name="News and Weather Team",
    members=[news_agent, weather_agent],
    model=DeepSeek(  # 使用 DeepSeek 官方聊天模型
            api_key="sk-a19832c6da69445d9f05d04116e0636c"
        ),
    instructions="Coordinate with team members to provide comprehensive information. Delegate tasks based on the user's request."
)

team.print_response("What's the latest news and weather in Tokyo?", stream=True)
