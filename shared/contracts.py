from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from shared.ir import EngineeringIR


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PromptRequest(ContractModel):
    prompt: str = Field(min_length=1, max_length=2_000)
    current_ir: EngineeringIR | None = None
    target_tool: Literal["blender", "openscad"]


class PromptResponse(ContractModel):
    ir: EngineeringIR | None = None
    status: Literal["ok", "error", "validation_failed"]
    error: str | None = None
    validation_errors: list[str] = Field(default_factory=list)
    request_id: str
    provider: str
    trace: list["TraceEvent"] = Field(default_factory=list)
    guild_trace_url: str | None = None
    openui_lang: str | None = None
    openui_elements: list[dict[str, Any]] = Field(default_factory=list)
    scene_headline: str | None = None
    clickhouse_exported: bool = False
    composio_status: str | None = None
    airbyte_context_exported: bool = False


class ExecutionReport(ContractModel):
    request_id: str
    target_tool: Literal["blender", "openscad"]
    status: Literal["ok", "error"]
    duration_ms: float = Field(ge=0)
    error: str | None = None


class ExecutionResponse(ContractModel):
    event: "TraceEvent"
    trace: list["TraceEvent"] = Field(default_factory=list)
    guild_trace_url: str | None = None
    openui_lang: str | None = None
    openui_elements: list[dict[str, Any]] = Field(default_factory=list)
    scene_headline: str | None = None
    clickhouse_exported: bool = False
    composio_status: str | None = None
    airbyte_context_exported: bool = False


class TraceEvent(ContractModel):
    request_id: str
    step: Literal["parse", "validate", "route", "execute"]
    status: Literal["started", "completed", "failed"]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    duration_ms: float | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(ContractModel):
    status: Literal["healthy"] = "healthy"
    version: str = "0.1.0"
    provider: str


class OpenScadPromptRequest(ContractModel):
    prompt: str = Field(min_length=1, max_length=2_000)
    current_ir: EngineeringIR | None = None
    export_formats: list[Literal["stl", "png", "3mf", "svg"]] = Field(
        default_factory=lambda: ["stl", "png", "3mf", "svg"]
    )


class OpenScadExecution(ContractModel):
    scad_path: str
    scad_source: str
    artifacts: dict[str, str] = Field(default_factory=dict)
    export_errors: list[str] = Field(default_factory=list)


class OpenScadPromptResponse(PromptResponse):
    execution: OpenScadExecution | None = None


class RuntimeStatus(ContractModel):
    tool: Literal["blender", "openscad", "companion"] = "companion"
    phase: Literal[
        "idle",
        "starting",
        "generating",
        "validating",
        "rendering",
        "completed",
        "failed",
    ] = "idle"
    message: str = "idō is ready"
    request_id: str | None = None
    active_project: str | None = None
    artifacts: dict[str, str] = Field(default_factory=dict)
    recent_errors: list[str] = Field(default_factory=list)
    provider: str | None = None
    inference_provider: str | None = None
    clickhouse_enabled: bool = False
    clickhouse_exported: bool | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class IntegrationsStatus(ContractModel):
    provider: str
    pioneer_configured: bool = False
    pioneer_model: str | None = None
    clickhouse_enabled: bool = False
    clickhouse_reachable: bool | None = None
    clickhouse_table: str | None = None
    guild_enabled: bool = False
    openui_active: bool = True
    composio_enabled: bool = False
    airbyte_enabled: bool = False
    truefoundry_available: bool = False
    render_blueprint: bool = False
    capabilities: list[str] = Field(default_factory=list)


class TraceAnalyticsRow(ContractModel):
    request_id: str
    step: str
    status: str
    duration_ms: float | None = None
    prompt: str | None = None
    target_tool: str | None = None
    exported_at: str | None = None


class TraceAnalyticsResponse(ContractModel):
    enabled: bool
    rows: list[TraceAnalyticsRow] = Field(default_factory=list)


def new_request_id() -> str:
    return uuid4().hex
