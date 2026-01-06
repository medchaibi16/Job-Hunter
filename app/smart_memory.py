"""
Smart Memory System - Advanced learning from user interactions
Foundation for AI-powered job discovery

Features:
- Vector embeddings for similarity search
- Decision tracking (approve/refuse patterns)
- Company relationship mapping
- Search strategy effectiveness tracking
- Continuous learning from outcomes
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np

# Try importing ChromaDB (vector database)
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️ ChromaDB not available. Install with: pip install chromadb")

class SmartMemory:
    """
    Advanced memory system that learns from user decisions
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Memory files
        self.interactions_file = self.data_dir / "interactions_memory.json"
        self.patterns_file = self.data_dir / "learned_patterns.json"
        self.company_graph_file = self.data_dir / "company_graph.json"
        self.search_history_file = self.data_dir / "search_history.json"
        
        # Initialize vector database if available
        self.vector_db = None
        if CHROMADB_AVAILABLE:
            self._init_vector_db()
        
        # Load existing memories
        self.interactions = self._load_json(self.interactions_file, [])
        self.patterns = self._load_json(self.patterns_file, {})
        self.company_graph = self._load_json(self.company_graph_file, {})
        self.search_history = self._load_json(self.search_history_file, [])
        
        print("✅ Smart Memory System initialized")
        if self.vector_db:
            print(f"   📊 Vector DB: {self.vector_db.count()} embeddings stored")
        print(f"   🧠 Interactions tracked: {len(self.interactions)}")
    
    def _init_vector_db(self):
        """Initialize ChromaDB for similarity search"""
        try:
            chroma_path = self.data_dir / "chroma_db"
            client = chromadb.PersistentClient(path=str(chroma_path))
            
            # Create or get collection
            self.vector_db = client.get_or_create_collection(
                name="job_hunter_memory",
                metadata={"description": "Job Hunter learning memory"}
            )
            print("✅ Vector database ready")
        except Exception as e:
            print(f"⚠️ Vector DB initialization failed: {e}")
            self.vector_db = None
    
    def _load_json(self, path: Path, default):
        """Load JSON file with error handling"""
        if not path.exists():
            return default
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default
    
    def _save_json(self, path: Path, data):
        """Save JSON file"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Save failed for {path}: {e}")
    
    # ==================== INTERACTION TRACKING ====================
    
    def record_decision(self, job: Dict, decision: str, reason: Optional[str] = None):
        """
        Record a user decision about a job
        
        Args:
            job: Job/company data
            decision: 'approved', 'refused', 'applied', 'interviewed', 'offered'
            reason: Optional reason for decision
        """
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'job_id': job.get('fingerprint', job.get('url')),
            'company': job.get('company'),
            'title': job.get('title'),
            'decision': decision,
            'reason': reason,
            'job_data': {
                'location': job.get('location'),
                'remote': job.get('analysis', {}).get('breakdown', {}).get('remote_available', False),
                'score': job.get('analysis', {}).get('score'),
                'category': job.get('analysis', {}).get('breakdown', {}).get('category'),
                'keywords': job.get('analysis', {}).get('breakdown', {}).get('emotion_keywords', []),
                'focus': job.get('focus', ''),
                'tech_stack': job.get('tech_stack', []),
            }
        }
        
        self.interactions.append(interaction)
        self._save_json(self.interactions_file, self.interactions)
        
        # Add to vector database for similarity search
        if self.vector_db:
            self._add_to_vector_db(job, decision)
        
        # Update patterns
        self._update_patterns(interaction)
        
        print(f"📝 Recorded: {decision} - {job.get('company')}")
    
    def _add_to_vector_db(self, job: Dict, decision: str):
        """Add job to vector database with decision label"""
        try:
            # Create text representation for embedding
            text = self._job_to_text(job)
            job_id = job.get('fingerprint', hashlib.md5(text.encode()).hexdigest())
            
            # Add to ChromaDB
            self.vector_db.add(
                documents=[text],
                metadatas=[{
                    'company': job.get('company', ''),
                    'decision': decision,
                    'timestamp': datetime.now().isoformat()
                }],
                ids=[job_id]
            )
        except Exception as e:
            print(f"⚠️ Vector DB add failed: {e}")
    
    def _job_to_text(self, job: Dict) -> str:
        """Convert job to text for embedding"""
        parts = [
            job.get('title', ''),
            job.get('company', ''),
            job.get('description', ''),
            job.get('focus', ''),
            ' '.join(job.get('tech_stack', [])),
            ' '.join(job.get('requirements', [])),
        ]
        return ' '.join(filter(None, parts))
    
    # ==================== PATTERN LEARNING ====================
    
    def _update_patterns(self, interaction: Dict):
        """Learn patterns from interactions"""
        decision = interaction['decision']
        job_data = interaction['job_data']
        
        # Initialize pattern counters
        if 'preferences' not in self.patterns:
            self.patterns['preferences'] = {
                'approved_companies': [],
                'refused_companies': [],
                'preferred_keywords': {},
                'avoided_keywords': {},
                'location_preferences': {},
                'remote_preference': {'approved': 0, 'refused': 0},
                'category_preferences': {},
                'tech_preferences': {},
            }
        
        prefs = self.patterns['preferences']
        
        # Track companies
        company = interaction['company']
        if decision == 'approved':
            if company not in prefs['approved_companies']:
                prefs['approved_companies'].append(company)
        elif decision == 'refused':
            if company not in prefs['refused_companies']:
                prefs['refused_companies'].append(company)
        
        # Track keywords
        keywords = job_data.get('keywords', [])
        keyword_dict = prefs['preferred_keywords'] if decision == 'approved' else prefs['avoided_keywords']
        for keyword in keywords:
            keyword_dict[keyword] = keyword_dict.get(keyword, 0) + 1
        
        # Track remote preference
        if job_data.get('remote'):
            prefs['remote_preference'][decision] = prefs['remote_preference'].get(decision, 0) + 1
        
        # Track category preferences
        category = job_data.get('category')
        if category:
            if category not in prefs['category_preferences']:
                prefs['category_preferences'][category] = {'approved': 0, 'refused': 0}
            prefs['category_preferences'][category][decision] = prefs['category_preferences'][category].get(decision, 0) + 1
        
        # Track tech stack preferences
        tech_stack = job_data.get('tech_stack', [])
        for tech in tech_stack:
            if tech not in prefs['tech_preferences']:
                prefs['tech_preferences'][tech] = {'approved': 0, 'refused': 0}
            prefs['tech_preferences'][tech][decision] = prefs['tech_preferences'][tech].get(decision, 0) + 1
        
        self._save_json(self.patterns_file, self.patterns)
    
    def get_learned_preferences(self) -> Dict:
        """Get learned user preferences"""
        prefs = self.patterns.get('preferences', {})
        
        # Calculate preference scores
        result = {
            'top_keywords': self._get_top_items(prefs.get('preferred_keywords', {}), 10),
            'avoided_keywords': self._get_top_items(prefs.get('avoided_keywords', {}), 10),
            'approved_companies': prefs.get('approved_companies', [])[:20],
            'remote_preference_score': self._calculate_preference_score(
                prefs.get('remote_preference', {})
            ),
            'top_categories': self._rank_categories(prefs.get('category_preferences', {})),
            'top_technologies': self._rank_categories(prefs.get('tech_preferences', {})),
        }
        
        return result
    
    def _get_top_items(self, items_dict: Dict, n: int) -> List[tuple]:
        """Get top N items from frequency dict"""
        sorted_items = sorted(items_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:n]
    
    def _calculate_preference_score(self, counts: Dict) -> float:
        """Calculate preference score from approve/refuse counts"""
        approved = counts.get('approved', 0)
        refused = counts.get('refused', 0)
        total = approved + refused
        return approved / total if total > 0 else 0.5
    
    def _rank_categories(self, categories: Dict) -> List[tuple]:
        """Rank categories by preference"""
        ranked = []
        for category, counts in categories.items():
            score = self._calculate_preference_score(counts)
            ranked.append((category, score, counts.get('approved', 0)))
        return sorted(ranked, key=lambda x: (x[1], x[2]), reverse=True)
    
    # ==================== SIMILARITY SEARCH ====================
    
    def find_similar_approved_jobs(self, current_job: Dict, n: int = 5) -> List[Dict]:
        """
        Find jobs similar to ones you approved
        
        Args:
            current_job: Job to compare
            n: Number of similar jobs to return
        
        Returns:
            List of similar approved jobs
        """
        if not self.vector_db:
            print("⚠️ Vector DB not available for similarity search")
            return []
        
        try:
            # Convert job to text
            query_text = self._job_to_text(current_job)
            
            # Query for similar approved jobs
            results = self.vector_db.query(
                query_texts=[query_text],
                where={'decision': 'approved'},
                n_results=n
            )
            
            if results and results['documents']:
                return [
                    {
                        'company': meta.get('company'),
                        'similarity': 1.0,  # ChromaDB returns by similarity
                        'timestamp': meta.get('timestamp')
                    }
                    for meta in results['metadatas'][0]
                ]
            
        except Exception as e:
            print(f"⚠️ Similarity search failed: {e}")
        
        return []
    
    def predict_approval_probability(self, job: Dict) -> float:
        """
        Predict probability user will approve this job
        Based on learned patterns
        
        Returns:
            Float between 0 and 1
        """
        if not self.interactions:
            return 0.5  # No data, neutral
        
        prefs = self.patterns.get('preferences', {})
        score = 0.5  # Start neutral
        
        # Check if company was previously approved/refused
        company = job.get('company', '')
        if company in prefs.get('approved_companies', []):
            score += 0.3
        elif company in prefs.get('refused_companies', []):
            score -= 0.3
        
        # Check keywords
        job_keywords = set(job.get('analysis', {}).get('breakdown', {}).get('emotion_keywords', []))
        preferred_keywords = set(self._get_top_items(prefs.get('preferred_keywords', {}), 5))
        avoided_keywords = set(self._get_top_items(prefs.get('avoided_keywords', {}), 5))
        
        keyword_overlap_good = len(job_keywords & set(k[0] for k in preferred_keywords))
        keyword_overlap_bad = len(job_keywords & set(k[0] for k in avoided_keywords))
        
        score += keyword_overlap_good * 0.1
        score -= keyword_overlap_bad * 0.1
        
        # Check remote preference
        if job.get('analysis', {}).get('breakdown', {}).get('remote_available'):
            remote_score = self._calculate_preference_score(prefs.get('remote_preference', {}))
            score += (remote_score - 0.5) * 0.2
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, score))
    
    # ==================== COMPANY GRAPH ====================
    
    def add_company_relationship(self, company1: str, company2: str, relationship: str):
        """
        Build knowledge graph of company relationships
        
        Args:
            company1: First company
            company2: Second company
            relationship: Type of relationship (similar_tech, funded_by, etc.)
        """
        if company1 not in self.company_graph:
            self.company_graph[company1] = {'connections': []}
        
        self.company_graph[company1]['connections'].append({
            'to': company2,
            'type': relationship,
            'discovered': datetime.now().isoformat()
        })
        
        self._save_json(self.company_graph_file, self.company_graph)
    
    def get_related_companies(self, company: str) -> List[str]:
        """Get companies related to given company"""
        if company not in self.company_graph:
            return []
        
        return [
            conn['to'] 
            for conn in self.company_graph[company].get('connections', [])
        ]
    
    # ==================== SEARCH STRATEGY TRACKING ====================
    
    def record_search_result(self, source: str, strategy: str, results_count: int, approved_count: int):
        """
        Track effectiveness of different search strategies
        
        Args:
            source: Where jobs were found (LinkedIn, YC, etc.)
            strategy: Search strategy used
            results_count: Number of jobs found
            approved_count: Number of jobs approved
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'strategy': strategy,
            'results_count': results_count,
            'approved_count': approved_count,
            'success_rate': approved_count / results_count if results_count > 0 else 0
        }
        
        self.search_history.append(entry)
        self._save_json(self.search_history_file, self.search_history)
    
    def get_best_sources(self, n: int = 5) -> List[Dict]:
        """Get most effective job sources"""
        if not self.search_history:
            return []
        
        # Aggregate by source
        source_stats = {}
        for entry in self.search_history:
            source = entry['source']
            if source not in source_stats:
                source_stats[source] = {
                    'total_results': 0,
                    'total_approved': 0,
                    'searches': 0
                }
            
            source_stats[source]['total_results'] += entry['results_count']
            source_stats[source]['total_approved'] += entry['approved_count']
            source_stats[source]['searches'] += 1
        
        # Calculate success rates
        ranked = []
        for source, stats in source_stats.items():
            success_rate = stats['total_approved'] / stats['total_results'] if stats['total_results'] > 0 else 0
            ranked.append({
                'source': source,
                'success_rate': success_rate,
                'total_approved': stats['total_approved'],
                'searches': stats['searches']
            })
        
        return sorted(ranked, key=lambda x: (x['success_rate'], x['total_approved']), reverse=True)[:n]
    
    # ==================== ANALYTICS ====================
    
    def get_memory_stats(self) -> Dict:
        """Get comprehensive memory statistics"""
        prefs = self.get_learned_preferences()
        
        stats = {
            'total_interactions': len(self.interactions),
            'companies_in_graph': len(self.company_graph),
            'search_experiments': len(self.search_history),
            'vector_db_entries': self.vector_db.count() if self.vector_db else 0,
            'learned_preferences': {
                'top_5_keywords': prefs['top_keywords'][:5],
                'avoided_keywords': prefs['avoided_keywords'][:5],
                'approved_companies_count': len(prefs['approved_companies']),
                'remote_preference': prefs['remote_preference_score'],
                'top_categories': prefs['top_categories'][:3],
            },
            'best_sources': self.get_best_sources(3)
        }
        
        return stats
    
    def export_for_ai_training(self) -> Dict:
        """
        Export memory in format suitable for AI training
        (for future RL agent)
        """
        return {
            'interactions': self.interactions,
            'learned_patterns': self.patterns,
            'company_graph': self.company_graph,
            'search_history': self.search_history,
            'preferences_summary': self.get_learned_preferences(),
            'export_date': datetime.now().isoformat()
        }


# ==================== INTEGRATION HELPERS ====================

def integrate_with_storage():
    """
    Update existing storage.py functions to use smart memory
    """
    memory = SmartMemory()
    
    # Monkey patch existing functions
    import app.storage as storage
    
    original_add_approved = storage.add_approved
    original_add_refused = storage.add_refused
    
    def smart_add_approved(job):
        original_add_approved(job)
        memory.record_decision(job, 'approved')
    
    def smart_add_refused(job):
        original_add_refused(job)
        memory.record_decision(job, 'refused')
    
    storage.add_approved = smart_add_approved
    storage.add_refused = smart_add_refused
    
    return memory


# ==================== CLI FOR TESTING ====================

def main():
    """Test the smart memory system"""
    print("\n" + "="*70)
    print("  🧠 SMART MEMORY SYSTEM TEST")
    print("="*70)
    
    memory = SmartMemory()
    
    # Show current stats
    stats = memory.get_memory_stats()
    
    print("\n📊 Current Memory Status:")
    print(f"   Interactions tracked: {stats['total_interactions']}")
    print(f"   Companies in graph: {stats['companies_in_graph']}")
    print(f"   Search experiments: {stats['search_experiments']}")
    print(f"   Vector DB entries: {stats['vector_db_entries']}")
    
    if stats['total_interactions'] > 0:
        print("\n🎯 Learned Preferences:")
        prefs = stats['learned_preferences']
        
        if prefs['top_5_keywords']:
            print(f"   Top keywords: {', '.join([k[0] for k in prefs['top_5_keywords']])}")
        
        print(f"   Remote preference: {prefs['remote_preference']:.0%}")
        print(f"   Companies approved: {prefs['approved_companies_count']}")
        
        if prefs['top_categories']:
            print(f"   Best category: {prefs['top_categories'][0][0]} ({prefs['top_categories'][0][1]:.0%})")
        
        if prefs['best_sources']:
            print("\n📈 Best Job Sources:")
            for source in prefs['best_sources']:
                print(f"   {source['source']}: {source['success_rate']:.0%} success rate")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()