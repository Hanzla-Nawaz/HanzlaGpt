# HanzlaGPT Frontend Deployment Guide

## Prerequisites
1. Vercel account connected to your GitHub repository
2. Backend running on EC2 with Cloudflare Tunnel active
3. Cloudflare Tunnel URL (e.g., https://wp-acquired-updates-providing.trycloudflare.com)

## Step 1: Install Dependencies
```bash
cd frontend
npm install
```

## Step 2: Vercel Project Settings
1. Go to your Vercel project dashboard
2. **Root Directory**: Set to `frontend`
3. **Environment Variables** (Production):
   - `BACKEND_URL` = `https://wp-acquired-updates-providing.trycloudflare.com`
   - Remove `VITE_API_URL` if it exists
4. **Build Command**: `npm run build`
5. **Output Directory**: `dist`

## Step 3: Deploy
1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Fix Vercel deployment configuration"
   git push origin main
   ```
2. In Vercel, click "Redeploy" with "Clear build cache" option

## Step 4: Verify Deployment
1. Check Functions tab in Vercel - should show `/api/proxy/[...path]`
2. Test health endpoint: `https://your-domain.vercel.app/api/chat/health`
3. Check Network tab in browser - requests should go to `/api/chat/...`

## Troubleshooting
- If 404: Check Root Directory is set to `frontend`
- If proxy error: Verify `BACKEND_URL` is correct
- If build fails: Clear build cache and redeploy
