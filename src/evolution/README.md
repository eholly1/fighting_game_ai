# Evolutionary Fighting Game AI Training System

A complete evolutionary training system that uses Claude API to generate and evolve fighting game AI agents through Swiss tournament evaluation.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Anthropic API key
- Required packages: `pip install anthropic python-dotenv pygame numpy`

### 2. Environment Setup
Create a `.env` file in your project root:
```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 3. Run Evolution
```bash
cd src/evolution
python run_evolution.py
```

This will show an interactive menu with options for different evolution runs.

## 📋 Command Line Usage

### Basic Usage
```bash
# Quick test (3 agents, 1 generation)
python evolution_runner.py --population 3 --generations 1

# Small evolution (good for testing)
python evolution_runner.py --population 8 --generations 3

# Full evolution (production run)
python evolution_runner.py --population 15 --generations 10
```

### Advanced Options
```bash
python evolution_runner.py \
  --population 20 \
  --generations 25 \
  --games-per-match 5 \
  --experiment-name "my_experiment" \
  --anthropic-model "claude-3-5-sonnet-20241022"
```

### Command Line Arguments
- `--population`: Number of agents per generation (default: 15)
- `--generations`: Number of evolution cycles (default: 10)
- `--games-per-match`: Games played per tournament match (default: 3)
- `--experiment-name`: Custom name for the experiment
- `--anthropic-key`: Override API key from .env file
- `--anthropic-model`: Override model from .env file
- `--skip-env-setup`: Skip automatic .env loading

## 📁 Output Structure

Each evolution run creates an organized experiment directory:

```
experiments/
└── evolutionary_run_YYYYMMDD_HHMMSS/
    ├── config.json                    # Experiment configuration
    ├── experiment.log                 # Detailed execution log
    ├── evolution_summary.json         # Progress tracking
    ├── hall_of_fame.json             # Top 100 agents metadata
    ├── tournament_logs/               # Swiss tournament results
    │   ├── generation_001_tournament.json
    │   └── generation_002_tournament.json
    ├── top_agents/                    # Best agent code files
    │   ├── rank_001_fitness_87.3_gen5_agent_042.py
    │   └── rank_002_fitness_85.1_gen3_agent_018.py
    ├── agent_archive/                 # All agents from all generations
    └── analysis/                      # Post-experiment analysis
        └── experiment_report.md
```

## 🏆 Key Features

### Swiss Tournament System
- **Efficient**: O(n log n) complexity vs O(n²) for round-robin
- **Fair**: Similar-strength opponents paired together
- **Scalable**: Handles populations from 5-100+ agents

### Code Quality Controls
- **Safe Execution**: Timeout protection and error isolation
- **Code Validation**: Syntax checking and security validation
- **LLM Optimization**: Enhanced prompts for bug-free code generation

### Top Agent Tracking
- **Hall of Fame**: Preserves top 100 agents across all generations
- **Experiment Management**: Organized directory structure and logging
- **Agent Serialization**: Human-readable Python files with metadata

## 🧬 Evolution Process

1. **Initial Population**: Claude generates diverse fighting styles
2. **Swiss Tournament**: Agents compete in efficient tournaments
3. **Fitness Evaluation**: Performance vs rule-based opponents
4. **Selection**: Tournament selection of best performers
5. **Evolution**: Mutation and crossover via Claude API
6. **Hall of Fame**: Best agents preserved permanently

## 🎯 Agent Interface

Each evolved agent implements this interface:
```python
def get_action(state):
    """
    Args:
        state: 26-element numpy array with game state
            state[22]: distance to opponent (0-1)
            state[23]: relative position (-1 to 1)
            state[25]: health advantage (-1 to 1)
    
    Returns:
        action: integer 0-9 representing game action
            0=idle, 1=move_left, 2=move_right, 3=jump,
            4=punch, 5=kick, 6=block, 
            7=move_left_block, 8=move_right_block, 9=projectile
    """
    # Strategic decision-making logic here
    return action
```

## 📊 Performance Characteristics

- **Population 15**: ~2 minutes per generation
- **Population 50**: ~5 minutes per generation
- **Efficiency**: 87-99% reduction vs round-robin tournaments
- **Scalability**: Tested up to 100 agents

## 🔧 Environment Variables

The system supports multiple environment variable names:

### API Key (use any one):
- `ANTHROPIC_API_KEY`
- `ANTHROPIC_KEY`
- `CLAUDE_API_KEY`
- `CLAUDE_KEY`

### Model Name (use any one):
- `ANTHROPIC_MODEL`
- `CLAUDE_MODEL`
- `ANTHROPIC_MODEL_NAME`
- `CLAUDE_MODEL_NAME`

## 🧪 Testing

Run the test suite to verify everything is working:
```bash
# Test individual components
python test_swiss_tournament.py
python test_code_quality.py
python test_top_agent_tracking.py

# Test complete integration
python test_simple_integration.py

# Test environment setup
python env_config.py
```

## 🐛 Troubleshooting

### Common Issues

**"No Anthropic API key found"**
- Check your .env file exists and contains `ANTHROPIC_API_KEY=sk-ant-...`
- Verify the .env file is in the project root directory
- Try using `--anthropic-key` command line argument

**"Environment not available"**
- Make sure you're in the correct directory: `cd src/evolution`
- Install required packages: `pip install -r ../../requirements.txt`
- Check that the training environment is available in `../training/`

**"Agent creation failed"**
- Check your internet connection (Claude API calls)
- Verify your API key is valid and has sufficient credits
- Try reducing population size for testing

**Performance Issues**
- Reduce `--games-per-match` for faster evaluation
- Use smaller populations for testing
- Check system resources (memory/CPU)

### Debug Mode
Add debug output by setting environment variables:
```bash
export DEBUG=1
python evolution_runner.py --population 5 --generations 1
```

## 📈 Monitoring Progress

### Real-time Monitoring
- Watch the console output for generation progress
- Check `experiment.log` for detailed logging
- Monitor `evolution_summary.json` for progress tracking

### Post-Evolution Analysis
- Review `analysis/experiment_report.md` for comprehensive analysis
- Examine top agents in `top_agents/` directory
- Load and test agents using the serialization system

## 🎮 Using Evolved Agents

Load and use evolved agents in your fighting game:
```python
from agent_serialization import AgentSerializer

# Load an agent
serializer = AgentSerializer("experiments/my_run/top_agents")
agent = serializer.load_agent_python("rank_001_fitness_87.3_gen5_agent_042.py")

# Use in game
if agent:
    action = agent.get_action(game_state)
```

## 🤝 Contributing

The evolutionary training system is modular and extensible:
- Add new fighting styles in `prompt_templates.py`
- Modify evaluation criteria in `match_runner.py`
- Extend tournament systems in `swiss_tournament.py`
- Add new analysis tools in the analysis framework

## 📄 License

This evolutionary training system is part of the fighting game AI project.
