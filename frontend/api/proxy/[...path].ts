import type { VercelRequest, VercelResponse } from '@vercel/node'

// Backend URL comes from Vercel env (Project Settings -> Environment Variables)
// Example: https://untitled-journals-earl-outlined.trycloudflare.com
const BACKEND_URL = process.env.BACKEND_URL

export default async function handler(req: VercelRequest, res: VercelResponse) {
  try {
    if (!BACKEND_URL) {
      res.status(500).json({ error: 'Missing BACKEND_URL env var' })
      return
    }

    const { path = [] } = req.query as { path?: string[] }
    const targetPath = Array.isArray(path) ? path.join('/') : String(path || '')

    const url = `${BACKEND_URL}/api/${targetPath}`

    const init: RequestInit = {
      method: req.method,
      headers: {
        ...(req.headers as Record<string, string>),
        host: undefined as unknown as string, // strip host header
      } as HeadersInit,
      body: ['GET', 'HEAD'].includes(req.method || 'GET') ? undefined : (req as any).body,
    }

    const response = await fetch(url, init)
    const contentType = response.headers.get('content-type') || ''
    res.status(response.status)
    response.headers.forEach((value, key) => {
      if (key.toLowerCase() === 'content-encoding') return
      res.setHeader(key, value)
    })

    if (contentType.includes('application/json')) {
      const data = await response.json()
      res.json(data)
    } else {
      const buffer = Buffer.from(await response.arrayBuffer())
      res.send(buffer)
    }
  } catch (err: any) {
    res.status(502).json({ error: 'Proxy error', detail: err?.message || String(err) })
  }
}


