# Amazo Core Integration
# Main entry point integrating all self-improvement systems

import sys
import json
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from context_manager import get_context_manager, ContextManager
from memory_system import get_memory, AmazoMemory
from ensemble import get_ensemble, MultiModelEnsemble, AdaptiveRouter

class AmazoCore:
    """
    Integrated AI executive companion with self-improvement capabilities.
    Combines DeerFlow's context engineering, Claude-Flow's ensemble reasoning,
    and Ouroboros's self-modification principles.
    """
    
    def __init__(self):
        self.context = get_context_manager()
        self.memory = get_memory()
        self.ensemble = get_ensemble()
        self.router = AdaptiveRouter()
        self.version = "2.0.0-alpha"
        self.capabilities = self._load_capabilities()
    
    def _load_capabilities(self) -> dict:
        return {
            'context_management': True,
            'progressive_skill_loading': True,
            'token_optimization': True,
            'hnsw_memory': True,
            'multi_model_consensus': True,
            'adaptive_routing': True,
            'self_learning': True,
            'procedural_memory': True,
        }
    
    async def process(self, user_message: str, system_context: str = "") -> dict:
        """
        Main processing pipeline with full self-improvement stack.
        """
        # 1. Prepare optimized context
        ctx = self.context.prepare_context(user_message, system_context)
        
        # 2. Recall relevant memories
        relevant_memories = self.memory.recall_similar(user_message, k=3)
        memory_context = "\n".join([m.content for m in relevant_memories])
        
        # 3. Route to optimal execution path
        route_config = self.router.route(user_message)
        
        # 4. Execute with appropriate method
        if route_config['method'] == 'ensemble':
            result = await self.ensemble.think(user_message, system_context)
            response = result.final_answer
            confidence = result.consensus_score
        else:
            # Single model or WASM
            response = f"[Routed via {route_config['method']}] Processing: {user_message}"
            confidence = 0.8
        
        # 5. Store experience
        self.memory.store_episodic(
            f"User: {user_message}\nResponse: {response}",
            importance=0.6 if confidence > 0.8 else 0.4
        )
        
        # 6. Update context history
        self.context.add_to_history('user', user_message)
        self.context.add_to_history('assistant', response)
        
        return {
            'response': response,
            'confidence': confidence,
            'route': route_config,
            'context_used': ctx.used_tokens,
            'memories_recalled': len(relevant_memories),
            'skills_active': len(ctx.active_skills)
        }
    
    def get_status(self) -> dict:
        """Report current system status"""
        return {
            'version': self.version,
            'capabilities': self.capabilities,
            'memory_stats': self.memory.get_insights(),
            'context_stats': self.context.report_usage(),
            'skills_available': len(self.context.skill_library.skills)
        }

# Global instance
_amazo = None

def get_amazo() -> AmazoCore:
    global _amazo
    if _amazo is None:
        _amazo = AmazoCore()
    return _amazo

if __name__ == "__main__":
    import asyncio
    
    amazo = AmazoCore()
    
    print("=" * 60)
    print("AMAZO CORE v2.0 - Self-Improvement System")
    print("=" * 60)
    
    # Show status
    status = amazo.get_status()
    print(f"\n📊 System Status:")
    print(f"  Version: {status['version']}")
    print(f"  Capabilities: {len(status['capabilities'])}")
    print(f"  Skills Available: {status['skills_available']}")
    print(f"  Memory Entries: {status['memory_stats']['total_memories']}")
    
    # Test processing
    print(f"\n🧪 Testing processing pipeline...")
    
    async def test():
        result = await amazo.process(
            "How do I deploy a Docker container to AWS?",
            "You are Amazo, an AI executive companion."
        )
        
        print(f"\n✅ Result:")
        print(f"  Route: {result['route']['method']}")
        print(f"  Confidence: {result['confidence']:.0%}")
        print(f"  Context Used: {result['context_used']} tokens")
        print(f"  Memories Recalled: {result['memories_recalled']}")
        print(f"  Active Skills: {result['skills_active']}")
    
    asyncio.run(test())
    
    print("\n" + "=" * 60)
    print("Amazo Core initialized and ready.")
    print("=" * 60)
