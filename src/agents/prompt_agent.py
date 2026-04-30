from __future__ import annotations
from typing import Any, Dict
from src.agents.base import BaseAgent

class PromptAgent(BaseAgent):
    name = "Prompt Compiler Agent"

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        return f"""
Compile video generation prompts for VEO, Seedance and WAN.
Return JSON with key prompts. Each prompt includes model, shot_id, positive_prompt,
negative_prompt, aspect_ratio, duration, notes.

Input:
{payload}
"""

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        brief = payload["product_brief"]
        storyboard = payload["storyboard"]["storyboard"]
        prompts = []
        for shot in storyboard:
            prompts.append(_compile_prompt("VEO", brief, shot))
            prompts.append(_compile_prompt("Seedance", brief, shot))
            prompts.append(_compile_prompt("WAN", brief, shot))
        image_prompt = _image_prompt(brief)
        return {"prompts": prompts, "cover_image_prompt": image_prompt}

def _compile_prompt(model: str, brief: Dict[str, Any], shot: Dict[str, Any]) -> Dict[str, Any]:
    product = brief["product_name"]
    style = "realistic commercial TikTok video, high detail, natural lighting, mobile-first composition"
    if model == "WAN":
        style = "realistic local video generation, stable motion, clear subject, simple action"
    positive = (
        f"{style}. Product: {product}. Scene: {shot['scene']}. "
        f"Camera: {shot['camera']}. Action: {shot['action']}. "
        f"Focus: {shot['product_focus']}. Caption idea: {shot['caption']}. "
        "Vertical 9:16, clean composition, product visible, natural motion."
    )
    negative = (
        "deformed hands, distorted product, unreadable label, bad anatomy, extra fingers, "
        "complex physics interaction, flickering logo, warped text, low resolution, fast chaotic camera"
    )
    return {
        "model": model,
        "shot_id": shot["shot_id"],
        "positive_prompt": positive,
        "negative_prompt": negative,
        "aspect_ratio": "9:16",
        "duration": shot["duration"],
        "notes": "Use image reference when available. Keep product identity consistent across shots.",
    }

def _image_prompt(brief: Dict[str, Any]) -> str:
    points = ", ".join(brief.get("core_selling_points", [])[:3])
    return (
        f"Premium TikTok e-commerce cover image for {brief['product_name']}, "
        f"core selling points: {points}, strong visual impact, clean typography area, "
        "realistic product hero shot, high-end commercial lighting, 9:16 layout."
    )
