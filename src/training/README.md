# Fighting Game RL Training

This directory contains the reinforcement learning training system for the 2D fighting game AI.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the setup:**
   ```bash
   python run_training.py --mode test
   ```

3. **Run quick training (for testing):**
   ```bash
   python run_training.py --mode quick --difficulty easy --steps 1000
   ```

4. **Run full training:**
   ```bash
   python run_training.py --mode full
   ```

## Training Modes

### Test Mode
```bash
python run_training.py --mode test
```
- Tests environment and models
- Verifies everything is working correctly
- Run this first!

### Quick Training Mode
```bash
python run_training.py --mode quick --difficulty easy --steps 1000
```
- Fast training for testing (1000 steps)
- Good for verifying training pipeline
- Options: `--difficulty {easy,medium,hard}` `--steps N`

### Full Training Mode
```bash
python run_training.py --mode full
```
- Complete training for all difficulties
- Easy: 100k steps, Medium: 150k steps, Hard: 200k steps
- Can specify specific difficulties: `--difficulties easy medium`

### List Policies
```bash
python run_training.py --mode list
```
- Shows all saved policies with timestamps and sizes

## Training Process

The training uses **self-play** with **PPO (Proximal Policy Optimization)**:

1. **Easy AI**: Trains against random and simple opponents
2. **Medium AI**: Trains against easy AI and medium opponents  
3. **Hard AI**: Trains against medium/hard opponents

Each difficulty level has different:
- **Reaction times** (easy: 0.3s, medium: 0.15s, hard: 0.05s)
- **Mistake rates** (easy: 30%, medium: 15%, hard: 5%)
- **Training opponents** (progressively harder)

## Output

Trained policies are saved in `policies/` directory:
- `easy_best.pth` - Best easy AI during training
- `medium_final.pth` - Final medium AI after training
- `hard_step_50000.pth` - Checkpoint at 50k steps
- etc.

## Files

- `environment.py` - RL environment wrapper for the game
- `models.py` - Neural network policies and training algorithms
- `train.py` - Main training logic and self-play system
- `run_training.py` - Command-line interface for training

## State Space (20 features)

The AI observes:
- **Self state**: position, health, velocity, grounded, attacking, blocking, cooldowns
- **Opponent state**: same as above
- **Relative info**: distance, relative position, height difference, health advantage

## Action Space (9 actions)

- `idle`, `move_left`, `move_right`, `jump`
- `punch`, `kick`, `block`
- `move_left_block`, `move_right_block`

## Reward Function

- **+5** for landing hits
- **-50/+50** for losing/winning
- **Small bonuses** for good positioning
- **Penalties** for being cornered

## Training Time

Approximate training times:
- **Quick test**: 1-2 minutes
- **Easy AI**: 10-20 minutes  
- **Medium AI**: 15-30 minutes
- **Hard AI**: 20-40 minutes

Total full training: ~1-2 hours depending on hardware.
