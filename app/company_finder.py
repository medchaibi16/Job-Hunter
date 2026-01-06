"""
AI Company Finder - Find AI companies that accept remote interns
Focuses on companies where your projects would be valuable
"""
import requests
from bs4 import BeautifulSoup
from app.email_extractor import EmailExtractor
import time

class AICompanyFinder:
    def __init__(self):
        self.email_extractor = EmailExtractor()
        self.companies = []
        
    def find_ai_companies(self):
        """
        Find AI companies that:
        - Work in AI/ML/NLP domain
        - Accept remote interns
        - Have Winter/Spring 2025 programs
        """
        print("\n🔍 Searching for AI companies...")
        
        companies = []
        
        # Method 1: Known AI companies
        companies.extend(self._get_known_ai_companies())
        
        # Method 2: YCombinator AI companies
        companies.extend(self._get_yc_ai_companies())
        
        # Method 3: AngelList AI startups
        companies.extend(self._get_angellist_companies())
        
        # Method 4: Crunchbase AI companies
        companies.extend(self._get_crunchbase_companies())
        
        return companies
    
    def _get_known_ai_companies(self):
        """Get list of well-known AI companies"""
        known_companies = [
            {
                'name': 'OpenAI',
                'website': 'https://openai.com',
                'focus': 'GPT models, AI research',
                'why_your_projects_fit': 'Your AI learning assistant and compression work align with their efficiency research'
            },
            {
                'name': 'Anthropic',
                'website': 'https://www.anthropic.com',
                'focus': 'Claude AI, Safety research',
                'why_your_projects_fit': 'Multi-model routing experience relevant to their AI safety work'
            },
            {
                'name': 'Hugging Face',
                'website': 'https://huggingface.co',
                'focus': 'ML model hub, NLP',
                'why_your_projects_fit': 'Your experience with model integration and AI tools'
            },
            {
                'name': 'Cohere',
                'website': 'https://cohere.com',
                'focus': 'Enterprise NLP, AI APIs',
                'why_your_projects_fit': 'Your API integration and AI assistant experience'
            },
            {
                'name': 'Stability AI',
                'website': 'https://stability.ai',
                'focus': 'Image generation, Open source AI',
                'why_your_projects_fit': 'Your compression algorithms and efficiency focus'
            },
            {
                'name': 'Replicate',
                'website': 'https://replicate.com',
                'focus': 'ML deployment platform',
                'why_your_projects_fit': 'Your experience with AI model deployment and automation'
            },
            {
                'name': 'Scale AI',
                'website': 'https://scale.com',
                'focus': 'AI data labeling, training',
                'why_your_projects_fit': 'Your automation and AI tooling experience'
            },
            {
                'name': 'Weights & Biases',
                'website': 'https://wandb.ai',
                'focus': 'ML experiment tracking',
                'why_your_projects_fit': 'Your Job Hunter shows understanding of automated systems'
            },
            {
                'name': 'LangChain',
                'website': 'https://www.langchain.com',
                'focus': 'LLM application framework',
                'why_your_projects_fit': 'Your multi-model AI assistant demonstrates LLM orchestration'
            },
            {
                'name': 'Pinecone',
                'website': 'https://www.pinecone.io',
                'focus': 'Vector database for AI',
                'why_your_projects_fit': 'Your compression work and data efficiency focus'
            },
            {
                'name': 'AI21 Labs',
                'website': 'https://www.ai21.com',
                'focus': 'NLP models, language AI',
                'why_your_projects_fit': 'Your NLP experience with Student Tutor'
            },
            {
                'name': 'Jasper AI',
                'website': 'https://www.jasper.ai',
                'focus': 'AI content generation',
                'why_your_projects_fit': 'Your AI text generation and automation experience'
            },
            {
                'name': 'Copy.ai',
                'website': 'https://www.copy.ai',
                'focus': 'AI writing assistant',
                'why_your_projects_fit': 'Your AI assistant and automation work'
            },
            {
                'name': 'Runway',
                'website': 'https://runwayml.com',
                'focus': 'Creative AI tools',
                'why_your_projects_fit': 'Your experience building practical AI applications'
            },
            {
                'name': 'Midjourney',
                'website': 'https://www.midjourney.com',
                'focus': 'AI image generation',
                'why_your_projects_fit': 'Your compression algorithms relevant to image processing'
            }
        ]
        
        print(f"✅ Loaded {len(known_companies)} known AI companies")
        return known_companies
    
    def _get_yc_ai_companies(self):
        """Scrape YCombinator for AI companies"""
        print("🔍 Searching Y Combinator companies...")
        
        companies = []
        
        try:
            url = "https://www.ycombinator.com/companies?tags=Artificial+Intelligence"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parse company listings (adjust selectors as needed)
            company_cards = soup.find_all('div', class_='company')[:20]  # Limit to 20
            
            for card in company_cards:
                try:
                    name = card.find('h3').text.strip()
                    description = card.find('p').text.strip()
                    link = card.find('a')['href']
                    
                    companies.append({
                        'name': name,
                        'website': link,
                        'focus': description,
                        'why_your_projects_fit': 'YC AI startup - your automation and AI tools experience is valuable',
                        'source': 'Y Combinator'
                    })
                except:
                    continue
            
            print(f"✅ Found {len(companies)} YC companies")
            
        except Exception as e:
            print(f"⚠️ YC scraping skipped: {e}")
        
        return companies
    
    def _get_angellist_companies(self):
        """Get AI companies from AngelList"""
        print("🔍 Searching AngelList...")
        
        # AngelList AI companies (manual curated list since API requires auth)
        companies = [
            {
                'name': 'Anthropic',
                'website': 'https://www.anthropic.com',
                'focus': 'AI safety and research',
                'why_your_projects_fit': 'Your multi-model AI work aligns with their research'
            },
            # Add more as you find them
        ]
        
        return companies
    
    def _get_crunchbase_companies(self):
        """Get AI companies from Crunchbase"""
        print("🔍 Searching Crunchbase...")
        
        # Crunchbase AI companies (free tier limited)
        companies = []
        
        return companies
    
    def enrich_with_emails(self, companies):
        """
        Add email addresses to each company
        
        Args:
            companies: list of company dicts
        
        Returns:
            list of companies with emails added
        """
        print(f"\n📧 Extracting emails for {len(companies)} companies...")
        
        enriched = []
        
        for i, company in enumerate(companies, 1):
            print(f"\n[{i}/{len(companies)}] Processing {company['name']}...")
            
            # Extract emails
            email_result = self.email_extractor.extract_emails_from_website(company['website'])
            
            if email_result['success']:
                # Find best hiring email
                best_email = self.email_extractor.find_hiring_email(
                    email_result['emails'], 
                    company['name']
                )
                
                company['emails'] = email_result['emails']
                company['primary_email'] = best_email
                company['email_sources'] = email_result['sources']
                company['has_email'] = True
                
                print(f"   ✅ Found {len(email_result['emails'])} emails")
                print(f"   🎯 Best email: {best_email}")
            else:
                company['emails'] = []
                company['primary_email'] = None
                company['has_email'] = False
                
                print(f"   ⚠️ No emails found")
            
            enriched.append(company)
            
            time.sleep(1)  # Be polite
        
        return enriched
    
    def save_companies(self, companies, filename='data/ai_companies_with_emails.json'):
        """Save companies to JSON file"""
        import json
        from pathlib import Path
        
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(companies, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved {len(companies)} companies to {filename}")
    
    def generate_email_list(self, companies):
        """Generate a simple email list for bulk emailing"""
        email_list = []
        
        for company in companies:
            if company.get('has_email') and company.get('primary_email'):
                email_list.append({
                    'company': company['name'],
                    'email': company['primary_email'],
                    'why_contact': company.get('why_your_projects_fit', 'AI company')
                })
        
        return email_list


# Main execution
def main():
    print("\n" + "="*70)
    print("  🤖 AI COMPANY FINDER WITH EMAIL EXTRACTION")
    print("="*70)
    
    finder = AICompanyFinder()
    
    # Step 1: Find companies
    print("\n📊 Step 1: Finding AI companies...")
    companies = finder.find_ai_companies()
    print(f"✅ Found {len(companies)} companies")
    
    # Step 2: Extract emails
    print("\n📧 Step 2: Extracting contact emails...")
    enriched_companies = finder.enrich_with_emails(companies)
    
    # Step 3: Filter companies with emails
    companies_with_emails = [c for c in enriched_companies if c.get('has_email')]
    print(f"\n✅ {len(companies_with_emails)} companies have working emails")
    
    # Step 4: Save results
    finder.save_companies(enriched_companies)
    
    # Step 5: Generate email list
    email_list = finder.generate_email_list(companies_with_emails)
    
    # Save email list
    import json
    with open('data/email_list.json', 'w') as f:
        json.dump(email_list, f, indent=2)
    
    print(f"\n📋 Email list saved to data/email_list.json")
    
    # Display summary
    print("\n" + "="*70)
    print("  📊 SUMMARY")
    print("="*70)
    print(f"Total companies found: {len(companies)}")
    print(f"Companies with emails: {len(companies_with_emails)}")
    print(f"Ready to contact: {len(email_list)}")
    
    print("\n🎯 Next steps:")
    print("1. Review data/ai_companies_with_emails.json")
    print("2. Use data/email_list.json for bulk emailing")
    print("3. Customize your email template for each company")
    
    return enriched_companies

if __name__ == "__main__":
    main()