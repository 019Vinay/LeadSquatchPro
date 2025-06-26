import streamlit as st
import pandas as pd
from utils.lead_enrichment import LeadEnrichment
from utils.data_processor import DataProcessor

st.set_page_config(
    page_title="Lead Enrichment",
    page_icon="📊",
    layout="wide"
)

# Enhanced CSS for lead enrichment page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .enrichment-header {
        background: linear-gradient(135deg, #06b6d4 0%, #10b981 50%, #f59e0b 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 
            0 25px 50px rgba(6, 182, 212, 0.4),
            0 0 100px rgba(16, 185, 129, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        transform: perspective(1000px) rotateX(3deg);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .enrichment-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }
    
    .enrichment-header:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-10px) scale(1.02);
        box-shadow: 
            0 35px 70px rgba(6, 182, 212, 0.6),
            0 0 150px rgba(16, 185, 129, 0.5);
    }
    
    .enrichment-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-align: center;
        margin: 0;
        font-size: 2.8rem;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.5),
            0 0 40px rgba(6, 182, 212, 0.8),
            0 0 80px rgba(16, 185, 129, 0.6);
        position: relative;
        z-index: 1;
    }
    
    .enrichment-card {
        background: linear-gradient(145deg, #ffffff, #f7fafc);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 3px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(168, 237, 234, 0.3);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .enrichment-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 10px 20px rgba(0,0,0,0.1);
    }
    
    .quality-score {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        color: white;
        text-align: center;
        min-width: 80px;
    }
    
    .score-high { background: linear-gradient(45deg, #22c55e, #16a34a); }
    .score-medium { background: linear-gradient(45deg, #f59e0b, #d97706); }
    .score-low { background: linear-gradient(45deg, #ef4444, #dc2626); }
    
    .data-field {
        background: rgba(168, 237, 234, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #a8edea;
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
    
    .stRadio > div {
        color: #f1f5f9 !important;
    }
    
    /* Labels and help text */
    .stSelectbox label, .stTextInput label, .stRadio label {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #06b6d4, #10b981) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.4) !important;
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
<div class="enrichment-header">
    <h1>📊 Lead Enrichment</h1>
    <p style="color: #4a5568; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
        Enhance leads with comprehensive company intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize components
if 'lead_enrichment' not in st.session_state:
    st.session_state.lead_enrichment = LeadEnrichment()

if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Method selection
st.subheader("Enrichment Method")
method = st.radio(
    "Choose enrichment method:",
    ["Enrich existing leads", "Enrich specific company"],
    horizontal=True
)

if method == "Enrich existing leads":
    # Show current leads
    if st.session_state.leads_data.empty:
        st.warning("No leads found. Please use Tech Stack Finder and Email Extractor first.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Go to Tech Stack Finder"):
                st.switch_page("pages/1_Tech_Stack_Finder.py")
        with col2:
            if st.button("📧 Go to Email Extractor"):
                st.switch_page("pages/2_Email_Extractor.py")
    else:
        # Show leads that can be enriched
        leads_to_enrich = st.session_state.leads_data[
            st.session_state.leads_data['domain'].notna()
        ].copy()
        
        # Check which leads need enrichment
        enrichment_fields = ['company_size', 'funding_status', 'linkedin_url', 'industry', 'location']
        needs_enrichment = pd.DataFrame()
        
        for field in enrichment_fields:
            if field not in leads_to_enrich.columns:
                leads_to_enrich[field] = None
        
        # Find leads that are missing enrichment data
        needs_enrichment = leads_to_enrich[
            leads_to_enrich[enrichment_fields].isna().any(axis=1) |
            (leads_to_enrich[enrichment_fields] == '').any(axis=1) |
            (leads_to_enrich[enrichment_fields] == 'Unknown').any(axis=1)
        ].copy()
        
        if needs_enrichment.empty:
            st.success("All leads are already enriched!")
            st.dataframe(leads_to_enrich, use_container_width=True)
        else:
            st.info(f"Found {len(needs_enrichment)} leads that can be enriched")
            
            # Show preview of leads to enrich
            preview_cols = ['company_name', 'domain', 'email']
            available_cols = [col for col in preview_cols if col in needs_enrichment.columns]
            st.dataframe(needs_enrichment[available_cols], use_container_width=True)
            
            # Enrichment controls
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                enrich_count = st.number_input(
                    "Number of leads to enrich",
                    min_value=1,
                    max_value=len(needs_enrichment),
                    value=min(3, len(needs_enrichment)),
                    help="Enrichment takes time, start with a few leads"
                )
            
            with col2:
                st.metric("Leads to enrich", len(needs_enrichment))
            
            with col3:
                enrichment_priority = st.selectbox(
                    "Enrichment priority",
                    ["High email scores first", "Random order", "Alphabetical"],
                    help="Order in which to enrich leads"
                )
            
            # Sort based on priority
            if enrichment_priority == "High email scores first" and 'email_score' in needs_enrichment.columns:
                needs_enrichment = needs_enrichment.sort_values('email_score', ascending=False)
            elif enrichment_priority == "Alphabetical" and 'company_name' in needs_enrichment.columns:
                needs_enrichment = needs_enrichment.sort_values('company_name')
            
            if st.button("📊 Enrich Leads", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_container = st.container()
                
                enrichment_results = []
                
                for i, (_, lead) in enumerate(needs_enrichment.head(enrich_count).iterrows()):
                    domain = lead['domain']
                    company_name = lead.get('company_name', 'Unknown')
                    
                    status_text.text(f"Enriching {company_name} ({domain})...")
                    progress_bar.progress((i + 1) / enrich_count)
                    
                    try:
                        enrichment_data = st.session_state.lead_enrichment.enrich_company(
                            domain, company_name
                        )
                        
                        # Update the lead in database
                        success = st.session_state.data_processor.add_enrichment_data(domain, enrichment_data)
                        
                        # Track results
                        result = {
                            'company_name': company_name,
                            'domain': domain,
                            'company_size': enrichment_data.get('company_size', 'Unknown'),
                            'industry': enrichment_data.get('industry', 'Unknown'),
                            'location': enrichment_data.get('location', 'Unknown'),
                            'funding_status': enrichment_data.get('funding_status', 'Unknown'),
                            'linkedin_url': enrichment_data.get('linkedin_url', 'Not found')
                        }
                        enrichment_results.append(result)
                        
                    except Exception as e:
                        st.error(f"Error enriching {domain}: {str(e)}")
                
                status_text.text("✅ Lead enrichment completed!")
                progress_bar.progress(1.0)
                
                # Show results
                if enrichment_results:
                    results_df = pd.DataFrame(enrichment_results)
                    
                    with results_container:
                        st.subheader("📊 Enrichment Results")
                        
                        # Summary metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            total_enriched = len(enrichment_results)
                            st.metric("Enriched", total_enriched)
                        
                        with col2:
                            companies_with_size = len([r for r in enrichment_results if r['company_size'] != 'Unknown'])
                            st.metric("Company Size Found", companies_with_size)
                        
                        with col3:
                            companies_with_linkedin = len([r for r in enrichment_results if r['linkedin_url'] != 'Not found'])
                            st.metric("LinkedIn Found", companies_with_linkedin)
                        
                        with col4:
                            companies_with_location = len([r for r in enrichment_results if r['location'] != 'Unknown'])
                            st.metric("Location Found", companies_with_location)
                        
                        # Detailed results
                        st.dataframe(results_df, use_container_width=True)

else:  # Enrich specific company
    st.subheader("Enrich Specific Company")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        domain_input = st.text_input(
            "Company domain",
            placeholder="example.com",
            help="Enter the company's domain"
        )
    
    with col2:
        company_name_input = st.text_input(
            "Company name (optional)",
            placeholder="Example Company",
            help="Company name helps with more accurate enrichment"
        )
    
    if st.button("📊 Enrich Company", type="primary", disabled=not domain_input):
        if domain_input:
            with st.spinner(f"Enriching {company_name_input or domain_input}..."):
                try:
                    enrichment_data = st.session_state.lead_enrichment.enrich_company(
                        domain_input, company_name_input
                    )
                    
                    # Display results in organized sections
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("🏢 Company Information")
                        
                        # Basic info
                        st.write("**Company Size:**", enrichment_data.get('company_size', 'Unknown'))
                        st.write("**Industry:**", enrichment_data.get('industry', 'Unknown'))
                        st.write("**Location:**", enrichment_data.get('location', 'Unknown'))
                        
                        if enrichment_data.get('founding_year'):
                            st.write("**Founded:**", enrichment_data['founding_year'])
                        
                        if enrichment_data.get('description'):
                            st.write("**Description:**")
                            st.write(enrichment_data['description'])
                    
                    with col2:
                        st.subheader("💰 Business Information")
                        
                        st.write("**Funding Status:**", enrichment_data.get('funding_status', 'Unknown'))
                        
                        if enrichment_data.get('employee_count'):
                            st.write("**Employee Count:**", enrichment_data['employee_count'])
                        
                        if enrichment_data.get('linkedin_url'):
                            st.write("**LinkedIn Profile:**")
                            st.link_button("View LinkedIn", enrichment_data['linkedin_url'])
                        else:
                            st.write("**LinkedIn Profile:** Not found")
                    
                    # Data quality assessment
                    st.markdown("---")
                    st.subheader("📈 Enrichment Quality Score")
                    
                    # Calculate enrichment score
                    fields_found = 0
                    total_fields = 6
                    
                    quality_data = [
                        ("Company Size", enrichment_data.get('company_size') not in [None, 'Unknown', '']),
                        ("Industry", enrichment_data.get('industry') not in [None, 'Unknown', '']),
                        ("Location", enrichment_data.get('location') not in [None, 'Unknown', '']),
                        ("Funding Status", enrichment_data.get('funding_status') not in [None, 'Unknown', '']),
                        ("LinkedIn Profile", enrichment_data.get('linkedin_url') not in [None, 'Not found', '']),
                        ("Description", enrichment_data.get('description') not in [None, '', 'Unknown'])
                    ]
                    
                    fields_found = sum(1 for _, found in quality_data if found)
                    quality_score = (fields_found / total_fields) * 100
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Quality Score", f"{quality_score:.0f}%")
                    
                    with col2:
                        st.metric("Fields Found", f"{fields_found}/{total_fields}")
                    
                    with col3:
                        quality_label = "High" if quality_score >= 70 else "Medium" if quality_score >= 40 else "Low"
                        st.metric("Quality Level", quality_label)
                    
                    # Detailed breakdown
                    st.subheader("📋 Data Completeness")
                    quality_df = pd.DataFrame(quality_data, columns=['Field', 'Found'])
                    quality_df['Status'] = quality_df['Found'].map({True: '✅ Found', False: '❌ Missing'})
                    st.dataframe(quality_df[['Field', 'Status']], use_container_width=True)
                    
                    # Add to leads option
                    if st.button("➕ Add to Leads Database"):
                        lead_data = [{
                            'company_name': company_name_input or st.session_state.lead_enrichment._extract_company_name_from_domain(domain_input),
                            'domain': domain_input,
                            **enrichment_data
                        }]
                        st.session_state.data_processor.add_tech_stack_data(lead_data)
                        st.success("Added to leads database!")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error enriching company: {str(e)}")

# Enrichment sources and methodology
st.markdown("---")
with st.expander("🔍 Enrichment Sources & Methodology"):
    st.markdown("""
    ### Data Sources
    
    **Company Website Analysis:**
    - About pages and company information sections
    - Team pages for employee count estimation
    - Contact pages for location information
    
    **LinkedIn Integration:**
    - Company profile discovery
    - Employee count verification
    - Industry classification
    
    **Public Business Data:**
    - Funding information from public sources
    - Company size classification
    - Industry categorization
    
    ### Data Points Collected
    
    **Company Demographics:**
    - Company size (Small, Medium, Large, Enterprise)
    - Employee count estimates
    - Geographic location
    - Industry classification
    
    **Business Intelligence:**
    - Funding status and history
    - LinkedIn company profile
    - Company description and mission
    - Founding year information
    
    ### Quality Assurance
    - Multiple source verification
    - Data freshness validation
    - Confidence scoring for each data point
    """)

# Current enriched leads overview
if not st.session_state.leads_data.empty:
    enriched_leads = st.session_state.leads_data.copy()
    
    # Check for enrichment data
    enrichment_cols = ['company_size', 'industry', 'location', 'funding_status', 'linkedin_url']
    has_enrichment = any(col in enriched_leads.columns for col in enrichment_cols)
    
    if has_enrichment:
        st.markdown("---")
        st.subheader("📊 Current Enriched Leads")
        
        # Show enrichment statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'company_size' in enriched_leads.columns:
                companies_with_size = len(enriched_leads[
                    enriched_leads['company_size'].notna() & 
                    (enriched_leads['company_size'] != 'Unknown')
                ])
                st.metric("With Company Size", companies_with_size)
        
        with col2:
            if 'industry' in enriched_leads.columns:
                companies_with_industry = len(enriched_leads[
                    enriched_leads['industry'].notna() & 
                    (enriched_leads['industry'] != 'Unknown')
                ])
                st.metric("With Industry", companies_with_industry)
        
        with col3:
            if 'location' in enriched_leads.columns:
                companies_with_location = len(enriched_leads[
                    enriched_leads['location'].notna() & 
                    (enriched_leads['location'] != 'Unknown')
                ])
                st.metric("With Location", companies_with_location)
        
        with col4:
            if 'linkedin_url' in enriched_leads.columns:
                companies_with_linkedin = len(enriched_leads[
                    enriched_leads['linkedin_url'].notna() & 
                    (enriched_leads['linkedin_url'] != 'Not found')
                ])
                st.metric("With LinkedIn", companies_with_linkedin)
        
        # Data table
        st.dataframe(enriched_leads, use_container_width=True)
        
        # Industry and size distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'industry' in enriched_leads.columns:
                industry_counts = enriched_leads['industry'].value_counts().head(10)
                if not industry_counts.empty:
                    st.subheader("🏭 Industry Distribution")
                    st.bar_chart(industry_counts)
        
        with col2:
            if 'company_size' in enriched_leads.columns:
                size_counts = enriched_leads['company_size'].value_counts()
                if not size_counts.empty:
                    st.subheader("📏 Company Size Distribution")
                    st.bar_chart(size_counts)
