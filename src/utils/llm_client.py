from __future__ import annotations
import json
import os
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", "demo")
    base_url: str = os.getenv("OPENAI_COMPATIBLE_BASE_URL", "")
    api_key: str = os.getenv("OPENAI_COMPATIBLE_API_KEY", "")
    model: str = os.getenv("OPENAI_COMPATIBLE_MODEL", "demo-model")
    timeout_seconds: int = 120

class LLMClient:
    def __init__(self, config: Optional[LLMConfig] = None) -> None:
        self.config = config or LLMConfig()

    def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback: Callable[[], Dict[str, Any]],
    ) -> Dict[str, Any]:
        if self.config.provider == "demo":
            return fallback()
        if not self.config.api_key or not self.config.base_url:
            return fallback()
        try:
            return self._call_openai_compatible(system_prompt, user_prompt)
        except Exception:
            return fallback()

    def _call_openai_compatible(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        base = self.config.base_url.rstrip("/")
        url = f"{base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
            "response_format": {"type": "json_object"},
        }
        response = requests.post(url, headers=headers, json=payload, timeout=self.config.timeout_seconds)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return _extract_json(content)

def _extract_json(content: str) -> Dict[str, Any]:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?", "", content).strip()
        content = re.sub(r"```$", "", content).strip()
    return json.loads(content)
