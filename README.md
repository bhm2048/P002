# Flask App

一個輕量的 Flask 後端範例，提供時間查詢與 Echo API，並附有完整的測試套件。

## 專案簡介

單一檔案架構的 Flask 應用，示範 RESTful API 設計、JSON 資料處理與 Jinja2 模板渲染。前端使用 Bootstrap 5，透過 `fetch` 呼叫後端 API 動態顯示當前時間。

## 技術棧

| 層級 | 技術 |
|------|------|
| 後端框架 | Flask 3.1 |
| 模板引擎 | Jinja2 3.1 |
| 前端 UI | Bootstrap 5.3.3 (CDN) |
| 測試框架 | pytest |
| Python | 3.8+ |

## 安裝步驟

```bash
# 1. 複製專案
git clone <repo-url>
cd P002

# 2. 建立虛擬環境（建議）
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. 安裝依賴
pip install -r requirements.txt
```

## 執行方式

**啟動開發伺服器**

```bash
python app.py
```

伺服器預設運行於 `http://127.0.0.1:5000`

**執行測試**

```bash
# 執行所有測試
python -m pytest test_app.py -v

# 執行單一測試
python -m pytest test_app.py::test_echo_adds_received_at -v
```

## API 列表

### `GET /`

渲染首頁，透過 JavaScript 呼叫 `/api/time` 顯示目前時間。

---

### `GET /api/time`

回傳伺服器目前時間。

**Response**

```json
{
  "time": "14:30:00",
  "date": "2026-04-29",
  "iso": "2026-04-29T14:30:00.123456"
}
```

---

### `POST /api/echo`

將 request body 原樣回傳，並附加 `received_at` 時間戳記。

**Request Headers**

```
Content-Type: application/json
```

**Request Body**

任意 JSON 物件（key 名稱不可與 `received_at` 衝突）。

**Response（成功）**

```json
{
  "msg": "hello",
  "value": 42,
  "received_at": "2026-04-29T14:30:00.123456"
}
```

**Response（失敗）**

| Status | 情境 |
|--------|------|
| `415 Unsupported Media Type` | Content-Type 非 `application/json` |
| `405 Method Not Allowed` | 使用 GET 呼叫此端點 |

錯誤回應格式：

```json
{
  "error": "Content-Type must be application/json"
}
```

## 專案結構

```
P002/
├── app.py              # Flask 應用主程式
├── requirements.txt    # 依賴套件
├── test_app.py         # pytest 測試
└── templates/
    ├── base.html       # 基礎模板（Bootstrap、Navbar）
    └── index.html      # 首頁模板
```
