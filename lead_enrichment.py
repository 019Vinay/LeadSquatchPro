import requests
import re
import time
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import streamlit as st
import trafilatura
from urllib.parse import urljoin, urlparse

class LeadEnrichment:
    """Enrich leads with additional company data from public sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def enrich_company(self, domain: str, company_name: str = None) -> Dict[str, Any]:
        """Enrich company data from multiple sources"""
        try:
            enrichment_data = {
                'company_size': None,
                'funding_status': 'Unknown',
                'linkedin_url': None,
                'industry': None,
                'location': None,
                'description': None,
                'employee_count': None,
                'founding_year': None
            }
            
            # Use company name from domain if not provided
            if not company_name:
                company_name = self._extract_company_name_from_domain(domain)
            
            # Method 1: Scrape company website for basic info
            website_data = self._scrape_company_website(domain)
            enrichment_data.update(website_data)
            
            # Method 2: Search for LinkedIn company page
            linkedin_data = self._find_linkedin_profile(company_name, domain)
            enrichment_data.update(linkedin_data)
            
            # Method 3: Search for funding information
            funding_data = self._search_funding_info(company_name)
            enrichment_data.update(funding_data)
            
            # Method 4: Industry classification
            industry_data = self._classify_industry(domain, website_data.get('description', ''))
            enrichment_data.update(industry_data)
            
            return enrichment_data
            
        except Exception as e:
            st.error(f"Error enriching company {company_name or domain}: {str(e)}")
            return {
                'company_size': None,
                'funding_status': 'Error',
                'linkedin_url': None,
                'industry': None,
                'location': None
            }
    
    def _extract_company_name_from_domain(self, domain: str) -> str:
        """Extract company name from domain"""
        # Remove www and TLD
        name = domain.replace('www.', '').split('.')[0]
        return name.replace('-', ' ').replace('_', ' ').title()
    
    def _scrape_company_website(self, domain: str) -> Dict[str, Any]:
        """Scrape basic company information from their website"""
        data = {}
        
        try:
            # Try different pages that might contain company info
            pages_to_check = [
                f"https://{domain}",
                f"https://{domain}/about",
                f"https://{domain}/about-us",
                f"https://{domain}/company",
                f"https://{domain}/team"
            ]
            
            for url in pages_to_check:
                try:
                    downloaded = trafilatura.fetch_url(url)
                    if downloaded:
                        text_content = trafilatura.extract(downloaded)
                        if text_content:
                            # Extract company size indicators
                            size_info = self._extract_company_size(text_content)
                            if size_info:
                                data['company_size'] = size_info
                            
                            # Extract location
                            location = self._extract_location(text_content)
                            if location:
                                data['location'] = location
                            
                            # Extract description
                            description = self._extract_description(text_content)
                            if description:
                                data['description'] = description
                            
                            # Extract founding year
                            founding_year = self._extract_founding_year(text_content)
                            if founding_year:
                                data['founding_year'] = founding_year
                    
                except Exception:
                    continue
                
                time.sleep(1)  # Be respectful
                
                # Stop if we got enough info
                if len(data) >= 3:
                    break
            
        except Exception as e:
            st.warning(f"Website scraping failed for {domain}: {str(e)}")
        
        return data
    
    def _extract_company_size(self, text: str) -> Optional[str]:
        """Extract company size from text"""
        text_lower = text.lower()
        
        # Look for employee count patterns
        employee_patterns = [
            r'(\d+)[\s\-]+(?:employees?|people|team members?|staff)',
            r'team of (\d+)',
            r'(\d+)[\s\-]+person team',
            r'over (\d+) (?:employees?|people)',
            r'more than (\d+) (?:employees?|people)'
        ]
        
        for pattern in employee_patterns:
            match = re.search(pattern, text_lower)
            if match:
                count = int(match.group(1))
                return self._categorize_company_size(count)
        
        # Look for size indicators
        if any(term in text_lower for term in ['startup', 'small team', 'boutique']):
            return 'Small (1-50)'
        elif any(term in text_lower for term in ['enterprise', 'fortune', 'global']):
            return 'Large (500+)'
        
        return None
    
    def _categorize_company_size(self, employee_count: int) -> str:
        """Categorize company size based on employee count"""
        if employee_count <= 50:
            return 'Small (1-50)'
        elif employee_count <= 200:
            return 'Medium (51-200)'
        elif employee_count <= 500:
            return 'Large (201-500)'
        else:
            return 'Enterprise (500+)'
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract company location from text"""
        # Common location patterns
        location_patterns = [
            r'(?:based in|located in|headquarters in|hq in)\s+([A-Za-z\s,]+)',
            r'([A-Za-z]+,\s*[A-Za-z]{2})',  # City, State
            r'([A-Za-z]+,\s*[A-Za-z]+)',    # City, Country
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                if len(location) > 2 and len(location) < 50:
                    return location
        
        return None
    
    def _extract_description(self, text: str) -> Optional[str]:
        """Extract company description from text"""
        # Look for the first substantial paragraph
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if (len(sentence) > 50 and len(sentence) < 300 and 
                not sentence.lower().startswith(('home', 'about', 'contact', 'copyright'))):
                return sentence + '.'
        
        return None
    
    def _extract_founding_year(self, text: str) -> Optional[int]:
        """Extract founding year from text"""
        # Look for founding year patterns
        year_patterns = [
            r'(?:founded|established|started|since)\s+(?:in\s+)?(\d{4})',
            r'(\d{4})[\s\-]+(?:founded|established|started)',
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                year = int(match.group(1))
                if 1900 <= year <= 2025:  # Reasonable year range
                    return year
        
        return None
    
    def _find_linkedin_profile(self, company_name: str, domain: str) -> Dict[str, Any]:
        """Find LinkedIn company profile"""
        data = {}
        
        try:
            # Generate possible LinkedIn URLs
            company_slug = company_name.lower().replace(' ', '-').replace('&', 'and')
            domain_slug = domain.split('.')[0]
            
            potential_urls = [
                f"https://www.linkedin.com/company/{company_slug}",
                f"https://www.linkedin.com/company/{domain_slug}",
                f"https://www.linkedin.com/company/{company_name.lower().replace(' ', '')}"
            ]
            
            for url in potential_urls:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200 and 'company' in response.url:
                        data['linkedin_url'] = response.url
                        
                        # Try to extract additional info from LinkedIn
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Look for company size on LinkedIn
                        size_text = soup.get_text()
                        size_info = self._extract_company_size(size_text)
                        if size_info:
                            data['company_size'] = size_info
                        
                        break
                        
                except Exception:
                    continue
                
                time.sleep(2)  # Be respectful to LinkedIn
            
        except Exception as e:
            st.warning(f"LinkedIn search failed for {company_name}: {str(e)}")
        
        return data
    
    def _search_funding_info(self, company_name: str) -> Dict[str, Any]:
        """Search for company funding information"""
        data = {}
        
        # This would ideally use Crunchbase API or similar
        # For now, we'll use some heuristics and public data
        
        try:
            # Search for funding keywords in general web search results
            # This is a simplified approach
            funding_keywords = ['funding', 'investment', 'raised', 'series', 'venture']
            
            # You could implement actual web search here
            # For demo purposes, we'll classify based on company characteristics
            
            # Simple heuristic: if company has LinkedIn and good web presence,
            # they might be funded
            data['funding_status'] = 'Unknown'
            
        except Exception:
            data['funding_status'] = 'Unknown'
        
        return data
    
    def _classify_industry(self, domain: str, description: str) -> Dict[str, Any]:
        """Classify company industry based on domain and description"""
        data = {}
        
        try:
            text_to_analyze = f"{domain} {description}".lower()
            
            # Industry classification based on keywords
            industry_keywords = {
                'Technology': ['tech', 'software', 'app', 'platform', 'ai', 'machine learning', 'saas'],
                'E-commerce': ['shop', 'store', 'retail', 'commerce', 'marketplace', 'buy', 'sell'],
                'Healthcare': ['health', 'medical', 'care', 'hospital', 'clinic', 'wellness'],
                'Finance': ['bank', 'finance', 'payment', 'fintech', 'investment', 'insurance'],
                'Education': ['education', 'learning', 'school', 'university', 'course', 'training'],
                'Marketing': ['marketing', 'advertising', 'agency', 'digital', 'seo', 'social media'],
                'Consulting': ['consulting', 'advisory', 'services', 'solutions', 'strategy'],
                'Manufacturing': ['manufacturing', 'production', 'industrial', 'factory', 'supply'],
                'Real Estate': ['real estate', 'property', 'housing', 'realty', 'construction'],
                'Media': ['media', 'publishing', 'content', 'news', 'entertainment', 'video']
            }
            
            industry_scores = {}
            for industry, keywords in industry_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_to_analyze)
                if score > 0:
                    industry_scores[industry] = score
            
            if industry_scores:
                data['industry'] = max(industry_scores, key=industry_scores.get)
            else:
                data['industry'] = 'Other'
                
        except Exception:
            data['industry'] = 'Unknown'
        
        return data
