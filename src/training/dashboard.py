"""
Web Dashboard for Fighting Game RL Training
Interactive visualization of experiments, metrics, and AI behavior
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from experiment_manager import ExperimentManager


class TrainingDashboard:
    """Interactive web dashboard for training visualization"""

    def __init__(self):
        self.setup_page()

    def setup_page(self):
        """Configure Streamlit page"""
        st.set_page_config(
            page_title="Fighting Game AI Training Dashboard",
            page_icon="🥊",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title("🥊 Fighting Game AI Training Dashboard")
        st.markdown("---")

    def run(self):
        """Main dashboard application"""
        # Sidebar for experiment selection
        self.render_sidebar()

        # Main content area
        if 'selected_experiments' in st.session_state and st.session_state.selected_experiments:
            self.render_main_content()
        else:
            self.render_welcome_screen()

    def render_sidebar(self):
        """Render sidebar with experiment selection"""
        st.sidebar.header("📋 Experiment Selection")

        # Get available experiments
        experiments = ExperimentManager.list_experiments()

        if not experiments:
            st.sidebar.warning("No experiments found. Run some training first!")
            return

        # Multi-select for experiments
        selected = st.sidebar.multiselect(
            "Select experiments to analyze:",
            experiments,
            default=experiments[:3] if len(experiments) >= 3 else experiments
        )

        st.session_state.selected_experiments = selected

        # Experiment info
        if selected:
            st.sidebar.markdown("### 📊 Selected Experiments")
            for exp in selected:
                summary = self.get_experiment_summary(exp)
                if summary and 'status' in summary:
                    status_emoji = "🟢" if summary['status'] == 'completed' else "🟡"
                    st.sidebar.markdown(f"{status_emoji} **{exp}**")
                    if 'total_episodes' in summary:
                        st.sidebar.markdown(f"   Episodes: {summary['total_episodes']}")
                        st.sidebar.markdown(f"   Steps: {summary['total_steps']}")

        # Refresh button
        if st.sidebar.button("🔄 Refresh Data"):
            st.experimental_rerun()

    def render_welcome_screen(self):
        """Render welcome screen when no experiments selected"""
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown("""
            ## Welcome to the AI Training Dashboard! 🎮

            ### Getting Started:
            1. **Run some training experiments** using the command line:
               ```bash
               python train.py --experiment my_first_experiment
               ```

            2. **Select experiments** from the sidebar to analyze

            3. **Explore the visualizations** to understand AI behavior

            ### Features:
            - 📈 **Training Progress** - Win rates, rewards, losses over time
            - 🎯 **Action Analysis** - What actions the AI chooses and when
            - 🗺️ **Behavioral Patterns** - Spatial movement and engagement metrics
            - 📊 **Experiment Comparison** - Side-by-side analysis
            """)

    def render_main_content(self):
        """Render main dashboard content"""
        experiments = st.session_state.selected_experiments

        # Load data for all selected experiments
        experiment_data = {}
        for exp in experiments:
            data = ExperimentManager.load_experiment_data(exp)
            if 'error' not in data:
                experiment_data[exp] = data

        if not experiment_data:
            st.error("No valid experiment data found!")
            return

        # Dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Training Progress",
            "🎯 Action Analysis",
            "🗺️ Behavioral Patterns",
            "📊 Experiment Comparison"
        ])

        with tab1:
            self.render_training_progress(experiment_data)

        with tab2:
            self.render_action_analysis(experiment_data)

        with tab3:
            self.render_behavioral_patterns(experiment_data)

        with tab4:
            self.render_experiment_comparison(experiment_data)

    def render_training_progress(self, experiment_data: Dict):
        """Render training progress visualizations"""
        st.header("📈 Training Progress")

        # Create subplots
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Win Rate Over Time")
            self.plot_win_rates(experiment_data)

        with col2:
            st.subheader("💰 Average Reward")
            self.plot_rewards(experiment_data)

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("📉 Training Losses")
            self.plot_losses(experiment_data)

        with col4:
            st.subheader("⏱️ Episode Lengths")
            self.plot_episode_lengths(experiment_data)

    def render_action_analysis(self, experiment_data: Dict):
        """Render action analysis visualizations"""
        st.header("🎯 Action Analysis")

        # Select experiment for detailed analysis
        if len(experiment_data) > 1:
            selected_exp = st.selectbox(
                "Select experiment for detailed action analysis:",
                list(experiment_data.keys())
            )
        else:
            selected_exp = list(experiment_data.keys())[0]

        data = experiment_data[selected_exp]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🥧 Action Distribution")
            self.plot_action_distribution(selected_exp, data)

        with col2:
            st.subheader("📊 Action Frequency Over Time")
            self.plot_action_evolution(selected_exp, data)

    def render_behavioral_patterns(self, experiment_data: Dict):
        """Render behavioral pattern visualizations"""
        st.header("🗺️ Behavioral Patterns")

        # Select experiment
        if len(experiment_data) > 1:
            selected_exp = st.selectbox(
                "Select experiment for behavioral analysis:",
                list(experiment_data.keys()),
                key="behavioral_exp_select"
            )
        else:
            selected_exp = list(experiment_data.keys())[0]

        data = experiment_data[selected_exp]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎯 Engagement Metrics")
            self.plot_engagement_metrics(selected_exp, data)

        with col2:
            st.subheader("📏 Distance from Opponent")
            self.plot_distance_metrics(selected_exp, data)

    def render_experiment_comparison(self, experiment_data: Dict):
        """Render experiment comparison"""
        st.header("📊 Experiment Comparison")

        if len(experiment_data) < 2:
            st.info("Select at least 2 experiments to compare them.")
            return

        # Summary table
        st.subheader("📋 Summary Table")
        self.render_comparison_table(experiment_data)

        # Side-by-side win rate comparison
        st.subheader("🏆 Win Rate Comparison")
        self.plot_win_rate_comparison(experiment_data)

    def plot_win_rates(self, experiment_data: Dict):
        """Plot win rates over time for all experiments"""
        fig = go.Figure()

        for exp_name, data in experiment_data.items():
            eval_data = data.get('evaluation_data', [])
            if eval_data:
                steps = [entry['step'] for entry in eval_data]
                win_rates = [entry['results']['win_rate'] * 100 for entry in eval_data]

                fig.add_trace(go.Scatter(
                    x=steps,
                    y=win_rates,
                    mode='lines+markers',
                    name=exp_name,
                    line=dict(width=2)
                ))

        fig.update_layout(
            xaxis_title="Training Steps",
            yaxis_title="Win Rate (%)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_rewards(self, experiment_data: Dict):
        """Plot average rewards over time"""
        fig = go.Figure()

        for exp_name, data in experiment_data.items():
            training_data = data.get('training_data', [])
            if training_data:
                episodes = [entry['episode'] for entry in training_data]
                rewards = [entry['metrics']['avg_reward'] for entry in training_data]

                fig.add_trace(go.Scatter(
                    x=episodes,
                    y=rewards,
                    mode='lines',
                    name=exp_name,
                    line=dict(width=2)
                ))

        fig.update_layout(
            xaxis_title="Episode",
            yaxis_title="Average Reward",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_losses(self, experiment_data: Dict):
        """Plot training losses"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Policy Loss', 'Value Loss'),
            shared_xaxes=True
        )

        for exp_name, data in experiment_data.items():
            training_data = data.get('training_data', [])
            if training_data:
                episodes = [entry['episode'] for entry in training_data]
                policy_losses = [entry['metrics']['policy_loss'] for entry in training_data]
                value_losses = [entry['metrics']['value_loss'] for entry in training_data]

                fig.add_trace(
                    go.Scatter(x=episodes, y=policy_losses, name=f"{exp_name} Policy",
                              line=dict(width=2)), row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=episodes, y=value_losses, name=f"{exp_name} Value",
                              line=dict(width=2)), row=2, col=1
                )

        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    def plot_episode_lengths(self, experiment_data: Dict):
        """Plot episode lengths over time"""
        fig = go.Figure()

        for exp_name, data in experiment_data.items():
            training_data = data.get('training_data', [])
            if training_data:
                episodes = [entry['episode'] for entry in training_data]
                lengths = [entry['metrics']['avg_length'] for entry in training_data]

                fig.add_trace(go.Scatter(
                    x=episodes,
                    y=lengths,
                    mode='lines',
                    name=exp_name,
                    line=dict(width=2)
                ))

        fig.update_layout(
            xaxis_title="Episode",
            yaxis_title="Average Episode Length",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_action_distribution(self, exp_name: str, data: Dict):
        """Plot action distribution pie chart"""
        eval_data = data.get('evaluation_data', [])
        if not eval_data:
            st.info("No evaluation data available for action analysis.")
            return

        # Get latest evaluation data
        latest_eval = eval_data[-1]
        action_dist = latest_eval['results'].get('action_distribution', {})

        if not action_dist:
            st.info("No action distribution data available.")
            return

        # Action names mapping
        action_names = {
            0: 'Idle', 1: 'Move Left', 2: 'Move Right', 3: 'Jump',
            4: 'Punch', 5: 'Kick', 6: 'Block', 7: 'Move+Block Left',
            8: 'Move+Block Right', 9: 'Projectile'
        }

        labels = [action_names.get(int(k), f'Action {k}') for k in action_dist.keys()]
        values = [v * 100 for v in action_dist.values()]  # Convert to percentages

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            textinfo='label+percent'
        )])

        fig.update_layout(
            title=f"Action Distribution - {exp_name}",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_action_evolution(self, exp_name: str, data: Dict):
        """Plot how action usage evolves over training"""
        eval_data = data.get('evaluation_data', [])
        if len(eval_data) < 2:
            st.info("Need at least 2 evaluations to show action evolution.")
            return

        # Extract action distributions over time
        steps = []
        action_data = {}

        for eval_entry in eval_data:
            steps.append(eval_entry['step'])
            action_dist = eval_entry['results'].get('action_distribution', {})

            for action_idx, freq in action_dist.items():
                if action_idx not in action_data:
                    action_data[action_idx] = []
                action_data[action_idx].append(freq * 100)

        # Plot top 5 most used actions
        fig = go.Figure()

        action_names = {
            0: 'Idle', 1: 'Move Left', 2: 'Move Right', 3: 'Jump',
            4: 'Punch', 5: 'Kick', 6: 'Block', 9: 'Projectile'
        }

        # Sort by average usage
        avg_usage = {k: sum(v)/len(v) for k, v in action_data.items()}
        top_actions = sorted(avg_usage.items(), key=lambda x: x[1], reverse=True)[:5]

        for action_idx, _ in top_actions:
            action_name = action_names.get(int(action_idx), f'Action {action_idx}')
            fig.add_trace(go.Scatter(
                x=steps,
                y=action_data[action_idx],
                mode='lines+markers',
                name=action_name,
                line=dict(width=2)
            ))

        fig.update_layout(
            title=f"Action Usage Evolution - {exp_name}",
            xaxis_title="Training Steps",
            yaxis_title="Action Frequency (%)",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_engagement_metrics(self, exp_name: str, data: Dict):
        """Plot engagement metrics over time"""
        eval_data = data.get('evaluation_data', [])
        if not eval_data:
            st.info("No evaluation data available for engagement analysis.")
            return

        steps = []
        engagement_scores = []
        avg_distances = []

        for eval_entry in eval_data:
            steps.append(eval_entry['step'])
            results = eval_entry['results']
            engagement_scores.append(results.get('engagement_score', 0) * 100)
            avg_distances.append(results.get('avg_distance_from_opponent', 0))

        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Engagement Score (%)', 'Average Distance from Opponent'),
            shared_xaxes=True
        )

        fig.add_trace(
            go.Scatter(x=steps, y=engagement_scores, mode='lines+markers',
                      name='Engagement Score', line=dict(color='green', width=2)),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=steps, y=avg_distances, mode='lines+markers',
                      name='Avg Distance', line=dict(color='blue', width=2)),
            row=2, col=1
        )

        fig.update_layout(height=500, title=f"Behavioral Metrics - {exp_name}")
        st.plotly_chart(fig, use_container_width=True)

    def plot_distance_metrics(self, exp_name: str, data: Dict):
        """Plot distance-related metrics"""
        eval_data = data.get('evaluation_data', [])
        if not eval_data:
            st.info("No evaluation data available.")
            return

        # Create histogram of distances from latest evaluation
        latest_eval = eval_data[-1]
        avg_distance = latest_eval['results'].get('avg_distance_from_opponent', 0)

        # Create a simple metric display
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Average Distance",
                value=f"{avg_distance:.1f} pixels"
            )

        with col2:
            engagement = latest_eval['results'].get('engagement_score', 0)
            st.metric(
                label="Engagement Score",
                value=f"{engagement:.1%}"
            )

        with col3:
            win_rate = latest_eval['results'].get('win_rate', 0)
            st.metric(
                label="Win Rate",
                value=f"{win_rate:.1%}"
            )

    def render_comparison_table(self, experiment_data: Dict):
        """Render comparison table of experiments"""
        comparison_data = []

        for exp_name, data in experiment_data.items():
            training_data = data.get('training_data', [])
            eval_data = data.get('evaluation_data', [])

            if training_data and eval_data:
                latest_eval = eval_data[-1]
                latest_training = training_data[-1]

                comparison_data.append({
                    'Experiment': exp_name,
                    'Episodes': len(training_data),
                    'Steps': latest_training['step'],
                    'Final Win Rate': f"{latest_eval['results']['win_rate']:.1%}",
                    'Final Reward': f"{latest_training['metrics']['avg_reward']:.2f}",
                    'Engagement Score': f"{latest_eval['results'].get('engagement_score', 0):.1%}",
                    'Avg Distance': f"{latest_eval['results'].get('avg_distance_from_opponent', 0):.1f}"
                })

        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No complete experiment data available for comparison.")

    def plot_win_rate_comparison(self, experiment_data: Dict):
        """Plot win rate comparison across experiments"""
        fig = go.Figure()

        for exp_name, data in experiment_data.items():
            eval_data = data.get('evaluation_data', [])
            if eval_data:
                steps = [entry['step'] for entry in eval_data]
                win_rates = [entry['results']['win_rate'] * 100 for entry in eval_data]

                fig.add_trace(go.Scatter(
                    x=steps,
                    y=win_rates,
                    mode='lines+markers',
                    name=exp_name,
                    line=dict(width=3)
                ))

        fig.update_layout(
            title="Win Rate Comparison Across Experiments",
            xaxis_title="Training Steps",
            yaxis_title="Win Rate (%)",
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    def get_experiment_summary(self, experiment_name: str) -> Optional[Dict]:
        """Get summary for a single experiment"""
        try:
            data = ExperimentManager.load_experiment_data(experiment_name)
            if 'error' in data:
                return None

            training_data = data.get('training_data', [])
            evaluation_data = data.get('evaluation_data', [])

            return {
                'status': 'completed' if training_data else 'no_data',
                'total_episodes': len(training_data),
                'total_steps': training_data[-1]['step'] if training_data else 0,
                'evaluations': len(evaluation_data),
                'latest_win_rate': evaluation_data[-1]['results']['win_rate'] if evaluation_data else None
            }
        except Exception:
            return None


def main():
    """Main dashboard application"""
    dashboard = TrainingDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
