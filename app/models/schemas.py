"""Pydantic schemas and domain models for DocAgent."""
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    REVISED = "REVISED"
    FAILED = "FAILED"

class TableData(BaseModel):
    headers: List[str]
    rows: List[List[str]]
    caption: Optional[str] = None

class DocumentSection(BaseModel):
    title: str
    level: int = 1  # 1 for Heading 1, 2 for Heading 2
    content: str
    callout: Optional[str] = None  # Key takeaway or executive alert
    table: Optional[TableData] = None
    bullet_points: Optional[List[str]] = None

class AgentTask(BaseModel):
    id: int
    title: str
    description: str
    tool: str = "internal_reasoning"
    status: TaskStatus = TaskStatus.PENDING
    output: Optional[str] = None
    execution_time_ms: Optional[int] = None

class ExecutionPlan(BaseModel):
    document_title: str
    document_type: str
    target_audience: str
    assumptions_made: List[str] = Field(default_factory=list)
    tasks: List[AgentTask] = Field(default_factory=list)

class ReflectionCheck(BaseModel):
    name: str
    passed: bool
    details: str

class ReflectionResult(BaseModel):
    score: int = Field(ge=0, le=100)
    passed: bool
    checks: List[ReflectionCheck]
    critique: str
    revisions_triggered: bool = False
    improvement_summary: Optional[str] = None

class DocumentMetadata(BaseModel):
    doc_id: str
    filename: str
    file_path: str
    file_size_bytes: int
    download_url: str
    total_sections: int
    total_tables: int

class AgentRequest(BaseModel):
    request: str = Field(..., description="Natural language prompt describing the document to generate.")
    document_type: Optional[str] = Field(None, description="Optional override for document type (e.g. proposal, report, sop, spec)")
    model_provider: Optional[str] = Field(None, description="Optional model provider override ('gemini', 'groq', 'fallback')")

class AgentResponse(BaseModel):
    success: bool
    request_id: str
    original_request: str
    execution_summary: str
    plan: ExecutionPlan
    reflection_report: ReflectionResult
    document: DocumentMetadata
    active_provider: str
