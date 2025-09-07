# Fighting Game AI

## Overview

This project is a research and development environment for building AI agents to play a custom fighting game. The goal is to create agents that can challenge human players at various difficulty levels, using a combination of reinforcement learning, evolutionary strategies, and human feedback.

The project includes:
- A fighting game engine with audio, rendering, and entity management
- AI agent training and evaluation tools
- Human demonstration recording and behavioral cloning
- Evolutionary agent generation and selection
- Experiment management and dashboards

## Basic Usage

### Running the Game
To launch the main game:
```bash
python src/main.py
```

### Training AI Agents
To train agents using reinforcement learning or behavioral cloning:
```bash
python src/human_demonstrations/train_from_demos.py  # Pretrain from human demonstrations
python src/training/run_training.py             # PPO training entry point
python src/evolution/run_evolution.py           # Evolutionary Training
```

### Playing Against AI
To play against an evolved agent:
```bash
python src/play_vs_evolved_agent.py
```

### Running Tests
To run the test suite:
```bash
pytest tests/
```

## AI Training and Evolution

Initially, the AI agents were trained using self-play with Proximal Policy Optimization (PPO), starting from models initialized with human demonstration data. However, the resulting agents were highly aggressive and difficult for humans to beat, even at lower difficulty settings.

To address this, the project pivoted to an evolutionary approach. Hardcoded agents were generated using Claude (an AI language model), and a population of these agents was evolved through competitive matches. From this population, the most aggressive and most defensive agents were selected and further modified using human feedback to create three distinct difficulty levels:
- **Easy**: Defensive agent, less aggressive, easier for beginners
- **Medium**: Balanced agent, moderate challenge
- **Hard**: Aggressive agent, challenging for experienced players

This approach allowed for more controllable and enjoyable difficulty scaling for human players.

## License
See `LICENSE` for details.
