"""DocAgent Core Orchestrator: Autonomous multi-step workflow from request to .docx."""
import uuid
import re
import logging
from typing import Optional

from app.models.schemas import AgentRequest, AgentResponse, ExecutionPlan
from app.llm.client import get_llm_client, BaseLLMClient
from app.agent.planner import Planner
from app.agent.executor import TaskExecutor
from app.agent.reflection import ReflectionReviewer
from app.document.builder import DocxBuilder

logger = logging.getLogger("DocAgent.Core")

class DocAgent:
    """Autonomous Document Generation Agent."""

    def __init__(self, provider_override: Optional[str] = None):
        self.llm: BaseLLMClient = get_llm_client(provider_override)
        self.planner = Planner(self.llm)
        self.executor = TaskExecutor(self.llm)
        self.reflection = ReflectionReviewer(self.llm)

    def run(self, request_payload: AgentRequest) -> AgentResponse:
        request_id = str(uuid.uuid4())[:8]
        user_request = request_payload.request
        logger.info(f"=== Starting DocAgent Run [{request_id}] ===")
        logger.info(f"User Request: {user_request}")

        # Step 1: Autonomous Planning & Assumption Generation
        plan: ExecutionPlan = self.planner.create_plan(user_request)
        if request_payload.document_type:
            plan.document_type = request_payload.document_type

        # Step 2: Multi-step Execution & Tool Dispatching
        plan, sections = self.executor.execute_plan(plan, user_request)

        # Step 3: Mandatory Engineering Improvement: Reflection & Self-Check
        reflection_report = self.reflection.evaluate(
            original_request=user_request,
            assumptions=plan.assumptions_made,
            sections=sections
        )
        if reflection_report.revisions_triggered or reflection_report.score < 85:
            sections = self.reflection.refine_sections(sections, reflection_report)

        # Step 4: Render Polished Microsoft Word Document (.docx)
        builder = DocxBuilder()
        builder.add_title_block(
            title=plan.document_title,
            doc_type=plan.document_type,
            audience=plan.target_audience,
            assumptions=plan.assumptions_made
        )

        for sec in sections:
            builder.add_section(sec)

        # Sanitize filename
        safe_title = re.sub(r"[^a-zA-Z0-9_\-]", "_", plan.document_title[:35]).strip("_")
        doc_metadata = builder.save(filename=f"{safe_title}_{request_id}")

        # Step 5: Assemble Final Agent Response
        summary_text = (
            f"Successfully planned and produced '{plan.document_title}' as a {plan.document_type}. "
            f"Executed {len(plan.tasks)} tasks, resolved {len(plan.assumptions_made)} assumptions, "
            f"and validated document quality with a reflection score of {reflection_report.score}/100."
        )

        active_provider_name = self.llm.__class__.__name__

        logger.info(f"=== DocAgent Run [{request_id}] Completed Successfully ===")
        return AgentResponse(
            success=True,
            request_id=request_id,
            original_request=user_request,
            execution_summary=summary_text,
            plan=plan,
            reflection_report=reflection_report,
            document=doc_metadata,
            active_provider=active_provider_name
        )
