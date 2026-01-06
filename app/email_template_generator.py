"""
Generate personalized email templates for each company
"""

def generate_email_for_company(company):
    """
    Generate personalized email based on company info
    
    Args:
        company: dict with company info
    
    Returns:
        str: personalized email template
    """
    
    template = f"""Subject: Winter/Spring 2025 Remote Internship - CS Student with AI Experience

Hi {company['name']} Team,

I'm Mohamed Chaibi, a final-year CS student from Tunisia specializing in AI systems. I discovered {company['name']}'s work in {company['focus']} and was immediately drawn to your mission.

{company['why_your_projects_fit']}

My recent projects include:
• Student Tutor: Multi-model AI learning assistant (Node.js, Gemini AI, HuggingFace)
  - Implemented intelligent model routing and conversation management
  - Built RESTful API for AI interactions

• dyncompressor: Custom compression system with dynamic algorithm selection (C#)
  - Achieved up to 60% compression improvement through intelligent chunking
  - Demonstrates understanding of optimization and efficiency

• Job Hunter: This autonomous AI agent that found your company!
  - Automated opportunity discovery and matching
  - Shows initiative in building practical tools

I'm seeking a remote internship for Winter/Spring 2025 (January-June) where I can contribute to your AI initiatives while learning from your team.

Portfolio: github.com/medchaibi16
Email: medchaibi965@proton.me
Location: Tunisia (Full remote, UTC+1 timezone)

Would you be open to a brief call to discuss how I might contribute to {company['name']}'s work?

Best regards,
Mohamed Chaibi
"""
    
    return template


def generate_all_emails(companies, output_file='data/generated_emails.txt'):
    """Generate emails for all companies"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for company in companies:
            if company.get('has_email'):
                f.write("=" * 70 + "\n")
                f.write(f"TO: {company['primary_email']}\n")
                f.write(f"COMPANY: {company['name']}\n")
                f.write("=" * 70 + "\n\n")
                
                email = generate_email_for_company(company)
                f.write(email)
                f.write("\n\n\n")
    
    print(f"✅ Generated emails saved to {output_file}") 