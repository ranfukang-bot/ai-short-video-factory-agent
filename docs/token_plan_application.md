# Token Plan Application Text

## 04 请描述你使用 Agent 或 AI 驱动构建的具体成果

我正在构建一个面向跨境电商短视频生产的多 Agent 系统：AI Short Video Factory Agent。它解决的核心痛点是：运营提供的产品资料通常零散、不标准，人工从产品卖点整理、TikTok 脚本创作、分镜拆解、VEO/Seedance/WAN 视频提示词生成到质量评估，链路长且质量波动大，导致团队产能难以稳定放大。

该项目通过多个 Agent 协作完成完整生产流程：Product Parser Agent 负责解析产品资料；Market Agent 负责根据目标国家和用户画像制定内容方向；Script Agent 生成多版本带货脚本；Storyboard Agent 将脚本拆解为可执行镜头；Prompt Agent 自动生成适配 VEO、Seedance、WAN 等视频模型的提示词；Evaluator Agent 对镜头可执行性、卖点清晰度、AI 生成风险和转化潜力进行评分；Cost Agent 统计每次任务的 Token 消耗和预估成本。

该系统已经可以将一个产品 Brief 自动转化为脚本、分镜、视频模型提示词、质检评分和导出文件，适用于 TikTok 海外电商短视频批量生产。后续计划接入 OpenClaw / Claude Code / MiMo API，用于团队级别的 Agent 工作流自动化，提高每日视频方案产出效率，并降低人工提示词编写和质检成本。

## 05 使用证明与影响力证明建议提交材料

建议提交：

1. GitHub 仓库链接。
2. 项目 README 截图。
3. 本地运行 Streamlit 页面截图。
4. Agent 工作流日志截图。
5. 生成脚本、分镜、Prompt、评分报告的结果截图。
6. `outputs/trace.json` 或 `outputs/result.md`，证明多 Agent 执行链路。
7. 1-2 分钟屏幕录制，从输入产品 Brief 到输出完整方案。
8. 如果有 API 使用账单或 Token 消耗截图，可以补充上传；没有则使用项目 trace 中的 Token 估算日志。

## GitHub 链接说明填写示例

GitHub Repository: `https://github.com/yourname/ai-short-video-factory-agent`

Demo Description:

This repository demonstrates a multi-agent workflow for cross-border e-commerce short-video production. It converts product briefs into TikTok scripts, storyboards, VEO/Seedance/WAN prompts, quality evaluation reports, and token/cost estimates. The project supports demo mode and OpenAI-compatible model integration, making it suitable for real-world high-frequency agentic tasks.
