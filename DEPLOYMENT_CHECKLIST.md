# 🚀 HanzlaGPT Deployment Checklist

## ✅ Pre-Deployment Checks

### 1. Backend (EC2 + Cloudflare Tunnel)
- [ ] EC2 instance running on port 8000
- [ ] Cloudflare Tunnel active and accessible
- [ ] Test: `curl https://wp-acquired-updates-providing.trycloudflare.com/api/chat/health`
- [ ] Should return: `{"status": "ok"}`

### 2. Frontend (Vercel)
- [ ] Root Directory set to `frontend` in Vercel
- [ ] Environment Variables (Production):
  - [ ] `BACKEND_URL` = `https://wp-acquired-updates-providing.trycloudflare.com`
  - [ ] `VITE_API_URL` = REMOVED (must not exist)
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`

## 🔧 Deployment Steps

### Step 1: Commit Changes
```bash
git add .
git commit -m "Fix Vercel deployment: v1.0.1 - Clean proxy configuration"
git push origin main
```

### Step 2: Vercel Deploy
1. Go to Vercel Dashboard
2. Select your project
3. Click "Redeploy" 
4. ✅ CHECK "Clear build cache"
5. Deploy

### Step 3: Verify Functions
1. In Vercel Dashboard → Functions tab
2. Should see: `/api/proxy/[...path]`
3. Status: Active

## 🧪 Testing

### Test 1: Health Endpoint
```bash
curl https://hanzlagpt11.vercel.app/api/chat/health
```
Expected: `{"status": "ok"}`

### Test 2: Frontend App
1. Open https://hanzlagpt11.vercel.app
2. Open Browser DevTools → Network tab
3. Send a message
4. Check: Request URL should be `/api/chat/query` (NOT `/api/proxy/chat/query`)

## 🚨 Troubleshooting

### If 404 on /api/chat/health:
- Check Vercel Root Directory = `frontend`
- Verify vercel.json exists in frontend folder
- Clear build cache and redeploy

### If frontend still calls localhost:
- Remove VITE_API_URL from Vercel env vars
- Clear browser cache
- Hard refresh (Ctrl+F5)

### If proxy function not found:
- Check Functions tab in Vercel
- Verify @vercel/node dependency installed
- Check build logs for errors

## 📱 Current Status
- Backend: ✅ EC2 + Cloudflare Tunnel
- Frontend: 🔄 Vercel (needs redeploy)
- Proxy: ✅ Configured
- Issue: Frontend calling wrong URL path
