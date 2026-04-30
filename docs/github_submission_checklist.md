# GitHub Submission Checklist

上传 GitHub 前确认：

- [ ] README.md 可以清楚说明项目背景、Agent 架构和运行方式。
- [ ] `streamlit run app.py` 可以正常打开页面。
- [ ] `python scripts/run_demo.py --sample samples/tshirt_product.json` 可以正常生成 outputs。
- [ ] `samples/` 里没有真实客户信息。
- [ ] `.env` 没有上传。
- [ ] `.env.example` 已上传。
- [ ] `outputs/` 里可以保留脱敏 demo 输出，也可以只保留 `.gitkeep`。
- [ ] 至少录制一条 1-2 分钟 demo 视频。
- [ ] GitHub 仓库不要只有一个 commit，建议拆成 8-12 个 commit。

## 推荐 Commit 顺序

```bash
git init
git add README.md ARCHITECTURE.md .gitignore .env.example requirements.txt
git commit -m "init project scaffold"

git add src/utils src/agents/base.py
git commit -m "add llm client and agent base classes"

git add src/agents/product_parser.py src/agents/market_agent.py
git commit -m "add product parser and market agents"

git add src/agents/script_agent.py src/agents/storyboard_agent.py
git commit -m "add script and storyboard agents"

git add src/agents/prompt_agent.py src/agents/evaluator_agent.py src/agents/cost_agent.py
git commit -m "add prompt evaluator and cost agents"

git add src/workflows scripts samples templates
git commit -m "add video production workflow and samples"

git add app.py
git commit -m "add streamlit demo ui"

git add docs tests
git commit -m "add docs tests and token plan materials"
```

## 提交到 GitHub

```bash
git branch -M main
git remote add origin https://github.com/yourname/ai-short-video-factory-agent.git
git push -u origin main
```
