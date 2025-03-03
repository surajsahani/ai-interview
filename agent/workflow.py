import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
import json
from langchain_core.messages import ToolMessage, SystemMessage, AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from agent.agent_state import AgentState
from pydantic import BaseModel, Field   
from utils.prompt_utils import load_prompt
from utils.llm import get_model
from agent.interview_response import Question, AnalyzeAnswerResponse
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime

def kickoff_interview(state: AgentState,     
                      config: RunnableConfig):
    
    print("========== Kickoff Interview ==========")

    prompt_content: str = load_prompt('prompts/kickoff_interview.txt')
    human_prompt: HumanMessage = HumanMessage(content=prompt_content.format(job_title=state["job_title"], 
                                                              knowledge_points=state["knowledge_points"],
                                                              interview_time=state["interview_time"],
                                                              language=state["language"]))

    model_name: str = config["configurable"].get("model_name", "gpt-4o")
    model: ChatOpenAI = get_model(model=model_name).with_structured_output(Question, strict=True, method="json_schema")
    
    print("System :> " + human_prompt.content)
    response: Question = model.invoke([human_prompt])

    ai_response: AIMessage = AIMessage(content=response.model_dump_json(indent=2))
    print("AI :> " + response.model_dump_json(indent=2))

    return {
        "messages": [human_prompt, response.question],
        "question": response
    }


def analyze_answer(state: AgentState,   
                   config: RunnableConfig):

    print("========== Analyze Answer ==========")

    elapsed_time = (datetime.now() - state["start_time"]).total_seconds() / 60

    answer: str = state["user_answer"]
    user_message = HumanMessage(content = answer + """\n\ntotal {elapsed_time} minutes passed
                                """)

    model_name = config["configurable"].get("model_name", "gpt-4o")
    model = get_model(model=model_name).with_structured_output(AnalyzeAnswerResponse, strict=True, method="json_schema")
    
    response: AnalyzeAnswerResponse = model.invoke(state["messages"] + [user_message])
    print("AI Analysis :> " + response.model_dump_json(indent=2))

    # append user answer into chat history
    # and get feedback from AI
    return {
        "messages": [user_message], 
        "analyze_answer_response": response
    }    


def repeat_question(state: AgentState,
                    config: RunnableConfig):
    
    print("========== Repeat Question ==========")  

    # append the feedback to the messages
    # and then send it back to user (and clean previous answer and its analysis)
    ai_response: AIMessage = AIMessage(content=state["analyze_answer_response"].feedback)   
    return {
        "messages": [ai_response],
        "user_answer": None,
        "analyze_answer_response": None,
    }


def send_next_question(state: AgentState,
                      config: RunnableConfig):

    print("========== Send Next Question ==========")

    analyze_answer_response: AnalyzeAnswerResponse = state["analyze_answer_response"]
    next_question: Question = analyze_answer_response.next_question

    # append the next question to the messages
    # and send it back to user (clean previous answer and its analysis)
    ai_message = AIMessage(content=next_question.question)
    return {
        "messages": [ai_message],
        "question": next_question,
        "user_answer": None,
        "analyze_answer_response": None,
    }


def summarize_interview(state: AgentState,
                        config: RunnableConfig):
    print("========== Summarize Interview ==========")
    pass


def check_analyze_answer_response_condition(state: AgentState,
                                            config: RunnableConfig):
    
    print("========== Check Analyze Answer Response Condition ==========")

    analyze_answer_response: AnalyzeAnswerResponse = state["analyze_answer_response"]

    if analyze_answer_response is None:
        return "repeat_question"

    if analyze_answer_response.is_interview_over:
        return "summarize_interview"

    if not analyze_answer_response.is_answer:
        return "repeat_question"

    if analyze_answer_response.next_question:
        return "send_next_question"

    return "repeat_question"

def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("kickoff_interview", kickoff_interview)
    workflow.add_node("analyze_answer", analyze_answer)
    workflow.add_node("repeat_question", repeat_question)
    workflow.add_node("send_next_question", send_next_question)
    workflow.add_node("summarize_interview", summarize_interview)


    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("kickoff_interview")

    workflow.add_edge("kickoff_interview", "analyze_answer")
    # We now add a conditional edge
    workflow.add_conditional_edges(
        "analyze_answer",
        check_analyze_answer_response_condition,
        {
            "summarize_interview": "summarize_interview",
            "repeat_question": "repeat_question",
            "send_next_question": "send_next_question"
        },
    )

    workflow.add_edge("repeat_question", "analyze_answer")
    workflow.add_edge("send_next_question", "analyze_answer")
    workflow.add_edge("summarize_interview", END)

    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory,
                             interrupt_before=["analyze_answer"])
    
    return graph

if __name__ == "__main__":
    graph = build_graph()
    print(graph)

