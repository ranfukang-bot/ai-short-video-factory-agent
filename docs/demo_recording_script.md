# Demo Recording Script

建议录屏时长：1-2 分钟。

## 录屏流程

1. 打开终端，运行：

```bash
streamlit run app.py
```

2. 浏览器打开 Streamlit 页面。

3. 左侧选择 `POV Oversized T-shirt` 示例。

4. 口播或字幕说明：

> This is a multi-agent workflow for cross-border e-commerce TikTok video production. It takes a product brief and generates scripts, storyboard, video model prompts, quality evaluation and token cost estimate.

5. 点击 `Run Agent Workflow`。

6. 展示 Quality Score：说明系统会评估卖点清晰度、TikTok 节奏、AI 可生成性、转化潜力、本地化适配度。

7. 展示 Storyboard：说明每个镜头都有时长、场景、运镜、动作、卖点焦点和 AI 风险。

8. 展示 Model Prompts：说明系统会自动生成 VEO / Seedance / WAN 三类视频模型提示词。

9. 展示 Agent Trace：说明每个 Agent 的输入、输出、耗时、Token 估算都被记录。

10. 展示导出文件：`outputs/result.md`、`outputs/result.json`、`outputs/storyboard.csv`、`outputs/prompts.csv`、`outputs/trace.json`。

## 一句话介绍

This project is not a simple chatbot. It is an agentic production pipeline for real e-commerce short-video creation, designed for repeated SKU-level batch processing and high-frequency token usage.
