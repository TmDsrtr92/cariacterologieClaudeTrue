"""
Enhanced callback handlers with transparency system integration
"""
import time
from langchain.callbacks.base import BaseCallbackHandler
from utils.transparency_system import (
    start_document_retrieval,
    start_context_generation,
    start_response_generation,
    start_memory_saving,
    complete_transparency_tracking
)

class TransparentStreamlitCallbackHandler(BaseCallbackHandler):
    """Enhanced streaming handler with transparency integration"""
    
    def __init__(self, placeholder, update_every=3, delay=0.05):
        self.placeholder = placeholder
        self.text = ""
        self.counter = 0
        self.update_every = update_every
        self.delay = delay
        self.response_started = False
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        """Called when LLM starts - trigger response generation stage"""
        if not self.response_started:
            start_response_generation()
            self.response_started = True
    
    def on_llm_new_token(self, token, **kwargs):
        """Handle new token with streaming display"""
        self.text += token
        self.counter += 1
        if self.counter % self.update_every == 1:
            self.placeholder.markdown(self.text + "▌")
            time.sleep(self.delay)
    
    def on_llm_end(self, *args, **kwargs):
        """Handle LLM completion"""
        self.placeholder.markdown(self.text)
        # Note: Don't complete transparency here as memory saving still needs to happen

class TransparentRetrievalCallbackHandler(BaseCallbackHandler):
    """Enhanced retrieval handler with transparency integration"""
    
    def __init__(self, memory=None):
        self.memory = memory
        self.original_question = None
        self.retrieval_started = False
    
    def on_retriever_start(self, serialized, query, **kwargs):
        """Called when retrieval starts"""
        if not self.retrieval_started:
            start_document_retrieval()
            self.retrieval_started = True
        
        # Store the original question for comparison
        self.original_question = query
        
        print(f"\n🔍 RECHERCHE DE CHUNKS pour la question: '{query}'")
        print("=" * 80)
        
        # Display memory content if available
        if self.memory and hasattr(self.memory, 'memory') and hasattr(self.memory.memory, 'chat_memory'):
            chat_memory = self.memory.memory.chat_memory
            messages = chat_memory.messages
            
            if messages:
                print(f"\n💬 MÉMOIRE DE CONVERSATION ({len(messages)} messages):")
                print("=" * 80)
                for i, msg in enumerate(messages, 1):
                    role = "👤 Utilisateur" if msg.type == "human" else "🤖 Assistant"
                    print(f"\n{i}. {role}:")
                    print("-" * 40)
                    print(msg.content)
                    print("-" * 40)
                    print(f"📊 Longueur: {len(msg.content)} caractères")
                print("=" * 80)
            else:
                print("\n💬 MÉMOIRE DE CONVERSATION: (vide)")
        else:
            print("\n💬 MÉMOIRE DE CONVERSATION: (non disponible)")
    
    def on_retriever_end(self, documents, **kwargs):
        """Called when retrieval ends - start context generation"""
        start_context_generation()
        
        print(f"📄 {len(documents)} chunks récupérés:")
        print("-" * 80)
        for i, doc in enumerate(documents, 1):
            print(f"\n📄 Chunk {i}:")
            print(f"   Source: {getattr(doc.metadata, 'source', 'N/A')}")
            print(f"   Page: {getattr(doc.metadata, 'page', 'N/A')}")
            print(f"   Contenu: {doc.page_content[:200]}...")
            if len(doc.page_content) > 200:
                print(f"   (tronqué, longueur totale: {len(doc.page_content)} caractères)")
            print("-" * 40)
        print("=" * 80)
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        """Display the prompt used by the system"""
        print(f"\n🤖 PROMPT UTILISÉ PAR LE SYSTÈME:")
        print("=" * 80)
        
        # Search for prompt in inputs
        prompt_text = ""
        
        # Try different ways to get the prompt
        if "question" in inputs:
            question = inputs["question"]
            # If it's a simple string
            if isinstance(question, str):
                prompt_text = question
            # If it's a list of messages (chat format)
            elif isinstance(question, list) and len(question) > 0:
                # Take the last user message
                last_message = question[-1]
                if hasattr(last_message, 'content'):
                    prompt_text = last_message.content
                elif isinstance(last_message, dict) and 'content' in last_message:
                    prompt_text = last_message['content']
        
        # If not found in "question", look in other possible keys
        if not prompt_text:
            for key in ["input", "query", "text", "prompt"]:
                if key in inputs:
                    value = inputs[key]
                    if isinstance(value, str):
                        prompt_text = value
                        break
                    elif isinstance(value, list) and len(value) > 0:
                        last_item = value[-1]
                        if hasattr(last_item, 'content'):
                            prompt_text = last_item.content
                            break
                        elif isinstance(last_item, dict) and 'content' in last_item:
                            prompt_text = last_item['content']
                            break
        
        # Check if question was reformulated
        if self.original_question and prompt_text and prompt_text != self.original_question:
            print(f"⚠️  ATTENTION: Question reformulée!")
            print(f"   Question originale: '{self.original_question}'")
            print(f"   Question reformulée: '{prompt_text}'")
            print("-" * 40)
        
        # Display first 500 characters
        if prompt_text:
            truncated_prompt = prompt_text[:500]
            print(f"📝 Question utilisateur (500 premiers caractères):")
            print("-" * 40)
            print(truncated_prompt)
            if len(prompt_text) > 500:
                print(f"... (tronqué, longueur totale: {len(prompt_text)} caractères)")
            print("-" * 40)
        else:
            print("❌ Impossible de récupérer le prompt")
            print("🔍 Clés disponibles dans inputs:", list(inputs.keys()) if inputs else "Aucune")
        
        print("=" * 80)
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        """Display the complete system prompt used by the LLM"""
        print(f"\n🤖 PROMPT SYSTÈME COMPLET UTILISÉ PAR LE LLM:")
        print("=" * 80)
        
        if prompts and len(prompts) > 0:
            # First prompt generally contains the complete system prompt
            system_prompt = prompts[0]
            
            # Display first 1000 characters of system prompt
            truncated_system = system_prompt[:1000]
            print(f"📝 Prompt système (1000 premiers caractères):")
            print("-" * 40)
            print(truncated_system)
            if len(system_prompt) > 1000:
                print(f"... (tronqué, longueur totale: {len(system_prompt)} caractères)")
            print("-" * 40)
            
            # If there are multiple prompts, show the count
            if len(prompts) > 1:
                print(f"📊 Nombre total de prompts: {len(prompts)}")
        else:
            print("❌ Aucun prompt système trouvé")
        
        print("=" * 80)

class TransparentMemoryCallbackHandler(BaseCallbackHandler):
    """Callback handler to track memory operations"""
    
    def __init__(self):
        self.memory_operations_started = False
    
    def on_chain_end(self, outputs, **kwargs):
        """Called when a chain ends - trigger memory saving if not started"""
        if not self.memory_operations_started:
            start_memory_saving()
            self.memory_operations_started = True
    
    def on_memory_save_complete(self):
        """Custom method to call when memory save is complete"""
        complete_transparency_tracking()