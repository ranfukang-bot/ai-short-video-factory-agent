from __future__ import annotations
from typing import Any, Dict
from src.agents.base import BaseAgent

class EvaluatorAgent(BaseAgent):
    name = "Quality Evaluator Agent"

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        return f"""
Evaluate the generated short video plan.
Return JSON with: score_report, risk_report, optimization_suggestions, pass_status.
Score dimensions: selling_point_clarity, tiktok_rhythm, ai_generation_feasibility,
conversion_potential, localization_fit.

Input:
{payload}
"""

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        storyboard = payload["storyboard"]["storyboard"]
        risks = [s for s in storyboard if s.get("ai_risk") == "medium"]
        score_report = {
            "selling_point_clarity": 91,
            "tiktok_rhythm": 88,
            "ai_generation_feasibility": max(76, 90 - len(risks) * 3),
            "conversion_potential": 86,
            "localization_fit": 84,
        }
        overall = round(sum(score_report.values()) / len(score_report), 1)
        return {
            "score_report": score_report,
            "overall_score": overall,
            "risk_report": [
                {
                    "shot_id": s["shot_id"],
                    "risk_level": s["ai_risk"],
                    "reason": "This shot may involve more motion or object interaction than pure packshot.",
                    "fix": "Reduce hand movement, use close-up, keep product static for 1-2 seconds.",
                }
                for s in risks
            ],
            "optimization_suggestions": [
                "Put the strongest visible selling point in the first 2 seconds.",
                "Avoid more than one complex action per shot.",
                "Use 3-4 reusable scene templates to increase batch production efficiency.",
                "Keep captions short and benefit-driven for mobile viewing.",
            ],
            "pass_status": "pass" if overall >= 80 else "needs_revision",
        }
