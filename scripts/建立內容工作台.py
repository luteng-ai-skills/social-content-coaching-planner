#!/usr/bin/env python3
"""從內容規劃 JSON 產生可離線開啟的單檔 HTML 工作台。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "assets" / "一個月內容工作台模板.html"
TOKEN = "__WORKSPACE_JSON__"


def load_workspace(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if data.get("schemaVersion") != 1:
        raise ValueError("只支援 schemaVersion 1")

    workspace = data.get("workspace")
    if not isinstance(workspace, dict):
        raise ValueError("缺少 workspace")

    required = ("id", "learnerName", "month", "periodWeeks", "timezone")
    missing = [key for key in required if not workspace.get(key)]
    if missing:
        raise ValueError(f"workspace 缺少必要欄位：{', '.join(missing)}")

    if workspace["periodWeeks"] not in (2, 4):
        raise ValueError("periodWeeks 只能是 2 或 4")

    for key in ("audiences", "pillars", "articles"):
        if not isinstance(data.get(key), list):
            raise ValueError(f"{key} 必須是陣列")

    return data


def render(template: str, data: dict) -> str:
    if template.count(TOKEN) != 1:
        raise ValueError("HTML 模板必須且只能包含一個資料佔位符")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")
    return template.replace(TOKEN, payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="內容規劃 JSON")
    parser.add_argument("--output", required=True, type=Path, help="輸出 HTML")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="HTML 模板")
    args = parser.parse_args()

    data = load_workspace(args.input.resolve())
    template = args.template.resolve().read_text(encoding="utf-8")
    html = render(template, data)
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    args.output.resolve().write_text(html, encoding="utf-8")
    print(f"已建立：{args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
