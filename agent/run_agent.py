
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.graph import StateGraph
import uuid
import os
from datetime import datetime
import json
from pydantic import BaseModel, Field
from workflow import build_graph
from langgraph.types import Command
from langgraph.types import StateSnapshot

def execute_ai_interview_agent(workflow):
    config = {
        "configurable": {"thread_id": uuid.uuid4(), "user_id": "Interviewer"},
        "model_name": "gpt-4o",
    }

    inputs = {
        "start_time": datetime.now(),
        "messages": [],
        "job_title": "Java API Engineer",
        "knowledge_points": "Java, SpringBoot",
        "interview_time": 3,
        "language": "Chinese"
    }

    events = workflow.stream(inputs, config=config, stream_mode="values")
    for event in events:
        if "messages" in event and len(event["messages"]) > 0:
            message = event["messages"][-1]
            print(message)

    snapshot: StateSnapshot = workflow.get_state(config)
    while snapshot.next:        
        
        question = snapshot.values["question"]
        print("AI :> " + question.question)

        user_input = input('User :> ')
        events = workflow.invoke(Command(resume="Go ahead", update={"user_answer": user_input}), config=config)
        for event in events:
            print(event)

        snapshot = workflow.get_state(config)



if __name__ == "__main__":
    workflow = build_graph()
    execute_ai_interview_agent(workflow)