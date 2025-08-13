# 🚀 HanzlaGPT Development Guide

## 🖥️ **Local Development Setup**

### **Prerequisites**
1. Backend running on localhost:8000
2. Frontend running locally
3. Both in separate terminal windows

### **Step 1: Start Backend (Terminal 1)**
```bash
# In your main project directory
cd app
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output**: `INFO: Started server process [PID] on 0.0.0.0:8000`

### **Step 2: Start Frontend (Terminal 2)**
```bash
# In frontend directory
cd frontend
npm run dev:local
```

**Expected Output**: `Local: http://localhost:5173/`

### **Step 3: Test Connection**
1. Open http://localhost:5173 in browser
2. Send a message
3. Check Network tab: should call `http://localhost:8000/api/chat/query`

## 🔧 **How It Works**

- **Development Mode**: Frontend automatically connects to `http://localhost:8000`
- **Production Mode**: Frontend uses Vercel proxy to EC2 backend
- **No Environment Variables Needed**: Automatically detects localhost

## 🚨 **Troubleshooting**

### **Backend Not Found (404)**
- Check backend is running on port 8000
- Verify `python main.py` or `uvicorn` command
- Check terminal for errors

### **CORS Error**
- Backend should have CORS configured for localhost:5173
- Check `main.py` CORS settings

### **Port Already in Use**
- Kill existing process: `sudo lsof -i :8000` then `sudo kill -9 <PID>`
- Or use different port: `uvicorn main:app --port 8001`

## 📱 **Current Status**
- ✅ Frontend: Automatically detects localhost
- ✅ Backend: Should run on localhost:8000
- ✅ Connection: Direct localhost communication
- 🔄 **Action**: Start both services and test
