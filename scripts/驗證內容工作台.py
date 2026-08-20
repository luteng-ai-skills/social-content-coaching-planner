#!/usr/bin/env python3
"""驗證 JSON、HTML 模板與已產生工作台的必要契約。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALLOWED_STATUSES = {
    "待研究",
    "研究完成",
    "待補本人觀點",
    "寫作中",
    "草稿待確認",
    "已確認",
    "待排程",
    "已排程",
    "已發布",
    "封存",
}
ALLOWED_EVIDENCE_STATUSES = {"未檢查", "待補資料", "足夠", "已確認可寫"}
ALLOWED_LENGTH_MODES = {"", "短篇", "中篇", "長篇", "自訂"}


def validate_json(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"JSON 無法讀取：{exc}"]

    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion 必須是 1")
    workspace = data.get("workspace", {})
    if workspace.get("periodWeeks") not in (2, 4):
        errors.append("periodWeeks 必須是 2 或 4")
    if not re.fullmatch(r"\d{4}-\d{2}", str(workspace.get("month", ""))):
        errors.append("workspace.month 必須是 YYYY-MM")

    ids: set[str] = set()
    for index, article in enumerate(data.get("articles", []), start=1):
        article_id = article.get("id")
        if not article_id:
            errors.append(f"第 {index} 篇缺少 id")
        elif article_id in ids:
            errors.append(f"文章 id 重複：{article_id}")
        ids.add(article_id)
        if article.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{article_id or index} 使用未知狀態：{article.get('status')}")
        evidence = article.get("evidenceGate")
        if evidence is not None:
            if evidence.get("status") not in ALLOWED_EVIDENCE_STATUSES:
                errors.append(f"{article_id or index} 使用未知素材狀態：{evidence.get('status')}")
            if evidence.get("status") == "待補資料" and article.get("status") != "待補本人觀點":
                errors.append(f"{article_id or index} 素材待補時，文章狀態必須是待補本人觀點")
        length_plan = article.get("lengthPlan")
        if length_plan is not None and length_plan.get("mode", "") not in ALLOWED_LENGTH_MODES:
            errors.append(f"{article_id or index} 使用未知篇幅：{length_plan.get('mode')}")

    confirmed = [pillar for pillar in data.get("pillars", []) if pillar.get("status") == "confirmed"]
    if confirmed:
        total = sum(float(pillar.get("ratio", 0)) for pillar in confirmed)
        if abs(total - 100) > 0.001:
            errors.append(f"已確認內容柱比例總和應為 100，目前為 {total:g}")
    library = data.get("sourceLibrary", {})
    source_ids = {item.get("id") for item in library.get("sources", []) if item.get("id")}
    for case in library.get("caseCards", []):
        if not case.get("id"):
            errors.append("案例卡缺少 id")
        if case.get("sourceId") and case.get("sourceId") not in source_ids:
            errors.append(f"案例卡 {case.get('id') or '未命名'} 連結不存在的來源：{case.get('sourceId')}")
    return errors


def validate_html(path: Path, generated: bool) -> list[str]:
    errors: list[str] = []
    html = path.read_text(encoding="utf-8")
    required = (
        'id="calendar-grid"',
        'id="article-drawer"',
        'id="import-file"',
        'id="export-json"',
        'id="export-markdown"',
        'aria-label="陪跑選單"',
        'id="open-next-article"',
        'id="save-status"',
        'id="initial-data"',
        "localStorage",
        "beforeunload",
        "scheduleDrawerAutosave",
        "evidenceGate",
        "lengthPlan",
        "appliedStyle",
        'data-tab="sources"',
        'id="source-library-grid"',
        "sourceLibrary",
        "exportChangeRequest",
    )
    for marker in required:
        if marker not in html:
            errors.append(f"HTML 缺少必要標記：{marker}")
    if generated and "__WORKSPACE_JSON__" in html:
        errors.append("已產生 HTML 仍含資料佔位符")
    if not generated and html.count("__WORKSPACE_JSON__") != 1:
        errors.append("模板必須且只能包含一個資料佔位符")
    if re.search(r"<script[^>]+src=|<link[^>]+href=", html, re.IGNORECASE):
        errors.append("HTML 不得依賴外部 script 或 stylesheet")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--html", required=True, type=Path)
    parser.add_argument("--generated", action="store_true")
    args = parser.parse_args()

    errors = validate_json(args.json.resolve()) + validate_html(args.html.resolve(), args.generated)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: JSON 與 HTML 契約驗證通過")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
