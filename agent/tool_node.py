import json
from langchain_core.messages import ToolMessage
from agent.agent_state import AgentState

# Define tools
tools = None
tools_by_name = {tool.name: tool for tool in tools}

# Define agent tool node
def tool_node(state: AgentState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}