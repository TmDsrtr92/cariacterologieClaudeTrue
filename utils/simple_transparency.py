"""
Simple transparency system using Streamlit's built-in components
"""
import streamlit as st
import time
from utils.transparency_system import ProcessingStage, STAGE_CONFIGS

def show_processing_status():
    """Show processing status using Streamlit's status component"""
    
    # Check if we should show transparency
    if not st.session_state.get('show_transparency', False):
        return None
    
    # Initialize completed stages tracking
    if 'completed_stages' not in st.session_state:
        st.session_state.completed_stages = []
    
    # Create status container
    status_container = st.status("🤖 Génération de la réponse en cours...", expanded=True)
    
    with status_container:
        # Create progress bar
        progress_bar = st.progress(0)
        
        # Create container for cumulative steps
        steps_text = st.empty()
        
        # Store these in session state for updates
        st.session_state.transparency_progress = progress_bar
        st.session_state.transparency_steps = steps_text
        st.session_state.transparency_container = status_container
        
    return status_container

def update_processing_status(stage: ProcessingStage):
    """Update the processing status"""
    if not st.session_state.get('show_transparency', False):
        return
    
    # Get stage info
    stage_info = STAGE_CONFIGS.get(stage, None)
    if not stage_info:
        return
    
    # Add current stage to completed stages (mark previous as completed)
    if 'current_stage' in st.session_state and st.session_state.current_stage not in st.session_state.get('completed_stages', []):
        if 'completed_stages' not in st.session_state:
            st.session_state.completed_stages = []
        st.session_state.completed_stages.append(st.session_state.current_stage)
    
    # Set new current stage
    st.session_state.current_stage = stage
    
    # Calculate progress
    stage_order = [
        ProcessingStage.QUESTION_PROCESSING,
        ProcessingStage.DOCUMENT_RETRIEVAL, 
        ProcessingStage.CONTEXT_GENERATION,
        ProcessingStage.RESPONSE_GENERATION,
        ProcessingStage.MEMORY_SAVING,
        ProcessingStage.COMPLETED
    ]
    
    if stage in stage_order:
        progress = (stage_order.index(stage) + 1) / len(stage_order)
    else:
        progress = 0
    
    # Update progress bar if available
    if 'transparency_progress' in st.session_state:
        try:
            st.session_state.transparency_progress.progress(progress)
        except:
            pass
    
    # Update steps display with cumulative list
    if 'transparency_steps' in st.session_state:
        try:
            # Build cumulative steps text
            steps_text = "**Étapes du traitement :**\n\n"
            
            # Show completed stages
            completed_stages = st.session_state.get('completed_stages', [])
            for completed_stage in completed_stages:
                if completed_stage in STAGE_CONFIGS:
                    completed_info = STAGE_CONFIGS[completed_stage]
                    steps_text += f"✅ {completed_info.icon} **{completed_info.name}** - Terminé\n\n"
            
            # Show current stage
            steps_text += f"🔄 {stage_info.icon} **{stage_info.name}** - {stage_info.user_message}\n\n"
            if stage_info.tooltip:
                steps_text += f"💡 *{stage_info.tooltip}*\n\n"
            
            # Update the display
            st.session_state.transparency_steps.markdown(steps_text)
        except:
            pass

def complete_processing_status():
    """Complete the processing status"""
    if not st.session_state.get('show_transparency', False):
        return
    
    # Update to completed
    if 'transparency_progress' in st.session_state:
        try:
            st.session_state.transparency_progress.progress(1.0)
        except:
            pass
    
    if 'transparency_status' in st.session_state:
        try:
            st.session_state.transparency_status.markdown(
                "**✅ Terminé**\n\nRéponse prête !"
            )
        except:
            pass
    
    if 'transparency_container' in st.session_state:
        try:
            # Update container to completed state
            st.session_state.transparency_container.update(
                label="✅ Réponse générée avec succès !",
                state="complete"
            )
        except:
            pass

def start_transparency():
    """Start transparency tracking"""
    st.session_state.show_transparency = True

def stop_transparency():
    """Stop transparency tracking"""
    st.session_state.show_transparency = False