"""
Lightweight Smart Memory - No ChromaDB/onnxruntime needed
Records decisions and learns patterns without vector embeddings
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class SmartMemoryLite:
    """Lightweight memory system (no vector DB)"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.memory_file = self.data_dir / "smart_memory_lite.json"
        self.memory = self._load_memory()
        
        print("✅ Lightweight Smart Memory initialized")
    
    def _load_memory(self):
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'decisions': [],
            'preferences': {
                'approved_companies': [],
                'refused_companies': [],
                'approved_keywords': {},
                'refused_keywords': {},
                'remote_stats': {'approved': 0, 'refused': 0},
                'categories': {}
            }
        }
    
    def _save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def record_decision(self, job: Dict, decision: str, reason=None):
        """Record a decision"""
        # Extract keywords
        keywords = []
        if 'analysis' in job and 'breakdown' in job['analysis']:
            bd = job['analysis']['breakdown']
            keywords = (bd.get('emotion_keywords', []) + 
                       bd.get('technical_keywords', []) +
                       bd.get('adoption_keywords', []))[:15]
        
        # Add to decisions
        self.memory['decisions'].append({
            'timestamp': datetime.now().isoformat(),
            'company': job.get('company'),
            'title': job.get('title'),
            'decision': decision,
            'category': job.get('analysis', {}).get('breakdown', {}).get('category', 'unknown'),
            'remote': job.get('analysis', {}).get('breakdown', {}).get('remote_available', False),
            'keywords': keywords
        })
        
        # Update preferences
        prefs = self.memory['preferences']
        company = job.get('company', '')
        
        # Track companies
        if decision == 'approved':
            if company not in prefs['approved_companies']:
                prefs['approved_companies'].append(company)
        else:
            if company not in prefs['refused_companies']:
                prefs['refused_companies'].append(company)
        
        # Track keywords
        keyword_dict = prefs['approved_keywords'] if decision == 'approved' else prefs['refused_keywords']
        for kw in keywords:
            keyword_dict[kw] = keyword_dict.get(kw, 0) + 1
        
        # Track remote
        if job.get('analysis', {}).get('breakdown', {}).get('remote_available'):
            prefs['remote_stats'][decision] = prefs['remote_stats'].get(decision, 0) + 1
        
        # Track categories
        category = job.get('analysis', {}).get('breakdown', {}).get('category', 'unknown')
        if category not in prefs['categories']:
            prefs['categories'][category] = {'approved': 0, 'refused': 0}
        prefs['categories'][category][decision] = prefs['categories'][category].get(decision, 0) + 1
        
        self._save_memory()
        print(f"   📝 Recorded: {decision} - {company}")
    
    def get_memory_stats(self):
        """Get stats"""
        prefs = self.memory['preferences']
        
        # Remote score
        remote_total = prefs['remote_stats']['approved'] + prefs['remote_stats']['refused']
        remote_score = prefs['remote_stats']['approved'] / remote_total if remote_total > 0 else 0.5
        
        # Top keywords
        approved_kw = sorted(prefs['approved_keywords'].items(), key=lambda x: x[1], reverse=True)
        refused_kw = sorted(prefs['refused_keywords'].items(), key=lambda x: x[1], reverse=True)
        
        # Categories
        category_stats = []
        for cat, counts in prefs['categories'].items():
            total = counts['approved'] + counts['refused']
            score = counts['approved'] / total if total > 0 else 0
            category_stats.append((cat, score, counts['approved']))
        category_stats.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        return {
            'total_interactions': len(self.memory['decisions']),
            'vector_db_entries': 0,
            'companies_in_graph': 0,
            'search_experiments': 0,
            'learned_preferences': {
                'top_keywords': approved_kw,
                'avoided_keywords': refused_kw,
                'approved_companies': prefs['approved_companies'],
                'remote_preference_score': remote_score,
                'top_categories': category_stats,
                'top_technologies': []
            },
            'best_sources': []
        }
    
    def predict_approval_probability(self, job: Dict) -> float:
        """Predict approval probability"""
        prefs = self.memory['preferences']
        score = 0.5
        
        company = job.get('company', '')
        if company in prefs['approved_companies']:
            score += 0.3
        elif company in prefs['refused_companies']:
            score -= 0.3
        
        # Check keywords
        job_keywords = set()
        if 'analysis' in job and 'breakdown' in job['analysis']:
            bd = job['analysis']['breakdown']
            job_keywords = set(bd.get('emotion_keywords', []) + bd.get('technical_keywords', []))
        
        for kw in job_keywords:
            if kw in prefs['approved_keywords']:
                score += 0.05
            if kw in prefs['refused_keywords']:
                score -= 0.05
        
        return max(0.0, min(1.0, score))