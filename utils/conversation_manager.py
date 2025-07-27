import streamlit as st
from core.langgraph_memory import create_langgraph_memory_manager, create_memory_manager

def initialize_conversations():
    """Initialize conversation state in session state with LangGraph memory"""
    if "conversations" not in st.session_state:
        st.session_state.conversations = {"conversation 1": []}
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = "conversation 1"
    if "conversation_memories" not in st.session_state:
        # Use LangGraph memory manager with backward compatibility wrapper
        st.session_state.conversation_memories = {"conversation 1": create_memory_manager()}
    if "langgraph_manager" not in st.session_state:
        # Create shared LangGraph manager for all conversations
        st.session_state.langgraph_manager = create_langgraph_memory_manager()
    if "conversation_threads" not in st.session_state:
        # Map conversation names to LangGraph thread IDs
        manager = st.session_state.langgraph_manager
        thread_id = manager.create_conversation("Conversation 1")
        st.session_state.conversation_threads = {"conversation 1": thread_id}

def get_conversation_names():
    """Get list of conversation names"""
    return list(st.session_state.conversations.keys())

def get_current_conversation():
    """Get the current conversation name"""
    return st.session_state.current_conversation

def set_current_conversation(conversation_name):
    """Set the current conversation and update LangGraph thread"""
    st.session_state.current_conversation = conversation_name
    
    # Update LangGraph manager to use the correct thread
    if conversation_name in st.session_state.conversation_threads:
        thread_id = st.session_state.conversation_threads[conversation_name]
        st.session_state.langgraph_manager.set_current_thread(thread_id)

def get_current_messages():
    """Get messages from current conversation"""
    return st.session_state.conversations[st.session_state.current_conversation]

def get_current_memory():
    """Get memory manager for current conversation (backward compatibility)"""
    current_conv = get_current_conversation()
    if current_conv not in st.session_state.conversation_memories:
        st.session_state.conversation_memories[current_conv] = create_memory_manager()
    
    # Ensure LangGraph manager is using the correct thread
    if current_conv in st.session_state.conversation_threads:
        thread_id = st.session_state.conversation_threads[current_conv]
        st.session_state.langgraph_manager.set_current_thread(thread_id)
        # Update the memory manager to use the correct LangGraph thread
        memory_manager = st.session_state.conversation_memories[current_conv]
        if hasattr(memory_manager, 'manager'):
            memory_manager.manager.set_current_thread(thread_id)
    
    return st.session_state.conversation_memories[current_conv]

def add_message(role, content):
    """Add a message to the current conversation (memory is handled by ConversationalRetrievalChain)"""
    messages = get_current_messages()
    messages.append({"role": role, "content": content})
    
    # Note: Memory is automatically managed by ConversationalRetrievalChain
    # No need to manually add to memory here

def create_new_conversation():
    """Create a new conversation with its own LangGraph thread and memory"""
    conversation_names = get_conversation_names()
    new_name = f"conversation {len(conversation_names) + 1}"
    
    # Create new conversation
    st.session_state.conversations[new_name] = []
    st.session_state.conversation_memories[new_name] = create_memory_manager()
    
    # Create new LangGraph thread
    manager = st.session_state.langgraph_manager
    thread_id = manager.create_conversation(f"Conversation {len(conversation_names) + 1}")
    st.session_state.conversation_threads[new_name] = thread_id
    
    # Set as current conversation
    st.session_state.current_conversation = new_name
    manager.set_current_thread(thread_id)
    
    return new_name

def clear_conversation_memory(conversation_name=None):
    """Clear memory for a specific conversation or current conversation"""
    if conversation_name is None:
        conversation_name = get_current_conversation()
    
    # Clear Streamlit conversation messages
    if conversation_name in st.session_state.conversations:
        st.session_state.conversations[conversation_name] = []
    
    # Clear memory manager
    if conversation_name in st.session_state.conversation_memories:
        st.session_state.conversation_memories[conversation_name].clear()
    
    # Clear LangGraph thread memory
    if conversation_name in st.session_state.conversation_threads:
        thread_id = st.session_state.conversation_threads[conversation_name]
        manager = st.session_state.langgraph_manager
        original_thread = manager.current_thread_id
        manager.set_current_thread(thread_id)
        manager.clear()
        # Restore original thread if different
        if original_thread and original_thread != thread_id:
            manager.set_current_thread(original_thread)


def get_conversation_summary(conversation_name=None):
    """Get summary of a conversation using LangGraph memory"""
    if conversation_name is None:
        conversation_name = get_current_conversation()
    
    if conversation_name in st.session_state.conversation_threads:
        thread_id = st.session_state.conversation_threads[conversation_name]
        manager = st.session_state.langgraph_manager
        return manager.get_conversation_summary(thread_id)
    
    return {}


def list_all_conversations():
    """List all conversations with their LangGraph summaries"""
    manager = st.session_state.langgraph_manager
    return manager.list_conversations()


def delete_conversation(conversation_name):
    """Delete a conversation completely"""
    if conversation_name == "conversation 1":
        # Don't delete the first conversation, just clear it
        clear_conversation_memory(conversation_name)
        return
    
    # Remove from Streamlit state
    if conversation_name in st.session_state.conversations:
        del st.session_state.conversations[conversation_name]
    if conversation_name in st.session_state.conversation_memories:
        del st.session_state.conversation_memories[conversation_name]
    
    # Delete LangGraph thread
    if conversation_name in st.session_state.conversation_threads:
        thread_id = st.session_state.conversation_threads[conversation_name]
        manager = st.session_state.langgraph_manager
        manager.delete_conversation(thread_id)
        del st.session_state.conversation_threads[conversation_name]
    
    # Switch to first conversation if current was deleted
    if st.session_state.current_conversation == conversation_name:
        first_conv = list(st.session_state.conversations.keys())[0]
        set_current_conversation(first_conv) 