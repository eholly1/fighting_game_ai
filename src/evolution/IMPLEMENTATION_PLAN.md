# Evolutionary Training System Implementation Plan

## 🎯 Overview
Evolutionary training system for fighting game AI using Claude API to generate and evolve rule-based agents through Swiss tournament evaluation.

## 📋 Design Decisions

### Swiss Tournament System
- **Efficiency**: O(n log n) vs O(n²) for round-robin
- **Rounds**: ceil(log2(population_size)) rounds per generation
- **Pairing**: Similar-strength opponents face each other
- **Scalability**: Supports populations of 50-200 agents

### Code Quality Constraints
- **Max Lines**: 1,400 lines (20x current SimplePolicy ~70 lines)
- **Max Characters**: 40,000 characters (20x current SimplePolicy ~2,000 chars)
- **Readability**: Clear variable names, comments, structured logic
- **No Fitness Penalty**: Hard limits only, no complexity penalties

### Agent Storage Strategy
- **Top 100 Agents**: Save best performers across all generations
- **Experiment Directory**: Organized structure with timestamps
- **No Generation Storage**: Only preserve hall of fame
- **File Format**: Individual Python files with metadata

### Future Features (Not Implemented Yet)
- Human-in-the-loop curation
- Meta-evolution of prompting strategies
- Strategy diversity mechanisms

## 🏗️ Implementation Phases

### Phase 1: Core Swiss Tournament System
**Goal**: Implement efficient tournament evaluation

**Components**:
- `swiss_tournament.py`: Core tournament logic
- `tournament_pairing.py`: Agent pairing algorithms
- `match_runner.py`: Individual match execution
- `tournament_results.py`: Results tracking and ranking

**Key Features**:
- Random pairings for round 1
- Swiss pairings for subsequent rounds (similar win rates)
- Strength of schedule tie-breaking
- Opponent history tracking (avoid repeat matches)

**Testing**:
- Unit tests with mock agents
- Performance benchmarks vs round-robin
- Fairness validation with known-strength agents

### Phase 2: Code Quality Controls
**Goal**: Ensure LLM generates clean, debuggable code

**Components**:
- `code_validator.py`: Syntax and length validation
- `safe_execution.py`: Isolated agent execution
- `prompt_templates.py`: Enhanced LLM prompting

**Key Features**:
- Line and character count limits
- AST parsing for syntax validation
- Dangerous pattern detection (imports, file I/O)
- Timeout and memory protection
- Enhanced prompts for readability

**Testing**:
- Validation with various code samples
- Safety tests with malicious code
- LLM prompt effectiveness evaluation

### Phase 3: Top Agent Tracking
**Goal**: Persistent storage of best performers

**Components**:
- `hall_of_fame.py`: Top agent management
- `experiment_manager.py`: Directory structure and metadata
- `agent_serialization.py`: Save/load agent code and stats

**Directory Structure**:
```
experiments/
└── evolutionary_run_YYYYMMDD_HHMMSS/
    ├── config.json                    # Evolution parameters
    ├── tournament_logs/               # Swiss tournament results
    │   ├── generation_001.json
    │   └── generation_002.json
    ├── top_agents/                    # Best 100 agents ever
    │   ├── rank_001_fitness_87.3_gen5_agent_042.py
    │   └── rank_002_fitness_85.1_gen3_agent_018.py
    └── evolution_summary.json         # Overall progress tracking
```

**Key Features**:
- Automatic ranking by fitness
- Metadata preservation (generation, fitness, lineage)
- Efficient updates (only save when top 100 changes)
- Human-readable Python files

### Phase 4: Integration Testing
**Goal**: End-to-end system validation

**Components**:
- `integration_tests.py`: Full evolution pipeline tests
- `performance_benchmarks.py`: Speed and efficiency metrics
- `evolution_runner.py`: Main execution script

**Key Features**:
- Small-scale evolution runs (10 agents, 5 generations)
- Performance comparison vs existing training
- Tournament fairness validation
- Agent quality progression tracking

## 🔧 Technical Specifications

### Agent Interface
```python
class EvolutionaryAgent:
    def get_action(self, state: np.ndarray) -> int:
        """
        Args:
            state: 26-element numpy array with game state
                state[22]: distance (0-1)
                state[23]: relative_position (-1 to 1)
                state[25]: health_advantage (-1 to 1)
        
        Returns:
            action: integer 0-9 representing game action
        """
```

### Action Space
```python
ACTIONS = {
    0: 'idle', 1: 'move_left', 2: 'move_right', 3: 'jump',
    4: 'punch', 5: 'kick', 6: 'block', 
    7: 'move_left_block', 8: 'move_right_block', 9: 'projectile'
}
```

### Fitness Evaluation
```python
def evaluate_agent_fitness(agent, opponents):
    """
    Multi-tier evaluation:
    1. Swiss tournament vs peers (30% weight)
    2. Matches vs rule-based opponents (70% weight)
    3. Behavioral metrics (future enhancement)
    
    Returns combined fitness score
    """
```

## 📊 Expected Performance

### Tournament Efficiency
- **Population 20**: 6 rounds vs 190 matches (97% reduction)
- **Population 50**: 6 rounds vs 1,225 matches (99.5% reduction)
- **Population 100**: 7 rounds vs 4,950 matches (99.9% reduction)

### Evaluation Speed (Estimated)
- **Small population (20)**: ~30 seconds per generation
- **Medium population (50)**: ~2 minutes per generation
- **Large population (100)**: ~5 minutes per generation

### Code Quality Metrics
- **Max agent complexity**: 20x rule-based baseline
- **Readability**: Structured prompts for clean code
- **Safety**: Isolated execution with timeouts

## 🚀 Getting Started

### Prerequisites
- Anthropic API key set in environment
- Python dependencies: anthropic, numpy, pygame
- Existing training environment in `src/training/`

### Quick Start
```bash
cd src/evolution
export ANTHROPIC_API_KEY="your_key_here"
python evolution_runner.py --population 20 --generations 10
```

### Configuration
```python
EvolutionConfig(
    population_size=20,
    generations=50,
    swiss_rounds=6,  # ceil(log2(20)) = 5, +1 for safety
    games_per_match=5,
    max_lines=1400,
    max_chars=40000,
    top_agents_to_save=100
)
```

## 📝 Development Notes

### Current Status
- [X] Phase 1: Swiss Tournament System
- [X] Phase 2: Code Quality Controls  
- [ ] Phase 3: Top Agent Tracking
- [ ] Phase 4: Integration Testing

### Next Steps
1. Implement core Swiss tournament logic
2. Create agent pairing algorithms
3. Add safety and validation layers
4. Build experiment management system

### Future Enhancements
- Human curation interface
- Meta-evolution of prompts
- Strategy diversity mechanisms
- Multi-objective optimization
- Behavioral analysis tools
