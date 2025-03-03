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
from agent.interview_response import Question, AnalyzeAnswerResponse, QAResult
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime   
from agent.qa_analyzer import analyze_question_answer   

def kickoff_interview(state: AgentState,     
                      config: RunnableConfig):
    
    print("========== Kickoff Interview ==========")

    prompt_content: str = load_prompt('prompts/kickoff_interview.txt')
    human_prompt: HumanMessage = HumanMessage(content=prompt_content.format(job_title=state["job_title"], 
                                                              knowledge_points=state["knowledge_points"],
                                                              interview_time=state["interview_time"],
                                                              language=state["language"]))

    model_name: str = config["configurable"].get("model_name", "gpt-4o")
    model: ChatOpenAI = get_model(model=model_name)
    
    print("System :> " + human_prompt.content)
    response = model.invoke([human_prompt])
    # print("AI :> " + response.content)

    return {
        "messages": [human_prompt, response],
        "question": response.content
    }


def analyze_answer(state: AgentState,   
                   config: RunnableConfig):

    print("========== Analyze Answer ==========")

    elapsed_time = (datetime.now() - state["start_time"]).total_seconds() / 60
    answer: str = state["user_answer"]
    user_message = answer + f"""\n\ntotal {elapsed_time} minutes passed"""

    model_name = config["configurable"].get("model_name", "gpt-4o")
    response: QAResult = analyze_question_answer(user_message, state["question"], state["language"])

    # append user answer into chat history
    # and get feedback from AI
    return {
        "messages": [HumanMessage(content=user_message)], 
        "analyze_answer_response": response
    }    


def repeat_question(state: AgentState,
                    config: RunnableConfig):
    
    print("========== Repeat Question ==========")  

    # append the feedback to the messages
    # and then send it back to user (and clean previous answer and its analysis)
    qa_result: QAResult = state["analyze_answer_response"]
    ai_response: AIMessage = AIMessage(content=qa_result.answer.feedback)   
    return {
        "messages": [ai_response],
        "user_answer": None,
        "analyze_answer_response": None,
    }


def send_next_question(state: AgentState,
                      config: RunnableConfig):

    print("========== Send Next Question ==========")

    model_name: str = config["configurable"].get("model_name", "gpt-4o")
    model: ChatOpenAI = get_model(model=model_name)
    
    response = model.invoke(state["messages"])
    # print("AI :> " + response.content)

    qa_result: QAResult = state["analyze_answer_response"]
    ai_analysis = "User answer analysis:\n\n" + qa_result.answer.model_dump_json(indent=2) + "\n\n"
    ai_message = AIMessage(content=ai_analysis + "Next question:\n\n" + response.content)

    # append the next question to the messages
    # and send it back to user (clean previous answer and its analysis)
    return {
        "messages": [ai_message],
        "question": response.content,
        "user_answer": None,
        "analyze_answer_response": None,
    }


def summarize_interview(state: AgentState,
                        config: RunnableConfig):
    print("========== Summarize Interview ==========")
    pass


def is_over_condition(state: AgentState,
                      config: RunnableConfig):
    print("========== Is Over Condition ==========")
    question: str = state["question"]
    if "面试结束" in question or "Interview Over" in question:
        print(f"{question} is over condition")
        return "summarize_interview"
    else:
        return "analyze_answer"


def check_analyze_answer_response_condition(state: AgentState,
                                            config: RunnableConfig):
    
    print("========== Check Analyze Answer Response Condition ==========")

    qa_result: QAResult = state["analyze_answer_response"]

    if qa_result is None:
        return "repeat_question"

    if qa_result.is_interview_over:
        return "summarize_interview"

    if qa_result.answer and not qa_result.answer.is_valid:
        return "repeat_question"

    return "send_next_question"

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
    workflow.add_conditional_edges(
        "send_next_question",
        is_over_condition,
        {
            "summarize_interview": "summarize_interview",
            "analyze_answer": "analyze_answer"
        },
    )
    workflow.add_edge("summarize_interview", END)

    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory,
                             interrupt_before=["analyze_answer"])
    
    return graph

if __name__ == "__main__":
    graph = build_graph()
    print(graph)

