import React, { useEffect, useRef } from 'react';
import { useChatStore } from '../../stores/chatStore';
import { useTransparencyWebSocket } from '../../hooks/useTransparencyWebSocket';
import { api } from '../../services/api';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import TransparencyPanel from '../transparency/TransparencyPanel';
import { Card } from '../ui';

const ChatContainer: React.FC = () => {
  const {
    currentConversation,
    isLoading,
    error,
    transparency,
    addMessage,
    createConversation,
    setLoading,
    setError,
    startTransparency,
    stopTransparency,
  } = useChatStore();

  // WebSocket connection for real-time transparency updates
  const transparencyWS = useTransparencyWebSocket(true);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentConversation?.messages]);

  // Initialize conversation if none exists
  useEffect(() => {
    if (!currentConversation) {
      createConversation();
    }
  }, [currentConversation, createConversation]);


  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    try {
      setError(undefined);
      setLoading(true);

      // Add user message immediately
      addMessage('user', message);

      // Start transparency tracking
      startTransparency();

      // Subscribe to conversation updates via WebSocket
      if (currentConversation?.id && transparencyWS.isConnected) {
        transparencyWS.subscribeToConversation(currentConversation.id);
      }

      // Call real API
      console.log('Calling API with:', {
        question: message,
        conversationId: currentConversation?.id,
        apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8001'
      });
      
      const response = await api.askQuestion({
        question: message,
        conversationId: currentConversation?.id,
      });

      console.log('API response:', response);

      // Add assistant response
      addMessage('assistant', response.answer, response.conversationId);

      // Stop transparency
      stopTransparency();
    } catch (err: any) {
      setError(err.message || 'Failed to send message. Please try again.');
      console.error('Error sending message:', err);
      stopTransparency();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-h-screen">
      {/* Chat Messages */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto custom-scrollbar px-4 py-6">
          <div className="max-w-4xl mx-auto">
            {/* WebSocket Connection Status */}
            {!transparencyWS.isConnected && (
              <div className="mb-4">
                <Card className="bg-yellow-900/20 border-yellow-500/50 text-yellow-200" padding="sm">
                  <div className="flex items-center gap-2 text-sm">
                    <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
                    <span>Connecting to real-time updates...</span>
                  </div>
                </Card>
              </div>
            )}

            {/* Transparency Panel */}
            {transparency.isActive && (
              <div className="mb-6">
                <TransparencyPanel transparencyState={transparency} />
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mb-4">
                <Card className="bg-red-900/20 border-red-500/50 text-red-200" padding="md">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="font-light">{error}</span>
                  </div>
                </Card>
              </div>
            )}

            {/* Messages */}
            {currentConversation?.messages.length === 0 ? (
              <div className="text-center py-16">
                <div className="w-16 h-16 mx-auto mb-4 bg-dark-700 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-light text-dark-200 mb-2">Start a Conversation</h3>
                <p className="text-dark-400 font-light max-w-md mx-auto">
                  Ask any question and watch the AI process your request with full transparency into each step.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {currentConversation?.messages.map((message) => (
                  <MessageBubble key={message.id} message={message} />
                ))}
                
                {/* Typing indicator */}
                {isLoading && (
                  <MessageBubble
                    message={{
                      id: 'typing',
                      role: 'assistant',
                      content: '',
                      timestamp: new Date(),
                    }}
                    isTyping={true}
                  />
                )}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Chat Input */}
      <ChatInput 
        onSendMessage={handleSendMessage}
        disabled={isLoading}
        placeholder={isLoading ? "AI is processing your request..." : "Ask your question here..."}
      />
    </div>
  );
};

export default ChatContainer;