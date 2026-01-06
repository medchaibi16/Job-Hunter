"""
Load environment variables from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Flask Config
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Job Search Settings
SEARCH_INTERVAL_MINUTES = int(os.getenv('SEARCH_INTERVAL_MINUTES', '10'))
AUTO_SEARCH_ENABLED = os.getenv('AUTO_SEARCH_ENABLED', 'True').lower() == 'true'

# Profile
PROFILE_NAME = os.getenv('PROFILE_NAME', 'Mohamed Chaibi')
PROFILE_EMAIL = os.getenv('PROFILE_EMAIL', 'medchaibi965@proton.me')
PROFILE_GITHUB = os.getenv('PROFILE_GITHUB', 'github.com/medchaibi16')
PROFILE_COUNTRY = os.getenv('PROFILE_COUNTRY', 'Tunisia')

# Validation
if not GEMINI_API_KEY and FLASK_ENV == 'production':
    raise ValueError("GEMINI_API_KEY must be set in .env file for production!")

print(f"✅ Environment loaded: {FLASK_ENV}")
if AUTO_SEARCH_ENABLED:
    print(f"🔄 Auto-search enabled: Every {SEARCH_INTERVAL_MINUTES} minutes")