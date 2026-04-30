from __future__ import annotations
import json
import time
from typing import Any, Dict
from src.utils.llm_client import LLMClient
from src.utils.token_counter import estimate_tokens
from src.utils.trace import WorkflowTrace

class BaseAgent:
    name = "BaseAgent"

    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def system_prompt(self) -> str:
        return (
            "You are a professional e-commerce short-video production agent. "
            "Always return valid JSON. Do not include markdown fences."
        )

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        raise NotImplementedError

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def run(self, payload: Dict[str, Any], trace: WorkflowTrace) -> Dict[str, Any]:
        prompt = self.user_prompt(payload)
        start = time.perf_counter()
        result = self.client.complete_json(
            system_prompt=self.system_prompt(),
            user_prompt=prompt,
            fallback=lambda: self.fallback(payload),
        )
        latency_ms = int((time.perf_counter() - start) * 1000)
        trace.add(
            agent_name=self.name,
            status="success",
            input_summary=json.dumps(payload, ensure_ascii=False)[:500],
            output_summary=json.dumps(result, ensure_ascii=False)[:500],
            prompt_tokens_estimate=estimate_tokens(prompt),
            completion_tokens_estimate=estimate_tokens(result),
            latency_ms=latency_ms,
        )
        return result
