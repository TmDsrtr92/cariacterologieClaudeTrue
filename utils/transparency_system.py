"""
Real-time transparency system for showing processing status during answer generation
"""
import streamlit as st
import time
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass
from threading import Lock

class ProcessingStage(Enum):
    """Processing stages for transparency display"""
    IDLE = "idle"
    QUESTION_PROCESSING = "question_processing"
    DOCUMENT_RETRIEVAL = "document_retrieval"
    CONTEXT_GENERATION = "context_generation"
    RESPONSE_GENERATION = "response_generation"
    MEMORY_SAVING = "memory_saving"
    COMPLETED = "completed"

@dataclass
class StageInfo:
    """Information about a processing stage"""
    name: str
    user_message: str
    icon: str
    estimated_duration: float = 2.0
    tooltip: str = ""

# Stage configurations with user-friendly messages
STAGE_CONFIGS = {
    ProcessingStage.QUESTION_PROCESSING: StageInfo(
        name="Analyse de votre question",
        user_message="Je comprends votre question...",
        icon="🤔",
        estimated_duration=1.0,
        tooltip="L'assistant analyse votre question et la contextualise avec l'historique de conversation"
    ),
    ProcessingStage.DOCUMENT_RETRIEVAL: StageInfo(
        name="Recherche dans la base de connaissances",
        user_message="Je cherche les informations pertinentes...",
        icon="🔍",
        estimated_duration=2.0,
        tooltip="Recherche des documents les plus pertinents dans la base de données de caractérologie"
    ),
    ProcessingStage.CONTEXT_GENERATION: StageInfo(
        name="Préparation du contexte",
        user_message="Je prépare les éléments de réponse...",
        icon="📚",
        estimated_duration=1.5,
        tooltip="Organisation des informations trouvées pour formuler une réponse cohérente"
    ),
    ProcessingStage.RESPONSE_GENERATION: StageInfo(
        name="Génération de la réponse",
        user_message="Je formule ma réponse...",
        icon="✍️",
        estimated_duration=3.0,
        tooltip="L'IA génère une réponse personnalisée basée sur les informations trouvées"
    ),
    ProcessingStage.MEMORY_SAVING: StageInfo(
        name="Sauvegarde de la conversation",
        user_message="Je mémorise notre échange...",
        icon="💾",
        estimated_duration=0.5,
        tooltip="Sauvegarde de la conversation pour maintenir le contexte lors des prochains échanges"
    ),
    ProcessingStage.COMPLETED: StageInfo(
        name="Terminé",
        user_message="Réponse prête !",
        icon="✅",
        estimated_duration=0.0,
        tooltip="Le traitement est terminé avec succès"
    )
}

class TransparencyManager:
    """Manager for the real-time transparency system"""
    
    def __init__(self):
        self.current_stage = ProcessingStage.IDLE
        self.stage_start_time = None
        self.total_start_time = None
        self.completed_stages = []
        self.container = None
        self.lock = Lock()
        
    def initialize_display(self):
        """Initialize the transparency display - will be rendered when needed"""
        # Don't create container here, we'll render directly when needed
        pass
    
    def start_processing(self):
        """Start the transparency tracking"""
        with self.lock:
            self.current_stage = ProcessingStage.IDLE
            self.total_start_time = time.time()
            self.completed_stages = []
            self.stage_start_time = None
    
    def set_stage(self, stage: ProcessingStage):
        """Set the current processing stage"""
        with self.lock:
            # Mark previous stage as completed if it exists
            if self.current_stage != ProcessingStage.IDLE and self.current_stage not in self.completed_stages:
                self.completed_stages.append(self.current_stage)
            
            self.current_stage = stage
            self.stage_start_time = time.time()
            
            # Update display
            self._update_display()
    
    def complete_processing(self):
        """Mark processing as completed"""
        with self.lock:
            # Mark current stage as completed
            if self.current_stage != ProcessingStage.IDLE and self.current_stage not in self.completed_stages:
                self.completed_stages.append(self.current_stage)
            
            self.current_stage = ProcessingStage.COMPLETED
            self._update_display()
    
    def _update_display(self):
        """Update the transparency display"""
        # Render the status card directly using session state
        if 'transparency_active' not in st.session_state:
            st.session_state.transparency_active = False
        
        if self.current_stage != ProcessingStage.IDLE:
            st.session_state.transparency_active = True
            st.session_state.transparency_stage = self.current_stage
            st.session_state.transparency_completed = self.completed_stages.copy()
            st.session_state.transparency_start_time = self.total_start_time
        
        # Force a rerun to show the updated status
        if st.session_state.transparency_active:
            self._render_status_card()
    
    def _render_status_card(self):
        """Render the floating status card"""
        if self.current_stage == ProcessingStage.IDLE:
            return
        
        # Calculate elapsed time
        elapsed_time = 0
        if self.total_start_time:
            elapsed_time = time.time() - self.total_start_time
        
        # Get current stage info
        current_info = STAGE_CONFIGS.get(self.current_stage)
        if not current_info:
            return
        
        # Create floating card HTML
        card_html = f"""
        <div style="
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            min-width: 300px;
            max-width: 350px;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            backdrop-filter: blur(10px);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 24px; margin-right: 10px;">{current_info.icon}</span>
                <div>
                    <div style="font-weight: 600; font-size: 16px; margin-bottom: 2px;">
                        {current_info.name}
                    </div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        {current_info.user_message}
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                {self._render_progress_bar()}
            </div>
            
            <div style="display: flex; justify-content: space-between; font-size: 12px; opacity: 0.8;">
                <span>Étape {len(self.completed_stages) + 1}/5</span>
                <span>{elapsed_time:.1f}s</span>
            </div>
            
            {self._render_completed_stages()}
        </div>
        """
        
        # Render the card
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Add tooltip functionality with enhanced details
        if current_info.tooltip:
            tooltip_html = f"""
            <div style="
                margin-top: 10px;
                padding: 8px 12px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                border-left: 3px solid #4facfe;
                font-size: 11px;
                opacity: 0.8;
                cursor: help;
            " title="{current_info.tooltip}">
                💡 {current_info.tooltip[:60]}{'...' if len(current_info.tooltip) > 60 else ''}
            </div>
            """
            st.markdown(tooltip_html, unsafe_allow_html=True)
    
    def _render_progress_bar(self) -> str:
        """Render progress bar HTML"""
        total_stages = len(STAGE_CONFIGS) - 1  # Exclude IDLE
        completed_count = len(self.completed_stages)
        current_progress = (completed_count / total_stages) * 100
        
        return f"""
        <div style="
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
                height: 100%;
                width: {current_progress}%;
                border-radius: 10px;
                transition: width 0.3s ease;
            "></div>
        </div>
        """
    
    def _render_completed_stages(self) -> str:
        """Render completed stages indicators"""
        if not self.completed_stages:
            return ""
        
        indicators = []
        for stage in self.completed_stages:
            stage_info = STAGE_CONFIGS.get(stage)
            if stage_info:
                indicators.append(f"""
                <span style="
                    display: inline-block;
                    margin: 2px;
                    padding: 2px 6px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    font-size: 10px;
                    opacity: 0.7;
                ">
                    {stage_info.icon} {stage_info.name}
                </span>
                """)
        
        if indicators:
            return f"""
            <div style="margin-top: 10px; font-size: 10px;">
                <div style="margin-bottom: 5px; opacity: 0.8;">Étapes terminées:</div>
                {''.join(indicators)}
            </div>
            """
        return ""

# Global transparency manager instance
_transparency_manager = None

def get_transparency_manager() -> TransparencyManager:
    """Get or create the global transparency manager"""
    global _transparency_manager
    if _transparency_manager is None:
        _transparency_manager = TransparencyManager()
    return _transparency_manager

def initialize_transparency_display() -> st.container:
    """Initialize the transparency display and return the container"""
    manager = get_transparency_manager()
    return manager.initialize_display()

def start_transparency_tracking():
    """Start tracking processing for transparency"""
    manager = get_transparency_manager()
    manager.start_processing()

def set_processing_stage(stage: ProcessingStage):
    """Set the current processing stage"""
    manager = get_transparency_manager()
    manager.set_stage(stage)

def complete_transparency_tracking():
    """Complete the transparency tracking"""
    manager = get_transparency_manager()
    manager.complete_processing()

# Convenience functions for each stage
def start_question_processing():
    """Convenience function to start question processing stage"""
    set_processing_stage(ProcessingStage.QUESTION_PROCESSING)

def start_document_retrieval():
    """Convenience function to start document retrieval stage"""
    set_processing_stage(ProcessingStage.DOCUMENT_RETRIEVAL)

def start_context_generation():
    """Convenience function to start context generation stage"""
    set_processing_stage(ProcessingStage.CONTEXT_GENERATION)

def start_response_generation():
    """Convenience function to start response generation stage"""
    set_processing_stage(ProcessingStage.RESPONSE_GENERATION)

def start_memory_saving():
    """Convenience function to start memory saving stage"""
    set_processing_stage(ProcessingStage.MEMORY_SAVING)