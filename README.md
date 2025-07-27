# CarIActerologie 🤖

## Introduction

**CarIActerologie** is an intelligent conversational agent specialized in French characterology, based on René Le Senne's *Traité de caractérologie* (Treatise on Characterology). This application helps users identify their character type and understand how to live with their personality traits through an interactive chat interface.

### What is Characterology?

Characterology is a branch of psychology that studies personality through the analysis of character traits. René Le Senne's system identifies 8 character types based on three fundamental factors:

1. **Emotivity (E/nE)** - Emotional reactivity and sensitivity
2. **Activity (A/nA)** - Response to obstacles and drive to act
3. **Resonance (P/S)** - How impressions are processed (Primary/Secondary)

The 8 character types are: Colérique, Passionné, Nerveux, Sentimental, Sanguin, Flegmatique, Amorphe, and Apathique.

## Features

- 🤖 **AI-Powered Conversations**: Interactive chat with an expert characterology psychologist
- 📚 **Knowledge Base**: Access to the complete *Traité de caractérologie* content
- 💬 **Multi-Conversation Support**: Manage multiple conversation threads with independent memory
- 🧠 **Advanced Memory Management**: Token-based conversation memory (2000 tokens) with real-time monitoring
- 🔄 **Real-time Streaming**: See responses being generated in real-time with typing indicators
- 📖 **Citation Integration**: Always includes relevant citations from the source material
- 🎯 **Personalized Guidance**: Tailored advice based on character analysis
- 🧹 **Response Cleaning**: Automatic removal of question repetition for cleaner responses
- 📊 **Memory Analytics**: Visual progress bars and token usage monitoring
- 🔍 **Retrieval Debugging**: Console logging for document retrieval and memory analysis

## Technology Stack

- **Frontend**: Streamlit
- **AI/LLM**: OpenAI GPT-4o-mini
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI Embeddings
- **Framework**: LangChain
- **Monitoring**: Langfuse
- **Memory Management**: ConversationTokenBufferMemory
- **Language**: Python

## Project Structure

```
CarIActerologie/
├── 📁 config/                    # Configuration and settings
│   ├── __init__.py
│   ├── settings.py              # API keys, model config, vectorstore settings
│   └── prompts.py               # System prompts and templates
├── 📁 core/                     # Core AI functionality
│   ├── __init__.py
│   ├── llm_setup.py            # LLM, embeddings, and vectorstore initialization
│   ├── qa_chain.py             # QA chain configuration with memory support
│   ├── callbacks.py            # Custom callback handlers for streaming and debugging
│   └── memory.py               # Advanced conversation memory management
├── 📁 utils/                    # Utility functions and helpers
│   ├── __init__.py
│   ├── conversation_manager.py  # Multi-conversation state management
│   └── streamlit_helpers.py    # Streamlit-specific UI utilities
├── 📁 documents/                # Source documents
│   ├── traite_de_caracterologie.txt
│   ├── traite_de_caracterologie_extrait.txt
│   └── traite_caracterologie.pdf
├── 📁 index_stores/             # Vector database storage
│   └── [ChromaDB files]
├── 📁 archives/                 # Development documentation
│   ├── MEMORY_IMPLEMENTATION.md
│   ├── MEMORY_FIXES.md
│   ├── MEMORY_DUPLICATE_FIX.md
│   ├── RESPONSE_CLEANING.md
│   └── REFACTORING_SUMMARY.md
├── 📁 .streamlit/               # Streamlit configuration
│   └── secrets.toml            # API keys and secrets
├── my_streamlit_app.py         # Main application entry point
├── chroma_script.py            # Document indexing script
├── compare_collections.py      # Vector collection comparison tool
├── test_structure_document.py  # Document structure testing
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## File Documentation

### Main Application Files

#### `my_streamlit_app.py` (75 lines)
The main Streamlit application that serves as the user interface. This file:
- Initializes the chat interface with memory-enabled QA chains
- Manages user interactions with response cleaning
- Handles conversation flow with streaming responses
- Integrates all components for a seamless user experience
- Uses `ConversationalRetrievalChain` with memory for context-aware conversations

#### `chroma_script.py` (50 lines)
Script for indexing the characterology documents into the vector database:
- Loads the *Traité de caractérologie* text
- Splits text into manageable chunks
- Creates embeddings using OpenAI
- Stores everything in ChromaDB for retrieval

#### `compare_collections.py` (91 lines)
Utility script for comparing different vector collections:
- Tests multiple collections with the same queries
- Provides detailed analysis of retrieval results
- Helps optimize document indexing and chunking strategies

### Configuration (`config/`)

#### `config/settings.py` (41 lines)
Centralized configuration management:
- **API Configuration**: Functions to retrieve OpenAI and Langfuse API keys
- **Model Configuration**: LLM parameters (model, temperature, tokens, streaming)
- **Vectorstore Configuration**: ChromaDB settings (directory, collection, search parameters)
- **Streaming Configuration**: Real-time response display settings
- **Memory Configuration**: Token limits and model settings for memory management

#### `config/prompts.py` (64 lines)
Contains the system prompt and prompt templates:
- **SYSTEM_PROMPT**: The main instruction set for the AI characterology expert
- **get_qa_prompt()**: Function that creates the LangChain prompt template
- Includes comprehensive characterology knowledge and response guidelines

### Core Functionality (`core/`)

#### `core/llm_setup.py` (32 lines)
Handles all AI model initialization:
- **setup_llm()**: Creates and configures the OpenAI ChatOpenAI instance
- **setup_embeddings()**: Initializes OpenAI embeddings for text processing
- **setup_vectorstore()**: Creates and configures the ChromaDB vector store
- **setup_retriever()**: Sets up the document retriever for context-aware responses

#### `core/qa_chain.py` (57 lines)
Configures the question-answering chain with memory support:
- **setup_qa_chain()**: Creates the basic RetrievalQA chain
- **setup_qa_chain_with_memory()**: Creates memory-enabled ConversationalRetrievalChain
- **clean_response()**: Removes question repetition and common prefixes from responses
- Integrates all components for context-aware characterology responses

#### `core/callbacks.py` (121 lines)
Advanced callback handlers for enhanced user experience and debugging:
- **StreamlitCallbackHandler**: Class that enables real-time streaming of AI responses with typing indicators
- **RetrievalCallbackHandler**: Debug handler that logs document retrieval and memory analysis
- Manages text display with smooth updates and detailed console logging
- Provides insights into memory usage and document retrieval process

#### `core/memory.py` (102 lines)
Advanced conversation memory management using LangChain:
- **ConversationMemory**: Class that handles conversation context and history
- **ConversationTokenBufferMemory**: Stores conversation history up to token limit (default: 2000 tokens)
- **create_memory_manager()**: Factory function for creating memory instances
- Provides memory variables for LLM context, chat history management, and token counting
- Includes methods for manual memory manipulation and token usage monitoring

### Utilities (`utils/`)

#### `utils/conversation_manager.py` (59 lines)
Manages multi-conversation functionality with memory:
- **initialize_conversations()**: Sets up conversation state in Streamlit session
- **get_conversation_names()**: Retrieves list of available conversations
- **get_current_messages()**: Gets messages from the active conversation
- **add_message()**: Adds new messages to the current conversation
- **create_new_conversation()**: Creates new conversation threads with independent memory
- **clear_conversation_memory()**: Clears memory for specific conversations

#### `utils/streamlit_helpers.py` (99 lines)
Streamlit-specific UI and integration utilities:
- **setup_langfuse()**: Configures Langfuse for monitoring and logging
- **get_langfuse_handler()**: Creates Langfuse callback handler
- **create_stream_handler()**: Creates streaming callback handler
- **render_conversation_sidebar()**: Renders the conversation management sidebar with:
  - Token-based memory controls and progress indicators
  - Real-time memory usage statistics
  - Color-coded memory status indicators
  - Recent conversation context preview
  - Memory clearing functionality
- **render_chat_messages()**: Displays chat messages in the main interface

### Data and Configuration Files

#### `documents/`
Contains the source characterology texts:
- `traite_de_caracterologie.txt`: Full text of René Le Senne's treatise
- `traite_de_caracterologie_extrait.txt`: Extracted portions for testing
- `traite_caracterologie.pdf`: Original PDF document

#### `index_stores/`
ChromaDB vector database storage:
- Contains indexed document chunks and embeddings
- Enables semantic search for relevant characterology content
- Supports multiple collections for testing and optimization

#### `archives/`
Development documentation and implementation notes:
- `MEMORY_IMPLEMENTATION.md`: Detailed memory system implementation
- `MEMORY_FIXES.md`: Memory-related bug fixes and improvements
- `MEMORY_DUPLICATE_FIX.md`: Solutions for memory duplication issues
- `RESPONSE_CLEANING.md`: Response cleaning implementation details
- `REFACTORING_SUMMARY.md`: Code refactoring documentation

#### `.streamlit/secrets.toml`
Secure configuration file for API keys:
- OpenAI API key for LLM and embeddings
- Langfuse keys for monitoring
- Langfuse host configuration

#### `requirements.txt`
Python dependencies:
- streamlit: Web application framework
- openai: OpenAI API client
- langchain: LLM framework
- tiktoken: Token counting
- chromadb: Vector database
- PyPDF2: PDF processing
- langfuse: Monitoring and logging

## Installation and Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- Langfuse account (optional, for monitoring)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd CarIActerologie
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**
   Create `.streamlit/secrets.toml` with your API keys:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key"
   LANGFUSE_SECRET_KEY = "your-langfuse-secret-key"
   LANGFUSE_PUBLIC_KEY = "your-langfuse-public-key"
   LANGFUSE_HOST = "https://cloud.langfuse.com"
   ```

4. **Index the documents**
   ```bash
   python chroma_script.py
   ```

5. **Run the application**
   ```bash
   streamlit run my_streamlit_app.py
   ```

## Usage

1. **Start a conversation**: The app opens with a clean chat interface
2. **Ask about characterology**: Ask questions about personality types, character traits, or personal analysis
3. **Manage conversations**: Use the sidebar to switch between different conversation threads
4. **Monitor memory**: Track token usage and memory status in the sidebar
5. **Get expert guidance**: Receive detailed responses with citations from the source material
6. **Clear memory**: Use the sidebar to clear conversation memory when needed

## Key Features Explained

### Memory Management
- **Token-based Buffer**: Each conversation maintains up to 2000 tokens of context
- **Real-time Monitoring**: Visual progress bars show memory usage
- **Independent Memory**: Each conversation thread has its own memory instance
- **Automatic Cleanup**: Old messages are automatically removed when token limit is reached

### Response Cleaning
- **Question Removal**: Automatically removes repeated user questions from responses
- **Prefix Cleaning**: Removes common response prefixes that repeat the question
- **Cleaner Output**: Provides more natural and focused responses

### Multi-Conversation Support
- **Independent Threads**: Each conversation maintains separate context and memory
- **Easy Switching**: Seamlessly switch between different conversation threads
- **Memory Isolation**: Changes in one conversation don't affect others

### Debugging and Monitoring
- **Retrieval Logging**: Console output shows document retrieval process
- **Memory Analysis**: Detailed logging of conversation memory usage
- **Langfuse Integration**: Professional monitoring and analytics

## Architecture Benefits

### Modular Design
- **Separation of Concerns**: Each module has a specific responsibility
- **Maintainability**: Easy to locate and modify specific functionality
- **Reusability**: Components can be reused across different parts of the application
- **Testability**: Individual components can be tested in isolation

### Scalability
- **Configuration Management**: Centralized settings for easy modification
- **Component Isolation**: Changes to one component don't affect others
- **Extensibility**: Easy to add new features or modify existing ones
- **Memory Optimization**: Efficient token-based memory management

### Advanced Features
- **Streaming Responses**: Real-time text generation with typing indicators
- **Memory Analytics**: Visual feedback on conversation memory usage
- **Response Quality**: Automatic cleaning for better user experience
- **Debug Capabilities**: Comprehensive logging for development and troubleshooting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Acknowledgments

- René Le Senne for his foundational work in characterology
- OpenAI for providing the language models
- Streamlit for the web application framework
- LangChain for the LLM orchestration framework
- Langfuse for monitoring and analytics capabilities
