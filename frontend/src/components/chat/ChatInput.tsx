import React, { useState, useRef, useEffect } from 'react';
import { Button } from '../ui';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "Ask your question here...",
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (!message.trim() || disabled) return;
    
    onSendMessage(message.trim());
    setMessage('');
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  }, [message]);

  return (
    <div className="bg-dark-800 border-t border-dark-700 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex gap-3 items-end">
          <div className="flex-1">
            <div className="relative">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                disabled={disabled}
                rows={1}
                className="
                  w-full px-4 py-3 bg-dark-700 border border-dark-600 rounded-lg
                  text-dark-100 placeholder-dark-400 font-light resize-none
                  focus:outline-none focus:ring-2 focus:ring-primary-blue focus:border-transparent
                  disabled:opacity-50 disabled:cursor-not-allowed
                  custom-scrollbar transition-colors duration-200
                  hover:border-dark-500
                "
                style={{ minHeight: '48px', maxHeight: '120px' }}
              />
              
              {/* Character count (optional) */}
              {message.length > 500 && (
                <div className="absolute bottom-2 right-2 text-xs text-dark-400">
                  {message.length}/1000
                </div>
              )}
            </div>
          </div>

          <Button
            onClick={handleSubmit}
            disabled={!message.trim() || disabled}
            className="mb-0 px-6 py-3 h-12"
          >
            <svg
              className="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
            Send
          </Button>
        </div>

        {/* Hint text */}
        <div className="mt-2 text-xs text-dark-400 text-center">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatInput;