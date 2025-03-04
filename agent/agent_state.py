import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from typing import (
    Annotated,
    Sequence,
    TypedDict,
)
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from agent.interview_response import QAResult
from enum import Enum
from datetime import datetime
from langchain_core.messages import HumanMessage
from typing import List, Tuple
import operator

class Language(str, Enum):
    ENGLISH = "English"
    CHINESE = "Chinese"

def add_or_remove_messages(left: list[BaseMessage], right: list[BaseMessage] | list[str]) -> List[BaseMessage]:
    """Add or remove messages from the list.
    Args:
        left: The list of messages to add or remove from.
        right: The list of messages to add or remove.

        if right is a list of str, delete the message in right list from left list
        if right is a list of BaseMessage, add the messages in right list to left list

    Returns:
        The list of messages after adding or removing.
    """
    if isinstance(right, list) and all(isinstance(x, str) for x in right):
        # delete message in right list from left list
        return [msg for msg in left if msg.id not in right]
    else:
        return add_messages(left, right)


class AgentState(TypedDict):
    """The state of the agent."""
    start_time: datetime

    # chat history (for user interaction and display)
    messages: Annotated[List[BaseMessage], add_or_remove_messages] = []

    # question & answer history (question, answer, QAResult)
    qa_history: Annotated[List[Tuple[str, str, QAResult]], operator.add] = []

    # interview requirement
    job_title: str
    knowledge_points: str
    interview_time: int = 3
    language: Language = Language.ENGLISH

    # current user answer and feedback
    question: str | None = None
    user_answer: str | None = None
    analyze_answer_response: QAResult | None = None



def get_qa_history(qa_history: List[Tuple[str, str, QAResult]]) -> str:
    if len(qa_history) == 0:
        return "None"
    else:
        return "\n".join([f"{qa[2].summary}" for i, qa in enumerate(qa_history)])


if __name__ == "__main__":
    msgs1 = [HumanMessage(content="Hello", id="1"), HumanMessage(content="Hello again", id="2"), HumanMessage(content="Hello again", id="3")]
    msgs2 = [HumanMessage(content="Hello again", id="1"), HumanMessage(content="", id="2")]
    print("\n")
    print(add_or_remove_messages(msgs1, []))
    print("\n")
    print(add_or_remove_messages(msgs1, ["2", "3"]))
