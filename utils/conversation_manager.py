import streamlit as st
from core.memory import create_memory_manager

def initialize_conversations():
    """Initialize conversation state in session state"""
    if "conversations" not in st.session_state:
        st.session_state.conversations = {"conversation 1": []}
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = "conversation 1"
    if "conversation_memories" not in st.session_state:
        st.session_state.conversation_memories = {"conversation 1": create_memory_manager()}

def get_conversation_names():
    """Get list of conversation names"""
    return list(st.session_state.conversations.keys())

def get_current_conversation():
    """Get the current conversation name"""
    return st.session_state.current_conversation

def set_current_conversation(conversation_name):
    """Set the current conversation"""
    st.session_state.current_conversation = conversation_name

def get_current_messages():
    """Get messages from current conversation"""
    return st.session_state.conversations[st.session_state.current_conversation]

def get_current_memory():
    """Get memory manager for current conversation"""
    current_conv = get_current_conversation()
    if current_conv not in st.session_state.conversation_memories:
        st.session_state.conversation_memories[current_conv] = create_memory_manager()
    return st.session_state.conversation_memories[current_conv]

def add_message(role, content):
    """Add a message to the current conversation (memory is handled by ConversationalRetrievalChain)"""
    messages = get_current_messages()
    messages.append({"role": role, "content": content})
    
    # Note: Memory is automatically managed by ConversationalRetrievalChain
    # No need to manually add to memory here

def create_new_conversation():
    """Create a new conversation with its own memory"""
    conversation_names = get_conversation_names()
    new_name = f"conversation {len(conversation_names) + 1}"
    st.session_state.conversations[new_name] = []
    st.session_state.conversation_memories[new_name] = create_memory_manager()
    st.session_state.current_conversation = new_name
    return new_name

def clear_conversation_memory(conversation_name=None):
    """Clear memory for a specific conversation or current conversation"""
    if conversation_name is None:
        conversation_name = get_current_conversation()
    
    if conversation_name in st.session_state.conversation_memories:
        st.session_state.conversation_memories[conversation_name].clear() 