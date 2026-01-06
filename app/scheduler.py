"""
Background job scheduler for automatic job searching
Runs every X minutes to find new opportunities
"""
import time
import threading
from datetime import datetime
from config.env_loader import SEARCH_INTERVAL_MINUTES, AUTO_SEARCH_ENABLED

class JobScheduler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_run = None
        
    def start(self):
        """Start the background scheduler"""
        if not AUTO_SEARCH_ENABLED:
            print("⏸️ Auto-search disabled in .env")
            return
        
        if self.running:
            print("⚠️ Scheduler already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"✅ Scheduler started: Searching every {SEARCH_INTERVAL_MINUTES} minutes")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("🛑 Scheduler stopped")
    
    def _run_loop(self):
        """Main scheduler loop"""
        while self.running:
            try:
                print(f"\n{'='*60}")
                print(f"🔄 AUTO-SEARCH TRIGGERED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}\n")
                
                # Run the job search
                self._search_jobs()
                
                self.last_run = datetime.now()
                
                # Wait for next interval
                time.sleep(SEARCH_INTERVAL_MINUTES * 60)
                
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
                time.sleep(60)  # Wait 1 minute before retry
    
    def _search_jobs(self):
        """Execute job search"""
        try:
            from app.hunter import JobHunter
            
            hunter = JobHunter()
            
            # Search all sources
            print("📊 Searching job boards...")
            hunter.search_all_sources()
            
            print("💡 Searching innovation programs...")
            from app.adoption_hunter import AdoptionHunter
            adoption = AdoptionHunter()
            adoption.search_all_programs()
            
            print("✅ Auto-search complete!")
            
        except Exception as e:
            print(f"❌ Search failed: {e}")

# Global scheduler instance
scheduler = JobScheduler()