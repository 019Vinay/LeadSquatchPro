import streamlit as st
import pandas as pd
from utils.tech_stack_finder import TechStackFinder
from utils.data_processor import DataProcessor

st.set_page_config(
    page_title="Tech Stack Finder",
    page_icon="🔍",
    layout="wide"
)

# Enhanced CSS for consistency with main page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .page-header {
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #10b981 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 
            0 25px 50px rgba(139, 92, 246, 0.4),
            0 0 100px rgba(6, 182, 212, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        transform: perspective(1000px) rotateX(3deg);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .page-header::before {
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
    
    .page-header:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-10px) scale(1.02);
        box-shadow: 
            0 35px 70px rgba(139, 92, 246, 0.6),
            0 0 150px rgba(6, 182, 212, 0.5);
    }
    
    .page-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-align: center;
        margin: 0;
        font-size: 2.8rem;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.5),
            0 0 40px rgba(139, 92, 246, 0.8),
            0 0 80px rgba(6, 182, 212, 0.6);
        position: relative;
        z-index: 1;
    }
    
    .tech-button {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        border: none;
        border-radius: 12px;
        color: white;
        padding: 8px 16px;
        margin: 4px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .tech-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.5);
    }
    
    .search-container {
        background: linear-gradient(145deg, #1a1b3a 0%, #2d1b69 100%);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.7),
            0 0 0 1px rgba(139, 92, 246, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin: 1.5rem 0;
    }
    
    .verification-card {
        background: rgba(26, 27, 58, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(139, 92, 246, 0.3);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(255,255,255,0.1);
    }
    
    /* Enhanced visibility for all content */
    .stMarkdown, .stText, .stMarkdown p, .stText p {
        color: #f1f5f9 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #f8fafc !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }
    
    /* Form inputs with enhanced visibility */
    .stTextInput > div > div > input {
        background-color: rgba(15, 15, 35, 0.9) !important;
        color: #f1f5f9 !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 10px !important;
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
    
    /* Labels and help text */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: rgba(26, 27, 58, 0.9) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 15px !important;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(26, 27, 58, 0.9) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>🔍 Tech Stack Finder</h1>
    <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
        Discover companies using specific technologies
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize components
if 'tech_finder' not in st.session_state:
    st.session_state.tech_finder = TechStackFinder()

if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Input section with enhanced styling
st.markdown('<div class="search-container">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    technology = st.text_input(
        "Technology to search for",
        placeholder="e.g., Shopify, React, WordPress, Django",
        help="Enter the technology stack you want to find companies using"
    )

with col2:
    limit = st.number_input(
        "Number of companies",
        min_value=1,
        max_value=50,
        value=10,
        help="How many companies to find"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Popular technology suggestions
st.markdown("**Popular technologies:**")
col1, col2, col3, col4 = st.columns(4)

popular_techs = [
    "Shopify", "React", "WordPress", "Django",
    "Vue.js", "Angular", "Next.js", "Rails",
    "Laravel", "Flask", "Magento", "WooCommerce"
]

for i, tech in enumerate(popular_techs):
    col = [col1, col2, col3, col4][i % 4]
    with col:
        if st.button(tech, key=f"tech_{i}"):
            st.session_state.selected_tech = tech
            st.rerun()

# Use selected technology if clicked
if hasattr(st.session_state, 'selected_tech'):
    technology = st.session_state.selected_tech
    # Clear the selection
    if 'selected_tech' in st.session_state:
        del st.session_state.selected_tech

# Search functionality
if st.button("🔍 Find Companies", type="primary", disabled=not technology):
    if technology:
        with st.spinner(f"Searching for companies using {technology}..."):
            try:
                # Find companies
                results = st.session_state.tech_finder.find_by_technology(technology, limit)
                
                if results:
                    st.success(f"Found {len(results)} companies using {technology}")
                    
                    # Display results
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    
                    # Add to leads database
                    st.session_state.data_processor.add_tech_stack_data(results)
                    
                    # Verification section
                    st.markdown("---")
                    st.subheader("🔬 Technology Verification")
                    
                    verify_col1, verify_col2 = st.columns([1, 1])
                    
                    with verify_col1:
                        st.info("**Verification Status**")
                        verification_results = []
                        
                        # Verify a few companies
                        for i, company in enumerate(results[:3]):  # Verify first 3
                            with st.spinner(f"Verifying {company['company_name']}..."):
                                is_verified = st.session_state.tech_finder.verify_technology(
                                    company['domain'], 
                                    technology
                                )
                                verification_results.append({
                                    'Company': company['company_name'],
                                    'Domain': company['domain'],
                                    'Verified': '✅' if is_verified else '❌'
                                })
                        
                        if verification_results:
                            verification_df = pd.DataFrame(verification_results)
                            st.dataframe(verification_df, use_container_width=True)
                    
                    with verify_col2:
                        st.info("**Next Steps**")
                        st.write("""
                        1. **Email Extraction**: Go to the Email Extractor page to find contact emails
                        2. **Lead Enrichment**: Use the Lead Enrichment page to add company data
                        3. **Export**: Download your enriched leads as CSV
                        """)
                        
                        if st.button("➡️ Go to Email Extractor"):
                            st.switch_page("pages/2_Email_Extractor.py")
                
                else:
                    st.warning(f"No companies found using {technology}. Try a different technology or search term.")
                    
            except Exception as e:
                st.error(f"Error searching for companies: {str(e)}")
                st.info("Please try again with a different technology or check your internet connection.")

# Current leads preview
if not st.session_state.leads_data.empty:
    st.markdown("---")
    st.subheader("📊 Current Leads Database")
    
    # Filter current leads by technology
    tech_leads = st.session_state.leads_data[
        st.session_state.leads_data['tech_stack'].notna()
    ] if 'tech_stack' in st.session_state.leads_data.columns else pd.DataFrame()
    
    if not tech_leads.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(tech_leads, use_container_width=True)
        
        with col2:
            # Technology distribution
            if 'tech_stack' in tech_leads.columns:
                tech_counts = tech_leads['tech_stack'].value_counts()
                st.bar_chart(tech_counts)
                st.caption("Technology Distribution")
    else:
        st.info("No technology-based leads found yet. Search for companies above!")

# Help section
with st.expander("ℹ️ How to use Tech Stack Finder"):
    st.markdown("""
    ### Finding Companies by Technology
    
    1. **Enter a technology**: Type the name of the technology you want to search for
    2. **Set the limit**: Choose how many companies you want to find
    3. **Click search**: The system will search multiple sources for companies using that technology
    
    ### Technology Sources
    - GitHub repositories with live websites
    - Technology showcase directories
    - Public company directories
    - Technology-specific listings
    
    ### Verification
    The system attempts to verify that companies actually use the specified technology by:
    - Analyzing website source code
    - Looking for technology-specific patterns
    - Checking for framework signatures
    
    ### Next Steps
    Once you find companies, use the other modules to:
    - Extract professional emails
    - Enrich with company data
    - Export to CSV for your CRM
    """)
