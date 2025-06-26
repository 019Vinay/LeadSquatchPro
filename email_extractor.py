import re
import requests
import dns.resolver
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Tuple
import time
import streamlit as st
from email_validator import validate_email, EmailNotValidError
import trafilatura

class EmailExtractor:
    """Extract and score professional emails from websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Email scoring weights
        self.email_types = {
            'ceo': 100,
            'founder': 95,
            'president': 90,
            'director': 85,
            'manager': 80,
            'head': 85,
            'chief': 90,
            'vp': 85,
            'vice': 85,
            'sales': 75,
            'business': 70,
            'marketing': 70,
            'contact': 60,
            'hello': 55,
            'hi': 55,
            'info': 30,
            'support': 25,
            'noreply': 10,
            'no-reply': 10
        }
    
    def extract_emails_from_domain(self, domain: str) -> Dict[str, Any]:
        """Extract emails from a domain and return the best one with score"""
        try:
            # Get emails from multiple sources
            emails = []
            
            # Method 1: Scrape website directly
            website_emails = self._scrape_website_emails(domain)
            emails.extend(website_emails)
            
            # Method 2: Check common email patterns
            pattern_emails = self._generate_common_patterns(domain)
            emails.extend(pattern_emails)
            
            # Method 3: Check social media and about pages
            social_emails = self._check_social_and_about_pages(domain)
            emails.extend(social_emails)
            
            if not emails:
                return {
                    'email': None,
                    'email_score': 0,
                    'email_type': 'not_found',
                    'validation_status': 'not_found',
                    'mx_valid': False
                }
            
            # Score and validate emails
            scored_emails = []
            for email in set(emails):  # Remove duplicates
                if self._is_valid_email_format(email):
                    score = self._score_email(email)
                    mx_valid = self._check_mx_record(email)
                    email_type = self._classify_email_type(email)
                    
                    scored_emails.append({
                        'email': email,
                        'score': score,
                        'mx_valid': mx_valid,
                        'email_type': email_type
                    })
            
            if not scored_emails:
                return {
                    'email': None,
                    'email_score': 0,
                    'email_type': 'invalid',
                    'validation_status': 'invalid_format',
                    'mx_valid': False
                }
            
            # Sort by score and MX validity
            scored_emails.sort(key=lambda x: (x['mx_valid'], x['score']), reverse=True)
            best_email = scored_emails[0]
            
            return {
                'email': best_email['email'],
                'email_score': best_email['score'],
                'email_type': best_email['email_type'],
                'validation_status': 'valid' if best_email['mx_valid'] else 'mx_invalid',
                'mx_valid': best_email['mx_valid']
            }
            
        except Exception as e:
            st.error(f"Error extracting emails from {domain}: {str(e)}")
            return {
                'email': None,
                'email_score': 0,
                'email_type': 'error',
                'validation_status': 'error',
                'mx_valid': False
            }
    
    def _scrape_website_emails(self, domain: str) -> List[str]:
        """Scrape emails directly from website content"""
        emails = []
        
        try:
            # Try different URL variations
            urls_to_try = [
                f"https://{domain}",
                f"https://www.{domain}",
                f"https://{domain}/contact",
                f"https://{domain}/about",
                f"https://{domain}/team"
            ]
            
            for url in urls_to_try:
                try:
                    # Use trafilatura for better content extraction
                    downloaded = trafilatura.fetch_url(url)
                    if downloaded:
                        # Extract text content
                        text_content = trafilatura.extract(downloaded)
                        if text_content:
                            found_emails = self._extract_emails_from_text(text_content)
                            emails.extend(found_emails)
                        
                        # Also check HTML directly for hidden emails
                        html_emails = self._extract_emails_from_text(downloaded)
                        emails.extend(html_emails)
                    
                except Exception:
                    continue
                
                # Don't overwhelm the server
                time.sleep(1)
                
                # Stop if we found enough emails
                if len(emails) >= 10:
                    break
            
        except Exception as e:
            st.warning(f"Website scraping failed for {domain}: {str(e)}")
        
        return emails
    
    def _generate_common_patterns(self, domain: str) -> List[str]:
        """Generate common email patterns for the domain"""
        patterns = [
            f"info@{domain}",
            f"hello@{domain}",
            f"contact@{domain}",
            f"admin@{domain}",
            f"sales@{domain}",
            f"support@{domain}",
            f"ceo@{domain}",
            f"founder@{domain}",
            f"business@{domain}"
        ]
        
        return patterns
    
    def _check_social_and_about_pages(self, domain: str) -> List[str]:
        """Check social media profiles and about pages for emails"""
        emails = []
        
        try:
            # Search for LinkedIn company page
            linkedin_url = f"https://www.linkedin.com/company/{domain.split('.')[0]}"
            try:
                response = self.session.get(linkedin_url, timeout=10)
                if response.status_code == 200:
                    found_emails = self._extract_emails_from_text(response.text)
                    emails.extend(found_emails)
            except:
                pass
            
            # Check if there's a contact form or page
            contact_pages = [
                f"https://{domain}/contact-us",
                f"https://{domain}/contact.html",
                f"https://{domain}/get-in-touch"
            ]
            
            for contact_url in contact_pages:
                try:
                    downloaded = trafilatura.fetch_url(contact_url)
                    if downloaded:
                        text_content = trafilatura.extract(downloaded)
                        if text_content:
                            found_emails = self._extract_emails_from_text(text_content)
                            emails.extend(found_emails)
                except:
                    continue
            
        except Exception:
            pass
        
        return emails
    
    def _extract_emails_from_text(self, text: str) -> List[str]:
        """Extract email addresses from text using regex"""
        if not text:
            return []
        
        # Email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Filter out common false positives
        filtered_emails = []
        for email in emails:
            email_lower = email.lower()
            if not any(skip in email_lower for skip in [
                'example.com', 'test.com', 'domain.com', 'email.com',
                'yourcompany.com', 'yourdomain.com', 'company.com'
            ]):
                filtered_emails.append(email)
        
        return filtered_emails
    
    def _is_valid_email_format(self, email: str) -> bool:
        """Validate email format"""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def _score_email(self, email: str) -> int:
        """Score an email based on its type and quality"""
        email_lower = email.lower()
        base_score = 50
        
        # Check for high-value keywords
        for keyword, score in self.email_types.items():
            if keyword in email_lower:
                return score
        
        # Personal name patterns (higher score)
        if re.match(r'^[a-z]+\.[a-z]+@', email_lower):
            return 80
        
        # First name only
        if re.match(r'^[a-z]+@', email_lower) and len(email_lower.split('@')[0]) > 2:
            return 70
        
        return base_score
    
    def _classify_email_type(self, email: str) -> str:
        """Classify the type of email"""
        email_lower = email.lower()
        
        for email_type, score in self.email_types.items():
            if email_type in email_lower:
                return email_type
        
        # Check for personal name patterns
        if re.match(r'^[a-z]+\.[a-z]+@', email_lower):
            return 'personal_name'
        elif re.match(r'^[a-z]+@', email_lower):
            return 'first_name'
        else:
            return 'generic'
    
    def _check_mx_record(self, email: str) -> bool:
        """Check if the email domain has valid MX records"""
        try:
            domain = email.split('@')[1]
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
    
    def validate_email_list(self, emails: List[str]) -> List[Dict[str, Any]]:
        """Validate and score a list of emails"""
        results = []
        
        for email in emails:
            if self._is_valid_email_format(email):
                score = self._score_email(email)
                mx_valid = self._check_mx_record(email)
                email_type = self._classify_email_type(email)
                
                results.append({
                    'email': email,
                    'score': score,
                    'email_type': email_type,
                    'mx_valid': mx_valid,
                    'validation_status': 'valid' if mx_valid else 'mx_invalid'
                })
            else:
                results.append({
                    'email': email,
                    'score': 0,
                    'email_type': 'invalid',
                    'mx_valid': False,
                    'validation_status': 'invalid_format'
                })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
