from __future__ import annotations
from typing import Any, Dict, Optional
from src.agents.product_parser import ProductParserAgent
from src.agents.market_agent import MarketAgent
from src.agents.script_agent import ScriptAgent
from src.agents.storyboard_agent import StoryboardAgent
from src.agents.prompt_agent import PromptAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.cost_agent import CostAgent
from src.utils.llm_client import LLMClient, LLMConfig
from src.utils.trace import WorkflowTrace

class VideoPipeline:
    def __init__(self, config: Optional[LLMConfig] = None) -> None:
        self.client = LLMClient(config)
        self.product_parser = ProductParserAgent(self.client)
        self.market_agent = MarketAgent(self.client)
        self.script_agent = ScriptAgent(self.client)
        self.storyboard_agent = StoryboardAgent(self.client)
        self.prompt_agent = PromptAgent(self.client)
        self.evaluator_agent = EvaluatorAgent(self.client)
        self.cost_agent = CostAgent(self.client)

    def run(self, product_input: Dict[str, Any]) -> Dict[str, Any]:
        trace = WorkflowTrace()
        product_brief = self.product_parser.run(product_input, trace)
        market_strategy = self.market_agent.run({"product_brief": product_brief}, trace)
        scripts = self.script_agent.run({"product_brief": product_brief, "market_strategy": market_strategy}, trace)
        storyboard = self.storyboard_agent.run({"product_brief": product_brief, "market_strategy": market_strategy, "scripts": scripts}, trace)
        prompts = self.prompt_agent.run({"product_brief": product_brief, "storyboard": storyboard}, trace)
        evaluation = self.evaluator_agent.run({"product_brief": product_brief, "storyboard": storyboard, "prompts": prompts}, trace)
        trace_before_cost = trace.to_dict()
        cost = self.cost_agent.run({"trace": trace_before_cost, "product_brief": product_brief}, trace)
        return {
            "product_brief": product_brief,
            "market_strategy": market_strategy,
            "scripts": scripts,
            "storyboard": storyboard,
            "prompts": prompts,
            "evaluation": evaluation,
            "cost": cost,
            "trace": trace.to_dict(),
        }
