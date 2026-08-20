# 社群內容陪跑規劃師

這是一套給內容新手使用的繁體中文 Skill。它會先確認本人思維、受眾與內容柱，再建立兩週或四週內容月曆，陪使用者逐篇完成研究、證據檢查、寫作、修改、歸檔與排程前確認。

目前版本：**v0.2.0**

## v0.2.0 重點

- 一次只問一題；工作頁保留可見的「陪跑選單」與「開啟下一篇」。
- 人物思維、來源索引、案例資料卡與單篇寫作依據分層，不把摘要當成完整案例庫。
- 每篇動筆前先檢查實際來源、已知事實、缺口與不可越界推論；素材不足時停止成稿。
- 依平台、主題與素材量，建議短篇、中篇、長篇或自訂字數，不再固定套用同一範圍。
- 依本人已確認的語氣、句長、段落、換行、開頭、收尾與 CTA 寫作。
- HTML 工作台支援自動暫存、未備份提示、附時間 JSON 匯出及舊版 `schemaVersion: 1` 資料。
- 不保存密碼、Token、Cookie 或 OAuth 憑證；不會自行發布或建立週期性排程。

## 下載

請從 [GitHub Releases](https://github.com/luteng-ai-skills/social-content-coaching-planner/releases) 下載最新正式 ZIP：

`social-content-coaching-planner-v0.2.0.zip`

SHA-256：`6c5ff89262ff66080d9e7ba79f26cf3d74305f9a0930e0a8c458b6cec0f27d67`

## 安裝到 Codex

1. 下載 ZIP 並解壓縮。
2. 確認解壓後的 `social-content-coaching-planner` 第一層直接包含 `SKILL.md`、`agents`、`assets`、`references` 與 `scripts`。
3. 新版 Codex 環境優先放到 `~/.agents/skills/social-content-coaching-planner`；若你的既有環境已明確使用 `~/.codex/skills`，沿用有效位置即可，不要同時安裝兩份。
4. 建立新任務後明確呼叫 `$social-content-coaching-planner`。

## 安裝到 Claude Cowork

1. 保留正式 ZIP，不要先解壓縮。
2. 到 **Customize → Skills → Add／Upload a skill** 上傳 ZIP。
3. 啟用新版並關閉舊版，建立新任務測試。
4. 新工作頁應看得到陪跑選單、案例與來源、目前階段及下一篇入口。

## 建議測試語

> 請使用「社群內容陪跑規劃師」，一次只問我一題。先確認我有沒有現成的本人思維或人設資料，不要直接替我寫貼文。

## 正式資料與更新

JSON 是跨任務與跨工具的正式主版本；HTML 與瀏覽器暫存是操作介面，不取代正式備份。更新 Skill 前先保留自己的 JSON，不要用新版範例覆蓋個人資料。安裝新版後，以原 JSON 重建工作台並重新讀回確認。

## 開發與驗證

需要 Python 3。可在 Skill 根目錄執行：

```bash
python3 scripts/測試內容工作台.py
python3 scripts/驗證內容工作台.py --json assets/範例內容規劃.json --html assets/一個月內容工作台模板.html
```

本儲存庫是公開的通用版本，不包含學員逐字稿、人物資料、客戶案例、內部 Notion 連結或平台憑證。
