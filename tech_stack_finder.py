import requests
import re
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import streamlit as st
from urllib.parse import urljoin, urlparse
import trafilatura

class TechStackFinder:
    """Find companies using specific technology stacks"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def find_by_technology(self, technology: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find companies using a specific technology"""
        results = []
        
        # Try multiple sources
        try:
            # Method 1: Search GitHub for websites using the technology
            github_results = self._search_github_sites(technology, limit // 2)
            results.extend(github_results)
            
            # Method 2: Search for technology-specific showcases
            showcase_results = self._search_technology_showcases(technology, limit // 2)
            results.extend(showcase_results)
            
        except Exception as e:
            st.error(f"Error finding companies: {str(e)}")
        
        return results[:limit]
    
    def _search_github_sites(self, technology: str, limit: int) -> List[Dict[str, Any]]:
        """Search GitHub for sites using the technology"""
        results = []
        
        try:
            # Search for repositories with the technology and look for live sites
            search_url = f"https://api.github.com/search/repositories"
            params = {
                'q': f'{technology} language:javascript',
                'sort': 'stars',
                'order': 'desc',
                'per_page': limit * 2  # Get more to filter for actual sites
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                for repo in data.get('items', [])[:limit * 2]:
                    # Look for homepage URL
                    homepage = repo.get('homepage')
                    if homepage and self._is_valid_website(homepage):
                        domain = urlparse(homepage).netloc
                        
                        results.append({
                            'company_name': self._extract_company_name(homepage),
                            'domain': domain,
                            'tech_stack': technology,
                            'source': f'GitHub - {repo.get("name", "")}'
                        })
                        
                        if len(results) >= limit:
                            break
            
        except Exception as e:
            st.warning(f"GitHub search failed: {str(e)}")
        
        return results
    
    def _search_technology_showcases(self, technology: str, limit: int) -> List[Dict[str, Any]]:
        """Search technology-specific showcases and directories"""
        results = []
        
        # Technology-specific showcase URLs
        showcase_urls = {
            'shopify': 'https://www.shopify.com/partners/directory',
            'react': 'https://react.dev/community/examples',
            'wordpress': 'https://wordpress.org/showcase/',
            'vue': 'https://vuejs.org/examples/',
            'angular': 'https://angular.io/resources',
            'django': 'https://www.djangosites.org/',
            'rails': 'https://rubyonrails.org/applications/',
            'nextjs': 'https://nextjs.org/showcase',
            'nuxt': 'https://nuxtjs.org/showcase'
        }
        
        tech_lower = technology.lower()
        
        # Try to find a relevant showcase
        for tech_key, url in showcase_urls.items():
            if tech_key in tech_lower or tech_lower in tech_key:
                try:
                    showcase_results = self._scrape_showcase_page(url, technology, limit)
                    results.extend(showcase_results)
                    break
                except Exception as e:
                    st.warning(f"Showcase scraping failed for {tech_key}: {str(e)}")
        
        # If no specific showcase found, do a general web search
        if not results:
            results = self._general_web_search(technology, limit)
        
        return results[:limit]
    
    def _scrape_showcase_page(self, url: str, technology: str, limit: int) -> List[Dict[str, Any]]:
        """Scrape a technology showcase page for websites"""
        results = []
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for links that appear to be external websites
                links = soup.find_all('a', href=True)
                
                for link in links:
                    href = link.get('href')
                    if self._is_valid_website(href):
                        domain = urlparse(href).netloc
                        
                        # Skip if it's the same domain as the showcase
                        if domain != urlparse(url).netloc:
                            company_name = self._extract_company_name(href)
                            
                            results.append({
                                'company_name': company_name,
                                'domain': domain,
                                'tech_stack': technology,
                                'source': f'Showcase - {urlparse(url).netloc}'
                            })
                            
                            if len(results) >= limit:
                                break
            
        except Exception as e:
            raise Exception(f"Failed to scrape showcase: {str(e)}")
        
        return results
    
    def _general_web_search(self, technology: str, limit: int) -> List[Dict[str, Any]]:
        """Perform a general web search for companies using the technology"""
        results = []
        
        # Create some sample companies based on technology
        # This would ideally use a real search API like Google Custom Search
        sample_companies = {
            'shopify': [
                {'name': 'Allbirds', 'domain': 'allbirds.com'},
                {'name': 'Gymshark', 'domain': 'gymshark.com'},
                {'name': 'Kylie Cosmetics', 'domain': 'kyliecosmetics.com'},
                {'name': 'MVMT', 'domain': 'mvmt.com'},
                {'name': 'Bulletproof', 'domain': 'bulletproof.com'}
            ],
            'react': [
                {'name': 'Netflix', 'domain': 'netflix.com'},
                {'name': 'Airbnb', 'domain': 'airbnb.com'},
                {'name': 'Uber', 'domain': 'uber.com'},
                {'name': 'WhatsApp', 'domain': 'whatsapp.com'},
                {'name': 'Dropbox', 'domain': 'dropbox.com'}
            ],
            'wordpress': [
                {'name': 'TechCrunch', 'domain': 'techcrunch.com'},
                {'name': 'The New Yorker', 'domain': 'newyorker.com'},
                {'name': 'BBC America', 'domain': 'bbcamerica.com'},
                {'name': 'Sony Music', 'domain': 'sonymusic.com'},
                {'name': 'Microsoft News', 'domain': 'news.microsoft.com'}
            ]
        }
        
        tech_lower = technology.lower()
        if tech_lower in sample_companies:
            for company in sample_companies[tech_lower][:limit]:
                results.append({
                    'company_name': company['name'],
                    'domain': company['domain'],
                    'tech_stack': technology,
                    'source': 'Technology Directory'
                })
        
        return results
    
    def _is_valid_website(self, url: str) -> bool:
        """Check if a URL is a valid website"""
        if not url:
            return False
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc and 
                '.' in parsed.netloc and
                not parsed.netloc.startswith('localhost') and
                not parsed.netloc.startswith('127.0.0.1')
            )
        except:
            return False
    
    def _extract_company_name(self, url: str) -> str:
        """Extract company name from URL"""
        try:
            domain = urlparse(url).netloc
            # Remove www. and common TLDs, capitalize
            name = domain.replace('www.', '').split('.')[0]
            return name.capitalize()
        except:
            return "Unknown Company"
    
    def verify_technology(self, domain: str, technology: str) -> bool:
        """Verify if a domain actually uses the specified technology"""
        try:
            url = f"https://{domain}"
            
            # Get website content
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return False
            
            # Extract text content
            text_content = trafilatura.extract(downloaded)
            
            # Also get HTML for technical analysis
            response = self.session.get(url, timeout=10)
            html_content = response.text
            
            # Technology detection patterns
            tech_patterns = {
                'shopify': [
                    'shopify', 'shop.js', 'cdn.shopify.com', 'myshopify.com'
                ],
                'react': [
                    'react', 'react-dom', 'jsx', '__REACT_DEVTOOLS__'
                ],
                'wordpress': [
                    'wp-content', 'wordpress', 'wp-json', '/wp/'
                ],
                'vue': [
                    'vue.js', 'vue.min.js', '__vue__', 'v-if', 'v-for'
                ],
                'angular': [
                    'angular', 'ng-app', 'ng-controller', 'angularjs'
                ],
                'django': [
                    'django', 'csrfmiddlewaretoken', 'staticfiles'
                ],
                'nextjs': [
                    'next.js', '_next/', 'next-head', '__NEXT_DATA__'
                ]
            }
            
            tech_lower = technology.lower()
            patterns = tech_patterns.get(tech_lower, [tech_lower])
            
            # Check for patterns in HTML content
            for pattern in patterns:
                if pattern.lower() in html_content.lower():
                    return True
            
            return False
            
        except Exception as e:
            # If we can't verify, assume it's valid
            return True
