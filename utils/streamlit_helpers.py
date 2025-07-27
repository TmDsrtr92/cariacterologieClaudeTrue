import streamlit as st
from langfuse.langchain import CallbackHandler
from config.settings import STREAMING_CONFIG
from core.callbacks import StreamlitCallbackHandler


def get_langfuse_handler():
    """Get Langfuse callback handler"""
    return CallbackHandler()

def create_stream_handler(placeholder):
    """Create a streaming callback handler for Streamlit"""
    return StreamlitCallbackHandler(
        placeholder, 
        update_every=STREAMING_CONFIG["update_every"], 
        delay=STREAMING_CONFIG["delay"]
    )

def render_conversation_sidebar():
    """Render the conversation sidebar"""
    from utils.conversation_manager import (
        get_conversation_names, 
        get_current_conversation, 
        set_current_conversation, 
        create_new_conversation,
        get_current_memory,
        clear_conversation_memory
    )
    from config.settings import MEMORY_CONFIG, AVAILABLE_COLLECTIONS, DEFAULT_COLLECTION_KEY
    
    conversation_names = get_conversation_names()
    current_conversation = get_current_conversation()
    
    with st.sidebar:
        st.title("Conversations")
        selected = st.radio(
            "Sélectionnez une conversation",
            conversation_names,
            index=conversation_names.index(current_conversation)
        )
        set_current_conversation(selected)
        
        if st.button("Nouvelle conversation"):
            create_new_conversation()
            st.rerun()
        
        # Collection selection section
        st.divider()
        st.subheader("📚 Collection de documents")
        
        # Get current collection from session state or use default
        if "selected_collection" not in st.session_state:
            st.session_state.selected_collection = DEFAULT_COLLECTION_KEY
        
        # Collection selector
        collection_options = list(AVAILABLE_COLLECTIONS.keys())
        current_index = collection_options.index(st.session_state.selected_collection)
        
        selected_collection = st.selectbox(
            "Type de chunking:",
            collection_options,
            index=current_index,
            help="Choisissez le type de découpage des documents"
        )
        
        # Update session state if selection changed
        if selected_collection != st.session_state.selected_collection:
            st.session_state.selected_collection = selected_collection
            st.rerun()
        
        # Display collection info
        collection_info = AVAILABLE_COLLECTIONS[selected_collection]
        st.write(f"**Description:** {collection_info['description']}")
        st.write(f"**Type:** {collection_info['chunk_type']}")
        
        # Collection status indicator
        if collection_info['chunk_type'] == 'semantic':
            st.success("✅ Chunking sémantique actif")
        else:
            st.info("ℹ️ Chunking par caractères actif")
        
        # Memory management section
        st.divider()
        st.subheader("🧠 Memory Management")
        
        current_memory = get_current_memory()
        chat_history = current_memory.get_chat_history()
        token_count = current_memory.get_token_count()
        max_tokens = MEMORY_CONFIG["max_token_limit"]
        
        # Display memory statistics
        st.write(f"**Messages:** {len(chat_history)}")
        st.write(f"**Tokens:** {token_count}/{max_tokens}")
        
        # Progress bar for token usage
        token_percentage = (token_count / max_tokens) * 100
        st.progress(token_percentage / 100)
        
        # Color-coded token status
        if token_percentage > 90:
            st.warning("⚠️ Memory nearly full")
        elif token_percentage > 70:
            st.info("ℹ️ Memory usage moderate")
        else:
            st.success("✅ Memory usage normal")
        
        if st.button("Clear Memory", type="secondary"):
            clear_conversation_memory()
            st.success("Memory cleared!")
            st.rerun()
        
        # Show recent conversation context
        if chat_history:
            st.write("**Recent context:**")
            recent_messages = chat_history[-4:]  # Show last 4 messages
            for msg in recent_messages:
                role = "👤" if msg.type == "human" else "🤖"
                content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                st.write(f"{role} {content}")

def get_selected_collection():
    """Get the currently selected collection from session state"""
    from config.settings import DEFAULT_COLLECTION_KEY
    
    if "selected_collection" not in st.session_state:
        st.session_state.selected_collection = DEFAULT_COLLECTION_KEY
    
    return st.session_state.selected_collection

def render_chat_messages(messages):
    """Render chat messages in the main area"""
    for message in messages:
        chat_msg = st.chat_message(message["role"])
        chat_msg.markdown(message["content"]) 