import { useEffect, useRef, useState } from 'react';

interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: number;
}

interface WebSocketOptions {
  url: string;
  protocols?: string[];
  reconnect?: boolean;
  reconnectAttempts?: number;
  reconnectInterval?: number;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  onMessage?: (message: WebSocketMessage) => void;
}

interface WebSocketState {
  socket: WebSocket | null;
  lastMessage: WebSocketMessage | null;
  readyState: number;
  isConnected: boolean;
  isConnecting: boolean;
  error: Event | null;
}

export const useWebSocket = (options: WebSocketOptions) => {
  const {
    url,
    protocols,
    reconnect = true,
    reconnectAttempts = 5,
    reconnectInterval = 3000,
    onOpen,
    onClose,
    onError,
    onMessage,
  } = options;

  const [state, setState] = useState<WebSocketState>({
    socket: null,
    lastMessage: null,
    readyState: WebSocket.CLOSED,
    isConnected: false,
    isConnecting: false,
    error: null,
  });

  const reconnectTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);
  const reconnectAttemptsRef = useRef(0);
  const shouldReconnectRef = useRef(reconnect);

  const connect = () => {
    if (state.socket?.readyState === WebSocket.OPEN || 
        state.socket?.readyState === WebSocket.CONNECTING) {
      return;
    }

    setState(prev => ({ ...prev, isConnecting: true, error: null }));

    try {
      const socket = new WebSocket(url, protocols);

      socket.onopen = () => {
        setState(prev => ({
          ...prev,
          socket,
          readyState: socket.readyState,
          isConnected: true,
          isConnecting: false,
          error: null,
        }));
        reconnectAttemptsRef.current = 0;
        if (onOpen) onOpen();
      };

      socket.onclose = () => {
        setState(prev => ({
          ...prev,
          socket: null,
          readyState: WebSocket.CLOSED,
          isConnected: false,
          isConnecting: false,
        }));
        if (onClose) onClose();

        // Attempt reconnection if enabled
        if (shouldReconnectRef.current && 
            reconnectAttemptsRef.current < reconnectAttempts) {
          reconnectAttemptsRef.current++;
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };

      socket.onerror = (error) => {
        setState(prev => ({
          ...prev,
          error,
          isConnecting: false,
        }));
        if (onError) onError(error);
      };

      socket.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          setState(prev => ({
            ...prev,
            lastMessage: message,
          }));
          if (onMessage) onMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      setState(prev => ({ ...prev, socket }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isConnecting: false,
        error: error as Event,
      }));
    }
  };

  const disconnect = () => {
    shouldReconnectRef.current = false;
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (state.socket) {
      state.socket.close();
    }
  };

  const sendMessage = (message: any) => {
    if (state.socket?.readyState === WebSocket.OPEN) {
      const wsMessage: WebSocketMessage = {
        type: 'message',
        data: message,
        timestamp: Date.now(),
      };
      state.socket.send(JSON.stringify(wsMessage));
      return true;
    }
    return false;
  };

  const sendTypedMessage = (type: string, data: any) => {
    if (state.socket?.readyState === WebSocket.OPEN) {
      const wsMessage: WebSocketMessage = {
        type,
        data,
        timestamp: Date.now(),
      };
      state.socket.send(JSON.stringify(wsMessage));
      return true;
    }
    return false;
  };

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [url]);

  useEffect(() => {
    shouldReconnectRef.current = reconnect;
  }, [reconnect]);

  return {
    ...state,
    connect,
    disconnect,
    sendMessage,
    sendTypedMessage,
    reconnectAttempts: reconnectAttemptsRef.current,
  };
};