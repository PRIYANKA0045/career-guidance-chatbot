import streamlit as st
import pandas as pd
import numpy as np
from chatbot_logic import CareerChatbot

# Page configuration
st.set_page_config(
    page_title="AI Career Guidance Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern visual styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Apply font to all text elements */
html, body, [data-testid="stAppViewContainer"], .stMarkdown {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Background overlay gradient matching theme */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 50% 50%, #0f172a 0%, #030712 100%) !important;
}

/* Main title styling */
.welcome-title {
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
    letter-spacing: -0.02em;
}

.welcome-subtitle {
    font-size: 1.15rem;
    text-align: center;
    color: #9ca3af;
    max-width: 700px;
    margin: 0 auto 35px auto;
    line-height: 1.6;
}

/* Chat bubble styling for the agent */
.chat-bubble-agent {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 16px 16px 16px 4px;
    padding: 24px;
    color: #e5e7eb;
    font-size: 1.15rem;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    line-height: 1.6;
}

/* Feature cards in welcome screen */
.info-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    height: 100%;
}

.info-card h4 {
    color: #818cf8;
    margin-bottom: 8px;
    font-weight: 700;
}

/* Results styles */
.result-header {
    text-align: center;
    padding: 10px 0 30px 0;
}

.result-category {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}


.role-card {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 12px;
    font-weight: 500;
    color: #e5e7eb;
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 4px;
}

.badge-skill {
    background: rgba(168, 85, 247, 0.15);
    color: #e9d5ff;
    border: 1px solid rgba(168, 85, 247, 0.3);
}

.timeline-item {
    border-left: 2px solid rgba(99, 102, 241, 0.3);
    padding-left: 20px;
    margin-left: 10px;
    padding-bottom: 20px;
    position: relative;
}

.timeline-item::before {
    content: '';
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #6366f1;
    position: absolute;
    left: -6px;
    top: 6px;
    box-shadow: 0 0 8px #6366f1;
}

.timeline-num {
    font-weight: 800;
    color: #818cf8;
    margin-right: 5px;
}

/* Custom styled buttons overrides */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    color: white !important;
    border: none !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100%;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4) !important;
}

div.stButton > button:first-child:active {
    transform: translateY(0px) !important;
}

/* Alternative style for restart button */
.restart-btn div.stButton > button:first-child {
    background: transparent !important;
    color: #9ca3af !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: none !important;
    padding: 10px 20px !important;
    font-size: 0.95rem !important;
}

.restart-btn div.stButton > button:first-child:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    color: white !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize chatbot engine
@st.cache_resource
def get_chatbot():
    return CareerChatbot()

chatbot = get_chatbot()

# Initialize session state variables
if "started" not in st.session_state:
    st.session_state.started = False
if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = chatbot.get_initial_state()

# Reload model in case it just finished training
if st.session_state.quiz_state["completed"] and chatbot.model is None:
    chatbot.reload_model()

# Welcome / Start Screen
if not st.session_state.started:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='welcome-title'>AI-Powered Career Guidance</h1>", unsafe_allow_html=True)
    st.markdown("""
<div style="display:flex; justify-content:center;">
    <p class='welcome-subtitle'>
        Discover your ideal career path through an adaptive dialogue analyzed in real-time by a Random Forest machine learning model.
    </p>
</div>
""", unsafe_allow_html=True)      
    # 3-Column Info cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h4>🔄 Adaptive Questions</h4>
            <p style='color: #9ca3af; font-size: 0.95rem; line-height: 1.5;'>The chatbot structures the questionnaire dynamically, focusing on your areas of highest interest based on your initial answers.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='info-card'>
            <h4>🌳 Machine Learning</h4>
            <p style='color: #9ca3af; font-size: 0.95rem; line-height: 1.5;'>We compute a 10-dimensional trait vector from your choices, processed through a Random Forest Classifier to identify optimal career matches.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='info-card'>
            <h4>💼 Rich Pathways</h4>
            <p style='color: #9ca3af; font-size: 0.95rem; line-height: 1.5;'>Get clear recommendations including specific job roles, required technical and soft skills, and a structured learning timeline.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # Start button
    left, center, right = st.columns([3, 2, 3])

    with center:
        if st.button("Begin Assessment", use_container_width=True):
            st.session_state.started = True
            st.session_state.quiz_state = chatbot.get_initial_state()
            st.rerun()

# Quiz Question Screen
elif not st.session_state.quiz_state["completed"]:
    state = st.session_state.quiz_state
    current_q_id = state["current_question_id"]
    
    # Check if question exists in bank
    if current_q_id in chatbot.questions:
        q_data = chatbot.questions[current_q_id]
        
        # Center card container
        _, main_col, _ = st.columns([1, 4, 1])
        
        with main_col:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            # Progress bar
            progress_val = float(state["question_count"]) / 10.0
            st.progress(progress_val)
            st.markdown(f"<p style='text-align: right; color: #6366f1; font-weight: 600; font-size: 0.95rem;'>Question {state['question_count'] + 1} of 10</p>", unsafe_allow_html=True)
            
            # Chat question bubble
            st.markdown(f"""
            <div class='chat-bubble-agent'>
                <span style='font-size: 0.85rem; color: #818cf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 6px;'>Career Counselor AI</span>
                {q_data['text']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<p style='color: #9ca3af; font-size: 0.9rem; margin-bottom: 15px; font-weight: 500;'>Choose the response that resonates most with you:</p>", unsafe_allow_html=True)
            
            # Options as vertical buttons
            for i, opt in enumerate(q_data["options"]):
                if st.button(opt["text"], key=f"opt_{current_q_id}_{i}"):
                    # Process response and update session state
                    updated_state = chatbot.process_answer(state, i)
                    st.session_state.quiz_state = updated_state
                    st.rerun()
                    
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
            
            # Cancel / restart button
            st.markdown("<div class='restart-btn'>", unsafe_allow_html=True)
            if st.button("Reset Assessment", key="quiz_reset"):
                st.session_state.started = False
                st.session_state.quiz_state = chatbot.get_initial_state()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Fallback if ID is invalid
        st.session_state.quiz_state["completed"] = True
        st.rerun()

# Results / Dashboard Screen
else:
    state = st.session_state.quiz_state
    
    # Reload model to ensure latest trained model is active
    chatbot.reload_model()
    
    # Get predictions
    career_probs = chatbot.predict_careers(state["trait_scores"])
    
    top_career = career_probs[0][0]
    top_confidence = career_probs[0][1]
    
    top_details = chatbot.get_career_details(top_career)
    
    # Header Banner
    st.markdown("<div class='result-header'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; color: #9ca3af; font-weight: 600; margin-bottom: 0;'>RECOMMENDED CAREER PATH</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='result-category'>{top_career}</h1>", unsafe_allow_html=True)
    
    # Confidence Badge
    conf_pct = int(top_confidence * 100)
    # If the model is rule-based, show default or calculated strength indicator
    conf_text = f"{conf_pct}% Match Score" if chatbot.model is not None else "Match Category"
    st.markdown(f"<p style='font-size: 1.2rem; color: #a5b4fc; font-weight: 700; margin-top: 0;'>✨ {conf_text}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2 Column layout: Left = Recommended details, Right = Trait charts and alternatives
    left_col, right_col = st.columns([5, 4])
    
    with left_col:
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Career Field Overview", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 1.05rem; line-height: 1.7; color: #d1d5db; margin-bottom: 25px;'>{top_details['description']}</p>", unsafe_allow_html=True)
        
        # Job roles
        st.markdown("### 💼 Specific Job Roles", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 0.9rem; margin-top: -10px; margin-bottom: 15px;'>Common career entry points and professional titles in this field:</p>", unsafe_allow_html=True)
        
        # Render roles in 2 columns
        r_cols = st.columns(2)
        for idx, role in enumerate(top_details["roles"]):
            col_target = r_cols[idx % 2]
            with col_target:
                st.markdown(f"<div class='role-card'>💼 {role}</div>", unsafe_allow_html=True)
                
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        # Skills
        st.markdown("### 🛠️ Required Core Skills", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 0.9rem; margin-top: -10px; margin-bottom: 15px;'>Technical tools, soft skills, and domains you should master:</p>", unsafe_allow_html=True)
        for skill in top_details["skills"]:
            st.markdown(f"<span class='badge badge-skill'>{skill}</span>", unsafe_allow_html=True)
            
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        
        # Learning Path
        st.markdown("### 🗺️ Recommended Learning Path", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 0.9rem; margin-top: -10px; margin-bottom: 20px;'>Step-by-step roadmap to start your professional journey:</p>", unsafe_allow_html=True)
        for idx, step in enumerate(top_details["learning_path"]):
            st.markdown(f"""
            <div class='timeline-item'>
                <span class='timeline-num'>Step {idx + 1}:</span> {step}
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    with right_col:
        # Trait Analysis Chart
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Your Interest Profile", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 0.9rem; margin-top: -10px; margin-bottom: 15px;'>Detailed breakdown of your accumulated trait scores:</p>", unsafe_allow_html=True)
        
        # Map trait database names to human-readable labels
        trait_labels = {
            "trait_coding_logic": "Coding & Logic",
            "trait_visual_creativity": "Visual Design",
            "trait_math_analytical": "Mathematics & Data",
            "trait_leadership_strategy": "Leadership & Strategy",
            "trait_physical_mechanical": "Physical & Mechanical",
            "trait_empathy_caregiving": "Empathy & Caregiving",
            "trait_writing_argument": "Writing & Policy",
            "trait_teaching_mentoring": "Teaching & Mentoring",
            "trait_scientific_inquiry": "Scientific Research",
            "trait_risk_operations": "Business Operations"
        }
        
        # Prepare data for chart
        scores = state["trait_scores"]
        chart_data = []
        for db_name, label in trait_labels.items():
            chart_data.append({
                "Trait": label,
                "Score": scores.get(db_name, 0.0)
            })
            
        df_chart = pd.DataFrame(chart_data).sort_values(by="Score", ascending=True)
        
        # Render bar chart
        st.bar_chart(
            data=df_chart,
            x="Trait",
            y="Score",
            horizontal=True,
            color="#6366f1"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Alternative career recommendations
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown("### 🔄 Alternative Career Options", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 0.9rem; margin-top: -10px; margin-bottom: 20px;'>Other areas that strongly align with your profile:</p>", unsafe_allow_html=True)
        
        # Render top alternatives (indices 1 and 2 in probabilities)
        for idx in range(1, min(3, len(career_probs))):
            alt_name, alt_prob = career_probs[idx]
            alt_pct = int(alt_prob * 100)
            alt_details = chatbot.get_career_details(alt_name)
            
            label_text = f"{alt_name} ({alt_pct}% Match)" if chatbot.model is not None else alt_name
            
            with st.expander(f"✨ {label_text}"):
                st.markdown(f"<p style='color: #d1d5db; font-size: 0.95rem; line-height: 1.5;'>{alt_details['description']}</p>", unsafe_allow_html=True)
                
                # Subheading for roles
                st.markdown("**Common Roles:**")
                st.markdown(", ".join(alt_details["roles"]))
                
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                
                # Subheading for skills
                st.markdown("**Core Skills:**")
                skills_html = "".join([f"<span class='badge badge-skill' style='padding: 3px 8px; font-size: 0.75rem; margin: 2px;'>{s}</span>" for s in alt_details["skills"]])
                st.markdown(skills_html, unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)

    # Reset button at bottom
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    _, reset_col, _ = st.columns([1, 1, 1])
    with reset_col:
        st.markdown("<div class='restart-btn'>", unsafe_allow_html=True)
        if st.button("Start New Assessment", key="restart_assessment"):
            st.session_state.started = False
            st.session_state.quiz_state = chatbot.get_initial_state()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
