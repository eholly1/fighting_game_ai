# Evolutionary Training Experiment: quick_test_final

## Experiment Overview
- **Started**: 2025-05-31 23:23:52
- **Population Size**: 3
- **Generations**: 1
- **Swiss Rounds**: 2

## Directory Structure
```
quick_test_final/
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
- **hall_of_fame.json**: Metadata for top 100 agents
- **top_agents/**: Individual Python files for each top agent
- **tournament_logs/**: Detailed tournament results for each generation
- **evolution_summary.json**: Progress tracking and key metrics

## Configuration
See `config.json` for complete experiment parameters.

## Usage
Load agents from `top_agents/` directory for testing or further evolution.
