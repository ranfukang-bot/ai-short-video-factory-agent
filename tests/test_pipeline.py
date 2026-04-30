from src.utils.llm_client import LLMConfig
from src.workflows.video_pipeline import VideoPipeline

def test_pipeline_demo_runs():
    product = {
        "product_name": "Test Product",
        "category": "household",
        "target_market": "Southeast Asia",
        "target_audience": "TikTok shoppers",
        "selling_points": ["simple", "useful", "affordable"],
        "constraints": ["9:16 vertical video"],
    }
    pipeline = VideoPipeline(LLMConfig(provider="demo"))
    result = pipeline.run(product)
    assert result["product_brief"]["product_name"] == "Test Product"
    assert len(result["storyboard"]["storyboard"]) > 0
    assert len(result["prompts"]["prompts"]) > 0
    assert result["evaluation"]["overall_score"] >= 70
    assert result["cost"]["total_tokens"] > 0
