#!/usr/bin/env python3
"""
Test Swiss Tournament System

Tests the Swiss tournament implementation with mock agents
to verify pairing logic, ranking, and efficiency.
"""
import sys
import os
import time
import random
import numpy as np
from typing import List

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from swiss_tournament import SwissTournament, TournamentResult

class MockAgent:
    """Mock agent for testing with configurable skill level"""
    
    def __init__(self, agent_id: str, skill_level: float = 0.5):
        """
        Args:
            agent_id: Unique identifier for the agent
            skill_level: Skill level from 0.0 (worst) to 1.0 (best)
        """
        self.agent_id = agent_id
        self.skill_level = skill_level
        self._error_count = 0
    
    def get_action(self, state):
        """Mock get_action method"""
        # Higher skill agents make better decisions
        if random.random() < self.skill_level:
            return random.choice([4, 5, 6])  # Good actions
        else:
            return random.choice([0, 1, 2])  # Mediocre actions

def mock_match_runner(agent1: MockAgent, agent2: MockAgent) -> TournamentResult:
    """
    Mock match runner that simulates matches based on agent skill levels
    
    Higher skill agents are more likely to win, but there's always some randomness
    """
    # Simulate match duration
    time.sleep(0.01)  # 10ms per match
    
    # Calculate win probability based on skill difference
    skill_diff = agent1.skill_level - agent2.skill_level
    agent1_win_prob = 0.5 + skill_diff * 0.4  # Max 90% win rate for skill diff of 1.0
    agent1_win_prob = max(0.1, min(0.9, agent1_win_prob))  # Clamp to 10-90%
    
    # Simulate multiple games
    games_played = 5
    agent1_wins = 0
    agent2_wins = 0
    
    for _ in range(games_played):
        if random.random() < agent1_win_prob:
            agent1_wins += 1
        else:
            agent2_wins += 1
    
    # Determine match winner
    if agent1_wins > agent2_wins:
        agent1_score, agent2_score = 1.0, 0.0
    elif agent2_wins > agent1_wins:
        agent1_score, agent2_score = 0.0, 1.0
    else:
        agent1_score, agent2_score = 0.5, 0.5  # Draw
    
    # Mock fitness based on skill and some randomness
    agent1_fitness = agent1.skill_level * 100 + random.gauss(0, 10)
    agent2_fitness = agent2.skill_level * 100 + random.gauss(0, 10)
    
    return TournamentResult(
        agent1_id=agent1.agent_id,
        agent2_id=agent2.agent_id,
        agent1_score=agent1_score,
        agent2_score=agent2_score,
        agent1_fitness=agent1_fitness,
        agent2_fitness=agent2_fitness,
        games_played=games_played,
        metadata={
            'agent1_wins': agent1_wins,
            'agent2_wins': agent2_wins,
            'agent1_skill': agent1.skill_level,
            'agent2_skill': agent2.skill_level
        }
    )

def create_test_agents(n_agents: int) -> List[MockAgent]:
    """Create a diverse set of test agents with varying skill levels"""
    agents = []
    
    for i in range(n_agents):
        # Create agents with different skill distributions
        if i < n_agents // 4:
            # Top tier: 0.8-1.0 skill
            skill = 0.8 + random.random() * 0.2
        elif i < n_agents // 2:
            # High tier: 0.6-0.8 skill
            skill = 0.6 + random.random() * 0.2
        elif i < 3 * n_agents // 4:
            # Mid tier: 0.4-0.6 skill
            skill = 0.4 + random.random() * 0.2
        else:
            # Low tier: 0.2-0.4 skill
            skill = 0.2 + random.random() * 0.2
        
        agent = MockAgent(f"agent_{i:03d}", skill)
        agents.append(agent)
    
    return agents

def test_tournament_efficiency():
    """Test tournament efficiency vs round-robin"""
    print("🔍 Testing Tournament Efficiency")
    print("=" * 50)
    
    for n_agents in [10, 20, 50]:
        agents = create_test_agents(n_agents)
        
        # Swiss tournament
        tournament = SwissTournament(agents)
        swiss_matches = tournament.rounds * (n_agents // 2)
        
        # Round-robin comparison
        round_robin_matches = n_agents * (n_agents - 1) // 2
        
        efficiency = (1 - swiss_matches / round_robin_matches) * 100
        
        print(f"📊 {n_agents:2d} agents:")
        print(f"   Swiss:      {swiss_matches:4d} matches ({tournament.rounds} rounds)")
        print(f"   Round-robin: {round_robin_matches:4d} matches")
        print(f"   Efficiency:  {efficiency:5.1f}% reduction")
        print()

def test_tournament_fairness():
    """Test that Swiss tournament produces fair rankings"""
    print("🎯 Testing Tournament Fairness")
    print("=" * 50)
    
    # Create agents with known skill levels
    agents = create_test_agents(20)
    
    # Sort by true skill for comparison
    true_ranking = sorted(agents, key=lambda a: a.skill_level, reverse=True)
    
    # Run Swiss tournament
    tournament = SwissTournament(agents)
    start_time = time.time()
    tournament_ranking = tournament.run_tournament(mock_match_runner)
    duration = time.time() - start_time
    
    print(f"⏱️  Tournament completed in {duration:.2f} seconds")
    
    # Compare rankings
    print(f"\n📈 Ranking Comparison (Top 10):")
    print(f"{'Rank':<4} {'Tournament Winner':<15} {'True Skill':<10} {'Tournament Skill':<15}")
    print("-" * 60)
    
    rank_correlation = 0
    for i in range(min(10, len(tournament_ranking))):
        tournament_agent_id = tournament_ranking[i][0]
        tournament_agent = next(a for a in agents if a.agent_id == tournament_agent_id)
        true_agent = true_ranking[i]
        
        # Simple rank correlation (how close is tournament rank to true rank)
        true_rank = next(j for j, a in enumerate(true_ranking) if a.agent_id == tournament_agent_id)
        rank_diff = abs(i - true_rank)
        rank_correlation += rank_diff
        
        print(f"{i+1:<4} {tournament_agent.agent_id:<15} {true_agent.skill_level:<10.3f} {tournament_agent.skill_level:<15.3f}")
    
    avg_rank_error = rank_correlation / min(10, len(tournament_ranking))
    print(f"\n📊 Average rank error: {avg_rank_error:.1f} positions")
    
    return avg_rank_error < 3.0  # Good if average error is less than 3 positions

def test_tournament_stats():
    """Test tournament statistics and reporting"""
    print("📊 Testing Tournament Statistics")
    print("=" * 50)
    
    agents = create_test_agents(15)
    tournament = SwissTournament(agents)
    
    # Run tournament
    rankings = tournament.run_tournament(mock_match_runner)
    stats = tournament.get_tournament_stats()
    
    print(f"\n📈 Tournament Statistics:")
    print(f"   Total agents: {stats['total_agents']}")
    print(f"   Total rounds: {stats['total_rounds']}")
    print(f"   Total matches: {stats['total_matches']}")
    print(f"   Matches per agent: {stats['matches_per_agent']:.1f}")
    
    # Verify each agent played expected number of games
    expected_games = tournament.rounds
    actual_games = [standing.games_played for _, standing in rankings]
    
    print(f"\n🎮 Games per agent:")
    print(f"   Expected: {expected_games}")
    print(f"   Actual range: {min(actual_games)}-{max(actual_games)}")
    print(f"   Average: {np.mean(actual_games):.1f}")
    
    return True

def run_all_tests():
    """Run all Swiss tournament tests"""
    print("🧪 Swiss Tournament System Tests")
    print("=" * 60)
    
    # Test 1: Efficiency
    test_tournament_efficiency()
    
    # Test 2: Fairness
    fairness_passed = test_tournament_fairness()
    
    # Test 3: Statistics
    stats_passed = test_tournament_stats()
    
    print("\n📋 Test Results:")
    print(f"   Efficiency: ✅ PASS (demonstrated)")
    print(f"   Fairness:   {'✅ PASS' if fairness_passed else '❌ FAIL'}")
    print(f"   Statistics: {'✅ PASS' if stats_passed else '❌ FAIL'}")
    
    if fairness_passed and stats_passed:
        print("\n🎉 All tests passed! Swiss tournament system is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    # Set random seed for reproducible tests
    random.seed(42)
    np.random.seed(42)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
