# AI Short Video Factory Agent

> Cross-border e-commerce short-video multi-agent production workflow.  
> 中文名：跨境电商 AI 带货视频多 Agent 生产系统。

这个项目用于把一个产品 Brief 自动转化为：

- TikTok 带货脚本
- 15s / 24s / 30s 短视频方案
- 可执行分镜表
- VEO / Seedance / WAN 视频生成提示词
- AI 生成风险评估
- 质量评分
- Token 与成本估算
- Markdown / JSON / CSV / Excel 导出文件

项目定位不是普通聊天机器人，而是一个面向真实业务链路的 **multi-agent workflow**，适合用于申请大模型 Token Plan、展示 Agent 架构能力、证明高频 Token 消耗场景。

---

## 1. 业务背景

跨境电商短视频生产中，运营给到的产品资料通常不标准：有时只有商品图，有时只有一句卖点，有时目标市场、用户画像、视频时长、镜头风格都不明确。人工从产品资料整理、脚本创作、分镜拆解、视频模型提示词编写到质量评估，需要反复沟通，导致团队产能不稳定、内容质量波动大。

本项目通过多个 Agent 协作，将产品资料转化为可直接执行的短视频生产方案，降低人工提示词编写成本，并让不同组员按照统一标准产出内容。

---

## 2. Agent 架构

```mermaid
flowchart TD
    A[Product Input / SKU Brief] --> B[Product Parser Agent]
    B --> C[Market & Audience Agent]
    C --> D[Script Agent]
    D --> E[Storyboard Agent]
    E --> F[Prompt Compiler Agent]
    F --> G[Quality Evaluator Agent]
    G --> H[Cost & Token Agent]
    H --> I[Export: Markdown / JSON / CSV / Excel]
```

### Agent 列表

| Agent | 作用 | 输出 |
|---|---|---|
| Product Parser Agent | 解析产品资料、标准化卖点、提取限制条件 | product brief |
| Market Agent | 根据目标国家和用户画像制定内容方向 | market strategy |
| Script Agent | 生成 15s / 24s / 30s TikTok 带货脚本 | scripts |
| Storyboard Agent | 将脚本拆成镜头、景别、动作、转场 | storyboard |
| Prompt Agent | 生成 VEO / Seedance / WAN / Image prompt | prompts |
| Evaluator Agent | 评估镜头可执行性、卖点清晰度、AI 风险 | score report |
| Cost Agent | 统计输入/输出 Token 和预估成本 | cost report |

---

## 3. 快速开始

### 3.1 安装依赖

```bash
pip install -r requirements.txt
```

### 3.2 Demo 模式运行

不需要 API Key，直接使用内置规则模拟多 Agent 工作流：

```bash
streamlit run app.py
```

或者命令行运行：

```bash
python scripts/run_demo.py --sample samples/tshirt_product.json
```


示例导出结果已经放在 `demo_outputs/`，可以作为 GitHub 页面展示素材；真实运行生成的文件会进入 `outputs/`。

运行后会在 `outputs/` 目录生成：

- `result.json`
- `result.md`
- `storyboard.csv`
- `prompts.csv`
- `trace.json`
- `result.xlsx`（如果本地安装了 openpyxl）

### 3.3 接入 OpenAI-compatible API

复制环境变量模板：

```bash
cp .env.example .env
```

填写：

```env
LLM_PROVIDER=openai_compatible
OPENAI_COMPATIBLE_BASE_URL=https://api.example.com/v1
OPENAI_COMPATIBLE_API_KEY=your_api_key
OPENAI_COMPATIBLE_MODEL=your-model-name
```

如果使用 MiMo / DeepSeek / OpenRouter / 其他兼容 OpenAI Chat Completions 的模型，只需要替换 base url、api key 和 model name。

---

## 4. 示例输入

```json
{
  "product_name": "POV Oversized T-shirt",
  "category": "fashion",
  "target_market": "Indonesia",
  "target_audience": "18-30 young TikTok users",
  "selling_points": [
    "oversized streetwear fit",
    "soft cotton fabric",
    "bold front print",
    "easy to match with jeans and cargo pants"
  ],
  "video_goal": "TikTok conversion short video",
  "preferred_style": "streetwear OOTD, realistic model, fast rhythm",
  "constraints": [
    "avoid complex cloth tearing interaction",
    "avoid exaggerated body deformation",
    "9:16 vertical video"
  ]
}
```
