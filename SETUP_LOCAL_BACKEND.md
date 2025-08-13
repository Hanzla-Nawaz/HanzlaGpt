# 🌐 Expose Localhost Backend to Internet

## 🎯 **Goal**: Vercel frontend → Your laptop backend (python main.py)

## 🚀 **Option 1: ngrok (Recommended - Easiest)**

### **Step 1: Install ngrok**
```bash
# Download from https://ngrok.com/download
# Or use chocolatey (Windows)
choco install ngrok

# Or download manually and add to PATH
```

### **Step 2: Start Your Backend**
```bash
# Terminal 1: Start your backend
python main.py
# Should show: INFO: Started server process on 0.0.0.0:8000
```

### **Step 3: Expose Backend with ngrok**
```bash
# Terminal 2: Expose localhost:8000
ngrok http 8000
```

**Expected Output**:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

### **Step 4: Update Vercel Environment**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. **Environment Variables** → **Production**
4. Set: `BACKEND_URL` = `https://abc123.ngrok.io` (your ngrok URL)
5. Remove `VITE_API_URL` if it exists

### **Step 5: Redeploy Vercel**
1. Click "Redeploy" with "Clear build cache"
2. Test: https://hanzlagpt11.vercel.app

## 🔄 **Option 2: Cloudflare Tunnel (Alternative)**

### **Step 1: Install cloudflared**
```bash
# Windows (PowerShell as Admin)
winget install Cloudflare.cloudflared
```

### **Step 2: Start Backend + Tunnel**
```bash
# Terminal 1: Start backend
python main.py

# Terminal 2: Create tunnel
cloudflared tunnel --url http://localhost:8000
```

### **Step 3: Update Vercel**
- Set `BACKEND_URL` = your Cloudflare tunnel URL
- Redeploy with cache clear

## ⚠️ **Important Notes**

### **Keep Backend Running**
- Your laptop must stay on and connected to internet
- Backend must run continuously: `python main.py`
- ngrok/cloudflared must stay active

### **Security**
- ngrok URLs are public (anyone can access)
- Consider ngrok authentication for production
- Use only for development/testing

### **Performance**
- Internet speed affects response time
- Your laptop internet upload speed matters
- Consider moving to cloud for production

## 🧪 **Test Setup**

1. **Backend**: `python main.py` (Terminal 1)
2. **Tunnel**: `ngrok http 8000` (Terminal 2)
3. **Vercel**: Update `BACKEND_URL` and redeploy
4. **Test**: Send message on Vercel frontend

## 📱 **Current Status**
- ✅ Frontend: Vercel deployed
- 🔄 Backend: Need to expose localhost
- 🔄 Connection: Vercel → Your laptop backend
- 🎯 **Action**: Install ngrok and expose backend
