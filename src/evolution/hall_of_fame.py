#!/usr/bin/env python3
"""
Hall of Fame System for Evolutionary Training

Manages the top 100 agents across all generations with persistent storage,
ranking, and metadata preservation.
"""
import os
import json
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class AgentRecord:
    """Record of a top-performing agent"""
    agent_id: str
    generation: int
    fitness: float
    win_rate: float
    avg_reward: float
    code: str
    fighting_style: str
    creation_time: float
    tournament_stats: Dict[str, Any]
    lineage: List[str]  # Parent agent IDs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentRecord':
        """Create from dictionary"""
        return cls(**data)

class HallOfFame:
    """
    Manages the top 100 agents across all evolutionary training
    
    Features:
    - Persistent storage of best performers
    - Automatic ranking and metadata
    - Efficient updates and queries
    - Human-readable Python files
    """
    
    def __init__(self, experiment_dir: str, max_agents: int = 100):
        """
        Initialize Hall of Fame
        
        Args:
            experiment_dir: Directory for this evolutionary experiment
            max_agents: Maximum number of agents to preserve
        """
        self.experiment_dir = experiment_dir
        self.max_agents = max_agents
        self.hall_of_fame_dir = os.path.join(experiment_dir, "top_agents")
        self.metadata_file = os.path.join(experiment_dir, "hall_of_fame.json")
        
        # Create directories
        os.makedirs(self.hall_of_fame_dir, exist_ok=True)
        
        # Load existing hall of fame
        self.agents: List[AgentRecord] = []
        self._load_hall_of_fame()
        
        print(f"🏆 Hall of Fame initialized: {len(self.agents)}/{self.max_agents} agents")
    
    def add_agents(self, new_agents: List[Dict[str, Any]], generation: int):
        """
        Add new agents to hall of fame if they qualify
        
        Args:
            new_agents: List of agent data dictionaries
            generation: Current generation number
        """
        added_count = 0
        
        for agent_data in new_agents:
            if self._should_add_agent(agent_data):
                record = self._create_agent_record(agent_data, generation)
                self.agents.append(record)
                added_count += 1
        
        # Sort by fitness and keep top agents
        self.agents.sort(key=lambda x: x.fitness, reverse=True)
        self.agents = self.agents[:self.max_agents]
        
        # Save updated hall of fame
        self._save_hall_of_fame()
        
        if added_count > 0:
            print(f"🏆 Added {added_count} agents to Hall of Fame (Generation {generation})")
            print(f"   Current size: {len(self.agents)}/{self.max_agents}")
            if self.agents:
                print(f"   Best fitness: {self.agents[0].fitness:.2f}")
    
    def get_top_agents(self, n: int = 10) -> List[AgentRecord]:
        """Get top N agents"""
        return self.agents[:min(n, len(self.agents))]
    
    def get_agent_by_id(self, agent_id: str) -> Optional[AgentRecord]:
        """Get specific agent by ID"""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        return None
    
    def get_agents_by_generation(self, generation: int) -> List[AgentRecord]:
        """Get all agents from a specific generation"""
        return [agent for agent in self.agents if agent.generation == generation]
    
    def get_agents_by_style(self, fighting_style: str) -> List[AgentRecord]:
        """Get all agents with a specific fighting style"""
        return [agent for agent in self.agents if agent.fighting_style == fighting_style]
    
    def get_hall_of_fame_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the hall of fame"""
        if not self.agents:
            return {'total_agents': 0}
        
        # Basic stats
        fitness_values = [agent.fitness for agent in self.agents]
        generations = [agent.generation for agent in self.agents]
        styles = [agent.fighting_style for agent in self.agents]
        
        # Style distribution
        style_counts = {}
        for style in styles:
            style_counts[style] = style_counts.get(style, 0) + 1
        
        # Generation distribution
        generation_counts = {}
        for gen in generations:
            generation_counts[gen] = generation_counts.get(gen, 0) + 1
        
        return {
            'total_agents': len(self.agents),
            'best_fitness': max(fitness_values),
            'avg_fitness': sum(fitness_values) / len(fitness_values),
            'fitness_range': [min(fitness_values), max(fitness_values)],
            'generation_range': [min(generations), max(generations)],
            'style_distribution': style_counts,
            'generation_distribution': generation_counts,
            'latest_addition': max(agent.creation_time for agent in self.agents),
            'oldest_agent': min(agent.creation_time for agent in self.agents)
        }
    
    def export_agent_code(self, agent_id: str, output_path: str) -> bool:
        """Export specific agent code to a file"""
        agent = self.get_agent_by_id(agent_id)
        if not agent:
            return False
        
        try:
            with open(output_path, 'w') as f:
                f.write(self._format_agent_file(agent))
            return True
        except Exception as e:
            print(f"❌ Failed to export agent {agent_id}: {e}")
            return False
    
    def _should_add_agent(self, agent_data: Dict[str, Any]) -> bool:
        """Determine if an agent should be added to hall of fame"""
        fitness = agent_data.get('fitness', 0.0)
        
        # Always add if we have space
        if len(self.agents) < self.max_agents:
            return fitness > 0.0
        
        # Only add if better than worst current agent
        worst_fitness = min(agent.fitness for agent in self.agents)
        return fitness > worst_fitness
    
    def _create_agent_record(self, agent_data: Dict[str, Any], generation: int) -> AgentRecord:
        """Create an AgentRecord from agent data"""
        return AgentRecord(
            agent_id=agent_data.get('agent_id', f'unknown_{int(time.time())}'),
            generation=generation,
            fitness=agent_data.get('fitness', 0.0),
            win_rate=agent_data.get('win_rate', 0.0),
            avg_reward=agent_data.get('avg_reward', 0.0),
            code=agent_data.get('code', ''),
            fighting_style=agent_data.get('fighting_style', 'unknown'),
            creation_time=time.time(),
            tournament_stats=agent_data.get('tournament_stats', {}),
            lineage=agent_data.get('lineage', [])
        )
    
    def _load_hall_of_fame(self):
        """Load existing hall of fame from disk"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                
                self.agents = [AgentRecord.from_dict(agent_data) 
                              for agent_data in data.get('agents', [])]
                
                print(f"📁 Loaded {len(self.agents)} agents from existing hall of fame")
                
            except Exception as e:
                print(f"⚠️  Could not load existing hall of fame: {e}")
                self.agents = []
    
    def _save_hall_of_fame(self):
        """Save hall of fame to disk"""
        try:
            # Save metadata
            metadata = {
                'experiment_info': {
                    'max_agents': self.max_agents,
                    'last_updated': time.time(),
                    'total_agents': len(self.agents)
                },
                'agents': [agent.to_dict() for agent in self.agents]
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save individual agent files
            self._save_agent_files()
            
        except Exception as e:
            print(f"❌ Failed to save hall of fame: {e}")
    
    def _save_agent_files(self):
        """Save individual Python files for each agent"""
        # Clear existing files
        for filename in os.listdir(self.hall_of_fame_dir):
            if filename.endswith('.py'):
                os.remove(os.path.join(self.hall_of_fame_dir, filename))
        
        # Save current agents
        for rank, agent in enumerate(self.agents, 1):
            filename = self._generate_agent_filename(agent, rank)
            filepath = os.path.join(self.hall_of_fame_dir, filename)
            
            try:
                with open(filepath, 'w') as f:
                    f.write(self._format_agent_file(agent, rank))
            except Exception as e:
                print(f"⚠️  Failed to save agent file {filename}: {e}")
    
    def _generate_agent_filename(self, agent: AgentRecord, rank: int) -> str:
        """Generate filename for agent"""
        # Clean agent ID for filename
        clean_id = ''.join(c for c in agent.agent_id if c.isalnum() or c in '_-')
        
        return f"rank_{rank:03d}_fitness_{agent.fitness:.1f}_gen_{agent.generation}_{clean_id}.py"
    
    def _format_agent_file(self, agent: AgentRecord, rank: Optional[int] = None) -> str:
        """Format agent code with metadata header"""
        header = f'''"""
Hall of Fame Agent
==================

Agent ID: {agent.agent_id}
Rank: {rank if rank else "N/A"}/{len(self.agents)}
Generation: {agent.generation}
Fighting Style: {agent.fighting_style}

Performance Metrics:
- Fitness: {agent.fitness:.2f}
- Win Rate: {agent.win_rate:.1%}
- Average Reward: {agent.avg_reward:.2f}

Created: {datetime.fromtimestamp(agent.creation_time).strftime("%Y-%m-%d %H:%M:%S")}
Lineage: {" -> ".join(agent.lineage) if agent.lineage else "Original"}

Tournament Stats:
{json.dumps(agent.tournament_stats, indent=2) if agent.tournament_stats else "None"}
"""

# Agent Code:
'''
        
        return header + agent.code

def test_hall_of_fame():
    """Test the Hall of Fame system"""
    print("🧪 Testing Hall of Fame System")
    print("=" * 50)
    
    # Create test directory
    test_dir = f"test_experiment_{int(time.time())}"
    
    try:
        # Initialize hall of fame
        hof = HallOfFame(test_dir, max_agents=5)  # Small size for testing
        
        # Test 1: Add agents
        test_agents = [
            {
                'agent_id': 'test_agent_1',
                'fitness': 85.5,
                'win_rate': 0.75,
                'avg_reward': 120.3,
                'code': 'def get_action(state): return 4',
                'fighting_style': 'aggressive',
                'tournament_stats': {'wins': 15, 'losses': 5}
            },
            {
                'agent_id': 'test_agent_2', 
                'fitness': 92.1,
                'win_rate': 0.80,
                'avg_reward': 135.7,
                'code': 'def get_action(state): return 6',
                'fighting_style': 'defensive',
                'tournament_stats': {'wins': 16, 'losses': 4}
            },
            {
                'agent_id': 'test_agent_3',
                'fitness': 78.3,
                'win_rate': 0.65,
                'avg_reward': 98.2,
                'code': 'def get_action(state): return 9',
                'fighting_style': 'zoner',
                'tournament_stats': {'wins': 13, 'losses': 7}
            }
        ]
        
        hof.add_agents(test_agents, generation=1)
        
        print(f"✅ Added {len(test_agents)} agents")
        print(f"   Hall of Fame size: {len(hof.agents)}")
        
        # Test 2: Check ranking
        top_agents = hof.get_top_agents(3)
        expected_order = ['test_agent_2', 'test_agent_1', 'test_agent_3']  # By fitness
        actual_order = [agent.agent_id for agent in top_agents]
        
        ranking_correct = actual_order == expected_order
        print(f"✅ Ranking test: {'PASS' if ranking_correct else 'FAIL'}")
        
        # Test 3: Statistics
        stats = hof.get_hall_of_fame_stats()
        stats_valid = (stats['total_agents'] == 3 and 
                      stats['best_fitness'] == 92.1 and
                      'aggressive' in stats['style_distribution'])
        
        print(f"✅ Statistics test: {'PASS' if stats_valid else 'FAIL'}")
        
        # Test 4: File generation
        agent_files = os.listdir(hof.hall_of_fame_dir)
        python_files = [f for f in agent_files if f.endswith('.py')]
        
        files_created = len(python_files) == 3
        print(f"✅ File generation test: {'PASS' if files_created else 'FAIL'}")
        
        # Test 5: Agent retrieval
        agent = hof.get_agent_by_id('test_agent_2')
        retrieval_works = agent is not None and agent.fitness == 92.1
        
        print(f"✅ Agent retrieval test: {'PASS' if retrieval_works else 'FAIL'}")
        
        print(f"\n📊 Hall of Fame test complete")
        
        return True
        
    except Exception as e:
        print(f"❌ Hall of Fame test failed: {e}")
        return False
    
    finally:
        # Cleanup test directory
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_hall_of_fame()
