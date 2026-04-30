from __future__ import annotations
from typing import Any, Dict, List
from src.agents.base import BaseAgent

class ProductParserAgent(BaseAgent):
    name = "Product Parser Agent"

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        return f"""
Parse and normalize this e-commerce product brief. Return JSON with:
product_name, category, target_market, target_audience, core_selling_points,
visual_features, ai_generation_constraints, content_angle, missing_information.

Input:
{payload}
"""

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        selling_points: List[str] = payload.get("selling_points") or []
        constraints: List[str] = payload.get("constraints") or []
        category = payload.get("category", "general e-commerce")
        preferred_style = payload.get("preferred_style", "realistic TikTok short video")
        return {
            "product_name": payload.get("product_name", "Unnamed Product"),
            "category": category,
            "target_market": payload.get("target_market", "Southeast Asia"),
            "target_audience": payload.get("target_audience", "TikTok users"),
            "core_selling_points": selling_points[:6],
            "visual_features": _infer_visual_features(category, selling_points, preferred_style),
            "ai_generation_constraints": constraints + [
                "use simple body movement and stable camera path",
                "avoid hand-object interactions that require precise physics",
                "keep product visible in the first 2 seconds",
            ],
            "content_angle": payload.get("video_goal", "conversion short video"),
            "missing_information": _missing(payload),
        }

def _missing(payload: Dict[str, Any]) -> List[str]:
    required = ["product_name", "category", "target_market", "target_audience", "selling_points"]
    return [key for key in required if not payload.get(key)]

def _infer_visual_features(category: str, selling_points: List[str], style: str) -> List[str]:
    joined = " ".join(selling_points).lower() + " " + category.lower() + " " + style.lower()
    if "t-shirt" in joined or "fashion" in joined or "shirt" in joined:
        return ["model wearing product", "front print close-up", "streetwear outfit", "fabric texture detail"]
    if "oil" in joined or "motor" in joined or "automotive" in joined:
        return ["product bottle hero shot", "engine maintenance scene", "macro label detail", "garage lighting"]
    return ["product hero shot", "usage scenario", "feature close-up", "clean background"]
