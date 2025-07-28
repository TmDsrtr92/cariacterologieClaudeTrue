# Cariacterologie Claude - React Frontend

A modern, professional React application for Q&A interactions with full transparency into the AI processing pipeline.

## 🚀 Features

### ✨ **Core Functionality**
- **Interactive Q&A Chat**: Real-time conversation interface
- **Processing Transparency**: Visual tracking of AI processing stages
- **Dark/Light Mode**: Toggle between themes with persistent storage
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **Real-time Updates**: WebSocket integration for live processing updates

### 🎨 **Design System**
- **Professional Dark Theme** with blue (#3B82F6) and purple (#6B46C1) accents
- **Thin Typography** using Inter font for elegant readability
- **Consistent Components** with hover states and animations
- **Accessibility**: ARIA labels, keyboard navigation, focus management

### 🧩 **Component Library**
- **Buttons**: Primary (dark purple), Secondary (black), Tertiary, Ghost
- **Form Controls**: Input, Textarea, Select with validation states
- **Chat Components**: Message bubbles, typing indicators, chat input
- **Transparency**: Processing stages, progress tracking, collapsible panels
- **Layout**: Cards, loading spinners, navigation header

## 📁 Project Structure

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Select.tsx
│   │   ├── Card.tsx
│   │   └── ...
│   ├── chat/            # Chat-specific components
│   │   ├── ChatContainer.tsx
│   │   ├── MessageBubble.tsx
│   │   └── ChatInput.tsx
│   ├── transparency/    # Processing transparency components
│   │   ├── TransparencyPanel.tsx
│   │   └── ProcessingStage.tsx
│   └── layout/          # Layout components
│       └── Header.tsx
├── pages/
│   ├── Home.tsx         # Main Q&A interface
│   └── StyleGuide.tsx   # Component documentation
├── stores/
│   ├── themeStore.ts    # Dark/light mode management
│   └── chatStore.ts     # Chat and transparency state
├── hooks/
│   ├── useWebSocket.ts  # WebSocket connection management
│   └── useTransparencyWebSocket.ts  # Real-time transparency updates
├── services/
│   └── api.ts           # Backend API integration
├── styles/
│   └── theme.ts         # Design system configuration
└── types/
    └── index.ts         # TypeScript type definitions
```

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for utility-first styling
- **Zustand** for state management
- **React Router** for navigation
- **WebSocket** for real-time updates

## 🚀 Quick Start

### Prerequisites
- Node.js v18+ (currently compatible with v21.4.0)
- npm or yarn

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Open in browser**
   - Main App: http://localhost:5173/
   - Style Guide: http://localhost:5173/styleguide

### Build for Production

```bash
npm run build
```

## 🔗 Backend Integration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### API Endpoints

The frontend expects these backend endpoints:

```
POST /api/qa                     # Send question, get answer
GET  /api/conversations          # List conversations
GET  /api/conversations/:id      # Get specific conversation
DELETE /api/conversations/:id    # Delete conversation
GET  /api/processing/:messageId  # Get processing status
GET  /health                     # Health check
WS   /ws                        # WebSocket for real-time updates
```

### WebSocket Messages

Real-time transparency updates via WebSocket:

```typescript
// Stage update
{
  type: 'stage_update',
  stageId: 'document_retrieval',
  status: 'in_progress',
  message: 'Searching documents...'
}

// Progress update  
{
  type: 'progress_update',
  progress: 0.4
}

// Processing complete
{
  type: 'processing_complete'
}
```

## 🎨 Style Guide

Visit `/styleguide` to see:
- **Color Palette**: All theme colors with hex codes
- **Typography**: Font weights and sizes
- **Component Examples**: Live interactive components
- **Usage Guidelines**: Do's and don'ts for consistent design

## 🤝 Integration with Python Backend

This React frontend is designed to work with your existing Python backend:

### Current Python Stack
- **LangChain** for LLM orchestration
- **LangGraph** for workflow management  
- **ChromaDB** for vector storage
- **LightSQL** for data persistence
- **Streamlit** (being replaced by this React app)

### Migration Strategy
1. **Keep Python Backend**: All your LangChain/LangGraph logic remains unchanged
2. **Add REST API**: Expose your functions via FastAPI endpoints
3. **Add WebSocket**: Stream processing updates to React frontend
4. **Gradual Migration**: Replace Streamlit components one by one

### Example Backend Integration

```python
# FastAPI backend example
from fastapi import FastAPI, WebSocket
from your_existing_code import setup_qa_chain_with_memory

app = FastAPI()

@app.post("/api/qa")
async def ask_question(request: QARequest):
    # Use your existing LangGraph chain
    result = await setup_qa_chain_with_memory(request.question)
    return {"answer": result, "conversationId": request.conversationId}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Stream transparency updates during processing
    await websocket.accept()
    # Your existing transparency logic here
```

---

**Ready to integrate with your Python backend and provide a modern, professional interface for your Q&A system!** 🚀