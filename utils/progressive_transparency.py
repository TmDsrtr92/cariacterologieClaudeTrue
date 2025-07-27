"""
Progressive transparency system that shows all steps cumulatively
"""
import streamlit as st
import time
from utils.transparency_system import ProcessingStage, STAGE_CONFIGS

def show_progressive_status():
    """Show progressive status display using st.status()"""
    
    # Check if we should show transparency
    if not st.session_state.get('show_transparency', False):
        return None
    
    # Get current state
    current_stage = st.session_state.get('current_transparency_stage', ProcessingStage.QUESTION_PROCESSING)
    completed_stages = st.session_state.get('completed_transparency_stages', [])
    
    # Get current stage info
    stage_info = STAGE_CONFIGS.get(current_stage)
    if not stage_info:
        return None
    
    # Create main status container
    if current_stage == ProcessingStage.COMPLETED:
        status_container = st.status("✅ Réponse générée avec succès !", state="complete", expanded=True)
    else:
        status_container = st.status(f"🤖 {stage_info.user_message}", expanded=True)
    
    with status_container:
        # Show overall progress
        stage_order = [
            ProcessingStage.QUESTION_PROCESSING,
            ProcessingStage.DOCUMENT_RETRIEVAL, 
            ProcessingStage.CONTEXT_GENERATION,
            ProcessingStage.RESPONSE_GENERATION,
            ProcessingStage.MEMORY_SAVING
        ]
        
        current_index = stage_order.index(current_stage) if current_stage in stage_order else 0
        progress = (current_index + 1) / len(stage_order)
        st.progress(progress)
        
        st.markdown("**Étapes du traitement :**")
        
        # Show all completed stages plus current one
        for i, stage in enumerate(stage_order):
            stage_info = STAGE_CONFIGS.get(stage)
            if not stage_info:
                continue
            
            if stage in completed_stages:
                # Completed stage
                st.write(f"✅ {stage_info.icon} **{stage_info.name}** - Terminé")
            elif stage == current_stage:
                # Current stage
                st.write(f"🔄 {stage_info.icon} **{stage_info.name}** - {stage_info.user_message}")
                if stage_info.tooltip:
                    st.caption(f"💡 {stage_info.tooltip}")
            elif i < current_index:
                # Should be completed but not in list (fallback)
                st.write(f"✅ {stage_info.icon} **{stage_info.name}** - Terminé")
            else:
                # Future stages - don't show yet
                break
        
        # Show completion message
        if current_stage == ProcessingStage.COMPLETED:
            st.success("🎉 Toutes les étapes sont terminées !")
    
    return status_container

def update_progressive_status(stage: ProcessingStage):
    """Update progressive status by moving to next stage"""
    if not st.session_state.get('show_transparency', False):
        return
    
    # Mark previous stage as completed if it exists
    current_stage = st.session_state.get('current_transparency_stage')
    if current_stage and current_stage not in st.session_state.get('completed_transparency_stages', []):
        if 'completed_transparency_stages' not in st.session_state:
            st.session_state.completed_transparency_stages = []
        st.session_state.completed_transparency_stages.append(current_stage)
    
    # Set new current stage
    st.session_state.current_transparency_stage = stage

def complete_progressive_status():
    """Complete the progressive status"""
    if not st.session_state.get('show_transparency', False):
        return
    
    # Mark current stage as completed
    current_stage = st.session_state.get('current_transparency_stage')
    if current_stage and current_stage not in st.session_state.get('completed_transparency_stages', []):
        if 'completed_transparency_stages' not in st.session_state:
            st.session_state.completed_transparency_stages = []
        st.session_state.completed_transparency_stages.append(current_stage)
    
    # Set to completed
    st.session_state.current_transparency_stage = ProcessingStage.COMPLETED

def start_progressive_transparency():
    """Start progressive transparency tracking"""
    st.session_state.show_transparency = True
    st.session_state.completed_transparency_stages = []
    st.session_state.current_transparency_stage = ProcessingStage.QUESTION_PROCESSING

def stop_progressive_transparency():
    """Stop progressive transparency tracking"""
    st.session_state.show_transparency = False
    if 'completed_transparency_stages' in st.session_state:
        del st.session_state.completed_transparency_stages
    if 'current_transparency_stage' in st.session_state:
        del st.session_state.current_transparency_stage