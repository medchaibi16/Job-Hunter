"""
AI API Configuration - Using .env file
"""
from config.env_loader import GEMINI_API_KEY

# ==================== GEMINI API ====================
GEMINI_CONFIG = {
    "api_key": GEMINI_API_KEY,  # Loaded from .env
    "model": "gemini-3-flash-preview",
    "enabled": True
}

# ==================== REWRITER CONFIG ====================
REWRITER_CONFIG = {
    "provider": "gemini",
    
    "gemini": {
        "api_key": GEMINI_API_KEY,  # Same key
        "model": "gemini-3-flash-preview",
        "enabled": True
    }
}

# ==================== ADVANCED SETTINGS ====================
EMAIL_GENERATION_CONFIG = {
    "max_retries": 3,
    "temperature": 0.7,
    "max_tokens": 800,
    "humanization_passes": 2,
    "research_depth": "medium",
    "scrape_company_website": True,
    "include_portfolio_link": True,
    "mention_specific_projects": True,
    "tone": "professional_friendly"
}

# ==================== WEB SCRAPING CONFIG ====================
SCRAPING_CONFIG = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "timeout": 10,
    "max_pages_per_company": 3,
    "respect_robots_txt": True
}