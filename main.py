# main.py (UPDATED)
# Enhanced pipeline with adoption hunter integration

import json
from pathlib import Path
from core.parser import clean_opportunities
from app.matcher import match_jobs, categorize_jobs
from app.adoption_hunter import search_adoption_opportunities
from app.adoption_matcher import match_adoption_opportunities
from app.storage import load_found, update_found, save_opportunity

def run_full_pipeline():
    """
    Complete job hunting pipeline:
    1. Search regular job boards
    2. Search adoption/innovation opportunities
    3. Clean and deduplicate
    4. Match and score
    5. Categorize
    6. Save results
    """
    
    print("\n" + "="*70)
    print(" FULL PIPELINE - SEARCH + PROCESS + CATEGORIZE")
    print("="*70 + "\n")
    
    # ========== STEP 1: SEARCH ADOPTION OPPORTUNITIES ==========
    print("\n[STEP 1/4] Searching for AI adoption opportunities...\n")
    
    adoption_opps = search_adoption_opportunities()
    print(f"\n✓ Found {len(adoption_opps)} adoption opportunities\n")
    
    # Save adoption opportunities to storage
    for opp in adoption_opps:
        save_opportunity(opp)
    
    # ========== STEP 2: LOAD ALL FOUND OPPORTUNITIES ==========
    print("[STEP 2/4] Loading all opportunities from storage...\n")
    
    raw_jobs = load_found()
    print(f"✓ Loaded {len(raw_jobs)} total opportunities from storage\n")
    
    # ========== STEP 3: CLEAN OPPORTUNITIES ==========
    print("[STEP 3/4] Cleaning and deduplicating opportunities...\n")
    
    clean = clean_opportunities(raw_jobs)
    print(f"✓ Cleaned: {len(clean)} unique opportunities\n")
    
    # ========== STEP 4: MATCH AND CATEGORIZE ==========
    print("[STEP 4/4] Matching, scoring, and categorizing opportunities...\n")
    
    # Match regular jobs
    matched_regular = match_jobs(clean)
    print(f"  • Regular jobs matched: {len(matched_regular)}")
    
    # Match adoption opportunities specifically
    adoption_opps_in_storage = [j for j in clean if "adoption_signals" in j]
    matched_adoption = match_adoption_opportunities(adoption_opps_in_storage)
    print(f"  • Adoption opportunities matched: {len(matched_adoption)}\n")
    
    # Merge all matched
    all_matched = matched_regular + matched_adoption
    
    # Remove duplicates by URL
    seen_urls = set()
    deduplicated = []
    for job in all_matched:
        url = job.get("url", "")
        if url not in seen_urls:
            seen_urls.add(url)
            deduplicated.append(job)
    
    print(f"✓ After deduplication: {len(deduplicated)} opportunities\n")
    
    # Save back to storage
    update_found(deduplicated)
    
    # ========== SUMMARY ==========
    print("="*70)
    print(" PIPELINE COMPLETE")
    print("="*70)
    print(f"\nResults:")
    print(f"  • Adoption opportunities found: {len(adoption_opps)}")
    print(f"  • Total unique opportunities: {len(deduplicated)}")
    print(f"  • Adoption-focused matches: {len(matched_adoption)}")
    
    if deduplicated:
        avg_score = sum(j.get('score', 0) for j in deduplicated) / len(deduplicated)
        print(f"  • Average relevance score: {avg_score:.1f}/100\n")
        
        # Categorize and show breakdown
        categories = categorize_jobs(deduplicated)
        print(f"\nOpportunity Breakdown:")
        print(f"  • Emotion AI Companies: {len(categories['emotion_ai'])}")
        print(f"  • Research Positions: {len(categories['research'])}")
        print(f"  • Adoption Programs: {len(categories['adoption'])}")
        
        print(f"\nTop 5 Adoption Opportunities:\n")
        adoption_sorted = sorted(matched_adoption, key=lambda x: x.get('score', 0), reverse=True)
        for i, job in enumerate(adoption_sorted[:5], 1):
            score = job.get('score', 0)
            title = job.get('title', 'Unknown')[:60]
            analysis = job.get('analysis', {})
            type_label = analysis.get('type_label', 'Unknown')
            print(f"   {i}. [{score}/100] {title}")
            print(f"      Type: {type_label}\n")
    
    print("="*70 + "\n")
    
    return deduplicated


def run_quick_pipeline():
    """
    Quick pipeline - only process existing opportunities
    (doesn't search, just matches)
    """
    
    print("\n" + "="*70)
    print(" QUICK PIPELINE - PROCESS EXISTING OPPORTUNITIES")
    print("="*70 + "\n")
    
    # Load existing
    raw_jobs = load_found()
    print(f"[1/3] Loaded {len(raw_jobs)} opportunities")
    
    # Clean
    clean = clean_opportunities(raw_jobs)
    print(f"[2/3] Cleaned: {len(clean)} unique opportunities")
    
    # Match
    matched = match_jobs(clean)
    print(f"[3/3] Matched: {len(matched)} relevant jobs")
    
    # Save
    update_found(matched)
    
    print("\n" + "="*70)
    print(" QUICK PIPELINE COMPLETE")
    print(f"   Total opportunities: {len(matched)}")
    print("="*70 + "\n")
    
    return matched


if __name__ == "__main__":
    import sys
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  JOB HUNTER - PIPELINE CONTROLLER".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    print("\nOptions:")
    print("  1. Full pipeline (search + adoption hunt + process)")
    print("  2. Quick pipeline (process existing only)")
    print("  3. Adoption search only")
    print("  4. Exit\n")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        print()
        run_full_pipeline()
    elif choice == "2":
        print()
        run_quick_pipeline()
    elif choice == "3":
        print()
        opportunities = search_adoption_opportunities()
        print(f"\nAdoption opportunities found: {len(opportunities)}")
        print("Run 'python main.py' option 1 to process and add to dashboard\n")
    elif choice == "4":
        print("\nGoodbye!\n")
        sys.exit(0)
    else:
        print("\nInvalid choice.\n")