"""
FastAPI backend server to connect React frontend with existing LangGraph QA system
"""
import asyncio
import json
import uuid
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

# Fix encoding issues with emojis on Windows
if os.name == 'nt':  # Windows
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import your existing modules
from core.langgraph_qa_chain import setup_qa_chain_with_memory, clean_response
from core.langgraph_memory import LangGraphMemoryManager
from utils.simple_transparency import (
    start_transparency,
    stop_transparency,
    update_processing_status,
    complete_processing_status
)
from utils.transparency_system import ProcessingStage

# Initialize FastAPI app
app = FastAPI(title="Cariacterologie Claude API", version="1.0.0")

# Initialize memory manager
memory_manager = LangGraphMemoryManager()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class QARequest(BaseModel):
    question: str
    conversationId: Optional[str] = None

class QAResponse(BaseModel):
    answer: str
    conversationId: str
    messageId: str

class Message(BaseModel):
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime

class Conversation(BaseModel):
    id: str
    messages: List[Message]
    title: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

class TransparencyUpdate(BaseModel):
    type: str  # 'stage_update', 'progress_update', 'stage_complete', 'processing_complete'
    stageId: Optional[str] = None
    status: Optional[str] = None  # 'pending', 'in_progress', 'completed', 'error'
    progress: Optional[float] = None
    message: Optional[str] = None
    conversationId: Optional[str] = None
    messageId: Optional[str] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.conversation_subscribers: Dict[str, List[WebSocket]] = {}
        self.message_subscribers: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        # Clean up subscriptions
        for conv_id, sockets in self.conversation_subscribers.items():
            if websocket in sockets:
                sockets.remove(websocket)
        for msg_id, sockets in self.message_subscribers.items():
            if websocket in sockets:
                sockets.remove(websocket)
        print(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_transparency_update(self, update: TransparencyUpdate, target_connections: List[WebSocket] = None):
        """Send transparency update to specific connections or all connections"""
        connections = target_connections or self.active_connections
        if not connections:
            return
            
        message = {
            "type": "transparency_update",
            "data": update.dict(),
            "timestamp": datetime.now().timestamp()
        }
        
        disconnected = []
        for connection in connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error sending WebSocket message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected:
            self.disconnect(conn)

    def subscribe_to_conversation(self, websocket: WebSocket, conversation_id: str):
        if conversation_id not in self.conversation_subscribers:
            self.conversation_subscribers[conversation_id] = []
        if websocket not in self.conversation_subscribers[conversation_id]:
            self.conversation_subscribers[conversation_id].append(websocket)

    def subscribe_to_message(self, websocket: WebSocket, message_id: str):
        if message_id not in self.message_subscribers:
            self.message_subscribers[message_id] = []
        if websocket not in self.message_subscribers[message_id]:
            self.message_subscribers[message_id].append(websocket)

manager = ConnectionManager()

# Database initialization
def init_db():
    """Initialize SQLite database for conversations"""
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    
    # Create conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Transparency update function that works with WebSocket
async def send_transparency_update(stage_id: str, status: str, message: str = None, progress: float = None):
    """Send transparency update via WebSocket"""
    update = TransparencyUpdate(
        type="stage_update",
        stageId=stage_id,
        status=status,
        message=message,
        progress=progress
    )
    await manager.send_transparency_update(update)

# Modified transparency functions to work with WebSocket
class WebSocketTransparency:
    """Custom transparency class that sends updates via WebSocket"""
    
    @staticmethod
    async def start_processing():
        await manager.send_transparency_update(TransparencyUpdate(
            type="processing_start"
        ))
    
    @staticmethod
    async def update_stage(stage_id: str, status: str, message: str = None):
        await send_transparency_update(stage_id, status, message)
    
    @staticmethod
    async def set_progress(progress: float):
        await manager.send_transparency_update(TransparencyUpdate(
            type="progress_update",
            progress=progress
        ))
    
    @staticmethod
    async def complete_processing():
        await manager.send_transparency_update(TransparencyUpdate(
            type="processing_complete"
        ))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Main Q&A endpoint
@app.post("/api/qa", response_model=QAResponse)
async def ask_question(request: QARequest):
    try:
        # Generate IDs
        message_id = str(uuid.uuid4())
        conversation_id = request.conversationId or str(uuid.uuid4())
        
        print(f"Processing question: {request.question[:100]}...")
        
        # Start transparency tracking
        await WebSocketTransparency.start_processing()
        
        # Stage 1: Question Processing
        await WebSocketTransparency.update_stage(
            "question_processing", 
            "in_progress", 
            "Analyzing and understanding your question..."
        )
        await asyncio.sleep(0.5)  # Small delay for demo
        
        # Stage 2: Document Retrieval  
        await WebSocketTransparency.update_stage(
            "question_processing", 
            "completed"
        )
        await WebSocketTransparency.update_stage(
            "document_retrieval", 
            "in_progress", 
            "Searching through knowledge base for relevant information..."
        )
        await WebSocketTransparency.set_progress(0.2)
        
        # Use your existing QA chain
        qa_chain = setup_qa_chain_with_memory(memory_manager)
        
        # Stage 3: Context Generation
        await WebSocketTransparency.update_stage(
            "document_retrieval", 
            "completed"
        )
        await WebSocketTransparency.update_stage(
            "context_generation", 
            "in_progress", 
            "Organizing retrieved information into context..."
        )
        await WebSocketTransparency.set_progress(0.6)
        
        # Stage 4: Response Generation
        await WebSocketTransparency.update_stage(
            "context_generation", 
            "completed"
        )
        await WebSocketTransparency.update_stage(
            "response_generation", 
            "in_progress", 
            "Generating comprehensive response based on context..."
        )
        await WebSocketTransparency.set_progress(0.8)
        
        # Get response from your existing system
        # Note: You may need to modify this to work with your specific setup
        response = qa_chain.invoke({"question": request.question})
        if hasattr(response, 'content'):
            answer = response.content
        elif isinstance(response, dict):
            answer = response.get('answer', str(response))
        else:
            answer = str(response)
        
        # Clean the response using your existing function
        clean_answer = clean_response(answer, request.question)
        
        # Stage 5: Memory Saving
        await WebSocketTransparency.update_stage(
            "response_generation", 
            "completed"
        )
        await WebSocketTransparency.update_stage(
            "memory_saving", 
            "in_progress", 
            "Saving conversation to memory for future reference..."
        )
        
        # Save to database
        save_conversation_to_db(conversation_id, request.question, clean_answer, message_id)
        
        await WebSocketTransparency.update_stage(
            "memory_saving", 
            "completed"
        )
        await WebSocketTransparency.set_progress(1.0)
        await WebSocketTransparency.complete_processing()
        
        print(f"Question processed successfully")
        
        return QAResponse(
            answer=clean_answer,
            conversationId=conversation_id,
            messageId=message_id
        )
        
    except Exception as e:
        print(f"Error processing question: {e}")
        await manager.send_transparency_update(TransparencyUpdate(
            type="stage_update",
            status="error",
            message=f"Error occurred: {str(e)}"
        ))
        raise HTTPException(status_code=500, detail=str(e))

def save_conversation_to_db(conversation_id: str, question: str, answer: str, message_id: str):
    """Save conversation to SQLite database"""
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    
    try:
        # Check if conversation exists
        cursor.execute('SELECT id FROM conversations WHERE id = ?', (conversation_id,))
        if not cursor.fetchone():
            # Create new conversation
            cursor.execute('''
                INSERT INTO conversations (id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (conversation_id, question[:50] + "...", datetime.now(), datetime.now()))
        else:
            # Update existing conversation
            cursor.execute('''
                UPDATE conversations SET updated_at = ? WHERE id = ?
            ''', (datetime.now(), conversation_id))
        
        # Add user message
        user_message_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO messages (id, conversation_id, role, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_message_id, conversation_id, 'user', question, datetime.now()))
        
        # Add assistant message
        cursor.execute('''
            INSERT INTO messages (id, conversation_id, role, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (message_id, conversation_id, 'assistant', answer, datetime.now()))
        
        conn.commit()
        
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

# Get conversations
@app.get("/api/conversations")
async def get_conversations():
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT c.id, c.title, c.created_at, c.updated_at,
                   COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            GROUP BY c.id
            ORDER BY c.updated_at DESC
        ''')
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                "id": row[0],
                "title": row[1],
                "createdAt": row[2],
                "updatedAt": row[3],
                "messageCount": row[4]
            })
        
        return conversations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Get specific conversation
@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    
    try:
        # Get conversation
        cursor.execute('SELECT * FROM conversations WHERE id = ?', (conversation_id,))
        conv_row = cursor.fetchone()
        if not conv_row:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get messages
        cursor.execute('''
            SELECT id, role, content, timestamp 
            FROM messages 
            WHERE conversation_id = ? 
            ORDER BY timestamp ASC
        ''', (conversation_id,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "id": row[0],
                "role": row[1],
                "content": row[2],
                "timestamp": row[3]
            })
        
        return {
            "id": conv_row[0],
            "title": conv_row[1],
            "createdAt": conv_row[2],
            "updatedAt": conv_row[3],
            "messages": messages
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Delete conversation
@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    
    try:
        # Delete messages first
        cursor.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
        # Delete conversation
        cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conn.commit()
        return {"message": "Conversation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "subscribe":
                    sub_type = message.get("data", {}).get("type")
                    if sub_type == "conversation":
                        conversation_id = message.get("data", {}).get("conversationId")
                        if conversation_id:
                            manager.subscribe_to_conversation(websocket, conversation_id)
                            print(f"Subscribed to conversation: {conversation_id}")
                    elif sub_type == "message_processing":
                        message_id = message.get("data", {}).get("messageId")
                        if message_id:
                            manager.subscribe_to_message(websocket, message_id)
                            print(f"Subscribed to message processing: {message_id}")
                
                elif message_type == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                    
            except json.JSONDecodeError:
                print(f"Invalid JSON received: {data}")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    import socket
    
    # Try different ports, starting with 8004 to avoid conflicts
    ports_to_try = [8004, 8005, 8006, 8007]
    
    for port in ports_to_try:
        try:
            # Test if port is available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', port))
                if result != 0:  # Port is free
                    print(f"Starting Cariacterologie Claude API server on port {port}...")
                    print(f"React Frontend: http://localhost:5173")
                    print(f"API Docs: http://localhost:{port}/docs")
                    print(f"WebSocket: ws://localhost:{port}/ws")
                    print(f"Health Check: http://localhost:{port}/health")
                    if port != 8001:
                        print("\nIMPORTANT: Update your React .env file:")
                        print(f"VITE_API_URL=http://localhost:{port}")
                        print(f"VITE_WS_URL=ws://localhost:{port}")
                    
                    uvicorn.run(app, host="0.0.0.0", port=port)
                    break
                else:
                    print(f"Port {port} is in use, trying next port...")
            
        except Exception as e:
            print(f"Error checking port {port}: {e}")
            if port == ports_to_try[-1]:
                print(f"All ports {ports_to_try} are in use. Please free up a port or kill existing processes.")
                input("Press Enter to exit...")
            continue