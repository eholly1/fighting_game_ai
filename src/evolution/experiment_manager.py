#!/usr/bin/env python3
"""
Experiment Manager for Evolutionary Training

Manages experiment directory structure, configuration, logging,
and coordination between all evolutionary training components.
"""
import os
import json
import time
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class ExperimentConfig:
    """Configuration for an evolutionary experiment"""
    # Population parameters
    population_size: int = 20
    generations: int = 50
    max_agents_hall_of_fame: int = 100
    
    # Tournament parameters
    swiss_rounds: Optional[int] = None  # Auto-calculated if None
    games_per_match: int = 5
    
    # Code constraints
    max_lines: int = 1400
    max_chars: int = 40000
    timeout_seconds: float = 1.0
    
    # Evolution parameters
    mutation_rate: float = 0.3
    elite_size: int = 3
    
    # LLM parameters
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # Evaluation parameters
    rule_based_opponents: List[str] = None
    
    def __post_init__(self):
        if self.rule_based_opponents is None:
            self.rule_based_opponents = ['easy', 'medium', 'hard']
        
        if self.swiss_rounds is None:
            import math
            self.swiss_rounds = max(1, math.ceil(math.log2(self.population_size)))

class ExperimentManager:
    """
    Manages evolutionary training experiments with proper organization
    """
    
    def __init__(self, experiment_name: Optional[str] = None, 
                 config: Optional[ExperimentConfig] = None):
        """
        Initialize experiment manager
        
        Args:
            experiment_name: Name for the experiment (auto-generated if None)
            config: Experiment configuration (default if None)
        """
        self.config = config or ExperimentConfig()
        
        # Generate experiment name and directory
        if experiment_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            experiment_name = f"evolutionary_run_{timestamp}"
        
        self.experiment_name = experiment_name
        self.experiment_dir = os.path.join("experiments", experiment_name)
        
        # Create directory structure
        self._create_directory_structure()
        
        # Save configuration
        self._save_config()
        
        # Initialize logging
        self.log_file = os.path.join(self.experiment_dir, "experiment.log")
        self._log(f"Experiment {experiment_name} initialized")
        
        print(f"🧪 Experiment initialized: {experiment_name}")
        print(f"📁 Directory: {self.experiment_dir}")
    
    def _create_directory_structure(self):
        """Create the experiment directory structure"""
        directories = [
            self.experiment_dir,
            os.path.join(self.experiment_dir, "tournament_logs"),
            os.path.join(self.experiment_dir, "top_agents"),
            os.path.join(self.experiment_dir, "generation_snapshots"),
            os.path.join(self.experiment_dir, "analysis")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Create README
        readme_path = os.path.join(self.experiment_dir, "README.md")
        with open(readme_path, 'w') as f:
            f.write(self._generate_readme())
    
    def _generate_readme(self) -> str:
        """Generate README for the experiment"""
        return f"""# Evolutionary Training Experiment: {self.experiment_name}

## Experiment Overview
- **Started**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Population Size**: {self.config.population_size}
- **Generations**: {self.config.generations}
- **Swiss Rounds**: {self.config.swiss_rounds}

## Directory Structure
```
{self.experiment_name}/
├── config.json                 # Experiment configuration
├── experiment.log              # Detailed experiment log
├── evolution_summary.json      # High-level progress summary
├── hall_of_fame.json          # Top 100 agents metadata
├── tournament_logs/            # Swiss tournament results by generation
├── top_agents/                 # Best agent code files (Python)
├── generation_snapshots/       # Full population snapshots (optional)
└── analysis/                   # Post-experiment analysis files
```

## Key Files
- **hall_of_fame.json**: Metadata for top {self.config.max_agents_hall_of_fame} agents
- **top_agents/**: Individual Python files for each top agent
- **tournament_logs/**: Detailed tournament results for each generation
- **evolution_summary.json**: Progress tracking and key metrics

## Configuration
See `config.json` for complete experiment parameters.

## Usage
Load agents from `top_agents/` directory for testing or further evolution.
"""
    
    def _save_config(self):
        """Save experiment configuration"""
        config_path = os.path.join(self.experiment_dir, "config.json")
        
        config_dict = asdict(self.config)
        config_dict['experiment_name'] = self.experiment_name
        config_dict['created_at'] = time.time()
        config_dict['created_at_human'] = datetime.now().isoformat()
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def log_generation_start(self, generation: int, population_size: int):
        """Log the start of a generation"""
        message = f"Generation {generation} started with {population_size} agents"
        self._log(message)
        print(f"🧬 {message}")
    
    def log_generation_complete(self, generation: int, stats: Dict[str, Any]):
        """Log generation completion with statistics"""
        message = f"Generation {generation} complete"
        self._log(message)
        self._log(f"  Best fitness: {stats.get('best_fitness', 'N/A')}")
        self._log(f"  Avg fitness: {stats.get('avg_fitness', 'N/A')}")
        self._log(f"  Valid agents: {stats.get('valid_agents', 'N/A')}")
        
        print(f"✅ {message}")
        print(f"   Best fitness: {stats.get('best_fitness', 'N/A')}")
    
    def save_tournament_results(self, generation: int, tournament_results: Dict[str, Any]):
        """Save tournament results for a generation"""
        filename = f"generation_{generation:03d}_tournament.json"
        filepath = os.path.join(self.experiment_dir, "tournament_logs", filename)
        
        tournament_data = {
            'generation': generation,
            'timestamp': time.time(),
            'results': tournament_results
        }
        
        with open(filepath, 'w') as f:
            json.dump(tournament_data, f, indent=2)
        
        self._log(f"Saved tournament results for generation {generation}")
    
    def save_generation_snapshot(self, generation: int, population_data: List[Dict[str, Any]]):
        """Save complete population snapshot (optional, for detailed analysis)"""
        filename = f"generation_{generation:03d}_population.json"
        filepath = os.path.join(self.experiment_dir, "generation_snapshots", filename)
        
        snapshot_data = {
            'generation': generation,
            'timestamp': time.time(),
            'population_size': len(population_data),
            'agents': population_data
        }
        
        with open(filepath, 'w') as f:
            json.dump(snapshot_data, f, indent=2)
        
        self._log(f"Saved population snapshot for generation {generation}")
    
    def update_evolution_summary(self, generation: int, summary_stats: Dict[str, Any]):
        """Update the high-level evolution summary"""
        summary_path = os.path.join(self.experiment_dir, "evolution_summary.json")
        
        # Load existing summary
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                summary = json.load(f)
        else:
            summary = {
                'experiment_name': self.experiment_name,
                'config': asdict(self.config),
                'started_at': time.time(),
                'generations': []
            }
        
        # Add generation data
        generation_data = {
            'generation': generation,
            'timestamp': time.time(),
            **summary_stats
        }
        
        # Update or append generation data
        existing_gen = next((i for i, g in enumerate(summary['generations']) 
                           if g['generation'] == generation), None)
        
        if existing_gen is not None:
            summary['generations'][existing_gen] = generation_data
        else:
            summary['generations'].append(generation_data)
        
        # Update summary metadata
        summary['last_updated'] = time.time()
        summary['current_generation'] = generation
        summary['total_generations_completed'] = len(summary['generations'])
        
        # Save updated summary
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self._log(f"Updated evolution summary for generation {generation}")
    
    def get_experiment_progress(self) -> Dict[str, Any]:
        """Get current experiment progress"""
        summary_path = os.path.join(self.experiment_dir, "evolution_summary.json")
        
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                summary = json.load(f)
            
            progress = {
                'experiment_name': summary['experiment_name'],
                'current_generation': summary.get('current_generation', 0),
                'total_generations': self.config.generations,
                'progress_percent': (summary.get('current_generation', 0) / self.config.generations) * 100,
                'generations_completed': summary.get('total_generations_completed', 0),
                'started_at': summary.get('started_at'),
                'last_updated': summary.get('last_updated'),
                'recent_stats': summary['generations'][-5:] if summary.get('generations') else []
            }
            
            return progress
        else:
            return {
                'experiment_name': self.experiment_name,
                'current_generation': 0,
                'total_generations': self.config.generations,
                'progress_percent': 0.0,
                'generations_completed': 0
            }
    
    def create_analysis_report(self) -> str:
        """Create a comprehensive analysis report"""
        report_path = os.path.join(self.experiment_dir, "analysis", "experiment_report.md")
        
        progress = self.get_experiment_progress()
        
        # Load hall of fame data
        hof_path = os.path.join(self.experiment_dir, "hall_of_fame.json")
        hof_data = {}
        if os.path.exists(hof_path):
            with open(hof_path, 'r') as f:
                hof_data = json.load(f)
        
        report_content = f"""# Experiment Analysis Report

## Experiment: {self.experiment_name}

### Overview
- **Progress**: {progress['progress_percent']:.1f}% ({progress['current_generation']}/{progress['total_generations']} generations)
- **Started**: {datetime.fromtimestamp(progress.get('started_at', 0)).strftime('%Y-%m-%d %H:%M:%S') if progress.get('started_at') else 'Unknown'}
- **Last Updated**: {datetime.fromtimestamp(progress.get('last_updated', 0)).strftime('%Y-%m-%d %H:%M:%S') if progress.get('last_updated') else 'Unknown'}

### Configuration
- Population Size: {self.config.population_size}
- Swiss Rounds: {self.config.swiss_rounds}
- Games per Match: {self.config.games_per_match}
- Code Limits: {self.config.max_lines} lines, {self.config.max_chars} chars

### Hall of Fame
- Total Agents: {hof_data.get('experiment_info', {}).get('total_agents', 0)}/{self.config.max_agents_hall_of_fame}
- Best Fitness: {max([agent.get('fitness', 0) for agent in hof_data.get('agents', [])], default=0):.2f}

### Recent Progress
"""
        
        for gen_data in progress.get('recent_stats', []):
            report_content += f"- Generation {gen_data['generation']}: Best fitness {gen_data.get('best_fitness', 'N/A')}\n"
        
        report_content += f"""
### Files Generated
- Tournament Logs: {len(os.listdir(os.path.join(self.experiment_dir, 'tournament_logs')))} files
- Agent Files: {len([f for f in os.listdir(os.path.join(self.experiment_dir, 'top_agents')) if f.endswith('.py')])} files

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        return report_path
    
    def _log(self, message: str):
        """Write message to experiment log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

def test_experiment_manager():
    """Test the experiment manager"""
    print("🧪 Testing Experiment Manager")
    print("=" * 50)
    
    # Create test experiment
    config = ExperimentConfig(
        population_size=10,
        generations=5,
        max_agents_hall_of_fame=20
    )
    
    experiment = ExperimentManager("test_experiment", config)
    
    try:
        # Test 1: Directory structure
        required_dirs = ["tournament_logs", "top_agents", "generation_snapshots", "analysis"]
        dirs_exist = all(os.path.exists(os.path.join(experiment.experiment_dir, d)) for d in required_dirs)
        print(f"✅ Directory structure: {'PASS' if dirs_exist else 'FAIL'}")
        
        # Test 2: Configuration saving
        config_exists = os.path.exists(os.path.join(experiment.experiment_dir, "config.json"))
        print(f"✅ Configuration saved: {'PASS' if config_exists else 'FAIL'}")
        
        # Test 3: Logging
        experiment.log_generation_start(1, 10)
        experiment.log_generation_complete(1, {'best_fitness': 85.5, 'avg_fitness': 72.3})
        
        log_exists = os.path.exists(experiment.log_file)
        print(f"✅ Logging works: {'PASS' if log_exists else 'FAIL'}")
        
        # Test 4: Tournament results saving
        tournament_results = {
            'total_matches': 25,
            'avg_fitness': 72.3,
            'best_agent': 'test_agent_1'
        }
        experiment.save_tournament_results(1, tournament_results)
        
        tournament_file = os.path.join(experiment.experiment_dir, "tournament_logs", "generation_001_tournament.json")
        tournament_saved = os.path.exists(tournament_file)
        print(f"✅ Tournament results: {'PASS' if tournament_saved else 'FAIL'}")
        
        # Test 5: Evolution summary
        summary_stats = {
            'best_fitness': 85.5,
            'avg_fitness': 72.3,
            'valid_agents': 8,
            'total_matches': 25
        }
        experiment.update_evolution_summary(1, summary_stats)
        
        summary_exists = os.path.exists(os.path.join(experiment.experiment_dir, "evolution_summary.json"))
        print(f"✅ Evolution summary: {'PASS' if summary_exists else 'FAIL'}")
        
        # Test 6: Progress tracking
        progress = experiment.get_experiment_progress()
        progress_valid = (progress['current_generation'] == 1 and 
                         progress['total_generations'] == 5)
        print(f"✅ Progress tracking: {'PASS' if progress_valid else 'FAIL'}")
        
        # Test 7: Analysis report
        report_path = experiment.create_analysis_report()
        report_created = os.path.exists(report_path)
        print(f"✅ Analysis report: {'PASS' if report_created else 'FAIL'}")
        
        print(f"\n📊 Experiment Manager test complete")
        return True
        
    except Exception as e:
        print(f"❌ Experiment Manager test failed: {e}")
        return False
    
    finally:
        # Cleanup
        if os.path.exists(experiment.experiment_dir):
            shutil.rmtree(experiment.experiment_dir)

if __name__ == "__main__":
    test_experiment_manager()
