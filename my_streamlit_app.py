import streamlit as st
from core.langgraph_qa_chain import setup_qa_chain_with_memory, clean_response
from utils.conversation_manager import (
    initialize_conversations, 
    get_current_messages, 
    add_message,
    get_current_memory
)
from utils.streamlit_helpers import (
    get_langfuse_handler, 
    create_stream_handler, 
    render_conversation_sidebar, 
    render_chat_messages,
    get_selected_collection
)
from core.callbacks import RetrievalCallbackHandler

# Initialize the app
st.title("CarIActérologie")

# Initialize conversations
initialize_conversations()

# Set up Langfuse handler
langfuse_handler = get_langfuse_handler()

# Render conversation sidebar
render_conversation_sidebar()

# Get current conversation messages and memory
messages = get_current_messages()
current_memory = get_current_memory()

# Get selected collection
selected_collection = get_selected_collection()

# Set up QA chain with memory and selected collection
qa_chain = setup_qa_chain_with_memory(current_memory, collection_key=selected_collection)

# Render existing chat messages
render_chat_messages(messages)

# Handle new user input
if prompt_input := st.chat_input("Comment puis-je t'aider aujourd'hui ?"):
    # Add user message to conversation
    add_message("user", prompt_input)
    
    # Display user message
    user_msg = st.chat_message("user")
    user_msg.markdown(prompt_input)

    # Create assistant message placeholder
    assistant_msg = st.chat_message("assistant")
    stream_placeholder = assistant_msg.empty()
    
    # Create streaming handler
    stream_handler = create_stream_handler(stream_placeholder)
    
    # Create retrieval callback handler with memory
    retrieval_handler = RetrievalCallbackHandler(memory=current_memory)

    # Get response from QA chain with streaming and memory
    result = qa_chain.invoke(
        {"question": prompt_input},
        config={"callbacks": [langfuse_handler, stream_handler, retrieval_handler]}
    )
    
    answer = result["answer"]
    # Note: source_documents not available with memory-enabled chain

    # Clean the response to remove any repetition of the user's question
    cleaned_answer = clean_response(answer, prompt_input)

    # Display final response (remove cursor)
    stream_placeholder.markdown(cleaned_answer)

    # Add assistant message to conversation
    add_message("assistant", cleaned_answer)
