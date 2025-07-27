"""
Streamlit-compatible transparency display component
"""
import streamlit as st
import time
from utils.transparency_system import ProcessingStage, STAGE_CONFIGS, get_transparency_manager

def render_transparency_status():
    """Render the transparency status if active"""
    # Check if transparency is active in session state
    if not st.session_state.get('transparency_active', False):
        return
    
    # Get current transparency state
    current_stage = st.session_state.get('transparency_stage', ProcessingStage.IDLE)
    completed_stages = st.session_state.get('transparency_completed', [])
    start_time = st.session_state.get('transparency_start_time', time.time())
    
    if current_stage == ProcessingStage.IDLE:
        return
    
    # Get stage info
    stage_info = STAGE_CONFIGS.get(current_stage)
    if not stage_info:
        return
    
    # Calculate progress and timing
    total_stages = len(STAGE_CONFIGS) - 1  # Exclude IDLE
    completed_count = len(completed_stages)
    progress_percent = (completed_count / total_stages) * 100
    elapsed_time = time.time() - start_time
    
    # Create a prominent status display at the top
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        color: white;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        animation: pulse 2s infinite;
    ">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
            <span style="font-size: 24px; margin-right: 10px; animation: bounce 1s infinite;">{stage_info.icon}</span>
            <div>
                <div style="font-weight: 600; font-size: 18px; margin-bottom: 5px;">
                    {stage_info.name}
                </div>
                <div style="font-size: 14px; opacity: 0.9;">
                    {stage_info.user_message}
                </div>
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <div style="
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
                margin-bottom: 8px;
            ">
                <div style="
                    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
                    height: 100%;
                    width: {progress_percent}%;
                    border-radius: 10px;
                    transition: width 0.5s ease;
                "></div>
            </div>
            <div style="font-size: 12px; opacity: 0.8;">
                Étape {completed_count + 1} sur {total_stages} • {elapsed_time:.1f}s écoulées
            </div>
        </div>
        
        <div style="font-size: 11px; opacity: 0.7; font-style: italic;">
            💡 {stage_info.tooltip[:80]}{'...' if len(stage_info.tooltip) > 80 else ''}
        </div>
    </div>
    
    <style>
        @keyframes pulse {{
            0% {{ box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3); }}
            50% {{ box-shadow: 0 4px 25px rgba(102, 126, 234, 0.5); }}
            100% {{ box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3); }}
        }}
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-5px); }}
            60% {{ transform: translateY(-3px); }}
        }}
    </style>
    """, unsafe_allow_html=True)

def start_transparency_display():
    """Start the transparency display"""
    st.session_state.transparency_active = True
    st.session_state.transparency_stage = ProcessingStage.IDLE
    st.session_state.transparency_completed = []
    st.session_state.transparency_start_time = time.time()

def update_transparency_stage(stage: ProcessingStage):
    """Update the current transparency stage"""
    if not st.session_state.get('transparency_active', False):
        return
    
    # Mark previous stage as completed
    current_stage = st.session_state.get('transparency_stage', ProcessingStage.IDLE)
    completed_stages = st.session_state.get('transparency_completed', [])
    
    if current_stage != ProcessingStage.IDLE and current_stage not in completed_stages:
        completed_stages.append(current_stage)
    
    # Update to new stage
    st.session_state.transparency_stage = stage
    st.session_state.transparency_completed = completed_stages
    
    # Force a rerun to show the update (but only if not already in the middle of one)
    try:
        if stage != ProcessingStage.COMPLETED:
            st.rerun()
    except:
        pass  # Ignore rerun errors during processing

def complete_transparency_display():
    """Complete the transparency display"""
    if not st.session_state.get('transparency_active', False):
        return
    
    # Mark current stage as completed
    current_stage = st.session_state.get('transparency_stage', ProcessingStage.IDLE)
    completed_stages = st.session_state.get('transparency_completed', [])
    
    if current_stage != ProcessingStage.IDLE and current_stage not in completed_stages:
        completed_stages.append(current_stage)
    
    # Set to completed
    st.session_state.transparency_stage = ProcessingStage.COMPLETED
    st.session_state.transparency_completed = completed_stages

def stop_transparency_display():
    """Stop the transparency display"""
    st.session_state.transparency_active = False