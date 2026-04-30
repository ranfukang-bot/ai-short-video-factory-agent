from __future__ import annotations
from typing import Any, Dict
from src.agents.base import BaseAgent

class StoryboardAgent(BaseAgent):
    name = "Storyboard Agent"

    def user_prompt(self, payload: Dict[str, Any]) -> str:
        return f"""
Convert the selected script into an executable storyboard.
Return JSON with key storyboard, a list of shots. Each shot includes:
shot_id, duration, scene, camera, action, product_focus, caption, ai_risk, generation_note.

Input:
{payload}
"""

    def fallback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        brief = payload["product_brief"]
        scripts = payload["scripts"]["scripts"]
        selected = scripts.get("24s") or list(scripts.values())[0]
        storyboard = [_shot(item, brief, selected) for item in selected["shot_plan"]]
        return {"selected_script_length": "24s", "storyboard": storyboard}

def _shot(item: Dict[str, Any], brief: Dict[str, Any], script: Dict[str, Any]) -> Dict[str, Any]:
    shot_id = item["shot"]
    category = brief.get("category", "general").lower()
    if "fashion" in category or "t-shirt" in category:
        scene = "streetwear sidewalk / clean studio wall / coffee shop entrance"
        action = "model makes small natural movement: turn slightly, adjust hem, walk two steps"
        product_focus = "fit, print, fabric texture, outfit matching"
    elif "automotive" in category or "oil" in category:
        scene = "clean garage bench with product and vehicle detail in background"
        action = "hand places bottle on table, camera pushes in, label remains readable"
        product_focus = "label, bottle shape, engine-care value"
    else:
        scene = "clean lifestyle tabletop with real usage context"
        action = "simple product reveal and close-up; avoid complex assembly"
        product_focus = "main visible feature and benefit"
    return {
        "shot_id": shot_id,
        "duration": f"{item.get('duration_sec', 3)}s",
        "scene": scene,
        "camera": _camera(shot_id),
        "action": action,
        "product_focus": product_focus,
        "caption": script["captions"][min(shot_id - 1, len(script["captions"]) - 1)],
        "ai_risk": "low" if shot_id in [1, 2, 4] else "medium",
        "generation_note": "Keep movement simple, product stable, no complex physics interaction.",
    }

def _camera(shot_id: int) -> str:
    cameras = [
        "fast push-in, 9:16 vertical, product center frame",
        "macro close-up, shallow depth of field",
        "medium shot with slight handheld movement",
        "side tracking shot, stable product visibility",
        "static packshot with clean text overlay",
        "slow orbit, avoid fast deformation",
        "cut-to-detail with rhythmic transition",
    ]
    return cameras[(shot_id - 1) % len(cameras)]
