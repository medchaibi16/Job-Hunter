"""
Email Extractor - Find valid company contact emails
Uses multiple methods to find working emails
"""
import re
import requests
from bs4 import BeautifulSoup
import time

class EmailExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def extract_emails_from_website(self, url):
        """
        Extract emails from company website
        
        Returns:
            dict: {
                'success': bool,
                'emails': list of found emails,
                'sources': dict of email -> where it was found
            }
        """
        print(f"📧 Searching for emails at: {url}")
        
        emails = set()
        sources = {}
        
        try:
            # Try main page
            main_emails = self._scrape_page_for_emails(url)
            for email in main_emails:
                emails.add(email)
                sources[email] = f"Main page: {url}"
            
            # Try common contact pages
            contact_pages = [
                '/contact',
                '/contact-us',
                '/about',
                '/about-us',
                '/careers',
                '/jobs',
                '/team',
                '/support',
                '/help'
            ]
            
            base_url = self._get_base_url(url)
            
            for page in contact_pages:
                try:
                    page_url = base_url + page
                    page_emails = self._scrape_page_for_emails(page_url)
                    for email in page_emails:
                        if email not in emails:
                            emails.add(email)
                            sources[email] = f"Contact page: {page_url}"
                    time.sleep(0.5)  # Be polite
                except:
                    continue
            
            # Filter out common fake emails
            real_emails = self._filter_real_emails(emails)
            
            return {
                'success': len(real_emails) > 0,
                'emails': list(real_emails),
                'sources': sources,
                'count': len(real_emails)
            }
            
        except Exception as e:
            print(f"❌ Error extracting emails: {e}")
            return {
                'success': False,
                'emails': [],
                'sources': {},
                'count': 0
            }
    
    def _scrape_page_for_emails(self, url):
        """Scrape a single page for emails"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Find emails in HTML
            html_content = response.text
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, html_content)
            
            # Also parse with BeautifulSoup for mailto: links
            soup = BeautifulSoup(html_content, 'html.parser')
            mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
            
            for link in mailto_links:
                email = link['href'].replace('mailto:', '').split('?')[0]
                found_emails.append(email)
            
            return set(found_emails)
            
        except:
            return set()
    
    def _get_base_url(self, url):
        """Get base URL from full URL"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _filter_real_emails(self, emails):
        """Filter out fake/example emails"""
        fake_patterns = [
            'example.com',
            'test.com',
            'domain.com',
            'email.com',
            'mail.com',
            'yourcompany.com',
            'company.com',
            'placeholder',
            'noreply',
            'no-reply',
            'donotreply'
        ]
        
        real_emails = []
        for email in emails:
            email_lower = email.lower()
            
            # Skip if contains fake patterns
            if any(fake in email_lower for fake in fake_patterns):
                continue
            
            # Skip if looks like a script or tracking email
            if any(x in email_lower for x in ['@sentry', '@tracking', '@analytics']):
                continue
            
            # Prefer certain email types
            priority_keywords = ['careers', 'jobs', 'hiring', 'hr', 'talent', 'recruit', 'internship', 'contact', 'info', 'hello', 'team']
            
            real_emails.append(email)
        
        return real_emails
    
    def find_hiring_email(self, emails, company_name):
        """
        Find the best email for hiring inquiries
        
        Args:
            emails: list of emails
            company_name: company name for guessing patterns
        
        Returns:
            str: best email for hiring, or first email if none found
        """
        if not emails:
            return None
        
        # Priority keywords for hiring
        hiring_keywords = [
            'careers', 'jobs', 'hiring', 'hr', 'talent', 
            'recruit', 'internship', 'intern', 'people'
        ]
        
        # Check for hiring-related emails
        for keyword in hiring_keywords:
            for email in emails:
                if keyword in email.lower():
                    return email
        
        # Check for general contact emails
        general_keywords = ['contact', 'info', 'hello', 'hi', 'team']
        for keyword in general_keywords:
            for email in emails:
                if keyword in email.lower():
                    return email
        
        # Return first email as fallback
        return emails[0]


# Test function
def test_extractor():
    extractor = EmailExtractor()
    
    # Test with a company
    test_url = "https://www.affectiva.com"
    
    print(f"\n{'='*60}")
    print(f"Testing Email Extractor")
    print(f"{'='*60}\n")
    
    result = extractor.extract_emails_from_website(test_url)
    
    if result['success']:
        print(f"✅ Found {result['count']} emails:")
        for email in result['emails']:
            source = result['sources'].get(email, 'Unknown')
            print(f"   📧 {email}")
            print(f"      Source: {source}\n")
        
        best_email = extractor.find_hiring_email(result['emails'], "Affectiva")
        print(f"\n🎯 Best email for hiring: {best_email}")
    else:
        print("❌ No emails found")

if __name__ == "__main__":
    test_extractor()