from __future__ import annotations
from typing import Any, Dict
from src.agents.base import BaseAgent

class MarketAgent(BaseAgent):
    name = "Market & Audience Agent"

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        return f"""
Analyze target market and TikTok content strategy for this product brief.
Return JSON with: market, audience_motivation, content_tone, hook_strategy,
cta_strategy, localization_notes, risk_notes.

Input:
{payload}
"""

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        brief = payload.get("product_brief", payload)
        market = brief.get("target_market", "Southeast Asia")
        category = brief.get("category", "general")
        if "Indonesia" in market or "印尼" in market:
            localization = ["use casual daily-life setting", "avoid long text overlays", "show product benefit visually"]
        elif "Philippines" in market or "菲律宾" in market:
            localization = ["use warm friendly tone", "clear price/value cue", "show lifestyle improvement"]
        else:
            localization = ["use simple English captions", "focus on visual proof", "short CTA"]
        return {
            "market": market,
            "audience_motivation": _audience_motivation(category),
            "content_tone": "fast, visual, direct, mobile-first",
            "hook_strategy": [
                "show product clearly within first 1.5 seconds",
                "open with a movement or visual contrast instead of abstract slogan",
                "use one main selling point per shot",
            ],
            "cta_strategy": ["limited-time value cue", "comment or shop now prompt", "repeat product name at ending frame"],
            "localization_notes": localization,
            "risk_notes": ["avoid overclaiming performance", "avoid showing unavailable price or logistics promises"],
        }

def _audience_motivation(category: str) -> str:
    c = category.lower()
    if "fashion" in c or "t-shirt" in c:
        return "wants affordable style, easy matching, and social-media-ready outfits"
    if "automotive" in c or "oil" in c:
        return "wants reliability, engine protection, and practical maintenance value"
    return "wants a clear daily-life benefit and low-friction purchase reason"
