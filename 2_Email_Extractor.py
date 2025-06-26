import streamlit as st
import pandas as pd
from utils.email_extractor import EmailExtractor
from utils.data_processor import DataProcessor

st.set_page_config(
    page_title="Email Extractor",
    page_icon="📧",
    layout="wide"
)

# Enhanced CSS for email extractor page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .email-header {
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 50%, #06b6d4 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 
            0 25px 50px rgba(236, 72, 153, 0.4),
            0 0 100px rgba(139, 92, 246, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        transform: perspective(1000px) rotateX(3deg);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .email-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }
    
    .email-header:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-10px) scale(1.02);
        box-shadow: 
            0 35px 70px rgba(236, 72, 153, 0.6),
            0 0 150px rgba(139, 92, 246, 0.5);
    }
    
    .email-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-align: center;
        margin: 0;
        font-size: 2.8rem;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.5),
            0 0 40px rgba(236, 72, 153, 0.8),
            0 0 80px rgba(139, 92, 246, 0.6);
        position: relative;
        z-index: 1;
    }
    
    .email-score-card {
        background: linear-gradient(145deg, #f0f9ff, #ffffff);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 
            0 10px 20px rgba(79, 172, 254, 0.1),
            inset 0 1px 0 rgba(255,255,255,0.6);
        border: 2px solid rgba(79, 172, 254, 0.2);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .email-score-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(79, 172, 254, 0.15),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .score-high { border-left: 5px solid #22c55e; }
    .score-medium { border-left: 5px solid #f59e0b; }
    .score-low { border-left: 5px solid #ef4444; }
    
    .progress-container {
        background: rgba(79, 172, 254, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
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
        background: linear-gradient(45deg, #ec4899, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.4) !important;
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
<div class="email-header">
    <h1>📧 Email Extractor & Scorer</h1>
    <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
        Extract and score professional emails with intelligent ranking
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize components
if 'email_extractor' not in st.session_state:
    st.session_state.email_extractor = EmailExtractor()

if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Method selection
st.subheader("Extraction Method")
method = st.radio(
    "Choose extraction method:",
    ["Extract from existing leads", "Extract from specific domain"],
    horizontal=True
)

if method == "Extract from existing leads":
    # Show current leads without emails
    if st.session_state.leads_data.empty:
        st.warning("No leads found. Please use Tech Stack Finder first to generate leads.")
        if st.button("🔍 Go to Tech Stack Finder"):
            st.switch_page("pages/1_Tech_Stack_Finder.py")
    else:
        # Filter leads that don't have emails yet
        leads_without_emails = st.session_state.leads_data[
            st.session_state.leads_data['email'].isna() | 
            (st.session_state.leads_data['email'] == '')
        ].copy() if 'email' in st.session_state.leads_data.columns else st.session_state.leads_data.copy()
        
        if leads_without_emails.empty:
            st.success("All leads already have emails extracted!")
            st.dataframe(st.session_state.leads_data, use_container_width=True)
        else:
            st.info(f"Found {len(leads_without_emails)} leads without emails")
            st.dataframe(leads_without_emails[['company_name', 'domain']], use_container_width=True)
            
            # Batch extraction
            col1, col2 = st.columns([1, 1])
            
            with col1:
                extract_count = st.number_input(
                    "Number of leads to process",
                    min_value=1,
                    max_value=len(leads_without_emails),
                    value=min(5, len(leads_without_emails)),
                    help="Processing many leads at once may take time"
                )
            
            with col2:
                st.metric("Leads without emails", len(leads_without_emails))
            
            if st.button("📧 Extract Emails", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_container = st.container()
                
                extracted_results = []
                
                for i, (_, lead) in enumerate(leads_without_emails.head(extract_count).iterrows()):
                    domain = lead['domain']
                    company_name = lead.get('company_name', 'Unknown')
                    
                    status_text.text(f"Extracting emails for {company_name} ({domain})...")
                    progress_bar.progress((i + 1) / extract_count)
                    
                    try:
                        email_data = st.session_state.email_extractor.extract_emails_from_domain(domain)
                        
                        # Update the lead in database
                        success = st.session_state.data_processor.add_email_data(domain, email_data)
                        
                        # Track results
                        result = {
                            'company_name': company_name,
                            'domain': domain,
                            'email': email_data.get('email', 'Not found'),
                            'score': email_data.get('email_score', 0),
                            'type': email_data.get('email_type', 'unknown'),
                            'status': email_data.get('validation_status', 'unknown')
                        }
                        extracted_results.append(result)
                        
                    except Exception as e:
                        st.error(f"Error processing {domain}: {str(e)}")
                
                status_text.text("✅ Email extraction completed!")
                progress_bar.progress(1.0)
                
                # Show results
                if extracted_results:
                    results_df = pd.DataFrame(extracted_results)
                    
                    with results_container:
                        st.subheader("📊 Extraction Results")
                        
                        # Summary metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            total_processed = len(extracted_results)
                            st.metric("Processed", total_processed)
                        
                        with col2:
                            emails_found = len([r for r in extracted_results if r['email'] != 'Not found'])
                            st.metric("Emails Found", emails_found)
                        
                        with col3:
                            high_quality = len([r for r in extracted_results if r['score'] >= 80])
                            st.metric("High Quality", high_quality)
                        
                        with col4:
                            valid_emails = len([r for r in extracted_results if r['status'] == 'valid'])
                            st.metric("Valid Emails", valid_emails)
                        
                        # Detailed results
                        st.dataframe(results_df, use_container_width=True)

else:  # Extract from specific domain
    st.subheader("Extract from Specific Domain")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        domain_input = st.text_input(
            "Domain to extract emails from",
            placeholder="example.com",
            help="Enter the domain without http:// or www."
        )
    
    with col2:
        if st.button("📧 Extract Emails", type="primary", disabled=not domain_input):
            if domain_input:
                with st.spinner(f"Extracting emails from {domain_input}..."):
                    try:
                        email_data = st.session_state.email_extractor.extract_emails_from_domain(domain_input)
                        
                        # Display results
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.subheader("📧 Email Results")
                            if email_data['email']:
                                st.success(f"Found email: {email_data['email']}")
                                
                                # Display metrics
                                metric_col1, metric_col2 = st.columns(2)
                                with metric_col1:
                                    st.metric("Email Score", email_data['email_score'])
                                with metric_col2:
                                    st.metric("Email Type", email_data['email_type'])
                                
                                # Validation status
                                if email_data['validation_status'] == 'valid':
                                    st.success("✅ Email validation: VALID")
                                else:
                                    st.warning(f"⚠️ Email validation: {email_data['validation_status']}")
                                
                                # MX Record check
                                if email_data['mx_valid']:
                                    st.success("✅ MX Record: VALID")
                                else:
                                    st.error("❌ MX Record: INVALID")
                            else:
                                st.error("No email found for this domain")
                        
                        with col2:
                            st.subheader("🎯 Scoring Explanation")
                            st.info(f"""
                            **Email Type**: {email_data['email_type']}
                            **Score**: {email_data['email_score']}/100
                            
                            **Scoring Criteria**:
                            - CEO/Founder: 90-100 points
                            - Director/Manager: 80-90 points  
                            - Sales/Business: 70-80 points
                            - Generic Contact: 50-70 points
                            - Info/Support: 20-50 points
                            """)
                            
                            # Add to leads option
                            if email_data['email'] and st.button("➕ Add to Leads Database"):
                                lead_data = [{
                                    'company_name': st.session_state.email_extractor._extract_company_name_from_domain(domain_input),
                                    'domain': domain_input,
                                    'email': email_data['email'],
                                    'email_score': email_data['email_score'],
                                    'email_type': email_data['email_type']
                                }]
                                st.session_state.data_processor.add_tech_stack_data(lead_data)
                                st.success("Added to leads database!")
                                st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error extracting emails: {str(e)}")

# Email scoring explanation
st.markdown("---")
with st.expander("📊 Email Scoring System"):
    st.markdown("""
    ### How Email Scoring Works
    
    **High Value Emails (80-100 points):**
    - CEO, Founder, President emails
    - Director, Manager, Head of Department
    - Personal name patterns (first.last@domain.com)
    
    **Medium Value Emails (50-79 points):**
    - Sales, Business Development
    - Marketing, Operations
    - First name only emails
    
    **Low Value Emails (20-49 points):**
    - Generic contact emails (contact@, hello@)
    - Department emails (info@, support@)
    
    **Very Low Value (0-19 points):**
    - No-reply emails
    - Automated system emails
    
    ### Validation Checks
    - **Format Validation**: Checks email format using regex
    - **MX Record Check**: Verifies domain can receive emails
    - **Domain Verification**: Ensures domain is active
    """)

# Bulk email validation tool
st.markdown("---")
st.subheader("🔍 Bulk Email Validator")

email_list_input = st.text_area(
    "Enter emails to validate (one per line)",
    placeholder="john@example.com\nsales@company.com\ninfo@business.com",
    height=100
)

if st.button("🔍 Validate Emails") and email_list_input:
    emails = [email.strip() for email in email_list_input.split('\n') if email.strip()]
    
    if emails:
        with st.spinner("Validating emails..."):
            validation_results = st.session_state.email_extractor.validate_email_list(emails)
            
            if validation_results:
                results_df = pd.DataFrame(validation_results)
                st.dataframe(results_df, use_container_width=True)
                
                # Summary
                valid_count = len([r for r in validation_results if r['validation_status'] == 'valid'])
                st.info(f"Validation complete: {valid_count}/{len(emails)} emails are valid")

# Current leads with emails
if not st.session_state.leads_data.empty:
    leads_with_emails = st.session_state.leads_data[
        st.session_state.leads_data['email'].notna() & 
        (st.session_state.leads_data['email'] != '')
    ].copy() if 'email' in st.session_state.leads_data.columns else pd.DataFrame()
    
    if not leads_with_emails.empty:
        st.markdown("---")
        st.subheader("📋 Leads with Emails")
        
        # Sort by email score
        if 'email_score' in leads_with_emails.columns:
            leads_with_emails = leads_with_emails.sort_values('email_score', ascending=False)
        
        st.dataframe(leads_with_emails, use_container_width=True)
        
        # Email quality distribution
        if 'email_score' in leads_with_emails.columns:
            st.subheader("📊 Email Quality Distribution")
            score_ranges = pd.cut(
                leads_with_emails['email_score'], 
                bins=[0, 50, 80, 100], 
                labels=['Low (0-50)', 'Medium (51-80)', 'High (81-100)']
            )
            score_counts = score_ranges.value_counts()
            st.bar_chart(score_counts)
