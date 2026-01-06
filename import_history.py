"""
Import existing approved/refused decisions into smart memory
"""

from app.storage import load_approved, load_refused

def import_history():
    print("\n" + "="*70)
    print("  🧠 IMPORTING DECISION HISTORY INTO AI MEMORY")
    print("="*70)
    
    # Try full version first, fall back to lite
    try:
        from app.smart_memory import SmartMemory
        memory = SmartMemory()
    except Exception as e:
        print(f"   ℹ️ Using lightweight memory (full version unavailable)")
        from app.smart_memory_lite import SmartMemoryLite
        memory = SmartMemoryLite()
    
    # Import approved
    approved = load_approved()
    print(f"\n📥 Importing {len(approved)} approved jobs...")
    
    for i, job in enumerate(approved, 1):
        try:
            memory.record_decision(job, 'approved')
            print(f"   ✅ {i}/{len(approved)}: {job.get('company')} - {job.get('title')[:80]}")
        except Exception as e:
            print(f"   ⚠️ Failed: {e}")
    
    # Import refused
    refused = load_refused()
    print(f"\n📥 Importing {len(refused)} refused jobs...")
    
    for i, job in enumerate(refused, 1):
        try:
            memory.record_decision(job, 'refused')
            if i <= 5 or i > len(refused) - 5:
                print(f"   ❌ {i}/{len(refused)}: {job.get('company')} - {job.get('title')[:80]}")
            elif i == 6:
                print(f"   ... ({len(refused) - 10} more) ...")
        except Exception as e:
            print(f"   ⚠️ Failed: {e}")
    
    # Summary
    stats = memory.get_memory_stats()
    
    print("\n" + "="*70)
    print("  ✅ IMPORT COMPLETE")
    print("="*70)
    print(f"\n   Total decisions: {stats['total_interactions']}")
    print(f"   Approved: {len(approved)}")
    print(f"   Refused: {len(refused)}")
    
    prefs = stats['learned_preferences']
    if prefs['approved_companies']:
        print(f"\n   ✅ You approved: {', '.join(prefs['approved_companies'])}")
    
    if prefs['top_keywords']:
        top_kw = ', '.join([k[0] for k in prefs['top_keywords'][:5]])
        print(f"   📊 Top keywords: {top_kw}")
    
    print(f"\n   🎉 AI is learning from your preferences!")
    print(f"\n   Run option 8 in run.py to see insights!")

if __name__ == "__main__":
    import_history()