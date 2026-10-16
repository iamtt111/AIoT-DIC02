const baseUrl = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

async function request(path, options) {
  const response = await fetch(`${baseUrl}${path}`, options)
  const contentType = response.headers.get('content-type') || ''
  if (!contentType.includes('application/json')) {
    throw new Error('模型 API 尚未連線。請部署 FastAPI 後端，並設定 VITE_API_BASE_URL 為後端的 HTTPS 網址。')
  }
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail || '目前無法連線至模型服務，請稍後再試。')
  }
  return response.json()
}

export const getDatasets = () => request('/api/datasets')
export const getExploration = (id) => request(`/api/datasets/${id}/exploration`)
export const runExperiment = (payload) => request('/api/experiments', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload),
})
