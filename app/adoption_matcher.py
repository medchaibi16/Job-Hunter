# app/adoption_matcher.py
# Specialized matcher for adoption/innovation program opportunities

from app.config import PREFERENCES, MIN_DISPLAY_SCORE
from app.score import (
    count_keyword_matches,
    check_citizenship_blocker,
    check_location_blocker,
    check_experience_blocker,
)

ADOPTION_SPECIFIC_KEYWORDS = [
    # Startup/innovation keywords
    "startup", "accelerator", "incubator", "venture",
    "innovation lab", "innovation challenge", "hackathon",
    "proof of concept", "poc", "prototype", "beta",
    
    # Project/idea keywords
    "student idea", "student project", "project proposal",
    "idea submission", "proposal", "pitch", "competition",
    
    # Funding/support keywords
    "funding available", "grant", "grant funding", "budget",
    "sponsored", "stipend", "award", "prize",
    
    # Community/open keywords
    "open innovation", "open source", "community driven",
    "collaborative", "partnership", "ecosystem",
    
    # Program keywords
    "program", "fellowship", "scholar", "development program",
    "mentorship", "mentoring", "coaching",
    
    # Remote/flexible keywords
    "flexible", "autonomous", "self-directed", "independent project",
    "work from anywhere", "distributed team",
]

ADOPTION_COMPANY_KEYWORDS = [
    # Known adoption-focused platforms
    "devpost", "hackerearth", "ideascale", "challengepost",
    "mlh", "major league hacking",
    "y combinator", "techstars", "plug and play",
    "500 global", "anterra capital",
    
    # Accelerator/incubator names
    "accelerator", "incubator", "startup studio",
    "venture studio", "innovation hub",
    
    # Research institution keywords
    "mit", "stanford", "carnegie mellon", "berkeley",
    "oxford", "cambridge", "eth zurich",
    "alan turing", "deepmind", "openai", "meta ai",
    "google research", "bell labs",
    
    # Grant/funding organizations
    "nserc", "nsf", "erasmus", "horizon europe",
    "google summer of code", "outreachy",
    "linux foundation", "mozilla", "apache",
]

def score_adoption_opportunity(opportunity):
    """
    Score adoption opportunities with specialized criteria
    Returns score (0-100) and breakdown
    """
    
    title = opportunity.get("title", "").lower()
    company = opportunity.get("company", "").lower()
    location = opportunity.get("location", "").lower()
    description = opportunity.get("description", "").lower()
    source = opportunity.get("source", "").lower()
    
    full_text = f"{title} {company} {location} {description} {source}"
    
    score = 0
    breakdown = {
        "adoption_keywords": [],
        "company_keywords": [],
        "location_match": False,
        "remote_available": False,
        "blocked": False,
        "block_reason": None,
        "adoption_type": "general",
    }
    
    # CRITICAL CHECKS FIRST
    citizenship_blocked, citizenship_reason = check_citizenship_blocker(opportunity)
    location_blocked, location_reason = check_location_blocker(opportunity)
    experience_blocked, experience_reason = check_experience_blocker(opportunity)
    
    if citizenship_blocked or location_blocked or experience_blocked:
        breakdown["blocked"] = True
        breakdown["block_reason"] = citizenship_reason or location_reason or experience_reason
        return 0, breakdown
    
    # Adoption-specific keywords (highest priority)
    adoption_matches = count_keyword_matches(full_text, ADOPTION_SPECIFIC_KEYWORDS)
    breakdown["adoption_keywords"] = adoption_matches
    score += len(adoption_matches) * 8  # Higher weight for adoption keywords
    
    # Company/platform keywords
    company_matches = count_keyword_matches(full_text, ADOPTION_COMPANY_KEYWORDS)
    breakdown["company_keywords"] = company_matches
    score += len(company_matches) * 5
    
    # Remote check
    if "remote" in location or "remote" in full_text or "online" in location or "global" in location:
        breakdown["remote_available"] = True
        score += 12
    
    # Location check
    for allowed_loc in PREFERENCES["allowed_locations"]:
        if allowed_loc.lower() in location:
            breakdown["location_match"] = True
            score += 8
            break
    
    # Check adoption signals from hunter
    adoption_signals = opportunity.get("adoption_signals", [])
    score += len(adoption_signals) * 3
    
    # Determine adoption type
    if "hackathon" in full_text or "challenge" in full_text:
        breakdown["adoption_type"] = "hackathon"
    elif "accelerator" in full_text or "incubator" in full_text:
        breakdown["adoption_type"] = "accelerator"
    elif "grant" in full_text or "funding" in full_text:
        breakdown["adoption_type"] = "funding"
    elif "summer" in full_text or "google" in full_text or "outreachy" in full_text:
        breakdown["adoption_type"] = "program"
    elif "open source" in full_text or "github" in full_text:
        breakdown["adoption_type"] = "open_source"
    else:
        breakdown["adoption_type"] = "innovation"
    
    # Bonus for paid opportunities
    if "paid" in full_text or "stipend" in full_text or "salary" in full_text or "award" in full_text:
        score += 10
        breakdown["paid"] = True
    else:
        breakdown["paid"] = False
    
    normalized_score = min(100, int((score / 100) * 100))
    
    return normalized_score, breakdown


def generate_adoption_explanation(opportunity, breakdown):
    """Generate detailed explanation for adoption opportunities"""
    explanation_parts = []
    adoption_type = breakdown.get("adoption_type", "innovation")
    
    type_descriptions = {
        "hackathon": " Hackathon/Competition - Great for quickly building and showcasing AI prototypes!",
        "accelerator": " Startup Accelerator - Perfect for turning your AI ideas into a real startup with mentorship and funding!",
        "funding": " Funded Research Program - Your ideas can receive grants and resources to develop them further!",
        "program": " Structured Program - Established program with comprehensive support for student projects!",
        "open_source": " Open Source Community - Contribute your AI ideas to open source and get recognized globally!",
        "innovation": " Innovation Initiative - Companies actively seeking creative AI solutions and student ideas!",
    }
    
    explanation_parts.append(type_descriptions.get(adoption_type, "💡 Innovation Opportunity"))
    
    # Highlight adoption keywords
    if len(breakdown["adoption_keywords"]) > 0:
        keywords = breakdown["adoption_keywords"][:3]
        keywords_str = ", ".join(keywords)
        explanation_parts.append(
            f"Focus areas: {keywords_str}"
        )
    
    # Remote advantage
    if breakdown.get("remote_available"):
        explanation_parts.append(
            " Fully remote - Perfect for working from Tunisia while developing your AI project!"
        )
    
    # Paid opportunity highlight
    if breakdown.get("paid"):
        explanation_parts.append(
            "This is a paid opportunity with stipend/award!"
        )
    
    # Platform/company emphasis
    if len(breakdown["company_keywords"]) > 0:
        company = breakdown["company_keywords"][0]
        explanation_parts.append(
            f"✨ {company.title()} is a recognized platform for innovation and idea adoption"
        )
    
    # Call to action
    explanation_parts.append(
        "Your AI project ideas could be developed, funded, or showcased here!"
    )
    
    full_explanation = " | ".join(explanation_parts)
    
    if len(full_explanation) > 700:
        full_explanation = full_explanation[:697] + "..."
    
    return full_explanation


def analyze_adoption_opportunity(opportunity):
    """Deep analysis of adoption opportunity"""
    score, breakdown = score_adoption_opportunity(opportunity)
    
    if breakdown.get("blocked"):
        return None
    
    explanation = generate_adoption_explanation(opportunity, breakdown)
    
    adoption_type = breakdown.get("adoption_type", "innovation")
    type_label = {
        "hackathon": "Hackathon/Challenge",
        "accelerator": " Accelerator Program",
        "funding": " Funded Program",
        "program": " Formal Program",
        "open_source": " Open Source",
        "innovation": " Innovation Lab",
    }.get(adoption_type, " Innovation")
    
    success_base = score * 0.7
    if adoption_type in ["hackathon", "program"]:
        success_base += 15
    if breakdown.get("paid"):
        success_base += 10
    
    success_chance = max(15, min(95, int(success_base)))
    
    # Recommendation
    if score >= 70:
        recommendation = "🟢 Highly Recommended"
    elif score >= 50:
        recommendation = "🟡 Great Opportunity"
    elif score >= 30:
        recommendation = "🟠 Worth Considering"
    elif score >= MIN_DISPLAY_SCORE:
        recommendation = "⚪ Check It Out"
    else:
        recommendation = "Low Match"
    
    notes = []
    notes.append(type_label)
    if breakdown.get("remote_available"):
        notes.append(" Remote")
    if breakdown.get("paid"):
        notes.append(" Paid")
    if breakdown.get("location_match"):
        notes.append(" Tunisia-friendly")
    
    return {
        "score": score,
        "type": adoption_type,
        "type_label": type_label,
        "notes": " | ".join(notes),
        "detailed_explanation": explanation,
        "success_chance": success_chance,
        "breakdown": breakdown,
        "recommendation": recommendation,
    }


def match_adoption_opportunities(opportunities):
    """
    Filter and analyze adoption opportunities
    Returns only high-quality matches
    """
    matched = []
    
    for opp in opportunities:
        analysis = analyze_adoption_opportunity(opp)
        
        if analysis is None:
            continue
        
        score = analysis["score"]
        
        # Only include if score is reasonable
        if score < MIN_DISPLAY_SCORE:
            continue
        
        opp["score"] = score
        opp["analysis"] = analysis
        matched.append(opp)
    
    # Sort by score
    matched.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    return matched