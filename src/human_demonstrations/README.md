# Human Demonstration System

This system allows recording human gameplay for behavioral cloning to create more human-like AI policies.

## 🎯 Purpose

Instead of training RL agents from scratch (which leads to button-mashing), we can:
1. **Record human demonstrations** of strategic gameplay
2. **Pre-train policies** to mimic human behavior (behavioral cloning)
3. **Fine-tune with RL** to improve beyond human performance

## 🎮 Recording Demonstrations

### Step 1: Start the Game
```bash
cd src
python main.py
```

### Step 2: Start a Fight
- Press `1` for Human vs AI (rule-based)
- Press `2` for Human vs Human
- **Recommended**: Fight against rule-based AI for consistent opponent

### Step 3: Record Gameplay
- **F1** - Start/Stop recording
- **F2** - Save demonstrations to file
- **F3** - Clear current demonstrations
- **F4** - Show recording statistics

### Step 4: Play Strategically
Record 5+ minutes of strategic gameplay:
- **Use projectiles strategically** (charge at range, quick shots up close)
- **Mix attacks and movement**
- **Use blocking defensively**
- **Show good spacing and timing**

### Step 5: Save Data
- Press **F2** to save demonstrations
- Files saved to `src/human_demonstrations/data/`

## 🧠 Training with Demonstrations

### Option 1: Behavioral Cloning Only
```bash
cd src/human_demonstrations
python train_from_demos.py --bc-only --bc-epochs 100
```

### Option 2: Behavioral Cloning + RL Fine-tuning
```bash
cd src/human_demonstrations
python train_from_demos.py --bc-epochs 50 --rl-steps 25000
```

### Option 3: Specify Demo File
```bash
cd src/human_demonstrations
python train_from_demos.py --demo-file data/human_demos_20250130_143022.json
```

## 📊 What Gets Recorded

Each demonstration step contains:
- **State vector** (26D): Fighter positions, health, velocities, projectile states, etc.
- **Action**: One of 10 possible actions (idle, move, jump, punch, kick, block, projectile, etc.)
- **Timestamp**: For analysis and debugging

## 🎯 Expected Benefits

### Before (Random Initialization):
- Button-mashing behavior
- No strategic projectile use
- Poor spacing and timing

### After (Behavioral Cloning):
- Human-like strategic behavior
- Proper projectile charging
- Good spacing and defensive play
- Foundation for RL improvement

## 📁 File Structure

```
src/human_demonstrations/
├── README.md                    # This file
├── recorder.py                  # Recording system
├── behavioral_cloning.py        # BC training
├── train_from_demos.py         # Training pipeline
└── data/                       # Recorded demonstrations
    └── human_demos_*.json      # Demo files
```

## 🔧 Technical Details

### State Representation
- **26-dimensional vector** with position mirroring
- **Consistent perspective**: Player always "on left", opponent "on right"
- **Normalized values**: All features in [0, 1] range

### Action Space
- **10 discrete actions**: idle, move_left, move_right, jump, punch, kick, block, move_left_block, move_right_block, projectile

### Training Process
1. **Load demonstrations** and split train/validation (80/20)
2. **Supervised learning** with cross-entropy loss
3. **Early stopping** based on validation accuracy
4. **Optional RL fine-tuning** starting from BC policy

## 📈 Monitoring Training

The system provides:
- **Training/validation loss** curves
- **Action prediction accuracy**
- **Action distribution** analysis
- **Training history** plots

## 🎮 Tips for Good Demonstrations

1. **Play strategically**, not just to win
2. **Use all mechanics**: projectiles, blocking, spacing
3. **Show variety**: Different situations and responses
4. **Record multiple sessions** for diverse data
5. **Quality over quantity**: 5 minutes of good play > 20 minutes of button-mashing

## 🚀 Next Steps

After recording demonstrations:
1. Train behavioral cloning policy
2. Test the BC policy in-game
3. Fine-tune with RL if needed
4. Compare against random-initialized policies
