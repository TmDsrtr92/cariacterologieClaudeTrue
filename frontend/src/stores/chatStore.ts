import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { 
  Message, 
  Conversation, 
  ProcessingStage, 
  TransparencyState,
  ChatState 
} from '../types';

interface ChatStore extends ChatState {
  // Actions
  addMessage: (role: 'user' | 'assistant', content: string, conversationId?: string) => void;
  createConversation: () => string;
  setCurrentConversation: (conversationId: string) => void;
  clearCurrentConversation: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | undefined) => void;
  
  // Transparency actions
  transparency: TransparencyState;
  startTransparency: () => void;
  stopTransparency: () => void;
  updateTransparencyStage: (stageId: string, updates: Partial<ProcessingStage>) => void;
  setTransparencyProgress: (progress: number) => void;
  addTransparencyStage: (stage: Omit<ProcessingStage, 'timestamp'>) => void;
}

const initialTransparencyState: TransparencyState = {
  isActive: false,
  stages: [],
  progress: 0,
};

const createDefaultStages = (): ProcessingStage[] => [
  {
    id: 'question_processing',
    name: 'Question Processing',
    description: 'Analyzing and understanding your question...',
    status: 'pending',
    icon: '🤔',
  },
  {
    id: 'document_retrieval',
    name: 'Document Retrieval',
    description: 'Searching through knowledge base for relevant information...',
    status: 'pending',
    icon: '🔍',
  },
  {
    id: 'context_generation',
    name: 'Context Generation',
    description: 'Organizing retrieved information into context...',
    status: 'pending',
    icon: '📝',
  },
  {
    id: 'response_generation',
    name: 'Response Generation',
    description: 'Generating comprehensive response based on context...',
    status: 'pending',
    icon: '💭',
  },
  {
    id: 'memory_saving',
    name: 'Memory Saving',
    description: 'Saving conversation to memory for future reference...',
    status: 'pending',
    icon: '💾',
  },
];

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      // Initial state
      conversations: [],
      currentConversation: undefined,
      isLoading: false,
      error: undefined,
      transparency: initialTransparencyState,

      // Chat actions
      addMessage: (role, content, conversationId) => {
        const state = get();
        const message: Message = {
          id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          role,
          content,
          timestamp: new Date(),
        };

        // If no conversationId provided, use current or create new
        const targetConversationId = conversationId || state.currentConversation?.id || get().createConversation();
        
        set(state => ({
          conversations: state.conversations.map(conv =>
            conv.id === targetConversationId
              ? {
                  ...conv,
                  messages: [...conv.messages, message],
                  updatedAt: new Date(),
                }
              : conv
          ),
          currentConversation: state.currentConversation?.id === targetConversationId
            ? {
                ...state.currentConversation,
                messages: [...state.currentConversation.messages, message],
                updatedAt: new Date(),
              }
            : state.currentConversation,
        }));
      },

      createConversation: () => {
        const conversation: Conversation = {
          id: `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          messages: [],
          title: 'New Conversation',
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        set(state => ({
          conversations: [conversation, ...state.conversations],
          currentConversation: conversation,
        }));

        return conversation.id;
      },

      setCurrentConversation: (conversationId) => {
        const state = get();
        const conversation = state.conversations.find(conv => conv.id === conversationId);
        if (conversation) {
          set({ currentConversation: conversation });
        }
      },

      clearCurrentConversation: () => {
        set({ currentConversation: undefined });
      },

      setLoading: (loading) => {
        set({ isLoading: loading });
      },

      setError: (error) => {
        set({ error });
      },

      // Transparency actions
      startTransparency: () => {
        set({
          transparency: {
            isActive: true,
            stages: createDefaultStages(),
            progress: 0,
          },
        });
      },

      stopTransparency: () => {
        set({
          transparency: {
            ...get().transparency,
            isActive: false,
          },
        });
      },

      updateTransparencyStage: (stageId, updates) => {
        set(state => ({
          transparency: {
            ...state.transparency,
            stages: state.transparency.stages.map(stage =>
              stage.id === stageId
                ? { ...stage, ...updates, timestamp: new Date() }
                : stage
            ),
            currentStage: updates.status === 'in_progress' 
              ? state.transparency.stages.find(s => s.id === stageId)
              : state.transparency.currentStage,
          },
        }));
      },

      setTransparencyProgress: (progress) => {
        set(state => ({
          transparency: {
            ...state.transparency,
            progress: Math.max(0, Math.min(1, progress)),
          },
        }));
      },

      addTransparencyStage: (stage) => {
        set(state => ({
          transparency: {
            ...state.transparency,
            stages: [
              ...state.transparency.stages,
              { ...stage, timestamp: new Date() },
            ],
          },
        }));
      },
    }),
    {
      name: 'chat-storage',
      partialize: (state) => ({
        conversations: state.conversations,
        currentConversation: state.currentConversation,
      }),
      onRehydrateStorage: () => (state) => {
        // Convert timestamp strings back to Date objects
        if (state?.conversations) {
          state.conversations = state.conversations.map(conv => ({
            ...conv,
            createdAt: new Date(conv.createdAt),
            updatedAt: new Date(conv.updatedAt),
            messages: conv.messages.map(msg => ({
              ...msg,
              timestamp: new Date(msg.timestamp),
            })),
          }));
        }
        if (state?.currentConversation) {
          state.currentConversation = {
            ...state.currentConversation,
            createdAt: new Date(state.currentConversation.createdAt),
            updatedAt: new Date(state.currentConversation.updatedAt),
            messages: state.currentConversation.messages.map(msg => ({
              ...msg,
              timestamp: new Date(msg.timestamp),
            })),
          };
        }
      },
    }
  )
);