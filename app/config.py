
PROFILE = {
    "full_name": "Mohamed Chaibi",
    "country": "Tunisia",
    "city": "Monastir",
    "email": "medchaibi965@proton.me",
    "timezone": "GMT+1",
    "availability": "Full-time",
    "education": "Computer Science Student",
    "experience_level": "Entry Level / Student",
    "linkedin": "www.linkedin.com/in/mohamed-chaibi-6037583a0",
    "portfolio": "https://github.com/medchaibi16/medchaibi16",
}

# 🌍 CITIZENSHIP & LOCATION FILTERS (STRICT)
CITIZENSHIP_BLOCKERS = [
    # US Citizenship Required
    "us citizen", "us citizenship", "american citizen", "u.s. citizen",
    "must be a us citizen", "requires us citizenship",
    
    # US Work Authorization
    "us work authorization", "work authorization in the us",
    "authorized to work in the us", "requires us authorization",
    
    # Canada Citizenship
    "canadian citizen", "canada citizen", "canadian citizenship",
    "must be canadian", "requires canadian citizenship",
    
    # Other restricted countries (add as needed)
    "uk citizen required", "british citizen required",
]

LOCATION_REQUIREMENT_BLOCKERS = [
    # Onsite/Relocation Required
    "on-site only", "onsite only", "no remote", "on site only",
    "relocation required", "must relocate", "willing to relocate",
    "must be willing to relocate", "local only", "on premises",
    "physically present", "in-office required",
]

EXPERIENCE_BLOCKERS = [
    "senior", "lead", "staff", "principal",
    "5+ years", "10+ years", "7+ years", "8+ years",
    "phd required", "doctorate required", "phd mandatory",
    "master's degree required", "m.sc required",
]

# Emotional AI keywords
EMOTION_AI_KEYWORDS = [
    "emotion", "emotional", "emotions", "affective", "affect", "sentiment", 
    "feeling", "feelings", "mood", "moods",
    "facial expression", "face recognition", "facial analysis", "face detection",
    "expression recognition", "micro-expression", "facial coding",
    "speech emotion", "voice emotion", "prosody", "vocal affect",
    "text emotion", "emotion classification", "emotion detection",
    "physiological signals", "biosignal", "eeg emotion", "heart rate variability",
    "computer vision", "cv", "image recognition", "video analysis",
    "natural language processing", "nlp", "text analysis", "sentiment analysis",
    "deep learning", "neural network", "cnn", "rnn", "lstm", "transformer",
    "machine learning", "ml", "pattern recognition",
    "human-computer interaction", "hci", "user experience", "ux research",
    "human-centered ai", "human-ai interaction", "social robotics",
    "mental health", "wellbeing", "psychological", "behavioral analysis",
    "customer experience", "user engagement", "personalization",
    "opencv", "tensorflow", "pytorch", "keras", "scikit-learn",
    "facial landmark", "action unit", "fer", "multimodal",
    "affective computing", "computational psychology", "emotion ai",
    "emotion understanding", "empathetic ai", "emotional intelligence",
    "social signal processing", "behavioral computing",
]

# Research keywords
RESEARCH_KEYWORDS = [
    "research", "research intern", "research assistant",
    "research project", "research collaboration",
    "funded research", "research grant",
    "academic collaboration", "industry partnership",
    "thesis", "master thesis", "student project",
    "open research", "call for proposals",
    "innovation lab", "r&d", "applied research",
    "lab intern", "supervised research", "publication opportunity",
    "peer-reviewed", "academic journal", "conference publication",
]

# Innovation/Adoption keywords
ADOPTION_KEYWORDS = [
    "adopt", "adoption", "idea adoption",
    "student idea", "student project",
    "prototype", "proof of concept", "poc",
    "innovation challenge", "hackathon winner",
    "incubation", "accelerator",
    "funding available", "stipend", "grant",
    "paid research", "sponsored project",
    "open innovation", "idea proposal",
    "startup", "venture", "startup program",
]

# Job role keywords
ROLE_KEYWORDS = [
    "intern", "internship", "student", "junior", "entry level",
    "graduate", "trainee", "apprentice", "co-op", "stage",
    "student project", "idea proposal", "innovation challenge",
]

# Technical skills
TECHNICAL_KEYWORDS = [
    "python", "machine learning", "deep learning", "ai", "artificial intelligence",
    "computer vision", "nlp", "data science", "research", "opencv",
    "tensorflow", "pytorch", "backend", "api", "automation",
]

# 🌍 LOCATION ACCEPTANCE PATTERNS (Tunisian-friendly)
LOCATION_ACCEPT_PATTERNS = [
    # Remote first
    "remote", "fully remote", "work from home", "distributed",
    
    # EMEA/EU friendly
    "emea", "europe", "european", "eu based", "eu timezone",
    "worldwide", "global", "international", "anywhere",
    
    # No specific country requirement
    "no location restriction", "location independent",
]

PREFERENCES = {
    "role_type": "Internship",
    "work_mode": ["Remote"],
    "min_duration_months": 3,
    "max_duration_months": 12,
    
    "fields": [
        "emotion recognition",
        "affective computing", 
        "sentiment analysis",
        "facial expression recognition",
        "emotion AI",
        "human-centered AI",
        "computer vision",
        "speech emotion recognition",
        "behavioral analysis",
        "empathetic AI",
        "emotional intelligence AI",
        "multimodal emotion",
        "mental health AI",
        "social signal processing",
    ],
    
    "allowed_locations": [
        "remote",
        "tunisia",
        "monastir",
        "sousse",
        "tunis",
        "sfax",
        "emea",
        "europe",
    ],
    
    "blocked_keywords": [
        *CITIZENSHIP_BLOCKERS,
        *LOCATION_REQUIREMENT_BLOCKERS,
        *EXPERIENCE_BLOCKERS,
    ],
    
    "accepts_unpaid": True,
    "accepts_paid": True,
    "min_monthly_salary": 0,
}

JOB_BOARDS = {
    "linkedin": {
        "enabled": True,
        "base_url": "https://www.linkedin.com/jobs/search",
        "search_queries": [
            "AI research intern",
            "machine learning intern",
            "computer vision intern",
            "NLP intern",
            "AI intern remote",
            "deep learning intern",
            "research intern AI",
            "data science intern AI",
        ]
    },
    "research_gate": {
        "enabled": True,
        "type": "research",
        "base_url": "https://www.researchgate.net/jobs",
        "search_queries": [
            "AI research intern",
            "computer vision research",
            "machine learning research",
        ]
    },
    "academic_jobs": {
        "enabled": True,
        "type": "research",
        "base_url": "https://www.jobs.ac.uk/search",
        "search_queries": [
            "AI intern",
            "research assistant AI",
            "computer science intern",
        ]
    },
}

SCORING_WEIGHTS = {
    "emotion_keyword_match": 5,
    "role_keyword_match": 3,
    "technical_keyword_match": 2,
    "remote_available": 10,
    "location_match": 8,
    "company_size_bonus": 5,
    "research_bonus": 8,
    "adoption_bonus": 10,
    "description_richness": 3,
}

MIN_DISPLAY_SCORE = 10
SEARCH_INTERVAL_SECONDS = 3600