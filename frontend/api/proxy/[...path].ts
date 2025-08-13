import type { VercelRequest, VercelResponse } from '@vercel/node'

// Backend URL comes from Vercel env (Project Settings -> Environment Variables)
const BACKEND_URL = process.env.BACKEND_URL

export default async function handler(req: VercelRequest, res: VercelResponse) {
  try {
    console.log('=== PROXY REQUEST START ===')
    console.log('Method:', req.method)
    console.log('URL:', req.url)
    console.log('Headers:', req.headers)
    console.log('Body:', (req as any).body)
    
    if (!BACKEND_URL) {
      console.error('Missing BACKEND_URL environment variable')
      res.status(500).json({ error: 'Missing BACKEND_URL env var' })
      return
    }

    console.log('BACKEND_URL:', BACKEND_URL)

    // Extract path from query parameters
    const { path = [] } = req.query as { path?: string[] }
    const targetPath = Array.isArray(path) ? path.join('/') : String(path || '')
    
    // Construct the full URL to the backend
    const url = `${BACKEND_URL.replace(/\/$/, '')}/api/${targetPath}`
    
    console.log('Target Path:', targetPath)
    console.log('Full Backend URL:', url)

    // Build headers for upstream, stripping hop-by-hop and problematic headers
    const upstreamHeaders: Record<string, string> = {}
    for (const [k, v] of Object.entries(req.headers)) {
      const key = k.toLowerCase()
      if (['host', 'content-length', 'connection', 'accept-encoding'].includes(key)) continue
      if (typeof v === 'string') upstreamHeaders[key] = v
      else if (Array.isArray(v)) upstreamHeaders[key] = v.join(',')
    }

    console.log('Upstream Headers:', upstreamHeaders)

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

    console.log('Request Body:', body)
    console.log('Making request to backend...')

    const response = await fetch(url, { method, headers: upstreamHeaders, body } as any)

    console.log('Backend Response Status:', response.status)
    console.log('Backend Response Headers:', Object.fromEntries(response.headers.entries()))

    // Mirror response
    res.status(response.status)
    response.headers.forEach((value, key) => {
      const lk = key.toLowerCase()
      if (['content-encoding', 'transfer-encoding'].includes(lk)) return
      res.setHeader(key, value)
    })

    const contentType = response.headers.get('content-type') || ''
    console.log('Content-Type:', contentType)
    
    if (contentType.includes('application/json')) {
      const data = await response.json()
      console.log('Response Data:', data)
      res.json(data)
    } else {
      const buffer = Buffer.from(await response.arrayBuffer())
      console.log('Response Buffer Length:', buffer.length)
      res.send(buffer)
    }
    
    console.log('=== PROXY REQUEST END ===')
    
  } catch (err: any) {
    console.error('=== PROXY ERROR ===')
    console.error('Error:', err)
    console.error('Error Message:', err?.message)
    console.error('Error Stack:', err?.stack)
    res.status(502).json({ error: 'Proxy error', detail: err?.message || String(err) })
  }
}


