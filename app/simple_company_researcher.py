"""
Simple Company Researcher using FREE Gemini API
"""

import google.generativeai as genai
from config.ai_config import GEMINI_CONFIG
import time

class SimpleCompanyResearcher:
    def __init__(self):
        if GEMINI_CONFIG["enabled"] and GEMINI_CONFIG["api_key"]:
            genai.configure(api_key=GEMINI_CONFIG["api_key"])
            self.model = genai.GenerativeModel(GEMINI_CONFIG["model"])
            self.enabled = True
            print("✅ Gemini researcher initialized")
        else:
            self.enabled = False
            print("⚠️ Gemini not configured - company research disabled")
    
    def research_company(self, company_name, job_title, job_url=""):
        """
        Research company using Gemini
        
        Returns:
            dict with company information formatted for display
        """
        if not self.enabled:
            return {
                "success": False,
                "research": "⚠️ Gemini API not configured. Add your API key to config/ai_config.py",
                "raw_data": {}
            }
        
        print(f"\n🔍 Researching: {company_name}")
        print("=" * 60)
        
        try:
            prompt = f"""Research this company and provide useful information for writing a job application email:

Company: {company_name}
Position: {job_title}
{f'Job URL: {job_url}' if job_url else ''}

Please provide:
1. What does this company do? (1-2 sentences)
2. Their main products or services
3. Recent news or achievements (if known)
4. Company culture or values (if known)
5. Why someone would want to work there

Format your response clearly with headers.
Be concise and focus on information useful for a job application.
If you don't have specific information, say so clearly."""

            print("📡 Sending request to Gemini...")
            response = self.model.generate_content(prompt)
            
            research_text = response.text.strip()
            
            print("✅ Research complete!")
            print("=" * 60)
            
            return {
                "success": True,
                "research": research_text,
                "company": company_name,
                "position": job_title,
                "raw_data": {
                    "company": company_name,
                    "position": job_title,
                    "url": job_url
                }
            }
        
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return {
                "success": False,
                "research": f"⚠️ Could not research company: {str(e)}",
                "raw_data": {}
            }


# Test function
def test_researcher():
    researcher = SimpleCompanyResearcher()
    result = researcher.research_company(
        "DeepMind",
        "AI Research Intern",
        "https://deepmind.com/careers"
    )
    
    print("\n" + "=" * 60)
    print("RESEARCH RESULT:")
    print("=" * 60)
    print(result["research"])

if __name__ == "__main__":
    test_researcher()