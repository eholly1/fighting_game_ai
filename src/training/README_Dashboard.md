# 🥊 Fighting Game AI Training Dashboard

An interactive web dashboard for visualizing and analyzing AI training experiments.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install streamlit plotly pandas
```

### 2. Launch Dashboard
```bash
# From the training directory
python launch_dashboard.py

# Or directly with streamlit
python -m streamlit run dashboard.py --server.port 8501
```

### 3. Open Browser
Navigate to `http://localhost:8501` to view the dashboard.

## 📊 Features

### 🏆 Training Progress
- **Win Rate Over Time** - Track how well your AI performs against opponents
- **Average Reward** - Monitor reward progression during training
- **Training Losses** - Policy and value loss curves
- **Episode Lengths** - How long games last (longer = more engaging?)

### 🎯 Action Analysis
- **Action Distribution** - Pie chart of what actions the AI chooses
- **Action Evolution** - How action usage changes over training
- **Top Actions** - Most frequently used actions

### 🗺️ Behavioral Patterns
- **Engagement Metrics** - How much time AI spends in combat range
- **Distance Analysis** - Average distance from opponent
- **Spatial Behavior** - Movement patterns and positioning

### 📈 Experiment Comparison
- **Side-by-side Analysis** - Compare multiple experiments
- **Summary Table** - Key metrics for all experiments
- **Win Rate Comparison** - Performance across different approaches

## 🎮 Usage Workflow

### 1. Run Training Experiments
```bash
# Run different experiments
python train.py --experiment baseline --config configs/baseline.yaml
python train.py --experiment aggressive --config configs/aggressive.yaml
python train.py --experiment defensive --config configs/defensive.yaml
```

### 2. Launch Dashboard
```bash
python launch_dashboard.py
```

### 3. Analyze Results
- Select experiments from the sidebar
- Explore different tabs for various analyses
- Compare experiments to understand what works

## 📁 Data Structure

The dashboard reads from the experiment directory structure:
```
experiments/
├── experiment_name/
│   ├── logs/
│   │   └── metrics.jsonl      # Training and evaluation data
│   ├── policies/
│   │   └── *.pth             # Saved model checkpoints
│   ├── plots/                # Generated visualizations
│   └── config.json           # Experiment configuration
```

## 🔧 Customization

### Adding New Visualizations
1. Add new methods to `TrainingDashboard` class
2. Call them from the appropriate tab in `render_main_content()`
3. Use Plotly for interactive charts

### Custom Metrics
1. Log additional metrics in `ExperimentManager.log_evaluation()`
2. Add visualization methods in the dashboard
3. Update the comparison table if needed

## 📊 Metrics Explained

### Training Metrics
- **Average Reward**: Rolling average of episode rewards
- **Policy Loss**: How much the policy is changing
- **Value Loss**: How accurate the value function is
- **Episode Length**: Average steps per episode

### Evaluation Metrics
- **Win Rate**: % of games won against rule-based AI
- **Action Distribution**: Frequency of each action type
- **Engagement Score**: % of time spent in combat range (<150 pixels)
- **Average Distance**: Mean distance from opponent during fights

### Behavioral Metrics
- **Aggression Score**: Frequency of attack actions
- **Defensive Score**: Frequency of blocking actions
- **Spatial Coverage**: How much of the stage the AI uses

## 🐛 Troubleshooting

### Dashboard Won't Start
- Check if streamlit is installed: `pip install streamlit`
- Try a different port: `python launch_dashboard.py --port 8502`
- Check for Python/package conflicts

### No Data Showing
- Make sure you've run training experiments first
- Check that experiments directory exists
- Verify metrics.jsonl files contain data

### Plots Not Loading
- Ensure plotly is installed: `pip install plotly`
- Check browser console for JavaScript errors
- Try refreshing the page

## 🎯 Best Practices

### Experiment Naming
- Use descriptive names: `baseline_v1`, `fixed_rewards`, `engagement_focus`
- Include version numbers for iterations
- Document changes in config files

### Data Collection
- Run experiments for sufficient steps (50k+ for meaningful data)
- Use consistent evaluation intervals (every 5k steps)
- Save multiple checkpoints during training

### Analysis Workflow
1. **Start with Training Progress** - Is the AI learning?
2. **Check Action Analysis** - What behaviors is it developing?
3. **Examine Behavioral Patterns** - Is it playing the game properly?
4. **Compare Experiments** - What approaches work best?

## 🚀 Advanced Features

### Real-time Monitoring
The dashboard automatically refreshes data, so you can monitor training in real-time by:
1. Starting a training job
2. Opening the dashboard
3. Selecting the experiment
4. Watching metrics update as training progresses

### Export Functionality
- Download plots as images
- Export data as CSV for external analysis
- Generate experiment reports

Happy training! 🎮🤖
