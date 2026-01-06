from app.config import PREFERENCES, MIN_DISPLAY_SCORE
from app.score import score_job, calculate_success_chance

def categorize_jobs(jobs):
    """
    Categorize jobs into 3 buckets:
    1. Emotion AI Company Internships
    2. Research Internships
    3. Innovation/Adoption Programs
    """
    categories = {
        "emotion_ai": [],
        "research": [],
        "adoption": [],
    }
    
    for job in jobs:
        score, breakdown = score_job(job)
        
        # Skip if blocked or too low score
        if breakdown.get("blocked") or score < MIN_DISPLAY_SCORE:
            continue
        
        # Add analysis
        job["score"] = score
        job["breakdown"] = breakdown
        job["analysis"] = analyze_job(job)
        
        category = breakdown.get("category", "uncategorized")
        
        if category == "emotion_ai":
            categories["emotion_ai"].append(job)
        elif category == "research":
            categories["research"].append(job)
        elif category == "adoption":
            categories["adoption"].append(job)
    
    # Sort each category by score
    for cat in categories:
        categories[cat].sort(key=lambda x: x.get("score", 0), reverse=True)
    
    return categories

def generate_detailed_explanation(job, breakdown):
    """Generate detailed explanation for why job matches"""
    explanation_parts = []
    category = breakdown.get("category", "")
    
    if category == "emotion_ai":
        if len(breakdown["emotion_keywords"]) > 0:
            keywords_str = ", ".join(breakdown["emotion_keywords"][:4])
            explanation_parts.append(
                f"✨ This is a true Emotion AI company opportunity with keywords: {keywords_str}."
            )
        explanation_parts.append(
            "Perfect match for your focus on affective computing and emotion recognition!"
        )
    
    elif category == "research":
        if len(breakdown["research_keywords"]) > 0:
            keywords_str = ", ".join(breakdown["research_keywords"][:3])
            explanation_parts.append(
                f"🔬 Research-focused position with emphasis on: {keywords_str}."
            )
        explanation_parts.append(
            "Excellent opportunity to publish and contribute to academic knowledge in AI."
        )
    
    elif category == "adoption":
        if len(breakdown["adoption_keywords"]) > 0:
            keywords_str = ", ".join(breakdown["adoption_keywords"][:3])
            explanation_parts.append(
                f"💡 Innovation program open to student projects and ideas: {keywords_str}."
            )
        explanation_parts.append(
            "Your ideas could be developed into real products or services!"
        )
    
    # Add common details
    if breakdown.get("remote_available"):
        explanation_parts.append(
            "✅ Fully remote - you can work from Tunisia without any issues."
        )
    
    if breakdown.get("location_match"):
        explanation_parts.append(
            f"✅ Location is compatible with your region (EMEA/Europe friendly)."
        )
    
    requirements = job.get("requirements", [])
    if "Paid internship" in requirements:
        explanation_parts.append("💰 This is a paid opportunity.")
    
    if len(breakdown["technical_keywords"]) > 0:
        tech_str = ", ".join(breakdown["technical_keywords"][:2])
        explanation_parts.append(
            f"🛠️ Uses technologies you're familiar with: {tech_str}."
        )
    
    full_explanation = " ".join(explanation_parts)
    
    if len(full_explanation) > 700:
        full_explanation = full_explanation[:697] + "..."
    
    return full_explanation

def analyze_job(job):
    """Deep analysis of a job posting"""
    score, breakdown = score_job(job)
    detailed_explanation = generate_detailed_explanation(job, breakdown)
    
    category = breakdown.get("category", "")
    category_label = {
        "emotion_ai": "💎 Emotion AI Company",
        "research": "🔬 Research Position",
        "adoption": "💡 Innovation/Adoption",
        "general_ai": "🤖 General AI Role",
    }.get(category, "General Position")
    
    notes = []
    notes.append(category_label)
    
    if breakdown.get("remote_available"):
        notes.append("✅ Remote")
    
    if breakdown.get("location_match"):
        notes.append("✅ EMEA/Tunisia friendly")
    
    return {
        "score": score,
        "category": category,
        "category_label": category_label,
        "notes": " | ".join(notes),
        "detailed_explanation": detailed_explanation,
        "success_chance": calculate_success_chance(job, score),
        "breakdown": breakdown,
        "recommendation": get_recommendation(score),
    }

def get_recommendation(score):
    """Get recommendation level"""
    if score >= 70:
        return "🟢 Highly Recommended"
    elif score >= 50:
        return "🟡 Good Match"
    elif score >= 30:
        return "🟠 Decent Match"
    elif score >= MIN_DISPLAY_SCORE:
        return "⚪ Consider"
    else:
        return "Low Match"

# Keep old match_jobs for compatibility
def match_jobs(jobs):
    """Legacy function - use categorize_jobs instead"""
    categories = categorize_jobs(jobs)
    all_jobs = (
        categories["emotion_ai"] +
        categories["research"] +
        categories["adoption"]
    )
    return all_jobs