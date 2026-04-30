from __future__ import annotations
import os
from typing import Any, Dict
from src.agents.base import BaseAgent

class CostAgent(BaseAgent):
    name = "Cost & Token Agent"

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        return f"""
Summarize estimated token usage and cost for this workflow.
Return JSON with: agent_count, input_tokens, output_tokens, total_tokens,
estimated_cost_usd, cost_notes, scale_projection.

Input:
{payload}
"""

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        trace_dict = payload["trace"]
        input_tokens = trace_dict["total_prompt_tokens_estimate"]
        output_tokens = trace_dict["total_completion_tokens_estimate"]
        input_price = float(os.getenv("INPUT_TOKEN_PRICE_PER_1M", "1.0"))
        output_price = float(os.getenv("OUTPUT_TOKEN_PRICE_PER_1M", "3.0"))
        cost = input_tokens / 1_000_000 * input_price + output_tokens / 1_000_000 * output_price
        return {
            "agent_count": trace_dict["total_agents"] + 1,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost_usd": round(cost, 4),
            "cost_notes": "This is an approximate estimate based on text length, not provider billing data.",
            "scale_projection": {
                "100_sku_estimated_tokens": (input_tokens + output_tokens) * 100,
                "100_sku_estimated_cost_usd": round(cost * 100, 2),
                "daily_team_use_case": "Batch-generate scripts, storyboards, prompts and evaluation reports for multiple e-commerce SKUs."
            },
        }
