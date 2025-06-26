import pandas as pd
import streamlit as st
from typing import Dict, List, Any

class DataProcessor:
    """Handles data processing and storage for the lead generation platform"""
    
    def __init__(self):
        self.leads_columns = [
            'company_name', 'domain', 'tech_stack', 'email', 'email_score', 
            'email_type', 'company_size', 'funding_status', 'linkedin_url',
            'industry', 'location', 'source'
        ]
    
    def add_tech_stack_data(self, data: List[Dict[str, Any]]):
        """Add tech stack data to the leads database"""
        if not data:
            return
        
        df = pd.DataFrame(data)
        df['source'] = 'Tech Stack Finder'
        
        # Ensure all required columns exist
        for col in self.leads_columns:
            if col not in df.columns:
                df[col] = None
        
        # Reorder columns
        df = df[self.leads_columns]
        
        # Add to session state
        if st.session_state.leads_data.empty:
            st.session_state.leads_data = df
        else:
            st.session_state.leads_data = pd.concat([st.session_state.leads_data, df], ignore_index=True)
        
        # Remove duplicates based on domain
        st.session_state.leads_data = st.session_state.leads_data.drop_duplicates(
            subset=['domain'], keep='last'
        ).reset_index(drop=True)
    
    def add_email_data(self, domain: str, email_data: Dict[str, Any]):
        """Add email data to existing leads"""
        if st.session_state.leads_data.empty:
            return False
        
        # Find the lead by domain
        mask = st.session_state.leads_data['domain'] == domain
        if not mask.any():
            return False
        
        # Update email information
        for key, value in email_data.items():
            if key in self.leads_columns:
                st.session_state.leads_data.loc[mask, key] = value
        
        return True
    
    def add_enrichment_data(self, domain: str, enrichment_data: Dict[str, Any]):
        """Add enrichment data to existing leads"""
        if st.session_state.leads_data.empty:
            return False
        
        # Find the lead by domain
        mask = st.session_state.leads_data['domain'] == domain
        if not mask.any():
            return False
        
        # Update enrichment information
        for key, value in enrichment_data.items():
            if key in self.leads_columns:
                st.session_state.leads_data.loc[mask, key] = value
        
        return True
    
    def get_leads_by_criteria(self, criteria: Dict[str, Any]) -> pd.DataFrame:
        """Filter leads based on criteria"""
        if st.session_state.leads_data.empty:
            return pd.DataFrame()
        
        df = st.session_state.leads_data.copy()
        
        for key, value in criteria.items():
            if key in df.columns and value is not None:
                if isinstance(value, str):
                    df = df[df[key].str.contains(value, case=False, na=False)]
                else:
                    df = df[df[key] == value]
        
        return df
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the current leads data"""
        if st.session_state.leads_data.empty:
            return {
                'total_leads': 0,
                'high_quality_emails': 0,
                'unique_companies': 0,
                'funded_companies': 0,
                'top_technologies': [],
                'top_industries': []
            }
        
        df = st.session_state.leads_data
        
        stats = {
            'total_leads': len(df),
            'high_quality_emails': len(df[df['email_score'] >= 80]) if 'email_score' in df.columns else 0,
            'unique_companies': df['company_name'].nunique() if 'company_name' in df.columns else 0,
            'funded_companies': len(df[
                df['funding_status'].notna() & 
                (df['funding_status'] != 'Unknown')
            ]) if 'funding_status' in df.columns else 0,
            'top_technologies': df['tech_stack'].value_counts().head(5).to_dict() if 'tech_stack' in df.columns else {},
            'top_industries': df['industry'].value_counts().head(5).to_dict() if 'industry' in df.columns else {}
        }
        
        return stats
    
    def export_to_csv(self) -> str:
        """Export leads data to CSV format"""
        if st.session_state.leads_data.empty:
            return ""
        
        return st.session_state.leads_data.to_csv(index=False)
    
    def clear_data(self):
        """Clear all leads data"""
        st.session_state.leads_data = pd.DataFrame()
