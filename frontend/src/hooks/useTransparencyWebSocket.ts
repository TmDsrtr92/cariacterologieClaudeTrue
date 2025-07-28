import { useEffect } from 'react';
import { useChatStore } from '../stores/chatStore';
import { useWebSocket } from './useWebSocket';
import { getWebSocketUrl } from '../services/api';

interface TransparencyUpdate {
  type: 'stage_update' | 'progress_update' | 'stage_complete' | 'processing_complete';
  stageId?: string;
  status?: 'pending' | 'in_progress' | 'completed' | 'error';
  progress?: number;
  message?: string;
  conversationId?: string;
  messageId?: string;
}

export const useTransparencyWebSocket = (enabled: boolean = true) => {
  const {
    updateTransparencyStage,
    setTransparencyProgress,
    stopTransparency,
  } = useChatStore();

  const webSocket = useWebSocket({
    url: getWebSocketUrl(),
    reconnect: enabled,
    reconnectAttempts: 5,
    reconnectInterval: 3000,
    onOpen: () => {
      console.log('🔗 WebSocket connected for transparency updates');
    },
    onClose: () => {
      console.log('🔌 WebSocket disconnected');
    },
    onError: (error) => {
      console.error('❌ WebSocket error:', error);
    },
    onMessage: (message) => {
      handleTransparencyUpdate(message.data);
    },
  });

  const handleTransparencyUpdate = (update: TransparencyUpdate) => {
    console.log('📡 Transparency update received:', update);

    switch (update.type) {
      case 'stage_update':
        if (update.stageId && update.status) {
          updateTransparencyStage(update.stageId, {
            status: update.status,
            description: update.message,
          });
        }
        break;

      case 'progress_update':
        if (typeof update.progress === 'number') {
          setTransparencyProgress(update.progress);
        }
        break;

      case 'stage_complete':
        if (update.stageId) {
          updateTransparencyStage(update.stageId, {
            status: 'completed',
            description: update.message || 'Completed successfully',
          });
        }
        break;

      case 'processing_complete':
        stopTransparency();
        break;

      default:
        console.warn('Unknown transparency update type:', update.type);
    }
  };

  // Subscribe to specific conversation updates
  const subscribeToConversation = (conversationId: string) => {
    webSocket.sendTypedMessage('subscribe', {
      type: 'conversation',
      conversationId,
    });
  };

  // Subscribe to specific message processing
  const subscribeToMessage = (messageId: string) => {
    webSocket.sendTypedMessage('subscribe', {
      type: 'message_processing',
      messageId,
    });
  };

  // Unsubscribe from updates
  const unsubscribe = (type: string, id: string) => {
    webSocket.sendTypedMessage('unsubscribe', {
      type,
      id,
    });
  };

  // Cleanup on unmount
  useEffect(() => {
    if (!enabled) {
      webSocket.disconnect();
    }
  }, [enabled]);

  return {
    isConnected: webSocket.isConnected,
    isConnecting: webSocket.isConnecting,
    error: webSocket.error,
    reconnectAttempts: webSocket.reconnectAttempts,
    subscribeToConversation,
    subscribeToMessage,
    unsubscribe,
    connect: webSocket.connect,
    disconnect: webSocket.disconnect,
  };
};