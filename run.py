#!/usr/bin/env python
# run.py (UPDATED) - One-click job hunting automation with adoption hunter

import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    print("\n" + "="*70)
    print("  🎯 JOB HUNTER - AI INTERNSHIP FINDER")
    print("  With Adoption/Innovation Program Search")
    print("="*70 + "\n")

def run_command(description, command):
    """Run a command and show progress"""
    print(f"[Running] {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[Success] {description} ✓\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] {description} failed:")
        print(e.stderr)
        return False

def show_memory_insights():
    """Show what the AI has learned"""
    from app.smart_memory import SmartMemory
    
    memory = SmartMemory()
    stats = memory.get_memory_stats()
    
    print("\n" + "="*70)
    print("  🧠 AI MEMORY INSIGHTS")
    print("="*70)
    
    print(f"\n📊 Learning Progress:")
    print(f"   {stats['total_interactions']} decisions tracked")
    print(f"   {stats['vector_db_entries']} jobs in similarity database")
    
    if stats['total_interactions'] > 0:
        prefs = stats['learned_preferences']
        
        print(f"\n✅ What You Like:")
        if prefs['top_5_keywords']:
            keywords = ', '.join([f"{k[0]} ({k[1]}x)" for k in prefs['top_5_keywords']])
            print(f"   Keywords: {keywords}")
        
        if prefs['approved_companies']:
            print(f"   Companies: {', '.join(prefs['approved_companies'][:5])}")
        
        print(f"   Remote jobs: {prefs['remote_preference']:.0%} preference")
        
        print(f"\n❌ What You Avoid:")
        if prefs['avoided_keywords']:
            avoided = ', '.join([f"{k[0]} ({k[1]}x)" for k in prefs['avoided_keywords'][:3]])
            print(f"   Keywords: {avoided}")
        
        print(f"\n📈 Best Job Sources:")
        for i, source in enumerate(stats['best_sources'], 1):
            print(f"   {i}. {source['source']}: {source['success_rate']:.0%} success ({source['total_approved']} approved)")
    
    input("\nPress Enter to continue...")

def show_memory_insights():
    """Show what the AI has learned"""
    from app.smart_memory import SmartMemory
    
    memory = SmartMemory()
    stats = memory.get_memory_stats()
    
    print("\n" + "="*70)
    print("  🧠 AI MEMORY INSIGHTS")
    print("="*70)
    
    print(f"\n📊 Learning Progress:")
    print(f"   {stats['total_interactions']} decisions tracked")
    print(f"   {stats['vector_db_entries']} jobs in similarity database")
    
    if stats['total_interactions'] > 0:
        prefs = stats['learned_preferences']
        
        print(f"\n✅ What You Like:")
        if prefs['top_5_keywords']:
            keywords = ', '.join([f"{k[0]} ({k[1]}x)" for k in prefs['top_5_keywords']])
            print(f"   Keywords: {keywords}")
        
        if prefs['approved_companies']:
            print(f"   Companies: {', '.join(prefs['approved_companies'][:5])}")
        
        print(f"   Remote jobs: {prefs['remote_preference']:.0%} preference")
        
        print(f"\n❌ What You Avoid:")
        if prefs['avoided_keywords']:
            avoided = ', '.join([f"{k[0]} ({k[1]}x)" for k in prefs['avoided_keywords'][:3]])
            print(f"   Keywords: {avoided}")
        
        print(f"\n📈 Best Job Sources:")
        for i, source in enumerate(stats['best_sources'], 1):
            print(f"   {i}. {source['source']}: {source['success_rate']:.0%} success ({source['total_approved']} approved)")
    
    input("\nPress Enter to continue...")

def show_memory_insights():
    """Show what the AI has learned"""
    from app.smart_memory import SmartMemory
    
    memory = SmartMemory()
    stats = memory.get_memory_stats()
    
    print("\n" + "="*70)
    print("  🧠 AI MEMORY INSIGHTS")
    print("="*70)
    
    print(f"\n📊 Learning Progress:")
    print(f"   {stats['total_interactions']} decisions tracked")
    print(f"   {stats['vector_db_entries']} jobs in similarity database")
    
    if stats['total_interactions'] > 0:
        prefs = stats['learned_preferences']
        
        print(f"\n✅ What You Like:")
        if prefs['top_5_keywords']:
            keywords = ', '.join([f"{k[0]} ({k[1]}x)" for k in prefs['top_5_keywords']])
            print(f"   Keywords: {keywords}")
        
        if prefs['approved_companies']:
            print(f"   Companies: {', '.join(prefs['approved_companies'][:5])}")
        
        print(f"   Remote jobs: {prefs['remote_preference']:.0%} preference")
        
        print(f"\n❌ What You Avoid:")
        if prefs['avoided_keywords']:
            avoided = ', '.join([f"{k[0]} ({k[1]}x)" for k in prefs['avoided_keywords'][:3]])
            print(f"   Keywords: {avoided}")
        
        print(f"\n📈 Best Job Sources:")
        for i, source in enumerate(stats['best_sources'], 1):
            print(f"   {i}. {source['source']}: {source['success_rate']:.0%} success ({source['total_approved']} approved)")
    
    input("\nPress Enter to continue...")

def main():
    print_banner()
    
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    
    while True:
        print("\n" + "=" * 70)
        print("  🎯 JOB HUNTER - AI INTERNSHIP FINDER")
        print("  With Adoption/Innovation Program Search")
        print("=" * 70)
        print("\nWhat would you like to do?\n")
        print("1.  Search job boards (LinkedIn, etc.)")
        print("2.  Search adoption/innovation programs")
        print("3.  Full pipeline (boards + adoption + process)")
        print("4.  Quick process (existing opportunities only)")
        print("5.  Start web dashboard")
        print("6.  View statistics")
        print("7.  Clean refused opportunities")
        print("8.  View AI Memory Insights 🧠 (NEW!)")  # NEW OPTION
        print("9.  Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            print("\n[Searching] Job boards...\n")
            run_command("Job Board Search", "python -m app.hunter")
            print("\n✓ Search complete! Run option 3 to process results.")
            
        elif choice == "2":
            print("\n[Searching] Adoption and innovation programs...\n")
            print("This will find:")
            print("  • AI startup accelerators")
            print("  • Hackathon platforms (Devpost, MLH, etc.)")
            print("  • Research grant programs")
            print("  • Open source programs (Google Summer of Code, etc.)")
            print("  • AI innovation labs and research centers\n")
            run_command("Adoption Opportunity Search", "python -c \"from app.adoption_hunter import search_adoption_opportunities; opportunities = search_adoption_opportunities(); print(f'\\n✓ Found {len(opportunities)} adoption opportunities')\"")
            print("\nRun 'python main.py' option 1 to process and add to dashboard")
            
        elif choice == "3":
            # NEW: Find AI companies with emails
            print("\n[Starting] AI Company Finder with Email Extraction...")
            from app.company_finder import main as find_companies
            find_companies()
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print("\n[Step 1/3] Searching job boards...\n")
            run_command("Job Board Search", "python -m app.hunter")
            
            time.sleep(2)
            
            print("\n[Step 2/3] Searching adoption programs...\n")
            print("(This may take a minute as it searches multiple platforms...)\n")
            run_command("Adoption Search", "python -c \"from app.adoption_hunter import search_adoption_opportunities; search_adoption_opportunities()\"")
            
            time.sleep(2)
            
            print("\n[Step 3/3] Processing and matching all opportunities...\n")
            run_command("Full Pipeline", "python main.py")
            
            time.sleep(2)
            
            print("\n[Ready] Starting web dashboard...\n")
            print("Dashboard opening at: http://localhost:5000")
            print("Press Ctrl+C to stop\n")
            time.sleep(2)
            subprocess.run(["python", "web/app.py"])
            
        elif choice == "5":
            print("\n[Processing] Existing opportunities...\n")
            subprocess.run(["python", "main.py"])
            
        elif choice == "6":
            print("\n[Starting] Web dashboard...")
            print("Dashboard will open at: http://localhost:5000")
            print("Press Ctrl+C to stop\n")
            time.sleep(2)
            subprocess.run(["python", "web/app.py"])
            
        elif choice == "7":
            print("\n 📊 Job Hunting Statistics\n")
            from app.storage import get_stats
            stats = get_stats()
            print(f"  Found Opportunities:  {stats['found']}")
            print(f"  Approved Jobs:        {stats['approved']}")
            print(f"  Refused Jobs:         {stats['refused']}")
            print(f"  Emails Sent:          {stats['sent']}")
            print()
            
        elif choice == "8":
            # NEW: Clean refused opportunities
            print("\n[Starting] Cleaning refused opportunities...")
            from app.storage import remove_refused_from_found, clean_all_duplicates
            
            print("\n🧹 Removing refused opportunities...")
            remove_refused_from_found()
            
            print("\n🧹 Removing duplicates...")
            clean_all_duplicates()
            
            print("\n✅ Cleanup complete!")
            input("\nPress Enter to continue...")
            
        elif choice == "9":
            print("\n[Exit] Goodbye! 👋")
            sys.exit(0)
        else:
            print("\n[Error] Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n ⏹️  Stopped by user. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n ❌ Error: {e}\n")
        sys.exit(1)