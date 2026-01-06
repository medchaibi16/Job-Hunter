"""
    Simple Email Rewriter using Gemini API
"""

import google.generativeai as genai
from config.ai_config import REWRITER_CONFIG, GEMINI_CONFIG

class SimpleEmailRewriter:
    def __init__(self):
        # Always use Gemini
        if GEMINI_CONFIG["enabled"] and GEMINI_CONFIG["api_key"]:
            genai.configure(api_key=GEMINI_CONFIG["api_key"])
            self.model = genai.GenerativeModel(GEMINI_CONFIG["model"])
            self.initialized = True
            print("✅ Gemini rewriter initialized")
        else:
            self.initialized = False
            print("⚠️ Gemini not configured - rewriter disabled")
    
    def enhance_email(self, email_text):
        """
        Enhance/rewrite the email to make it more professional
        
        Args:
            email_text: The email draft written by user
        
        Returns:
            dict with enhanced email
        """
        if not self.initialized:
            return {
                "success": False,
                "enhanced_email": email_text,
                "message": "⚠️ Gemini not configured. Please add API key to config/ai_config.py"
            }
        
        print("\n✨ Enhancing email with Gemini...")
        print("=" * 60)
        
        try:
            prompt = f"""You are helping someone improve their job application email.

Original email:
{email_text}

Please enhance this email to make it:
1. More professional and polished
2. Clear and concise
3. Confident but not arrogant
4. Natural and human-sounding (not robotic)
5. Fix any grammar or spelling errors
6. Keep the same core message and structure

IMPORTANT: 
- Keep it under 300 words
- Don't change the meaning or add false information
- Keep the friendly, genuine tone
- Make it sound natural, not AI-generated

Return ONLY the enhanced email, nothing else."""

            print("📡 Sending to Gemini for enhancement...")
            response = self.model.generate_content(prompt)
            
            enhanced = response.text.strip()
            
            print("✅ Email enhanced!")
            print("=" * 60)
            
            return {
                "success": True,
                "enhanced_email": enhanced,
                "message": "✅ Email enhanced successfully with Gemini!"
            }
        
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return {
                "success": False,
                "enhanced_email": email_text,
                "message": f"Enhancement failed: {str(e)}"
            }


# Test function
def test_rewriter():
    rewriter = SimpleEmailRewriter()
    
    test_email = """Hi,

I saw your job posting and I think I would be good for it. I have done some projects with AI and Python. I made a student tutor app and a compression tool.

Can we talk about this job?

Thanks,
Mohamed"""

    result = rewriter.enhance_email(test_email)
    
    print("\n" + "=" * 60)
    print("ORIGINAL EMAIL:")
    print("=" * 60)
    print(test_email)
    
    print("\n" + "=" * 60)
    print("ENHANCED EMAIL:")
    print("=" * 60)
    print(result["enhanced_email"])
    print("\n" + "=" * 60)
    print(f"Status: {result['message']}")

if __name__ == "__main__":
    test_rewriter()