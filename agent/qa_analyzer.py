import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interview_response import QAResult
from utils.llm import get_model
from langchain_core.messages import HumanMessage
from utils.prompt_utils import load_prompt


def analyze_question_answer(answer: str, question: str, language: str = "Chinese", model_name: str = "gpt-4o") -> QAResult:
    prompt_content: str = load_prompt('prompts/analyze_answer.txt')
    human_prompt: HumanMessage = HumanMessage(content=prompt_content.format(question=question, answer=answer, language=language))
    model = get_model(model=model_name).with_structured_output(QAResult)
    response: QAResult = model.invoke([human_prompt])
    print(response.model_dump_json(indent=2))
    return response


if __name__ == "__main__":
    question = "Q2. What is the capital of France?"
    answer = "adfadsfdasf"
    qa_result = analyze_question_answer(answer, question, language="Chinese")

    question = "Q2. What is the capital of France?\nA. Paris\nB. London\nC. Rome\nD. Madrid"
    answer = "A"
    qa_result = analyze_question_answer(answer, question, language="Chinese")

