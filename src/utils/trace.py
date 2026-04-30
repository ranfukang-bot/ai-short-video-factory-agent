from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any, Dict, List
import json

@dataclass
class AgentTraceItem:
    agent_name: str
    status: str
    input_summary: str
    output_summary: str
    prompt_tokens_estimate: int
    completion_tokens_estimate: int
    latency_ms: int
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

class WorkflowTrace:
    def __init__(self) -> None:
        self.items: List[AgentTraceItem] = []

    def add(
        self,
        agent_name: str,
        status: str,
        input_summary: str,
        output_summary: str,
        prompt_tokens_estimate: int,
        completion_tokens_estimate: int,
        latency_ms: int,
    ) -> None:
        self.items.append(
            AgentTraceItem(
                agent_name=agent_name,
                status=status,
                input_summary=input_summary[:500],
                output_summary=output_summary[:500],
                prompt_tokens_estimate=prompt_tokens_estimate,
                completion_tokens_estimate=completion_tokens_estimate,
                latency_ms=latency_ms,
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_agents": len(self.items),
            "total_prompt_tokens_estimate": sum(i.prompt_tokens_estimate for i in self.items),
            "total_completion_tokens_estimate": sum(i.completion_tokens_estimate for i in self.items),
            "items": [asdict(i) for i in self.items],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
