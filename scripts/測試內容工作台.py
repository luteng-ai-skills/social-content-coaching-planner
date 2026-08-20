#!/usr/bin/env python3
"""內容工作台產生器的最小行為測試。"""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = Path(__file__).with_name("建立內容工作台.py")
SAMPLE_PATH = ROOT / "assets" / "範例內容規劃.json"
TEMPLATE_PATH = ROOT / "assets" / "一個月內容工作台模板.html"


def load_generator():
    spec = importlib.util.spec_from_file_location("workbench_generator", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    generator = load_generator()
    sample = generator.load_workspace(SAMPLE_PATH)
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    rendered = generator.render(template, sample)
    check("__WORKSPACE_JSON__" not in rendered, "產生結果不應保留佔位符")
    check('"periodWeeks":2' in rendered, "兩週模式資料未內嵌")
    check('id="calendar-grid"' in rendered, "月曆容器不存在")
    check("localStorage" in rendered, "缺少本機暫存能力")
    check("exportChangeRequest" in rendered, "缺少單篇修改需求輸出")
    check('aria-label="陪跑選單"' in rendered, "Cowork 工作台缺少可見陪跑選單")
    check('id="open-next-article"' in rendered, "缺少下一篇快捷入口")
    check("beforeunload" in rendered, "缺少未匯出離頁警告")
    check("scheduleDrawerAutosave" in rendered, "缺少文章輸入自動暫存")
    check("lengthPlan" in rendered, "缺少短中長篇幅設定")
    check("evidenceGate" in rendered, "缺少素材充足度閘門")
    check("appliedStyle" in rendered, "缺少本篇語氣與排版套用設定")
    check('data-tab="sources"' in rendered, "陪跑選單缺少案例與來源入口")
    check('id="source-library-grid"' in rendered, "缺少來源索引與案例卡容器")
    check("sourceLibrary" in rendered, "缺少來源索引與案例卡資料")

    four_weeks = json.loads(json.dumps(sample, ensure_ascii=False))
    four_weeks["workspace"]["periodWeeks"] = 4
    four_weeks["publishingBatch"]["scope"] = "四週"
    four_weeks["publishingBatch"]["confirmationPhrase"] = "確認整月排程"
    rendered_four = generator.render(template, four_weeks)
    check('"periodWeeks":4' in rendered_four, "四週模式資料未內嵌")
    check("確認整月排程" in rendered_four, "四週確認語句未保留")

    hostile = json.loads(json.dumps(sample, ensure_ascii=False))
    hostile["articles"][0]["draft"]["body"] = "測試 </script><script>alert(1)</script>"
    rendered_hostile = generator.render(template, hostile)
    check("</script><script>alert(1)</script>" not in rendered_hostile, "內嵌 JSON 未處理 script 結束標記")

    invalid = json.loads(json.dumps(sample, ensure_ascii=False))
    invalid["workspace"]["periodWeeks"] = 3
    with tempfile.TemporaryDirectory() as temp_dir:
        invalid_path = Path(temp_dir) / "invalid.json"
        invalid_path.write_text(json.dumps(invalid, ensure_ascii=False), encoding="utf-8")
        try:
            generator.load_workspace(invalid_path)
        except ValueError:
            pass
        else:
            raise AssertionError("錯誤週期應被拒絕")

    print("PASS: 兩週、四週、HTML 內嵌與錯誤資料測試通過")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
