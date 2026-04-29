# Vibe Coding 入門教程:Antigravity + WSL + Claude Code 完整工作流

> 本教程示範如何在 **Google Antigravity IDE** + **WSL2 (Ubuntu)** 環境中,使用 **Claude Code** 開發一個簡易的 Flask 網頁應用,並透過 **Git** 管理版本、最後推送到 **GitHub**。
>
> 預計完成時間:約 60 分鐘
> 適用對象:會基本 Linux/Git 指令,但尚未整合過這套 AI 輔助工作流的開發者。

---

## 目錄

1. [什麼是 Vibe Coding?](#1-什麼是-vibe-coding)
2. [環境準備清單](#2-環境準備清單)
3. [WSL Ubuntu 環境設定](#3-wsl-ubuntu-環境設定)
4. [安裝並設定 Google Antigravity](#4-安裝並設定-google-antigravity)
5. [安裝 Claude Code](#5-安裝-claude-code)
6. [建立專案與 venv 虛擬環境](#6-建立專案與-venv-虛擬環境)
7. [使用 Claude Code 開發 Flask 應用](#7-使用-claude-code-開發-flask-應用)
8. [Git 版本控制流程](#8-git-版本控制流程)
9. [推送到 GitHub](#9-推送到-github)
10. [常見問題排解](#10-常見問題排解)

---

## 1. 什麼是 Vibe Coding?

「Vibe Coding」這個詞源自 Andrej Karpathy 在 2025 年初的描述,指的是一種以**自然語言對 AI 表達意圖**、由 AI 撰寫實際程式碼,開發者則專注於**驗證、測試、迭代**的開發風格。

這套工作流的核心三角:

- **Antigravity**:agent-first 的 IDE,提供 Mission Control 來管理多個 AI agent 平行任務。
- **Claude Code**:在終端機中執行的 AI 編碼助手,能讀取檔案、執行指令、操作 Git。
- **WSL + venv + Git**:確保開發環境乾淨、可重現、可追溯。

工具是 AI,但「乾淨可重現」這件事還是要靠工程基本功。

---

## 2. 環境準備清單

開始前請確認:

- Windows 10/11(建議 Windows 11)
- 已啟用 WSL2,並安裝 Ubuntu(20.04 以上)
- 一個 GitHub 帳號
- 一個 Anthropic 帳號(需要 Claude Pro 或 API credits 才能使用 Claude Code,免費版不含)
- 一個 Google 帳號(用於 Antigravity 登入)

### 確認 WSL 已安裝

開啟 PowerShell:

```powershell
wsl -l -v
```

應該看到類似:

```
NAME      STATE     VERSION
Ubuntu    Running   2
```

若沒有,執行(以系統管理員身份):

```powershell
wsl --install -d Ubuntu
```

完成後重開機。

---

## 3. WSL Ubuntu 環境設定

### 3.1 為什麼要用 WSL?

簡單一句:**讓 Windows 開發者用 Linux 工具鏈,而不必雙開機或裝 VM**。

具體理由:

- Python、Node.js 套件大量依賴 POSIX 行為,在 Linux 上跑得最順。
- 部署目標多半是 Linux server,本機環境一致能避免「我電腦上是好的」的悲劇。
- WSL2 是真正的 Linux kernel,效能比 WSL1 好得多。

### 3.2 進入 Ubuntu 並更新

從開始選單開啟 Ubuntu,首次進入時會要你建立使用者名稱與密碼。然後:

```bash
sudo apt update && sudo apt upgrade -y
```

### 3.3 安裝開發必備工具

```bash
sudo apt install -y python3 python3-venv python3-pip git curl build-essential
```

確認版本:

```bash
python3 --version    # 應為 3.10 以上
git --version
```

### 3.4 設定 Git 身份

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

### 3.5 重要:把專案放在 Linux 檔案系統內

請**務必**把專案放在 `~/projects/` 之類的 Linux 路徑,**不要**放在 `/mnt/c/...`。

原因:WSL2 跨檔案系統存取的 I/O 效能差將近 20 倍,而且 Git、Python 套件管理在 Windows 檔案系統上常出現權限與行尾(CRLF)問題。

```bash
mkdir -p ~/projects
cd ~/projects
```

---

## 4. 安裝並設定 Google Antigravity

### 4.1 下載與安裝(Windows 端)

1. 前往 [antigravity.google/download](https://antigravity.google/download)
2. 選擇 **Download for x64**(一般 PC)或 ARM64(Surface Pro X 等)
3. 雙擊 `.exe` 安裝(發行者應顯示 Google LLC)
4. 從開始選單啟動 Antigravity

> Antigravity 是 Google 的 agent-first IDE,基於 VS Code fork 而來,因此熟悉的快捷鍵、設定、外觀都通用。

### 4.2 首次設定

啟動精靈會詢問:

- **Setup flow**:選 *Fresh Start*(或從 VS Code/Cursor 匯入設定)
- **Theme**:依個人喜好
- **Agent execution mode**:建議先選 *Ask before executing*(每次執行終端機指令前先詢問),熟悉後再考慮放寬

### 4.3 連接到 WSL

雖然 Antigravity 的擴充市集會說 Remote-WSL 擴充「不相容」,但實際上 Remote-WSL 連線功能仍然可用。

操作步驟:

1. 按 `Ctrl + Shift + P` 開啟命令面板
2. 輸入 `WSL: Connect to WSL`
3. 選擇你的 Ubuntu 發行版

連線成功後,左下角會顯示 `[WSL: Ubuntu]`,接下來開啟資料夾、開終端機都會在 WSL 內執行。

### 4.4 開啟內建終端機

`` Ctrl + ` ``(反引號)開啟終端機,確認 prompt 是 Linux 形式(例如 `username@HOSTNAME:~$`),而非 PowerShell。

---

## 5. 安裝 Claude Code

> ⚠️ Claude Code 必須安裝在 **WSL Ubuntu 內**,而非 Windows 端。確認你的終端機 prompt 是 Linux 形式再繼續。

### 5.1 用原生安裝程式安裝(推薦)

原生安裝程式不需要 Node.js,且支援自動更新:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

完成後重啟終端機,驗證:

```bash
claude --version
```

### 5.2 替代方案:用 npm 安裝

如果你已有 Node.js 18+,也可:

```bash
# 設定使用者層級 npm 路徑,避免 sudo 權限問題
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

npm install -g @anthropic-ai/claude-code
```

> **不要**用 `sudo npm install -g`,會造成權限問題。

### 5.3 首次認證

在任何目錄執行:

```bash
claude
```

它會開啟瀏覽器讓你登入 Anthropic 帳號。完成後 token 會存在本機,之後就不必再登入。

---

## 6. 建立專案與 venv 虛擬環境

### 6.1 建立專案資料夾

```bash
cd ~/projects
mkdir flask-vibe-demo && cd flask-vibe-demo
```

### 6.2 建立 venv 虛擬環境(關鍵!)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

啟動成功後,prompt 前面會出現 `(.venv)`。

### 6.3 為什麼一定要用 venv?

這是新手最容易跳過的步驟,但其實是工程基本功裡最重要的一環。

| 沒用 venv | 用 venv |
|---|---|
| 所有專案的套件都裝在系統 Python | 每個專案有獨立的套件目錄 |
| A 專案需要 Flask 2.x、B 需要 Flask 3.x → 衝突 | 各自獨立,互不影響 |
| `pip install` 可能要 sudo,容易把系統弄壞 | 完全在使用者目錄,無權限風險 |
| 專案搬家或部署時不知該裝什麼 | `pip freeze > requirements.txt` 一鍵還原 |
| Ubuntu 24.04 之後會直接拒絕安裝(PEP 668) | 唯一被官方推薦的做法 |

特別是最後一點:從 Ubuntu 23.04 / Python 3.11 之後,系統 Python 會被標記為「externally-managed」,不用 venv 直接 `pip install` 會直接報錯。所以 venv 不是「最佳實踐」,而是**現在的唯一實踐**。

### 6.4 安裝 Flask

```bash
pip install flask
pip freeze > requirements.txt
```

`requirements.txt` 是專案依賴的快照,之後別人(或部署環境)只要 `pip install -r requirements.txt` 就能還原一模一樣的環境。

### 6.5 建立 .gitignore

```bash
cat > .gitignore <<EOF
.venv/
__pycache__/
*.pyc
.env
.DS_Store
instance/
EOF
```

`.venv/` **絕對不能** commit 進 Git。它體積龐大、跟 OS 綁定、別人 clone 下來也用不了。Git 該追蹤的是 `requirements.txt`,不是虛擬環境本身。

---

## 7. 使用 Claude Code 開發 Flask 應用

### 7.1 在 Antigravity 中開啟專案

在 WSL 終端機:

```bash
cd ~/projects/flask-vibe-demo
code .       # 或在 Antigravity 中:File > Open Folder
```

### 7.2 啟動 Claude Code

在 Antigravity 內建終端機(`` Ctrl + ` ``):

```bash
source .venv/bin/activate    # 每次新終端都要重新啟動 venv
claude
```

進入 Claude Code 互動模式後,你可以用自然語言下指令。

### 7.3 第一個 prompt:讓 Claude 幫你建立基本結構

直接打:

```
請幫我建立一個簡單的 Flask 應用:
- 入口檔 app.py
- 首頁 / 顯示 "Hello, Vibe Coding!"
- /api/time 路徑回傳 JSON 格式的目前時間
- 使用 templates 目錄放 HTML
- 首頁要載入一個 base.html 模板,包含基本的 Bootstrap 5 CDN
```

Claude Code 會:

1. 列出它打算建立/修改的檔案
2. 在每個動作前詢問你確認(預設模式)
3. 寫完後自動跑語法檢查

### 7.4 驗證執行

請 Claude 跑起來:

```
請執行這個 Flask 應用,並告訴我用什麼網址可以打開
```

它會執行 `flask run` 或 `python app.py`,你打開瀏覽器到 `http://127.0.0.1:5000` 應該看到首頁。

> **WSL 網路提示**:WSL2 預設的 localhost 轉發在大多情況下能直接從 Windows 瀏覽器存取。若不行,參考第 10 節。

### 7.5 迭代改進

繼續 vibe:

```
我想加一個 /api/echo 路徑,接收 POST 請求的 JSON,
把收到的內容加上 "received_at" 時間戳後回傳。
也幫我寫對應的 pytest 測試。
```

Claude 會修改 `app.py`、新增 `tests/test_app.py`、必要時更新 `requirements.txt`。

### 7.6 給 Claude 留下專案備忘錄

最重要、但常被略過的一步:

```
請執行 /init
```

這會在專案根目錄產生 `CLAUDE.md`,記錄專案結構、執行指令、慣例。下次再開 Claude Code 時,它會自動讀取這個檔案,保持上下文一致。

---

## 8. Git 版本控制流程

Vibe coding 速度快,**正因如此** Git 不能省。每次有意義的進展都該 commit,出錯時才能回退。

### 8.1 初始化 Repo

```bash
git init
git add .
git status        # 確認 .venv/ 沒被追蹤
git commit -m "chore: initial project setup with Flask and venv"
```

### 8.2 commit message 慣例(建議)

採用 [Conventional Commits](https://www.conventionalcommits.org):

| 前綴 | 用途 | 範例 |
|---|---|---|
| `feat:` | 新功能 | `feat: add /api/echo endpoint` |
| `fix:` | 修 bug | `fix: handle empty request body` |
| `docs:` | 文件 | `docs: update README with setup steps` |
| `chore:` | 雜務 | `chore: add .gitignore` |
| `test:` | 測試 | `test: add tests for echo endpoint` |
| `refactor:` | 重構 | `refactor: extract route handlers to blueprint` |

### 8.3 讓 Claude Code 幫你 commit

Claude Code 內建 Git 整合,可以直接說:

```
請檢查我的修改、寫一個適當的 commit message、然後 commit
```

它會:

1. 跑 `git status` + `git diff`
2. 根據實際變更寫出符合 Conventional Commits 的訊息
3. 顯示給你確認後才執行

### 8.4 一個健康的迭代節奏

```
[改一小塊功能] → claude 驗證/測試 → git commit
```

不要一次寫完整個應用才 commit。小步快跑,出錯時 `git reset --hard HEAD~1` 就回去了。

### 8.5 查看歷史

```bash
git log --oneline --graph --decorate
```

---

## 9. 推送到 GitHub

### 9.1 在 GitHub 建立空 repo

1. 登入 [github.com](https://github.com)
2. 右上角 `+` → `New repository`
3. 名稱:`flask-vibe-demo`
4. **不要**勾選 「Add a README」、「Add .gitignore」(本機已有,避免衝突)
5. 點 Create

### 9.2 設定 SSH 金鑰(推薦,只要做一次)

```bash
ssh-keygen -t ed25519 -C "you@example.com"
# 一路按 Enter 用預設值

cat ~/.ssh/id_ed25519.pub
```

複製輸出內容,到 GitHub:`Settings` → `SSH and GPG keys` → `New SSH key`,貼上、儲存。

測試:

```bash
ssh -T git@github.com
# 看到 "Hi <username>! You've successfully authenticated..." 就成功
```

### 9.3 連結遠端並推送

```bash
git remote add origin git@github.com:<your-username>/flask-vibe-demo.git
git branch -M main
git push -u origin main
```

`-u` 旗標把本地 main 與遠端 main 建立追蹤關係,之後 `git push` 不必再加參數。

### 9.4 之後的工作流

```bash
# 改完一塊
git add .
git commit -m "feat: ..."
git push
```

或直接讓 Claude Code 一條龍:

```
請幫我 commit 並 push 到 origin
```

### 9.5 加上 README

請 Claude:

```
請根據目前的專案內容,幫我寫一個 README.md,
包含:專案簡介、安裝步驟、執行方式、API 列表、技術棧
```

寫完後 commit + push,你的 GitHub 頁面就有像樣的首頁了。

---

## 10. 常見問題排解

### 10.1 在 WSL 執行 `claude` 卻出現 "command not found"

原因:PATH 沒設好。

```bash
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
which claude       # 應該看到路徑
```

### 10.2 `which node` 顯示 `/mnt/c/...`

WSL 抓到 Windows 端的 Node,會出問題。在 WSL 內重新安裝 Node:

```bash
# 用 nvm 是最乾淨的方式
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts
which node     # 現在應該是 /home/<user>/.nvm/...
```

### 10.3 Flask 在 WSL 跑了,Windows 瀏覽器打不開

先試 `http://localhost:5000`。若不行,在 `app.py` 改:

```python
app.run(host="0.0.0.0", port=5000)
```

仍不行則在 `%USERPROFILE%\.wslconfig` 加:

```ini
[wsl2]
networkingMode=mirrored
```

然後 PowerShell `wsl --shutdown` 後重新啟動 WSL。

### 10.4 Antigravity 終端機開出來是 PowerShell

代表沒有用 Remote-WSL 連線。重做 4.3 節步驟,確認左下角顯示 `[WSL: Ubuntu]`。

### 10.5 `git push` 被拒(403 / Permission denied)

最可能原因:用了 HTTPS 但密碼認證。GitHub 自 2021 年起就不接受密碼,要用 SSH(本教程做法)或 Personal Access Token。建議改用 SSH(9.2 節)。

### 10.6 不小心把 `.venv/` commit 進去了

```bash
git rm -r --cached .venv
echo ".venv/" >> .gitignore
git add .gitignore
git commit -m "chore: properly ignore venv directory"
```

---

## 結語

整套工作流總結成一張流程圖:

```
[Windows]
    │
    ├── Antigravity IDE ──┐
    │                     │ Remote-WSL
    ▼                     ▼
[WSL2 Ubuntu]      ┌─────────────┐
    ├── venv ──────│  Claude     │
    ├── Flask app  │  Code       │
    └── Git ───────│  (在終端機) │
              │    └─────────────┘
              ▼
         [GitHub]
```

關鍵原則回顧:

1. **WSL 解決環境一致性** —— Linux 是 Python/Node 的母語環境。
2. **venv 解決套件隔離** —— 一個專案一個籠子。
3. **Git 解決時間旅行** —— 出錯能回退,自信才能加速。
4. **Claude Code 解決打字** —— 但前三項是地基,沒它們你會被 AI 帶下懸崖。

Vibe coding 的「vibe」不是放棄思考,而是把思考放在更高一層:**架構、驗證、判斷**。下層的 boilerplate 交給 Claude,你專心當好那個拿方向盤的人。

---

## 延伸閱讀

- Antigravity 官方教學:[codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
- Claude Code 文件:[code.claude.com/docs](https://code.claude.com/docs)
- Conventional Commits:[conventionalcommits.org](https://www.conventionalcommits.org)
- WSL 官方文件:[learn.microsoft.com/windows/wsl](https://learn.microsoft.com/windows/wsl)
