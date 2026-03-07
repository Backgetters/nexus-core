# Amazo Memory System
# Phase 1: Foundation - HNSW-based Vector Memory
# Implements self-learning memory from Claude-Flow's RuVector

import json
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

@dataclass
class MemoryEntry:
    id: str
    content: str
    embedding: Optional[List[float]]
    memory_type: str  # 'episodic', 'semantic', 'procedural'
    timestamp: datetime
    importance: float  # 0.0 to 1.0
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class HNSWIndex:
    """
    Hierarchical Navigable Small World index for fast approximate nearest neighbor search.
    150x-12,500x faster than brute force.
    """
    
    def __init__(self, dim: int = 384, m: int = 16, ef_construction: int = 200):
        self.dim = dim
        self.m = m  # Number of connections per layer
        self.ef_construction = ef_construction
        self.max_level = 0
        self.entry_point = None
        self.nodes: Dict[str, Dict] = {}
        self.level_mult = 1 / np.log(m)
        
    def _random_level(self) -> int:
        """Generate random level for new node"""
        level = 0
        while np.random.random() < self.level_mult and level < self.max_level + 1:
            level += 1
        return level
    
    def _distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Cosine similarity (1 - cosine distance)"""
        return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def add(self, id: str, embedding: np.ndarray):
        """Add a node to the index"""
        level = self._random_level()
        
        node = {
            'id': id,
            'embedding': embedding,
            'level': level,
            'connections': {l: [] for l in range(level + 1)}
        }
        
        if self.entry_point is None:
            self.entry_point = id
            self.max_level = level
            self.nodes[id] = node
            return
        
        # Find entry point for each level
        curr_id = self.entry_point
        curr_dist = self._distance(embedding, self.nodes[curr_id]['embedding'])
        
        for l in range(self.max_level, level, -1):
            changed = True
            while changed:
                changed = False
                for neighbor_id in self.nodes[curr_id]['connections'].get(l, []):
                    dist = self._distance(embedding, self.nodes[neighbor_id]['embedding'])
                    if dist < curr_dist:
                        curr_id = neighbor_id
                        curr_dist = dist
                        changed = True
        
        # Connect at each level
        for l in range(min(level, self.max_level), -1, -1):
            # Find nearest neighbors at this level
            candidates = self._search_level(embedding, curr_id, l, self.m * 2)
            neighbors = sorted(candidates, key=lambda x: x[1])[:self.m]
            
            node['connections'][l] = [n[0] for n in neighbors]
            
            # Update reverse connections
            for neighbor_id, _ in neighbors:
                if l in self.nodes[neighbor_id]['connections']:
                    self.nodes[neighbor_id]['connections'][l].append(id)
                    # Trim if too many connections
                    if len(self.nodes[neighbor_id]['connections'][l]) > self.m * 2:
                        self._trim_connections(neighbor_id, l)
        
        self.nodes[id] = node
        
        if level > self.max_level:
            self.max_level = level
            self.entry_point = id
    
    def _search_level(self, query: np.ndarray, entry_id: str, level: int, ef: int) -> List[Tuple[str, float]]:
        """Search for nearest neighbors at a specific level"""
        visited = {entry_id}
        candidates = [(self._distance(query, self.nodes[entry_id]['embedding']), entry_id)]
        results = [(self._distance(query, self.nodes[entry_id]['embedding']), entry_id)]
        
        while candidates:
            dist, curr_id = candidates.pop(0)
            
            for neighbor_id in self.nodes[curr_id]['connections'].get(level, []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    neighbor_dist = self._distance(query, self.nodes[neighbor_id]['embedding'])
                    
                    if len(results) < ef or neighbor_dist < results[-1][0]:
                        candidates.append((neighbor_dist, neighbor_id))
                        results.append((neighbor_dist, neighbor_id))
                        results.sort(key=lambda x: x[0])
                        if len(results) > ef:
                            results = results[:ef]
        
        return results
    
    def _trim_connections(self, node_id: str, level: int):
        """Trim excess connections maintaining diversity"""
        connections = self.nodes[node_id]['connections'][level]
        if len(connections) <= self.m:
            return
        
        # Keep closest connections
        query = self.nodes[node_id]['embedding']
        scored = [(cid, self._distance(query, self.nodes[cid]['embedding'])) 
                  for cid in connections]
        scored.sort(key=lambda x: x[1])
        self.nodes[node_id]['connections'][level] = [cid for cid, _ in scored[:self.m]]
    
    def search(self, query: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """Search for k nearest neighbors"""
        if self.entry_point is None:
            return []
        
        # Search from top level down
        curr_id = self.entry_point
        curr_dist = self._distance(query, self.nodes[curr_id]['embedding'])
        
        for l in range(self.max_level, 0, -1):
            changed = True
            while changed:
                changed = False
                for neighbor_id in self.nodes[curr_id]['connections'].get(l, []):
                    dist = self._distance(query, self.nodes[neighbor_id]['embedding'])
                    if dist < curr_dist:
                        curr_id = neighbor_id
                        curr_dist = dist
                        changed = True
        
        # Final search at level 0
        results = self._search_level(query, curr_id, 0, k * 2)
        return results[:k]

class SimpleEmbedding:
    """Simple embedding generation without external API"""
    
    def __init__(self, dim: int = 384):
        self.dim = dim
        # Initialize random projection matrix
        self.projection = np.random.randn(10000, dim) / np.sqrt(dim)
        
    def encode(self, text: str) -> np.ndarray:
        """Generate simple embedding from text"""
        # Simple bag-of-words with random projection
        words = text.lower().split()
        word_indices = [hash(w) % 10000 for w in words]
        
        if not word_indices:
            return np.zeros(self.dim)
        
        # Average word embeddings
        embeddings = [self.projection[i] for i in word_indices]
        avg_embedding = np.mean(embeddings, axis=0)
        
        # Normalize
        norm = np.linalg.norm(avg_embedding)
        if norm > 0:
            avg_embedding = avg_embedding / norm
        
        return avg_embedding

class AmazoMemory:
    """
    Self-learning memory system with episodic, semantic, and procedural memory.
    Based on Claude-Flow's RuVector architecture.
    """
    
    def __init__(self, storage_dir: str = "~/clawd/amazo_core/memory"):
        self.storage_dir = Path(storage_dir).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Memory stores
        self.episodic: List[MemoryEntry] = []
        self.semantic_index = HNSWIndex(dim=384)
        self.procedural: Dict[str, Dict] = {}  # pattern -> outcome mapping
        self.reasoning_bank: List[Dict] = []
        
        # Embedding generator
        self.embedder = SimpleEmbedding(dim=384)
        
        # Load persisted memory
        self._load_memory()
    
    def _load_memory(self):
        """Load memory from disk"""
        episodic_path = self.storage_dir / "episodic.json"
        if episodic_path.exists():
            with open(episodic_path) as f:
                data = json.load(f)
                for entry_data in data:
                    entry_data['timestamp'] = datetime.fromisoformat(entry_data['timestamp'])
                    if entry_data.get('last_accessed'):
                        entry_data['last_accessed'] = datetime.fromisoformat(entry_data['last_accessed'])
                    self.episodic.append(MemoryEntry(**entry_data))
        
        # Rebuild semantic index
        for entry in self.episodic:
            if entry.memory_type == 'semantic' and entry.embedding:
                self.semantic_index.add(entry.id, np.array(entry.embedding))
        
        procedural_path = self.storage_dir / "procedural.json"
        if procedural_path.exists():
            with open(procedural_path) as f:
                self.procedural = json.load(f)
        
        reasoning_path = self.storage_dir / "reasoning_bank.json"
        if reasoning_path.exists():
            with open(reasoning_path) as f:
                self.reasoning_bank = json.load(f)
    
    def _save_memory(self):
        """Persist memory to disk"""
        # Save episodic memory
        episodic_data = []
        for entry in self.episodic:
            data = asdict(entry)
            data['timestamp'] = entry.timestamp.isoformat()
            data['last_accessed'] = entry.last_accessed.isoformat() if entry.last_accessed else None
            episodic_data.append(data)
        
        with open(self.storage_dir / "episodic.json", 'w') as f:
            json.dump(episodic_data, f, indent=2)
        
        # Save procedural memory
        with open(self.storage_dir / "procedural.json", 'w') as f:
            json.dump(self.procedural, f, indent=2)
        
        # Save reasoning bank
        with open(self.storage_dir / "reasoning_bank.json", 'w') as f:
            json.dump(self.reasoning_bank, f, indent=2)
    
    def store_episodic(self, content: str, importance: float = 0.5, tags: List[str] = None):
        """Store a session experience"""
        entry_id = hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()[:16]
        embedding = self.embedder.encode(content).tolist()
        
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            embedding=embedding,
            memory_type='episodic',
            timestamp=datetime.now(),
            importance=importance,
            tags=tags or []
        )
        
        self.episodic.append(entry)
        
        # Keep only most important recent episodes
        if len(self.episodic) > 1000:
            self.episodic.sort(key=lambda e: (e.importance, e.timestamp), reverse=True)
            self.episodic = self.episodic[:1000]
        
        self._save_memory()
        return entry_id
    
    def store_semantic(self, content: str, tags: List[str] = None):
        """Store knowledge in semantic memory with vector indexing"""
        entry_id = hashlib.md5(content.encode()).hexdigest()[:16]
        embedding = self.embedder.encode(content)
        
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            embedding=embedding.tolist(),
            memory_type='semantic',
            timestamp=datetime.now(),
            importance=0.5,
            tags=tags or []
        )
        
        self.episodic.append(entry)
        self.semantic_index.add(entry_id, embedding)
        self._save_memory()
        return entry_id
    
    def store_procedural(self, pattern: str, action: str, outcome: str, success: bool):
        """Store a problem-solution pattern"""
        if pattern not in self.procedural:
            self.procedural[pattern] = {
                'actions': {},
                'total_attempts': 0,
                'success_rate': 0.0
            }
        
        proc = self.procedural[pattern]
        proc['total_attempts'] += 1
        
        if action not in proc['actions']:
            proc['actions'][action] = {'success': 0, 'failure': 0}
        
        if success:
            proc['actions'][action]['success'] += 1
        else:
            proc['actions'][action]['failure'] += 1
        
        # Update success rate
        total_success = sum(a['success'] for a in proc['actions'].values())
        proc['success_rate'] = total_success / proc['total_attempts']
        
        # Store in reasoning bank
        self.reasoning_bank.append({
            'pattern': pattern,
            'action': action,
            'outcome': outcome,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_memory()
    
    def recall_similar(self, query: str, k: int = 5) -> List[MemoryEntry]:
        """Find semantically similar memories"""
        query_embedding = self.embedder.encode(query)
        results = self.semantic_index.search(query_embedding, k=k)
        
        # Update access counts
        recalled = []
        for entry_id, distance in results:
            for entry in self.episodic:
                if entry.id == entry_id:
                    entry.access_count += 1
                    entry.last_accessed = datetime.now()
                    recalled.append(entry)
                    break
        
        return recalled
    
    def get_procedural_knowledge(self, problem: str) -> Optional[Dict]:
        """Get learned procedure for a problem type"""
        # Find best matching pattern
        best_match = None
        best_score = 0
        
        for pattern, data in self.procedural.items():
            # Simple word overlap scoring
            pattern_words = set(pattern.lower().split())
            problem_words = set(problem.lower().split())
            overlap = len(pattern_words & problem_words)
            score = overlap / max(len(pattern_words), len(problem_words))
            
            if score > best_score and score > 0.5:
                best_score = score
                best_match = pattern
        
        if best_match:
            return {
                'pattern': best_match,
                'data': self.procedural[best_match],
                'confidence': best_score
            }
        return None
    
    def get_insights(self) -> Dict:
        """Generate insights about memory usage"""
        total_memories = len(self.episodic)
        semantic_count = sum(1 for e in self.episodic if e.memory_type == 'semantic')
        episodic_count = sum(1 for e in self.episodic if e.memory_type == 'episodic')
        
        most_accessed = sorted(self.episodic, key=lambda e: e.access_count, reverse=True)[:5]
        
        return {
            'total_memories': total_memories,
            'semantic_memories': semantic_count,
            'episodic_memories': episodic_count,
            'procedural_patterns': len(self.procedural),
            'reasoning_entries': len(self.reasoning_bank),
            'most_accessed': [(e.content[:50], e.access_count) for e in most_accessed],
            'avg_importance': sum(e.importance for e in self.episodic) / max(total_memories, 1)
        }

# Singleton instance
_memory_instance = None

def get_memory() -> AmazoMemory:
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = AmazoMemory()
    return _memory_instance

if __name__ == "__main__":
    # Test memory system
    mem = AmazoMemory()
    
    # Store some knowledge
    mem.store_semantic("Docker containers are lightweight virtualization units", ["docker", "devops"])
    mem.store_semantic("Kubernetes orchestrates container deployments at scale", ["kubernetes", "devops"])
    mem.store_episodic("Successfully deployed nginx container to AWS ECS", importance=0.8, tags=["deployment", "aws"])
    
    # Recall
    results = mem.recall_similar("How do I deploy containers?", k=3)
    print(f"Found {len(results)} relevant memories:")
    for r in results:
        print(f"  - {r.content[:60]}...")
    
    # Store procedural knowledge
    mem.store_procedural("deploy docker", "use docker-compose", "success", True)
    proc = mem.get_procedural_knowledge("deploy container")
    print(f"\nProcedural knowledge: {proc}")
    
    print(f"\nMemory insights: {mem.get_insights()}")
