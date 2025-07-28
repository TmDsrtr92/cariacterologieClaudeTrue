import React from 'react';
import { Card } from '../ui';
import type { Message } from '../../types';

interface MessageBubbleProps {
  message: Message;
  isTyping?: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isTyping = false }) => {
  const isUser = message.role === 'user';

  const formatTimestamp = (date: Date) => {
    try {
      // Check if date is valid
      if (!date || isNaN(date.getTime())) {
        return new Date().toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true,
        });
      }
      
      return new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
      }).format(date);
    } catch (error) {
      console.warn('Error formatting timestamp:', error);
      return 'now';
    }
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-3`}>
        {/* Avatar */}
        <div className={`
          flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-light
          ${isUser 
            ? 'bg-primary-purple text-white' 
            : 'bg-primary-blue text-white'
          }
        `}>
          {isUser ? 'U' : 'AI'}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <Card
            className={`
              ${isUser 
                ? 'bg-primary-purple border-primary-purple text-white' 
                : 'bg-dark-800 border-dark-700 text-dark-50'
              }
              ${isTyping ? 'animate-pulse' : ''}
            `}
            padding="md"
            shadow="sm"
          >
            {isTyping ? (
              <div className="flex items-center space-x-1">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                </div>
                <span className="ml-2 text-sm font-light opacity-70">AI is thinking...</span>
              </div>
            ) : (
              <div className="whitespace-pre-wrap font-light leading-relaxed">
                {message.content}
              </div>
            )}
          </Card>

          {/* Timestamp */}
          <div className={`
            text-xs text-dark-400 mt-1 px-2
            ${isUser ? 'text-right' : 'text-left'}
          `}>
            {formatTimestamp(message.timestamp)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;