import type { VercelRequest, VercelResponse } from '@vercel/node'

// Backend URL comes from Vercel env (Project Settings -> Environment Variables)
// Example: https://wp-acquired-updates-providing.trycloudflare.com
const BACKEND_URL = process.env.BACKEND_URL

export default async function handler(req: VercelRequest, res: VercelResponse) {
  try {
    if (!BACKEND_URL) {
      console.error('Missing BACKEND_URL environment variable')
      res.status(500).json({ error: 'Missing BACKEND_URL env var' })
      return
    }

    // Extract path from query parameters
    const { path = [] } = req.query as { path?: string[] }
    const targetPath = Array.isArray(path) ? path.join('/') : String(path || '')
    
    // Construct the full URL to the backend
    const url = `${BACKEND_URL.replace(/\/$/, '')}/api/${targetPath}`
    
    console.log(`Proxying request: ${req.method} ${req.url} -> ${url}`)

    // Build headers for upstream, stripping hop-by-hop and problematic headers
    const upstreamHeaders: Record<string, string> = {}
    for (const [k, v] of Object.entries(req.headers)) {
      const key = k.toLowerCase()
      if (['host', 'content-length', 'connection', 'accept-encoding'].includes(key)) continue
      if (typeof v === 'string') upstreamHeaders[key] = v
      else if (Array.isArray(v)) upstreamHeaders[key] = v.join(',')
    }

    // Prepare body for non-GET/HEAD
    let body: any = undefined
    const method = (req.method || 'GET').toUpperCase()
    if (!['GET', 'HEAD'].includes(method)) {
      const ct = (req.headers['content-type'] || '').toString()
      const raw = (req as any).body
      if (!raw) body = undefined
      else if (typeof raw === 'string' || Buffer.isBuffer(raw)) body = raw
      else if (ct.includes('application/json')) body = JSON.stringify(raw)
      else body = String(raw)
    }

    console.log(`Making request to backend: ${method} ${url}`)
    const response = await fetch(url, { method, headers: upstreamHeaders, body } as any)

    console.log(`Backend response: ${response.status}`)

    // Mirror response
    res.status(response.status)
    response.headers.forEach((value, key) => {
      const lk = key.toLowerCase()
      if (['content-encoding', 'transfer-encoding'].includes(lk)) return
      res.setHeader(key, value)
    })

    const contentType = response.headers.get('content-type') || ''
    if (contentType.includes('application/json')) {
      const data = await response.json()
      res.json(data)
    } else {
      const buffer = Buffer.from(await response.arrayBuffer())
      res.send(buffer)
    }
  } catch (err: any) {
    console.error('Proxy error:', err)
    res.status(502).json({ error: 'Proxy error', detail: err?.message || String(err) })
  }
}


