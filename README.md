# Regression Visualization Lab

以 **50 Startups** 與 **Boston Housing** 為素材的互動式迴歸分析網站。使用者可探索資料、選擇模型與訓練比例，並檢視即時預測成效與特徵解釋

> 本專案用於教學與課程展示。Boston Housing 帶有已知的歷史偏誤，僅適合示範迴歸流程，不應用於真實房價、信貸或人事決策

## 功能

- 在 **50 Startups** 與 **Boston Housing** 之間切換資料集
- 顯示資料筆數、特徵數、目標分布、主要特徵散點圖與相關係數熱圖
- 選擇線性迴歸、決策樹迴歸或隨機森林迴歸
- 調整訓練集比例（60%–90%），即時執行模型實驗
- 顯示測試集 R²、RMSE、MAE、實際值 vs. 預測值與特徵重要性
- 以環境變數連接不同的 FastAPI 正式環境網址

## 網站流程

```text
選擇資料集 → 檢視分布與相關性 → 選模型／訓練比例
                                      ↓
                         FastAPI 前處理、訓練、評估
                                      ↓
                  顯示 R² / RMSE / MAE、預測圖與特徵解釋
```

前端每次按下「執行實驗」時，會把資料集、模型和訓練比例交給 FastAPI。後端固定使用 `random_state=42` 切分資料，使實驗結果可重現。

## 技術架構

| 層級 | 技術 | 職責 |
| --- | --- | --- |
| 使用者介面 | React + Vite | 控制項、頁面狀態與 API 呼叫 |
| 圖表 | Plotly.js | 分布、散點、熱圖、預測與特徵解釋 |
| 模型 API | FastAPI | 資料摘要、探索資料及模型實驗端點 |
| 分析與機器學習 | pandas + scikit-learn | 前處理、訓練與評估 |
| 部署目標 | Vercel | React 網頁服務與 Python FastAPI 服務，由同一個專案轉送 `/api/*` |

```text
Browser (React + Plotly)
         │  HTTPS /api
         ▼
FastAPI + scikit-learn
         │
         ├── 50_Startups.csv
         └── BostonHousing.csv
```

## 專案結構

```text
regression-visualization-lab/
├── frontend/                    # React + Vite 使用者介面
│   ├── src/
│   │   ├── App.jsx              # 頁面與互動流程
│   │   ├── api.js               # API 呼叫與錯誤處理
│   │   └── styles.css           # 響應式樣式
│   ├── .env.example             # API 網址範例
│   └── package.json
├── backend/                     # FastAPI 模型服務
│   ├── app/
│   │   ├── main.py              # API、CORS 與輸入驗證
│   │   ├── data.py              # 資料集載入與摘要
│   │   └── ml.py                # 前處理、模型與評估
│   ├── data/                    # 下載後的 CSV
│   ├── scripts/download_data.py # 教學資料下載腳本
│   ├── tests/                   # API 與模型測試
│   ├── Dockerfile               # 容器化部署選項
│   └── requirements.txt
└── README.md
```

## 資料集

| 資料集 | 筆數 | 預測目標 | 特徵 |
| --- | ---: | --- | --- |
| 50 Startups | 50 | `Profit` | R&D Spend、Administration、Marketing Spend、State |
| Boston Housing | 506 | `MEDV` | CRIM、ZN、INDUS、CHAS、NOX、RM、AGE、DIS、RAD、TAX、PTRATIO、B、LSTAT |

`backend/scripts/download_data.py` 會從公開教學鏡像下載 CSV。公開發佈前請自行確認資料來源與授權要求

## 模型與前處理

| 模型 | 設定與輸出 |
| --- | --- |
| 線性迴歸 | 數值特徵標準化；顯示標準化係數絕對值。 |
| 決策樹迴歸 | `random_state=42`、`max_depth=5`；顯示特徵重要性。 |
| 隨機森林迴歸 | 180 棵樹、`min_samples_leaf=2`、`random_state=42`；顯示特徵重要性。 |

- 數值欄位使用中位數補值
- 類別欄位使用眾數補值及 one-hot 編碼
- 所有 R²、RMSE、MAE 均以測試集計算

## API

| 方法 | 路徑 | 說明 |
| --- | --- | --- |
| `GET` | `/api/health` | 健康檢查，成功時回傳 `{"status":"ok"}` |
| `GET` | `/api/datasets` | 回傳可用資料集與欄位摘要 |
| `GET` | `/api/datasets/{dataset_id}/exploration` | 回傳分布、主要關係與相關係數繪圖資料 |
| `POST` | `/api/experiments` | 執行模型實驗，回傳指標、預測資料及特徵解釋 |

`POST /api/experiments` 範例：

```json
{
  "dataset_id": "boston",
  "model": "random_forest",
  "train_size": 0.8
}
```

資料集 ID：`startups`、`boston`。模型 ID：`linear_regression`、`decision_tree`、`random_forest`。

## 本機啟動

### 1. 啟動後端

在第一個 PowerShell 視窗執行：

```powershell
cd regression-visualization-lab\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\download_data.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

成功後可開啟 <http://127.0.0.1:8000/docs> 查看 FastAPI 自動產生的 API 文件。

### 2. 啟動前端

在第二個 PowerShell 視窗執行：

```powershell
cd regression-visualization-lab\frontend
npm install
Copy-Item .env.example .env
npm run dev
```

開啟 <http://127.0.0.1:5173>。開發模式下 Vite 會將 `/api` 代理到 `http://localhost:8000`，因此 `.env` 可維持空白

## 環境變數

| 位置 | 變數 | 用途 |
| --- | --- | --- |
| `frontend/.env` | `VITE_API_BASE_URL` | 選用的外部 API HTTPS 網址；使用本專案的 Vercel 設定時留空，讓瀏覽器呼叫同網域的 `/api` |
| `backend/.env` | `CORS_ORIGINS` | 僅在前端與 API 分開網域時設定；可用逗號分隔多個網域。 |

```dotenv
# frontend/.env.production
# 同一個 Vercel 專案不需設定 VITE_API_BASE_URL。
# 僅在 API 放在另一個網域時才填入完整 HTTPS 網址。
```

```dotenv
# backend/.env
CORS_ORIGINS=https://your-project.vercel.app,http://localhost:5173
```

## 測試與建置

後端測試：

```powershell
cd backend
python -m pytest
```

測試涵蓋資料集載入、三種模型、資料探索端點、模型實驗端點與 health check

前端 production build：

```powershell
cd frontend
npm run build
```

## Vercel 部署

專案已可作為一個 Vercel 專案部署。根目錄的 `vercel.toml` 定義兩個服務：

- `frontend/`：Vite 建置的 React 網頁。
- `backend/`：以 `app.main:app` 啟動的 FastAPI 服務。

路由會優先把 `/api/*` 交給 FastAPI，其餘網址交給 React。兩者使用相同網域，因此正式環境不必設定 `VITE_API_BASE_URL`，也不需要為同網域請求設定 CORS。`backend/data/` 沒有被忽略，部署時會一併放入 API 執行環境。

### 用 Vercel Dashboard 部署

1. 將目前根目錄的內容放到新的 GitHub、GitLab 或 Bitbucket 儲存庫。若你要從零開始，初始化新的版本庫即可；不需保留原本的歷史。
2. 在 [Vercel Dashboard](https://vercel.com/new) 選擇 **Add New → Project**，匯入該儲存庫。
3. 將 **Root Directory** 保持在儲存庫根目錄（也就是含有 `vercel.toml`、`frontend/` 與 `backend/` 的資料夾），不要選成 `frontend/` 或 `backend/`。
4. 不必新增 `VITE_API_BASE_URL`。Vercel 會讀取 `vercel.toml`，建立網頁與 API 服務。
5. 部署完成後先開啟 `https://你的網址/api/health`。它應回傳 JSON，接著再測試兩個資料集與三種模型。
6. 確認預覽部署正常後，在 Vercel 將該部署提升為 Production。

### 本機模擬部署

平常仍可使用本機啟動方式。若已安裝並登入 Vercel CLI，可在根目錄執行 `vercel dev`，以 `vercel.toml` 同時模擬前端與 API 路由；這不是部署的必要條件。

Vercel 的 Python Runtime 已支援 FastAPI；目前資料集很小，但第一次部署仍應在 Vercel 的 Build Logs 確認 `scikit-learn` 與資料檔案都成功打包。詳見 [Vercel FastAPI 文件](https://vercel.com/docs/frameworks/backend/fastapi)與 [Vercel Python Runtime 公告](https://vercel.com/changelog/python-on-vercel-is-now-generally-available)。

## 常見問題

### `Unexpected token '<' … is not valid JSON`

前端預期收到 JSON，實際卻收到 HTML（通常是靜態網站的 `index.html`）。這通常表示 FastAPI 尚未啟動、`VITE_API_BASE_URL` 未設定，或部署平台沒有將 `/api/*` 路由到 FastAPI。請先檢查 `/api/health` 是否回傳 JSON

### 下拉選單有資料集，但圖表沒有載入

資料集名稱會先顯示，探索圖表仍需由 API 提供。請確認 FastAPI 正在執行，並檢查瀏覽器開發者工具中是否有 CORS 或網路錯誤

### 第一次執行模型較慢

後端需要讀取 CSV、前處理並訓練模型。資料規模很小，正常情況下會在短時間內完成；在 serverless 平台上，第一次請求也可能包含 cold start 時間

## 授權與資料使用

程式碼供課程與學習使用。資料來源各自適用其授權與使用規範；公開發佈前請重新確認資料授權、來源標示與課程要求
