
from app.config import (
    EMOTION_AI_KEYWORDS, 
    ROLE_KEYWORDS, 
    TECHNICAL_KEYWORDS,
    RESEARCH_KEYWORDS,
    ADOPTION_KEYWORDS,
    SCORING_WEIGHTS,
    PREFERENCES,
    CITIZENSHIP_BLOCKERS,
    LOCATION_REQUIREMENT_BLOCKERS,
    EXPERIENCE_BLOCKERS,
)

def count_keyword_matches(text, keywords):
    """Count how many keywords appear in text"""
    text_lower = text.lower()
    matches = []
    for keyword in keywords:
        if keyword.lower() in text_lower:
            matches.append(keyword)
    return matches

def check_citizenship_blocker(job):
    """
    Check if job has citizenship requirements that block Tunisians
    Returns (is_blocked, reason)
    """
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    full_text = f"{title} {description}"
    
    for blocker in CITIZENSHIP_BLOCKERS:
        if blocker.lower() in full_text:
            return True, f"Citizenship requirement: {blocker}"
    
    return False, None

def check_location_blocker(job):
    """
    Check if job requires onsite/relocation (blocks remote)
    Returns (is_blocked, reason)
    """
    location = job.get("location", "").lower()
    description = job.get("description", "").lower()
    full_text = f"{location} {description}"
    
    for blocker in LOCATION_REQUIREMENT_BLOCKERS:
        if blocker.lower() in full_text:
            return True, f"Location requirement: {blocker}"
    
    return False, None

def check_experience_blocker(job):
    """
    Check if job requires excessive experience
    Returns (is_blocked, reason)
    """
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    full_text = f"{title} {description}"
    
    for blocker in EXPERIENCE_BLOCKERS:
        if blocker.lower() in full_text:
            return True, f"Experience requirement: {blocker}"
    
    return False, None

def score_job(job):
    """
    Score a job and categorize it
    Returns score (0-100), breakdown, and category
    """
    # CRITICAL CHECKS FIRST
    citizenship_blocked, citizenship_reason = check_citizenship_blocker(job)
    location_blocked, location_reason = check_location_blocker(job)
    experience_blocked, experience_reason = check_experience_blocker(job)
    
    breakdown = {
        "emotion_keywords": [],
        "research_keywords": [],
        "adoption_keywords": [],
        "role_keywords": [],
        "technical_keywords": [],
        "location_match": False,
        "remote_available": False,
        "blocked": False,
        "block_reason": None,
        "category": "uncategorized",
    }
    
    # Instant disqualification
    if citizenship_blocked or location_blocked or experience_blocked:
        breakdown["blocked"] = True
        breakdown["block_reason"] = citizenship_reason or location_reason or experience_reason
        return 0, breakdown
    
    title = job.get("title", "").lower()
    company = job.get("company", "").lower()
    location = job.get("location", "").lower()
    description = job.get("description", "").lower()
    full_text = f"{title} {company} {location} {description}"
    
    score = 0
    
    # Emotion AI keywords
    emotion_matches = count_keyword_matches(full_text, EMOTION_AI_KEYWORDS)
    breakdown["emotion_keywords"] = emotion_matches
    score += len(emotion_matches) * SCORING_WEIGHTS["emotion_keyword_match"]
    
    # Research keywords
    research_matches = count_keyword_matches(full_text, RESEARCH_KEYWORDS)
    breakdown["research_keywords"] = research_matches
    score += len(research_matches) * SCORING_WEIGHTS["research_bonus"]
    
    # Adoption keywords
    adoption_matches = count_keyword_matches(full_text, ADOPTION_KEYWORDS)
    breakdown["adoption_keywords"] = adoption_matches
    score += len(adoption_matches) * SCORING_WEIGHTS["adoption_bonus"]
    
    # Role keywords
    role_matches = count_keyword_matches(full_text, ROLE_KEYWORDS)
    breakdown["role_keywords"] = role_matches
    score += len(role_matches) * SCORING_WEIGHTS["role_keyword_match"]
    
    # Technical keywords
    tech_matches = count_keyword_matches(full_text, TECHNICAL_KEYWORDS)
    breakdown["technical_keywords"] = tech_matches
    score += len(tech_matches) * SCORING_WEIGHTS["technical_keyword_match"]
    
    # Remote check
    if "remote" in location or "remote" in full_text:
        breakdown["remote_available"] = True
        score += SCORING_WEIGHTS["remote_available"]
    
    # Location check
    for allowed_loc in PREFERENCES["allowed_locations"]:
        if allowed_loc.lower() in location:
            breakdown["location_match"] = True
            score += SCORING_WEIGHTS["location_match"]
            break
    
    # Determine category
    if len(emotion_matches) > 0:
        breakdown["category"] = "emotion_ai"
    elif len(research_matches) > 0:
        breakdown["category"] = "research"
    elif len(adoption_matches) > 0:
        breakdown["category"] = "adoption"
    else:
        breakdown["category"] = "general_ai"
    
    normalized_score = min(100, int((score / 150) * 100))
    
    return normalized_score, breakdown

def calculate_success_chance(job, score):
    """Calculate estimated success chance"""
    base_chance = score * 0.6
    
    title = job.get("title", "").lower()
    
    if "emotion" in title or "affective" in title:
        base_chance += 15
    
    if "senior" in title or "lead" in title:
        base_chance -= 20
    
    if "research" in title:
        base_chance += 10
    
    return max(10, min(95, int(base_chance)))

