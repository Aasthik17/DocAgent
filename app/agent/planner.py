"""Autonomous Planner: decomposes requests, resolves ambiguities, generates execution TODO plan."""
import logging
from typing import Dict, Any, List
from app.models.schemas import ExecutionPlan, AgentTask, TaskStatus
from app.llm.client import BaseLLMClient
from app.llm.prompts import PLANNING_SYSTEM_PROMPT

logger = logging.getLogger("DocAgent.Planner")

class Planner:
    """Creates structured multi-step execution plans and assumption registers."""
    
    def __init__(self, llm_client: BaseLLMClient):
        self.llm = llm_client

    def create_plan(self, user_request: str) -> ExecutionPlan:
        logger.info(f"Generating execution plan for request: '{user_request[:80]}...'")
        
        prompt = f"""User Request:
{user_request}

Analyze this document request. Identify any ambiguous or conflicting parameters (e.g. budget, conflicting architectures, tight deadlines, missing specs), formulate explicit assumptions, and generate the step-by-step task list."""
        
        raw_plan = self.llm.generate_json(
            system_prompt=PLANNING_SYSTEM_PROMPT,
            user_prompt=prompt
        )
        
        tasks: List[AgentTask] = []
        for t in raw_plan.get("tasks", []):
            task_obj = AgentTask(
                id=t.get("id", len(tasks) + 1),
                title=t.get("title", f"Task {len(tasks) + 1}"),
                description=t.get("description", ""),
                tool=t.get("tool", "internal_reasoning"),
                status=TaskStatus.PENDING
            )
            tasks.append(task_obj)
            
        plan = ExecutionPlan(
            document_title=raw_plan.get("document_title", "Business Document"),
            document_type=raw_plan.get("document_type", "Formal Report"),
            target_audience=raw_plan.get("target_audience", "Key Stakeholders"),
            assumptions_made=raw_plan.get("assumptions_made", []),
            tasks=tasks
        )
        
        logger.info(f"Plan created with {len(tasks)} tasks and {len(plan.assumptions_made)} explicit assumptions.")
        return plan
