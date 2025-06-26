import streamlit as st
import pandas as pd
from utils.data_processor import DataProcessor

# Initialize session state
if 'leads_data' not in st.session_state:
    st.session_state.leads_data = pd.DataFrame()

if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Page configuration
st.set_page_config(
    page_title="B2B Lead Generation Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with stunning 3D effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Dark base styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1b3a 50%, #2d1b69 100%);
        background-attachment: fixed;
        color: #f1f5f9 !important;
    }
    
    /* Global text color overrides */
    * {
        color: #f1f5f9 !important;
    }
    
    .main .block-container {
        color: #f1f5f9 !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 50%, #f59e0b 100%);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 
            0 25px 50px rgba(139, 92, 246, 0.4),
            0 0 100px rgba(236, 72, 153, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        transform: perspective(1000px) rotateX(3deg);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-header:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-10px) scale(1.02);
        box-shadow: 
            0 35px 70px rgba(139, 92, 246, 0.6),
            0 0 150px rgba(236, 72, 153, 0.5);
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-align: center;
        margin: 0;
        font-size: 3.5rem;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.5),
            0 0 40px rgba(139, 92, 246, 0.8),
            0 0 80px rgba(236, 72, 153, 0.6);
        animation: glow 3s ease-in-out infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    @keyframes glow {
        from { 
            text-shadow: 
                0 0 20px rgba(255,255,255,0.5),
                0 0 40px rgba(139, 92, 246, 0.8),
                0 0 80px rgba(236, 72, 153, 0.6);
        }
        to { 
            text-shadow: 
                0 0 30px rgba(255,255,255,0.8),
                0 0 60px rgba(139, 92, 246, 1),
                0 0 120px rgba(236, 72, 153, 0.9);
        }
    }
    
    .metric-card {
        background: linear-gradient(145deg, #1e1e3f 0%, #2a2d5f 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.6),
            0 0 0 1px rgba(139, 92, 246, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 2px solid transparent;
        background-clip: padding-box;
        transition: all 0.4s ease;
        transform: translateZ(0);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #8b5cf6, #ec4899, #f59e0b, #8b5cf6);
        background-size: 300% 300%;
        border-radius: 20px;
        z-index: -1;
        animation: gradientShift 4s ease infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover::before {
        opacity: 0.8;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05) rotateX(10deg);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.8),
            0 0 60px rgba(139, 92, 246, 0.6);
        border-color: rgba(139, 92, 246, 0.8);
    }
    
    .feature-card {
        background: linear-gradient(145deg, #1a1b3a 0%, #2d1b69 100%);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.7),
            0 0 0 1px rgba(139, 92, 246, 0.2),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #8b5cf6, #ec4899, #f59e0b, #06b6d4, #8b5cf6);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .feature-card:hover {
        transform: translateY(-15px) rotateX(8deg) scale(1.02);
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.9),
            0 0 80px rgba(139, 92, 246, 0.4);
        border-color: rgba(139, 92, 246, 0.8);
    }
    
    .feature-card h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .feature-card ul li {
        color: #cbd5e1 !important;
        margin: 0.5rem 0;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .glass-panel {
        background: rgba(26, 27, 58, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(255,255,255,0.1);
        padding: 2.5rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .glass-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        border-radius: 25px;
        z-index: -1;
    }
    
    .floating-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
        animation: float 4s ease-in-out infinite;
        text-shadow: 
            0 0 20px rgba(139, 92, 246, 0.8),
            0 0 40px rgba(236, 72, 153, 0.6);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-15px) rotate(2deg); }
        50% { transform: translateY(-10px) rotate(0deg); }
        75% { transform: translateY(-20px) rotate(-2deg); }
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        text-shadow: none;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .data-table {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.6),
            0 0 0 1px rgba(139, 92, 246, 0.3);
        border: 1px solid rgba(139, 92, 246, 0.2);
        background: rgba(26, 27, 58, 0.8);
    }
    
    /* Custom dark scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 35, 0.8);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c3aed, #db2777);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.8);
    }
    
    /* Dark sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1b3a 0%, #2d1b69 100%);
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: 
            0 8px 25px rgba(139, 92, 246, 0.4),
            0 0 0 1px rgba(139, 92, 246, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 15px 35px rgba(139, 92, 246, 0.6),
            0 0 40px rgba(236, 72, 153, 0.5);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Enhanced text visibility */
    .stMarkdown, .stText, .stMarkdown p, .stText p {
        color: #f1f5f9 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #f8fafc !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }
    
    /* Metric card content styling */
    .metric-card h3 {
        color: #f1f5f9 !important;
        margin-bottom: 0.5rem;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }
    
    .metric-card div[style*="font-size: 2.5rem"] {
        color: #cbd5e1 !important;
        text-shadow: 0 0 20px rgba(139, 92, 246, 0.8);
        font-weight: 700;
    }
    
    /* Form inputs styling for better visibility */
    .stTextInput > div > div > input {
        background-color: rgba(15, 15, 35, 0.9) !important;
        color: #f1f5f9 !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(139, 92, 246, 1) !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3) !important;
    }
    
    .stSelectbox > div > div > select {
        background-color: rgba(15, 15, 35, 0.9) !important;
        color: #f1f5f9 !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 10px !important;
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(15, 15, 35, 0.9) !important;
        color: #f1f5f9 !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 10px !important;
    }
    
    /* Radio button styling */
    .stRadio > div {
        color: #f1f5f9 !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > div {
        color: #f1f5f9 !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        color: #f1f5f9 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1b3a 0%, #2d1b69 100%) !important;
    }
    
    .css-1d391kg .stMarkdown {
        color: #f1f5f9 !important;
    }
    
    /* Button text styling */
    .stButton > button {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: rgba(26, 27, 58, 0.9) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 15px !important;
    }
    
    /* Info, warning, error boxes */
    .stAlert {
        background: rgba(26, 27, 58, 0.9) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        color: #f1f5f9 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(26, 27, 58, 0.8) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 27, 58, 0.6) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #8b5cf6, #ec4899) !important;
    }
    
    /* Metric value styling */
    .metric-value {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(139, 92, 246, 0.6) !important;
    }
    
    /* Labels and help text */
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox .help, .stTextInput .help, .stNumberInput .help {
        color: #cbd5e1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main page with 3D header
st.markdown("""
<div class="main-header">
    <h1>🎯 B2B Lead Generation Platform</h1>
</div>
""", unsafe_allow_html=True)

# Overview with 3D metric cards
st.markdown('<div class="stats-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="floating-icon">📊</div>
        <h3 class="gradient-text">Total Leads</h3>
        <div style="font-size: 2.5rem; font-weight: 700; color: #2d3748;">{}</div>
    </div>
    """.format(len(st.session_state.leads_data)), unsafe_allow_html=True)

with col2:
    if not st.session_state.leads_data.empty and 'email_score' in st.session_state.leads_data.columns:
        high_quality = len(st.session_state.leads_data[st.session_state.leads_data['email_score'] >= 80])
    else:
        high_quality = 0
    
    st.markdown("""
    <div class="metric-card">
        <div class="floating-icon">⭐</div>
        <h3 class="gradient-text">High Quality</h3>
        <div style="font-size: 2.5rem; font-weight: 700; color: #2d3748;">{}</div>
    </div>
    """.format(high_quality), unsafe_allow_html=True)

with col3:
    if not st.session_state.leads_data.empty and 'company_name' in st.session_state.leads_data.columns:
        unique_companies = st.session_state.leads_data['company_name'].nunique()
    else:
        unique_companies = 0
    
    st.markdown("""
    <div class="metric-card">
        <div class="floating-icon">🏢</div>
        <h3 class="gradient-text">Companies</h3>
        <div style="font-size: 2.5rem; font-weight: 700; color: #2d3748;">{}</div>
    </div>
    """.format(unique_companies), unsafe_allow_html=True)

with col4:
    if not st.session_state.leads_data.empty and 'funding_status' in st.session_state.leads_data.columns:
        funded_companies = len(st.session_state.leads_data[
            st.session_state.leads_data['funding_status'].notna() & 
            (st.session_state.leads_data['funding_status'] != 'Unknown')
        ])
    else:
        funded_companies = 0
    
    st.markdown("""
    <div class="metric-card">
        <div class="floating-icon">💰</div>
        <h3 class="gradient-text">Funded</h3>
        <div style="font-size: 2.5rem; font-weight: 700; color: #2d3748;">{}</div>
    </div>
    """.format(funded_companies), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Platform Features with 3D cards
st.markdown("## Platform Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="floating-icon">🔍</div>
        <h3>Tech Stack Finder</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6; color: #4a5568;">
            <li>Find companies using specific technologies (Shopify, React, WordPress)</li>
            <li>Filter by technology stack and company characteristics</li>
            <li>Discover potential clients based on their tech choices</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="floating-icon">📧</div>
        <h3>Email Extractor & Scorer</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6; color: #4a5568;">
            <li>Extract professional emails from company websites</li>
            <li>Intelligent scoring system (CEO > Info@ emails)</li>
            <li>Email validation with MX record checking</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="floating-icon">📊</div>
        <h3>Lead Enrichment</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6; color: #4a5568;">
            <li>Enrich leads with company data from public sources</li>
            <li>Find funding information and company size</li>
            <li>Locate decision-maker LinkedIn profiles</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="floating-icon">📁</div>
        <h3>CSV Export</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6; color: #4a5568;">
            <li>Export all enriched leads to CSV format</li>
            <li>Combine data from all modules</li>
            <li>Ready for CRM import</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Current Data Preview with glass panel effect
if not st.session_state.leads_data.empty:
    st.markdown("""
    <div class="glass-panel">
        <h2 class="gradient-text" style="text-align: center; margin-bottom: 1.5rem;">Current Leads Database</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.dataframe(st.session_state.leads_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick actions with enhanced buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Clear All Data", type="secondary"):
            st.session_state.leads_data = pd.DataFrame()
            st.rerun()
    
    with col2:
        if st.button("📈 Sort by Score", type="secondary"):
            if 'email_score' in st.session_state.leads_data.columns:
                st.session_state.leads_data = st.session_state.leads_data.sort_values(
                    'email_score', ascending=False
                )
                st.rerun()
    
    with col3:
        csv_data = st.session_state.leads_data.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name="leads_data.csv",
            mime="text/csv"
        )
else:
    st.markdown("""
    <div class="glass-panel" style="text-align: center;">
        <div class="floating-icon" style="font-size: 4rem;">🚀</div>
        <h3 class="gradient-text">Ready to Generate Leads?</h3>
        <p style="font-size: 1.2rem; color: #4a5568; margin-top: 1rem;">
            Use the sidebar to navigate to different modules and start building your lead database!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Instructions with enhanced styling
st.markdown("""
<div class="glass-panel">
    <h2 class="gradient-text" style="text-align: center; margin-bottom: 2rem;">Getting Started</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
        <div style="text-align: center; padding: 1rem;">
            <div class="floating-icon" style="font-size: 2.5rem;">🔍</div>
            <h4 style="color: #2d3748; margin: 0.5rem 0;">Tech Stack Finder</h4>
            <p style="color: #4a5568; font-size: 0.9rem;">Find companies using specific technologies</p>
        </div>
        <div style="text-align: center; padding: 1rem;">
            <div class="floating-icon" style="font-size: 2.5rem;">📧</div>
            <h4 style="color: #2d3748; margin: 0.5rem 0;">Email Extractor</h4>
            <p style="color: #4a5568; font-size: 0.9rem;">Extract and score professional emails</p>
        </div>
        <div style="text-align: center; padding: 1rem;">
            <div class="floating-icon" style="font-size: 2.5rem;">📊</div>
            <h4 style="color: #2d3748; margin: 0.5rem 0;">Lead Enrichment</h4>
            <p style="color: #4a5568; font-size: 0.9rem;">Add company data and insights</p>
        </div>
        <div style="text-align: center; padding: 1rem;">
            <div class="floating-icon" style="font-size: 2.5rem;">📁</div>
            <h4 style="color: #2d3748; margin: 0.5rem 0;">Export Leads</h4>
            <p style="color: #4a5568; font-size: 0.9rem;">Download enriched data</p>
        </div>
    </div>
    <p style="text-align: center; margin-top: 2rem; color: #4a5568; font-size: 1.1rem;">
        Navigate using the sidebar to access each module and build your lead database.
    </p>
</div>
""", unsafe_allow_html=True)
