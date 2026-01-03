from typing import Iterator, List

from agno.agent import (
    Agent,
    RunContentEvent,
    RunOutputEvent,
    ToolCallCompletedEvent,
    ToolCallStartedEvent,
)
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=DeepSeek(  # 使用 DeepSeek 官方聊天模型
            api_key="sk-a19832c6da69445d9f05d04116e0636c"
        ),
    tools=[DuckDuckGoTools()],
    markdown=True,
)
run_response: Iterator[RunOutputEvent] = agent.run(
    "Whats happening in USA and Canada?", stream=True
)

response: List[str] = []
for chunk in run_response:
    if isinstance(chunk, RunContentEvent):
        response.append(chunk.content)  # type: ignore
    elif isinstance(chunk, ToolCallStartedEvent):
        response.append(
            f"Tool call started: {chunk.tool.tool_name} with args: {chunk.tool.tool_args}"  # type: ignore
        )
    elif isinstance(chunk, ToolCallCompletedEvent):
        response.append(
            f"Tool call completed: {chunk.tool.tool_name} with result: {chunk.tool.result}"  # type: ignore
        )

print("\n".join(response))
