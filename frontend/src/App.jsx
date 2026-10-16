import { useEffect, useMemo, useState } from 'react'
import Plot from 'react-plotly.js'
import { getDatasets, getExploration, runExperiment } from './api.js'

const MODEL_OPTIONS = [
  ['linear_regression', '線性迴歸'],
  ['decision_tree', '決策樹迴歸'],
  ['random_forest', '隨機森林迴歸'],
]

const DATASET_OPTIONS = [
  { id: 'startups', name: '50 Startups', source: 'Kaggle 50 Startups dataset' },
  { id: 'boston', name: 'Boston Housing', source: 'UCI Machine Learning Repository' },
]

const plotLayout = (title, extra = {}) => ({
  title: { text: title, font: { size: 15, color: '#e6edf7' }, x: 0.03 },
  paper_bgcolor: 'transparent', plot_bgcolor: '#0d1a2c',
  font: { color: '#b9c7d9', family: 'Inter, system-ui, sans-serif' },
  margin: { l: 48, r: 20, t: 48, b: 42 },
  ...extra,
})

function Metric({ label, value }) {
  return <article className="metric"><span>{label}</span><strong>{Number(value).toLocaleString('en-US', { maximumFractionDigits: 3 })}</strong></article>
}

export default function App() {
  const [datasets, setDatasets] = useState(DATASET_OPTIONS)
  const [datasetId, setDatasetId] = useState('startups')
  const [exploration, setExploration] = useState(null)
  const [model, setModel] = useState('random_forest')
  const [trainSize, setTrainSize] = useState(80)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    getDatasets().then((items) => {
      setDatasets(items)
      if (items.length && !items.some((item) => item.id === datasetId)) setDatasetId(items[0].id)
    }).catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    setLoading(true); setResult(null); setError('')
    getExploration(datasetId).then(setExploration).catch((err) => setError(err.message)).finally(() => setLoading(false))
  }, [datasetId])

  const selected = useMemo(() => datasets.find((item) => item.id === datasetId), [datasets, datasetId])
  async function handleExperiment(event) {
    event.preventDefault(); setRunning(true); setError('')
    try { setResult(await runExperiment({ dataset_id: datasetId, model, train_size: trainSize / 100 })) }
    catch (err) { setError(err.message) }
    finally { setRunning(false) }
  }

  return <main>
    <header className="hero">
      <p className="eyebrow">DATA SCIENCE STUDIO</p>
      <h1>Regression<br /><em>Visual Lab</em></h1>
      <p className="hero-copy">從資料特徵到預測品質，以可重現的實驗比較三種迴歸模型。</p>
      <div className="hero-tags"><span>50 Startups</span><span>Boston Housing</span><span>scikit-learn</span></div>
    </header>

    <section className="control-panel" aria-label="實驗設定">
      <div><label htmlFor="dataset">資料集</label><select id="dataset" value={datasetId} onChange={(e) => setDatasetId(e.target.value)}>{datasets.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select></div>
      <div><label htmlFor="model">模型</label><select id="model" value={model} onChange={(e) => setModel(e.target.value)}>{MODEL_OPTIONS.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></div>
      <form onSubmit={handleExperiment}>
        <label htmlFor="train">訓練集 {trainSize}%</label><input id="train" type="range" min="60" max="90" step="5" value={trainSize} onChange={(e) => setTrainSize(Number(e.target.value))} />
        <button disabled={running || loading}>{running ? '模型運算中…' : '執行實驗 →'}</button>
      </form>
    </section>

    {error && <p className="notice error">{error}</p>}
    {loading && <p className="notice">正在讀取資料集…</p>}
    {exploration && <>
      <section className="dataset-intro"><div><p className="eyebrow">SELECTED DATASET</p><h2>{exploration.name}</h2><p>{exploration.description}</p></div><div className="stats"><Metric label="觀測值" value={exploration.record_count} /><Metric label="特徵數" value={exploration.feature_count} /><Metric label="預測目標" value={exploration.target} /></div></section>
      <section className="chart-grid">
        <Plot className="chart" useResizeHandler data={[{ type: 'histogram', x: exploration.target_distribution.values, marker: { color: '#7c6cff' }, opacity: .88 }]} layout={plotLayout(`${exploration.target} 分布`, { xaxis: { title: exploration.target }, yaxis: { title: '筆數' } })} config={{ responsive: true, displayModeBar: false }} />
        <Plot className="chart" useResizeHandler data={[{ type: 'scatter', mode: 'markers', x: exploration.relationship.x, y: exploration.relationship.y, marker: { color: '#2dd4bf', size: 7, opacity: .72 } }]} layout={plotLayout(`${exploration.relationship.feature} 與 ${exploration.target}`, { xaxis: { title: exploration.relationship.feature }, yaxis: { title: exploration.target } })} config={{ responsive: true, displayModeBar: false }} />
        <Plot className="chart wide" useResizeHandler data={[{ type: 'heatmap', z: exploration.correlation.matrix, x: exploration.correlation.columns, y: exploration.correlation.columns, colorscale: [[0, '#16243c'], [.5, '#6e6af5'], [1, '#f8c55b']], zmin: -1, zmax: 1, colorbar: { thickness: 12 } }]} layout={plotLayout('數值欄位相關係數', { margin: { l: 90, r: 48, t: 48, b: 110 } })} config={{ responsive: true, displayModeBar: false }} />
      </section>
    </>}

    {result && <section className="results"><div className="section-heading"><p className="eyebrow">EXPERIMENT RESULT</p><h2>{result.model_label} <span>· 測試集</span></h2></div><div className="metrics"><Metric label="R²" value={result.metrics.r2} /><Metric label="RMSE" value={result.metrics.rmse} /><Metric label="MAE" value={result.metrics.mae} /></div><div className="chart-grid"><Plot className="chart" useResizeHandler data={[{ type: 'scatter', mode: 'markers', x: result.predictions.actual, y: result.predictions.predicted, marker: { color: '#ff8a65', size: 7, opacity: .75 } }, { type: 'scatter', mode: 'lines', x: result.predictions.line, y: result.predictions.line, line: { color: '#f4f7fb', dash: 'dot' }, hoverinfo: 'skip' }]} layout={plotLayout('實際值 vs. 預測值', { xaxis: { title: '實際值' }, yaxis: { title: '預測值' } })} config={{ responsive: true, displayModeBar: false }} /><Plot className="chart" useResizeHandler data={[{ type: 'bar', x: result.feature_importance.names, y: result.feature_importance.values, marker: { color: '#ffbf69' } }]} layout={plotLayout(result.feature_importance.label, { xaxis: { tickangle: -35 }, yaxis: { title: '影響程度' } })} config={{ responsive: true, displayModeBar: false }} /></div></section>}

    <footer><p>資料分析與模型結果僅供教學展示。Boston Housing 含有歷史偏誤，不應作為真實房價決策依據。</p><p>{selected?.source ? `來源：${selected.source}` : '選擇資料集以檢視來源。'}</p></footer>
  </main>
}
