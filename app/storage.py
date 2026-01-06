# app/storage.py

from datetime import datetime
import json
import hashlib
from pathlib import Path

# Add smart memory integration
_smart_memory = None

def get_smart_memory():
    """Get or create smart memory instance"""
    global _smart_memory
    if _smart_memory is None:
        try:
            from app.smart_memory import SmartMemory
            _smart_memory = SmartMemory()
        except ImportError:
            # ChromaDB not installed, skip memory features
            _smart_memory = None
    return _smart_memory

# Ensure data directory exists
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

FOUND = DATA_DIR / "found_opportunities.json"
REFUSED = DATA_DIR / "refused.json"
APPROVED = DATA_DIR / "approved.json"
SENT = DATA_DIR / "sent_emails.json"

def job_fingerprint(job):
    """
    Create a stable fingerprint for a job to prevent duplicates
    Based on title + company + location (not URL)
    """
    title = job.get("title", "").strip().lower()
    company = job.get("company", "").strip().lower()
    location = job.get("location", "").strip().lower()

    raw = f"{title}|{company}|{location}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def _load(path):
    """Load JSON data from file"""
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not read {path}, returning empty list")
        return []

def _save(path, data):
    """Save data to JSON file"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to {path}: {e}")

def load_found():
    """Load found opportunities"""
    return _load(FOUND)

def save_opportunity(job):
    """Save a new opportunity to found_opportunities.json"""
    jobs = load_found()
    
    # Add timestamp
    job["found_at"] = datetime.now().isoformat()

    # Generate fingerprint
    fp = job_fingerprint(job)
    job["fingerprint"] = fp

    # Check duplicates by URL OR fingerprint
    existing_fingerprints = {j.get("fingerprint") for j in jobs}
    existing_urls = {j.get("url") for j in jobs}

    if job.get("url") in existing_urls or fp in existing_fingerprints:
        return False  # Duplicate detected
    
    jobs.append(job)
    _save(FOUND, jobs)
    return True

def update_found(jobs):
    """Update the entire found opportunities list"""
    _save(FOUND, jobs)

def load_refused():
    """Load refused jobs"""
    return _load(REFUSED)

def add_refused(job):
    """Add job to refused list AND record in smart memory"""
    data = load_refused()
    job["refused_at"] = datetime.now().isoformat()
    data.append(job)
    _save(REFUSED, data)
    
    # Record in smart memory
    memory = get_smart_memory()
    if memory:
        try:
            memory.record_decision(job, 'refused')
            print(f"   🧠 Recorded refusal in AI memory")
        except Exception as e:
            print(f"   ⚠️ Memory recording failed: {e}")

def load_approved():
    """Load approved jobs"""
    return _load(APPROVED)

def add_approved(job):
    """Add job to approved list AND record in smart memory"""
    data = load_approved()
    job["approved_at"] = datetime.now().isoformat()
    data.append(job)
    _save(APPROVED, data)
    
    # Record in smart memory
    memory = get_smart_memory()
    if memory:
        try:
            memory.record_decision(job, 'approved')
            print(f"   🧠 Recorded approval in AI memory")
        except Exception as e:
            print(f"   ⚠️ Memory recording failed: {e}")

def load_sent():
    """Load sent emails log"""
    return _load(SENT)

def add_sent(job, email_content):
    """Log a sent email"""
    data = load_sent()
    entry = {
        "job": job,
        "email": email_content,
        "sent_at": datetime.now().isoformat()
    }
    data.append(entry)
    _save(SENT, data)

def clear_found():
    """Clear all found opportunities (useful for testing)"""
    _save(FOUND, [])

def get_stats():
    """Get statistics about the job hunting"""
    return {
        "found": len(load_found()),
        "refused": len(load_refused()),
        "approved": len(load_approved()),
        "sent": len(load_sent()),
    }

def remove_refused_from_found():
    """
    Remove all refused opportunities from found_opportunities.json
    This prevents refused jobs from reappearing
    """
    # Load both files
    found = load_found()
    refused = load_refused()
    
    if not refused:
        print("✅ No refused opportunities to clean up")
        return
    
    # Create set of refused fingerprints for fast lookup
    refused_fingerprints = {job.get('fingerprint') for job in refused if job.get('fingerprint')}
    
    # Filter out refused opportunities
    original_count = len(found)
    cleaned = [job for job in found if job.get('fingerprint') not in refused_fingerprints]
    removed_count = original_count - len(cleaned)
    
    if removed_count > 0:
        # Save cleaned list
        update_found(cleaned)
        print(f"🧹 Removed {removed_count} refused opportunities from found list")
        print(f"📊 {len(cleaned)} opportunities remaining")
    else:
        print("✅ No refused opportunities found in current list")
    
    return removed_count


def clean_all_duplicates():
    """
    Remove duplicates from found_opportunities.json based on fingerprint
    """
    found = load_found()
    
    seen_fingerprints = set()
    unique_jobs = []
    duplicates = 0
    
    for job in found:
        fingerprint = job.get('fingerprint')
        if fingerprint and fingerprint not in seen_fingerprints:
            seen_fingerprints.add(fingerprint)
            unique_jobs.append(job)
        else:
            duplicates += 1
    
    if duplicates > 0:
        update_found(unique_jobs)
        print(f"🧹 Removed {duplicates} duplicate opportunities")
        print(f"📊 {len(unique_jobs)} unique opportunities remaining")
    else:
        print("✅ No duplicates found")
    
    return duplicates