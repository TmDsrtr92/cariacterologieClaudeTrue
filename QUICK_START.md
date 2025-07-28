# 🚀 Quick Start Guide - Port 8001 Configuration

## ✅ **Ready to Use!**

Your React app is now fully connected to your Python backend on **port 8001** to avoid conflicts.

### **🏃‍♂️ Start Your Application**

#### **Option 1: Automatic Start (Recommended)**
```bash
# Double-click this file:
start_app.bat
```

#### **Option 2: Manual Start**
```bash
# Terminal 1: Python Backend
python api_server.py

# Terminal 2: React Frontend
cd frontend
npm run dev
```

### **🌐 Access Your App**

- **Main App**: http://localhost:5173/
- **Style Guide**: http://localhost:5173/styleguide
- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

### **✅ Configuration Complete**

- ✅ **Backend**: Running on port **8001** (auto-configured)
- ✅ **Frontend**: Configured to connect to port **8001**
- ✅ **WebSocket**: Real-time transparency updates enabled
- ✅ **Database**: SQLite conversations storage ready

### **🧪 Test the Integration**

1. Open http://localhost:5173/
2. Ask a question like "What is machine learning?"
3. Watch the real-time processing steps appear
4. See the response from your actual LangChain backend
5. Check that conversations are saved (refresh page to verify)

### **🔧 Current Configuration**

```
Backend API: http://localhost:8001
Frontend: http://localhost:5173
WebSocket: ws://localhost:8001/ws
Database: conversations.db (auto-created)
```

### **📱 Features Working**

- ✅ **Real Q&A**: Your LangChain/LangGraph backend responding
- ✅ **Live Transparency**: Processing steps update in real-time
- ✅ **Chat History**: Conversations saved to database
- ✅ **Professional UI**: Modern React interface
- ✅ **Responsive Design**: Works on mobile, tablet, desktop
- ✅ **Dark/Light Mode**: Theme toggle in header

### **🆘 If You Have Issues**

1. **Backend won't start**: Check console for port conflicts
2. **Frontend can't connect**: Verify backend is running on 8001
3. **WebSocket not working**: Check for "Connecting..." message in UI
4. **Database errors**: Delete `conversations.db` file to reset

**Your app is ready for production use!** 🎉