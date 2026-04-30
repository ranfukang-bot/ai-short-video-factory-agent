from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.llm_client import LLMConfig
from src.utils.exporter import export_all
from src.workflows.video_pipeline import VideoPipeline

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", default="samples/tshirt_product.json")
    parser.add_argument("--output", default="outputs")
    args = parser.parse_args()

    sample_path = ROOT / args.sample
    product = json.loads(sample_path.read_text(encoding="utf-8"))
    pipeline = VideoPipeline(LLMConfig(provider="demo"))
    result = pipeline.run(product)
    files = export_all(result, ROOT / args.output)
    print(json.dumps({"status": "success", "files": files, "cost": result["cost"]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
