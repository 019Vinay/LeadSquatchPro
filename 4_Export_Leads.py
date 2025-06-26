import streamlit as st
import pandas as pd
from datetime import datetime
import io
from utils.data_processor import DataProcessor

st.set_page_config(
    page_title="Export Leads",
    page_icon="📁",
    layout="wide"
)

# Enhanced CSS for export page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .export-header {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #ec4899 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 
            0 25px 50px rgba(245, 158, 11, 0.4),
            0 0 100px rgba(239, 68, 68, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        transform: perspective(1000px) rotateX(3deg);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .export-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }
    
    .export-header:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-10px) scale(1.02);
        box-shadow: 
            0 35px 70px rgba(245, 158, 11, 0.6),
            0 0 150px rgba(239, 68, 68, 0.5);
    }
    
    .export-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-align: center;
        margin: 0;
        font-size: 2.8rem;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.5),
            0 0 40px rgba(245, 158, 11, 0.8),
            0 0 80px rgba(239, 68, 68, 0.6);
        position: relative;
        z-index: 1;
    }
    
    .download-card {
        background: linear-gradient(145deg, #ffffff, #f7fafc);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 3px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(252, 182, 159, 0.3);
        margin: 1rem 0;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .download-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 10px 20px rgba(0,0,0,0.1);
    }
    
    .export-button {
        background: linear-gradient(45deg, #ffecd2, #fcb69f);
        border: none;
        border-radius: 15px;
        color: #2d3748;
        padding: 1rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 8px 25px rgba(252, 182, 159, 0.3);
        transition: all 0.3s ease;
        font-size: 1.1rem;
        margin: 0.5rem;
        cursor: pointer;
    }
    
    .export-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(252, 182, 159, 0.5);
    }
    
    .filter-panel {
        background: rgba(255, 236, 210, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(252, 182, 159, 0.2);
        margin: 1rem 0;
    }
    
    .stats-panel {
        background: linear-gradient(145deg, #f0f9ff, #ffffff);
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 5px solid #fcb69f;
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
    
    .stMultiSelect > div > div {
        background-color: rgba(15, 15, 35, 0.9) !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 10px !important;
    }
    
    .stCheckbox > div {
        color: #f1f5f9 !important;
    }
    
    /* Labels and help text */
    .stSelectbox label, .stTextInput label, .stMultiSelect label, .stCheckbox label {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #f59e0b, #ef4444) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4) !important;
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
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #22c55e, #16a34a) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="export-header">
    <h1>📁 Export Leads</h1>
    <p style="color: #4a5568; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
        Download your enriched leads in multiple formats
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize components
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# Check if we have data to export
if st.session_state.leads_data.empty:
    st.warning("No leads data available for export.")
    st.info("Please use the other modules to generate leads first:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Tech Stack Finder"):
            st.switch_page("pages/1_Tech_Stack_Finder.py")
    
    with col2:
        if st.button("📧 Email Extractor"):
            st.switch_page("pages/2_Email_Extractor.py")
    
    with col3:
        if st.button("📊 Lead Enrichment"):
            st.switch_page("pages/3_Lead_Enrichment.py")

else:
    # Data overview
    st.subheader("📊 Current Leads Overview")
    
    # Statistics
    stats = st.session_state.data_processor.get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", stats['total_leads'])
    
    with col2:
        st.metric("High Quality Emails", stats['high_quality_emails'])
    
    with col3:
        st.metric("Unique Companies", stats['unique_companies'])
    
    with col4:
        st.metric("Funded Companies", stats['funded_companies'])
    
    # Data preview
    st.markdown("---")
    st.subheader("📋 Data Preview")
    st.dataframe(st.session_state.leads_data, use_container_width=True)
    
    # Export options
    st.markdown("---")
    st.subheader("📤 Export Options")
    
    # Column selection
    available_columns = list(st.session_state.leads_data.columns)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Select columns to export:**")
        selected_columns = st.multiselect(
            "Choose columns",
            available_columns,
            default=available_columns,
            help="Select which columns to include in the export"
        )
    
    with col2:
        st.write("**Export settings:**")
        
        # File naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = st.text_input(
            "Filename",
            value=f"leads_export_{timestamp}",
            help="Filename without extension"
        )
        
        # Filtering options
        filter_empty_emails = st.checkbox(
            "Exclude leads without emails",
            value=False,
            help="Only export leads that have email addresses"
        )
        
        min_email_score = st.slider(
            "Minimum email score",
            min_value=0,
            max_value=100,
            value=0,
            help="Only export leads with email score above this threshold"
        )
    
    # Apply filters
    export_data = st.session_state.leads_data.copy()
    
    if filter_empty_emails and 'email' in export_data.columns:
        export_data = export_data[
            export_data['email'].notna() & 
            (export_data['email'] != '') & 
            (export_data['email'] != 'Not found')
        ]
    
    if min_email_score > 0 and 'email_score' in export_data.columns:
        export_data = export_data[export_data['email_score'] >= min_email_score]
    
    # Select only chosen columns
    if selected_columns:
        available_selected = [col for col in selected_columns if col in export_data.columns]
        export_data = export_data[available_selected]
    
    # Show filtered data preview
    if len(export_data) != len(st.session_state.leads_data):
        st.info(f"After filtering: {len(export_data)} leads will be exported (from {len(st.session_state.leads_data)} total)")
        st.dataframe(export_data.head(10), use_container_width=True)
    
    # Export buttons
    st.markdown("---")
    st.subheader("💾 Download Options")
    
    if not export_data.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV Export
            csv_data = export_data.to_csv(index=False)
            st.download_button(
                label="📊 Download as CSV",
                data=csv_data,
                file_name=f"{filename}.csv",
                mime="text/csv",
                type="primary",
                help="Standard CSV format, compatible with Excel and most CRM systems"
            )
        
        with col2:
            # Excel Export
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                export_data.to_excel(writer, sheet_name='Leads', index=False)
                
                # Add a summary sheet
                summary_data = pd.DataFrame([
                    ['Total Leads', len(export_data)],
                    ['Export Date', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    ['Columns Exported', len(selected_columns)],
                    ['High Quality Emails', len(export_data[export_data['email_score'] >= 80]) if 'email_score' in export_data.columns else 'N/A']
                ], columns=['Metric', 'Value'])
                summary_data.to_excel(writer, sheet_name='Summary', index=False)
            
            excel_buffer.seek(0)
            
            st.download_button(
                label="📈 Download as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"{filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Excel format with multiple sheets including summary"
            )
        
        with col3:
            # JSON Export
            json_data = export_data.to_json(orient='records', indent=2)
            st.download_button(
                label="🔗 Download as JSON",
                data=json_data,
                file_name=f"{filename}.json",
                mime="application/json",
                help="JSON format for API integration and custom processing"
            )
        
        # Export statistics
        st.markdown("---")
        st.subheader("📈 Export Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Data Quality Metrics:**")
            if 'email' in export_data.columns:
                emails_found = len(export_data[
                    export_data['email'].notna() & 
                    (export_data['email'] != '') & 
                    (export_data['email'] != 'Not found')
                ])
                st.write(f"- Leads with emails: {emails_found}/{len(export_data)} ({emails_found/len(export_data)*100:.1f}%)")
            
            if 'email_score' in export_data.columns:
                high_quality = len(export_data[export_data['email_score'] >= 80])
                st.write(f"- High quality emails: {high_quality}/{len(export_data)} ({high_quality/len(export_data)*100:.1f}%)")
            
            if 'company_size' in export_data.columns:
                enriched_size = len(export_data[
                    export_data['company_size'].notna() & 
                    (export_data['company_size'] != 'Unknown')
                ])
                st.write(f"- Company size data: {enriched_size}/{len(export_data)} ({enriched_size/len(export_data)*100:.1f}%)")
        
        with col2:
            st.write("**Top Industries:**")
            if 'industry' in export_data.columns and not export_data['industry'].isna().all():
                top_industries = export_data['industry'].value_counts().head(5)
                for industry, count in top_industries.items():
                    if industry and industry != 'Unknown':
                        st.write(f"- {industry}: {count}")
            else:
                st.write("No industry data available")
        
        # CRM Integration templates
        st.markdown("---")
        st.subheader("🔧 CRM Integration Templates")
        
        with st.expander("📋 CRM Import Instructions"):
            st.markdown("""
            ### Salesforce
            1. Go to **Setup** → **Data Import Wizard**
            2. Choose **Leads** object
            3. Upload the CSV file
            4. Map fields:
               - `company_name` → Company
               - `email` → Email
               - `domain` → Website
               - `industry` → Industry
               - `location` → City/State
            
            ### HubSpot
            1. Navigate to **Contacts** → **Import**
            2. Select **File from computer**
            3. Choose **Contacts** and upload CSV
            4. Map fields according to HubSpot properties
            
            ### Pipedrive
            1. Go to **Contacts** → **People**
            2. Click **Import data**
            3. Upload CSV and map fields:
               - `company_name` → Organization
               - `email` → Email
               - `domain` → Website
            
            ### General CSV Import Tips
            - Ensure email format is valid
            - Remove any special characters from company names
            - Use consistent date formats
            - Split location into separate city/state columns if required
            """)
        
        # Custom export templates
        st.markdown("---")
        st.subheader("🎯 Quick Export Templates")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Email Marketing List"):
                email_marketing_data = export_data[['company_name', 'email', 'email_score']].copy()
                email_marketing_data = email_marketing_data[
                    email_marketing_data['email'].notna() & 
                    (email_marketing_data['email'] != '') & 
                    (email_marketing_data['email'] != 'Not found')
                ]
                csv_marketing = email_marketing_data.to_csv(index=False)
                st.download_button(
                    "Download Email List",
                    csv_marketing,
                    f"{filename}_email_marketing.csv",
                    "text/csv"
                )
        
        with col2:
            if st.button("🎯 Sales Prospects"):
                sales_columns = ['company_name', 'domain', 'email', 'email_score', 'company_size', 'industry', 'linkedin_url']
                available_sales_cols = [col for col in sales_columns if col in export_data.columns]
                sales_data = export_data[available_sales_cols].copy()
                csv_sales = sales_data.to_csv(index=False)
                st.download_button(
                    "Download Sales List",
                    csv_sales,
                    f"{filename}_sales_prospects.csv",
                    "text/csv"
                )
        
        with col3:
            if st.button("📊 Research Data"):
                research_data = export_data.copy()
                csv_research = research_data.to_csv(index=False)
                st.download_button(
                    "Download Research Data",
                    csv_research,
                    f"{filename}_research_data.csv",
                    "text/csv"
                )
    
    else:
        st.warning("No data available for export after applying filters.")
        st.info("Try adjusting your filter settings to include more leads.")

# Data management
st.markdown("---")
st.subheader("🗄️ Data Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Clear All Data", type="secondary"):
        if st.button("⚠️ Confirm Clear All Data"):
            st.session_state.data_processor.clear_data()
            st.success("All data cleared!")
            st.rerun()

with col2:
    if not st.session_state.leads_data.empty:
        st.write(f"**Current data size:** {len(st.session_state.leads_data)} leads")
        st.write(f"**Memory usage:** {st.session_state.leads_data.memory_usage(deep=True).sum() / 1024:.1f} KB")
