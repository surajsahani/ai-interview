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
from agent.interview_response import Question, AnalyzeAnswerResponse, QAResult, Answer, QuestionType
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime   
from agent.qa_analyzer import analyze_question_answer   
from utils.log_utils import logger
from agent.agent_state import get_qa_history
from agent.interview_response import InterviewResult

def kickoff_interview(state: AgentState,     
                      config: RunnableConfig):
    
    logger.info("========== Kickoff Interview ==========")

    prompt_content: str = load_prompt('prompts/kickoff_interview.txt')
    human_prompt: HumanMessage = HumanMessage(content=prompt_content.format(job_title=state["job_title"], 
                                                              knowledge_points=state["knowledge_points"],
                                                              interview_time=state["interview_time"],
                                                              language=state["language"],
                                                              qa_history=get_qa_history(state["qa_history"])))

    model_name: str = config["configurable"].get("model_name", "gpt-4o")
    model: ChatOpenAI = get_model(model=model_name)
    
    logger.info(f"System : {human_prompt.content}")
    response = model.invoke([human_prompt])

    return {
        "messages": [human_prompt, response],
        "question": response.content
    }


def is_stop_by_user(user_answer: str) -> bool:
    return "结束面试" in user_answer or "End Interview" in user_answer or "Stop Interview" in user_answer


def analyze_answer(state: AgentState,   
                   config: RunnableConfig):

    logger.info("========== Analyze Answer ==========")

    elapsed_time = (datetime.now() - state["start_time"]).total_seconds() / 60
    answer: str = state["user_answer"]
    user_message = answer + f"""\n\ntotal {elapsed_time} minutes passed"""
    if is_stop_by_user(answer):
        logger.info(f"Interview is stopped by user answer {answer}")
        qa_result = QAResult(question=Question(question=state["question"],
                                                question_number=-1,
                                                question_type=QuestionType.NONE,
                                                knowledge_point="",
                                                answer=""), 
                            answer=Answer(is_valid=False, 
                                        feedback="Interview is stopped by user", 
                                        is_correct=False, 
                                        analysis="", 
                                        score=0),
                            is_interview_over=True,
                            summary="Last question is not answered due to the interview is stopped by user")
        return {
            "messages": [HumanMessage(content=user_message)], 
            "analyze_answer_response": qa_result,
            "qa_history": [(state["question"], answer, qa_result)]
        }

    model_name = config["configurable"].get("model_name", "gpt-4o")
    response: QAResult = analyze_question_answer(user_message, state["question"], state["language"])

    qa_tuple = (state["question"], answer, response)

    return {
        "messages": [HumanMessage(content=user_message)], 
        "analyze_answer_response": response,
        "qa_history": [qa_tuple]
    }    


def repeat_question(state: AgentState,
                    config: RunnableConfig):
    
    logger.info("========== Repeat Question ==========")  

    qa_result: QAResult = state["analyze_answer_response"]
    ai_response: AIMessage = AIMessage(content=qa_result.answer.feedback)   
    
    logger.info(f"Feedback : {qa_result.answer.feedback}")

    return {
        "messages": [ai_response],
        "user_answer": None,
        "analyze_answer_response": None,
    }


def send_next_question(state: AgentState,
                      config: RunnableConfig):

    logger.info("========== Send Next Question ==========")

    model_name: str = config["configurable"].get("model_name", "gpt-4o")
    model: ChatOpenAI = get_model(model=model_name)
    
    prompt_content: str = load_prompt('prompts/kickoff_interview.txt')
    human_prompt: HumanMessage = HumanMessage(content=prompt_content.format(job_title=state["job_title"], 
                                                              knowledge_points=state["knowledge_points"],
                                                              interview_time=state["interview_time"],
                                                              language=state["language"],
                                                              qa_history=get_qa_history(state["qa_history"])))

    # response = model.invoke(state["messages"])
    logger.info(f"System : {human_prompt.content}")
    response = model.invoke([human_prompt])

    qa_result: QAResult = state["analyze_answer_response"]
    ai_analysis = "User answer analysis:\n\n" + qa_result.answer.model_dump_json(indent=2) + "\n\n"
    ai_message = AIMessage(content=ai_analysis + "Next question:\n\n" + response.content)

    return {
        "messages": [ai_message],
        "question": response.content,
        "user_answer": None,
        "analyze_answer_response": None,
    }


def summarize_interview(state: AgentState,
                        config: RunnableConfig):
    logger.info("========== Summarize Interview ==========")

    prompt_content: str = load_prompt('prompts/summarize_interview.txt')
    human_prompt: HumanMessage = HumanMessage(content=prompt_content.format(job_title=state["job_title"], 
                                                              knowledge_points=state["knowledge_points"],
                                                              interview_time=state["interview_time"],
                                                              language=state["language"],
                                                              qa_history=get_qa_history(state["qa_history"])))

    model_name: str = config["configurable"].get("model_name", "gpt-4o")
    model: ChatOpenAI = get_model(model=model_name).with_structured_output(InterviewResult)
    
    logger.info(f"System : {human_prompt.content}")
    response: InterviewResult = model.invoke([human_prompt])
    logger.info(f"Interview Result : {response.model_dump_json(indent=2)}")

    return {
        "interview_result": response
    }


def is_over_condition(state: AgentState,
                      config: RunnableConfig):
    logger.info("========== Check Is Over Condition ==========")
    question: str = state["question"]
    if "面试结束" in question or "Interview Over" in question:
        logger.info(f"Interview is over: {question}")
        return "summarize_interview"
    else:
        return "analyze_answer"


def check_analyze_answer_response_condition(state: AgentState,
                                            config: RunnableConfig):
    
    logger.info("========== Check Analysis Response Condition ==========")

    qa_result: QAResult = state["analyze_answer_response"]

    if qa_result is None:
        logger.info("No analysis result, continuing analysis")
        return "repeat_question"

    if qa_result.is_interview_over:
        logger.info("Interview is over")
        return "summarize_interview"

    if qa_result.answer and not qa_result.answer.is_valid:
        logger.info("Invalid answer, repeating question")
        return "repeat_question"

    logger.info("Moving to next question")
    return "send_next_question"


def build_graph():
    logger.info("Building interview workflow graph")

    workflow = StateGraph(AgentState)

    workflow.add_node("kickoff_interview", kickoff_interview)
    workflow.add_node("analyze_answer", analyze_answer)
    workflow.add_node("repeat_question", repeat_question)
    workflow.add_node("send_next_question", send_next_question)
    workflow.add_node("summarize_interview", summarize_interview)

    workflow.set_entry_point("kickoff_interview")

    workflow.add_edge("kickoff_interview", "analyze_answer")
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

