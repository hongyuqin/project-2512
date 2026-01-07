## 跑不通

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools

reddit_researcher = Agent(
    name="Reddit Researcher",
    role="Research a topic on Reddit",
    model=DeepSeek(
        api_key="sk-a19832c6da69445d9f05d04116e0636c"),
    tools=[DuckDuckGoTools()],
    add_name_to_context=True,
    instructions=dedent("""
    You are a Reddit researcher.
    You will be given a topic to research on Reddit.
    You will need to find the most relevant posts on Reddit.
    """),
)

hackernews_researcher = Agent(
    name="HackerNews Researcher",
    model=DeepSeek(
        api_key="sk-a19832c6da69445d9f05d04116e0636c"),
    role="Research a topic on HackerNews.",
    tools=[HackerNewsTools()],
    add_name_to_context=True,
    instructions=dedent("""
    You are a HackerNews researcher.
    You will be given a topic to research on HackerNews.
    You will need to find the most relevant posts on HackerNews.
    """),
)


agent_team = Team(
    name="Discussion Team",
    model=DeepSeek(
        api_key="sk-a19832c6da69445d9f05d04116e0636c"),
    members=[
        reddit_researcher,
        hackernews_researcher,
    ],
    instructions=[
        "You are a discussion master.",
        "You have to stop the discussion when you think the team has reached a consensus.",
    ],
    markdown=True,
    delegate_to_all_members=True,
    show_members_responses=True,
)


async def main():
    await agent_team.aprint_response(
        input="Start the discussion on the topic: 'What is the best way to learn to code?'",
        stream=True,
        stream_intermediate_steps=True,
    )


if __name__ == "__main__":
    asyncio.run(main())