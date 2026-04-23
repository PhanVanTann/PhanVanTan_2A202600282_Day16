from __future__ import annotations
import json
from .schemas import QAExample, JudgeResult, ReflectionEntry
from .prompts import ACTOR_SYSTEM, EVALUATOR_SYSTEM, REFLECTOR_SYSTEM
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# Initialize Ollama models
llm = ChatOllama(model="llama3", temperature=0)
llm_json = ChatOllama(model="llama3", temperature=0, format="json")

FAILURE_MODE_BY_QID = {"hp2": "incomplete_multi_hop", "hp4": "wrong_final_answer", "hp6": "entity_drift", "hp8": "entity_drift"}
def actor_answer(example: QAExample, attempt_id: int, agent_type: str, reflection_memory: list[str]) -> str:
    context_str = "\n\n".join([f"[{c.title}]\n{c.text}" for c in example.context])
    human_content = f"Context:\n{context_str}\n\nQuestion: {example.question}"
    
    if agent_type == "reflexion" and reflection_memory:
        reflections_str = "\n".join([f"- {r}" for r in reflection_memory])
        human_content += f"\n\nPrevious Reflections and Strategies:\n{reflections_str}"
        
    messages = [
        SystemMessage(content=ACTOR_SYSTEM),
        HumanMessage(content=human_content)
    ]
    response = llm.invoke(messages)
    return response.content.strip()

def evaluator(example: QAExample, answer: str) -> JudgeResult:
    human_content = f"Question: {example.question}\nGold Answer: {example.gold_answer}\nPredicted Answer: {answer}"
    messages = [
        SystemMessage(content=EVALUATOR_SYSTEM),
        HumanMessage(content=human_content)
    ]
    response = llm_json.invoke(messages)
    try:
        data = json.loads(response.content)
        return JudgeResult(score=data.get("score", 0), reason=data.get("reason", "No reason provided"))
    except Exception as e:
        return JudgeResult(score=0, reason=f"Failed to parse Evaluator JSON: {str(e)}. Raw Output: {response.content}")

def reflector(example: QAExample, attempt_id: int, answer: str, judge: JudgeResult) -> ReflectionEntry:
    context_str = "\n\n".join([f"[{c.title}]\n{c.text}" for c in example.context])
    human_content = f"Context:\n{context_str}\n\nQuestion: {example.question}\nIncorrect Answer: {answer}\nEvaluator's Reason for Failure: {judge.reason}"
    messages = [
        SystemMessage(content=REFLECTOR_SYSTEM),
        HumanMessage(content=human_content)
    ]
    response = llm_json.invoke(messages)
    try:
        data = json.loads(response.content)
        return ReflectionEntry(
            attempt_id=attempt_id,
            failure_reason=data.get("failure_reason", "Unknown"),
            lesson=data.get("lesson", "No lesson provided"),
            next_strategy=data.get("next_strategy", "Try again carefully")
        )
    except Exception as e:
        return ReflectionEntry(
            attempt_id=attempt_id,
            failure_reason="Parsing Error",
            lesson="Failed to generate reflection",
            next_strategy="Read the context more carefully"
        )
