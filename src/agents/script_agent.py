from __future__ import annotations
from typing import Any, Dict, List
from src.agents.base import BaseAgent

class ScriptAgent(BaseAgent):
    name = "Script Agent"

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        return f"""
Generate TikTok conversion video scripts for the product.
Return JSON with keys: scripts. scripts must contain 15s, 24s, 30s versions.
Each version contains hook, shot_plan, captions, voiceover, cta.

Input:
{payload}
"""

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        brief = payload["product_brief"]
        market = payload["market_strategy"]
        product = brief["product_name"]
        points = brief.get("core_selling_points", []) or ["clear product benefit"]
        scripts = {
            "15s": _make_script(product, points, market, 5, "fast conversion"),
            "24s": _make_script(product, points, market, 7, "balanced detail"),
            "30s": _make_script(product, points, market, 9, "full explanation"),
        }
        return {"scripts": scripts}

def _make_script(product: str, points: List[str], market: Dict[str, Any], shots: int, mode: str) -> Dict[str, Any]:
    captions = []
    shot_plan = []
    for idx in range(shots):
        point = points[idx % len(points)]
        shot_plan.append(
            {
                "shot": idx + 1,
                "duration_sec": 3 if shots <= 5 else 4,
                "purpose": "hook" if idx == 0 else "selling_point" if idx < shots - 1 else "cta",
                "content": _shot_content(idx, product, point),
            }
        )
        captions.append(_caption(idx, product, point))
    return {
        "mode": mode,
        "hook": f"Stop scrolling — see why {product} fits daily TikTok shopping.",
        "shot_plan": shot_plan,
        "captions": captions,
        "voiceover": [
            f"Here is {product}.",
            f"Main benefit: {points[0] if points else 'easy to use'}.",
            "Clean look, simple decision, quick purchase.",
        ],
        "cta": "Tap to shop / Check the product card now.",
    }

def _shot_content(idx: int, product: str, point: str) -> str:
    options = [
        f"Hero shot of {product} entering frame with fast camera push-in",
        f"Close-up showing {point}",
        "Realistic usage or wearing scene with simple movement",
        "Side angle detail, keep product centered and stable",
        "Before/after or match-with scenario",
        "Macro texture/detail shot",
        "Social proof style frame with clean text overlay",
        "Final product packshot with CTA",
    ]
    return options[idx % len(options)]

def _caption(idx: int, product: str, point: str) -> str:
    if idx == 0:
        return f"{product}: made for daily TikTok style"
    return f"Benefit {idx}: {point}"
