from __future__ import annotations
import json
from pathlib import Path

import streamlit as st

from src.utils.llm_client import LLMConfig
from src.utils.exporter import export_all
from src.workflows.video_pipeline import VideoPipeline

st.set_page_config(page_title="AI Short Video Factory Agent", page_icon="🎬", layout="wide")

SAMPLES = {
    "POV Oversized T-shirt": "samples/tshirt_product.json",
    "Motor Oil Product": "samples/motor_oil_product.json",
    "Household Product": "samples/household_product.json",
}

def load_sample(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

st.title("🎬 AI Short Video Factory Agent")
st.caption("Multi-agent workflow for cross-border e-commerce TikTok video production")

with st.sidebar:
    st.header("LLM Settings")
    provider = st.selectbox("Provider", ["demo", "openai_compatible"], index=0)
    base_url = st.text_input("Base URL", value="")
    api_key = st.text_input("API Key", value="", type="password")
    model = st.text_input("Model", value="demo-model")
    st.divider()
    sample_name = st.selectbox("Load Sample", list(SAMPLES.keys()))
    sample = load_sample(SAMPLES[sample_name])

st.subheader("1. Product Brief")
col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("Product Name", value=sample.get("product_name", ""))
    category = st.text_input("Category", value=sample.get("category", ""))
    target_market = st.text_input("Target Market", value=sample.get("target_market", ""))
    target_audience = st.text_input("Target Audience", value=sample.get("target_audience", ""))
with col2:
    video_goal = st.text_input("Video Goal", value=sample.get("video_goal", "TikTok conversion short video"))
    preferred_style = st.text_area("Preferred Style", value=sample.get("preferred_style", ""), height=80)
    selling_points_text = st.text_area("Selling Points, one per line", value="\n".join(sample.get("selling_points", [])), height=120)
    constraints_text = st.text_area("Constraints, one per line", value="\n".join(sample.get("constraints", [])), height=120)

product_input = {
    "product_name": product_name,
    "category": category,
    "target_market": target_market,
    "target_audience": target_audience,
    "selling_points": [x.strip() for x in selling_points_text.splitlines() if x.strip()],
    "video_goal": video_goal,
    "preferred_style": preferred_style,
    "constraints": [x.strip() for x in constraints_text.splitlines() if x.strip()],
}

run = st.button("Run Agent Workflow", type="primary")

if run:
    config = LLMConfig(provider=provider, base_url=base_url, api_key=api_key, model=model)
    pipeline = VideoPipeline(config)
    with st.spinner("Running multi-agent workflow..."):
        result = pipeline.run(product_input)
        files = export_all(result, "outputs")
    st.success("Workflow completed")

    st.subheader("2. Quality Score")
    score_cols = st.columns(5)
    score_report = result["evaluation"]["score_report"]
    for idx, (name, score) in enumerate(score_report.items()):
        with score_cols[idx % 5]:
            st.metric(name.replace("_", " ").title(), score)
    st.metric("Overall Score", result["evaluation"]["overall_score"])

    st.subheader("3. Storyboard")
    st.dataframe(result["storyboard"]["storyboard"], use_container_width=True)

    st.subheader("4. Model Prompts")
    st.dataframe(result["prompts"]["prompts"], use_container_width=True)

    st.subheader("5. Agent Trace")
    st.dataframe(result["trace"]["items"], use_container_width=True)

    st.subheader("6. Token & Cost Estimate")
    st.json(result["cost"])

    st.subheader("7. Exported Files")
    for label, path in files.items():
        st.write(f"- **{label}**: `{path}`")

    with st.expander("Full JSON Result"):
        st.json(result)
else:
    st.info("Choose a sample or edit the product brief, then click Run Agent Workflow.")
