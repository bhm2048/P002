# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# 安裝依賴
pip install flask pytest

# 啟動開發伺服器 (http://127.0.0.1:5000)
python app.py

# 執行所有測試
python -m pytest test_app.py -v

# 執行單一測試
python -m pytest test_app.py::test_echo_adds_received_at -v
```

## Architecture

單一檔案 Flask 應用，`app.py` 即為完整後端。

**路由：**
- `GET /` — 渲染 `templates/index.html`
- `GET /api/time` — 回傳目前時間（JSON，含 `time`、`date`、`iso` 欄位）
- `POST /api/echo` — 接收 JSON body，原樣回傳並附加 `received_at`（ISO 8601）；非 JSON Content-Type 回傳 415

**Templates：**
- `templates/base.html` — Bootstrap 5.3.3 CDN（SRI hash 已內嵌）、navbar、`title` / `content` blocks
- `templates/index.html` — 繼承 `base.html`，透過 `fetch /api/time` 顯示目前時間

**測試：**
- `test_app.py` 使用 Flask `test_client()` fixture，不需啟動伺服器
- 目前測試集中於 `/api/echo`；`/api/time` 與首頁渲染尚無測試

## API 規範

`/api/echo` 的回傳格式為 request body 原地 mutation 後加上 `received_at`，因此呼叫端的 key 名稱不能與 `received_at` 衝突。
