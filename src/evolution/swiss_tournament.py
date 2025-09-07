#!/usr/bin/env python3
"""
Swiss Tournament System for Evolutionary Training

Implements efficient O(n log n) tournament evaluation where agents with
similar performance are paired against each other.
"""
import math
import random
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class TournamentResult:
    """Result of a single match between two agents"""
    agent1_id: str
    agent2_id: str
    agent1_score: float  # 1.0 for win, 0.5 for draw, 0.0 for loss
    agent2_score: float
    agent1_fitness: float  # Raw fitness/reward from the match
    agent2_fitness: float
    games_played: int
    metadata: Dict = None

@dataclass
class AgentStanding:
    """Current standing of an agent in the tournament"""
    agent_id: str
    wins: float  # Can be fractional due to draws
    games_played: int
    total_fitness: float
    opponents_faced: Set[str]
    match_history: List[TournamentResult]
    
    @property
    def win_rate(self) -> float:
        return self.wins / self.games_played if self.games_played > 0 else 0.0
    
    @property
    def avg_fitness(self) -> float:
        return self.total_fitness / self.games_played if self.games_played > 0 else 0.0
    
    @property
    def strength_of_schedule(self) -> float:
        """Average win rate of opponents faced"""
        if not self.opponents_faced:
            return 0.0
        # This will be calculated by the tournament manager
        return getattr(self, '_strength_of_schedule', 0.0)

class SwissTournament:
    """
    Swiss Tournament implementation for agent evaluation
    
    In Swiss tournaments, agents are paired based on similar performance
    rather than elimination brackets, allowing all agents to play multiple
    rounds and providing better ranking information.
    """
    
    def __init__(self, agents: List, rounds: Optional[int] = None):
        """
        Initialize Swiss tournament
        
        Args:
            agents: List of agent objects that have .agent_id attribute
            rounds: Number of rounds to play (default: ceil(log2(n_agents)))
        """
        self.agents = agents
        self.n_agents = len(agents)
        self.rounds = rounds or max(1, math.ceil(math.log2(self.n_agents)))
        
        # Initialize standings
        self.standings: Dict[str, AgentStanding] = {}
        for agent in agents:
            self.standings[agent.agent_id] = AgentStanding(
                agent_id=agent.agent_id,
                wins=0.0,
                games_played=0,
                total_fitness=0.0,
                opponents_faced=set(),
                match_history=[]
            )
        
        self.current_round = 0
        self.all_results: List[TournamentResult] = []
        
    def run_tournament(self, match_runner_func) -> List[Tuple[str, AgentStanding]]:
        """
        Run the complete Swiss tournament
        
        Args:
            match_runner_func: Function that takes (agent1, agent2) and returns TournamentResult
            
        Returns:
            List of (agent_id, standing) tuples sorted by performance
        """
        print(f"🏆 Starting Swiss tournament: {self.n_agents} agents, {self.rounds} rounds")
        
        for round_num in range(self.rounds):
            self.current_round = round_num + 1
            print(f"\n⚔️  Round {self.current_round}/{self.rounds}")
            
            # Create pairings for this round
            pairings = self._create_pairings()
            print(f"   Created {len(pairings)} pairings")
            
            # Play all matches in this round
            round_results = self._play_round(pairings, match_runner_func)
            
            # Update standings
            self._update_standings(round_results)
            
            # Print round summary
            self._print_round_summary()
        
        # Calculate final rankings
        final_rankings = self._get_final_rankings()
        
        print(f"\n🏁 Tournament complete!")
        self._print_final_results(final_rankings[:10])  # Top 10
        
        return final_rankings
    
    def _create_pairings(self) -> List[Tuple]:
        """Create pairings for the current round"""
        if self.current_round == 1:
            return self._create_random_pairings()
        else:
            return self._create_swiss_pairings()
    
    def _create_random_pairings(self) -> List[Tuple]:
        """Create random pairings for the first round"""
        agents_copy = self.agents.copy()
        random.shuffle(agents_copy)
        
        pairings = []
        for i in range(0, len(agents_copy) - 1, 2):
            pairings.append((agents_copy[i], agents_copy[i + 1]))
        
        # Handle odd number of agents (bye)
        if len(agents_copy) % 2 == 1:
            bye_agent = agents_copy[-1]
            pairings.append((bye_agent, None))  # None indicates bye
        
        return pairings
    
    def _create_swiss_pairings(self) -> List[Tuple]:
        """Create Swiss pairings based on current standings"""
        # Update strength of schedule for all agents
        self._update_strength_of_schedule()
        
        # Sort agents by performance (wins, then strength of schedule, then fitness)
        sorted_agents = sorted(
            self.agents,
            key=lambda a: (
                self.standings[a.agent_id].wins,
                self.standings[a.agent_id].strength_of_schedule,
                self.standings[a.agent_id].avg_fitness
            ),
            reverse=True
        )
        
        pairings = []
        used_agents = set()
        
        for agent in sorted_agents:
            if agent.agent_id in used_agents:
                continue
            
            # Find best available opponent
            opponent = self._find_best_opponent(agent, sorted_agents, used_agents)
            
            if opponent:
                pairings.append((agent, opponent))
                used_agents.add(agent.agent_id)
                used_agents.add(opponent.agent_id)
            else:
                # Bye round
                pairings.append((agent, None))
                used_agents.add(agent.agent_id)
        
        return pairings
    
    def _find_best_opponent(self, agent, sorted_agents: List, used_agents: Set) -> Optional:
        """Find the best available opponent for an agent"""
        agent_standing = self.standings[agent.agent_id]
        
        # Look for opponents with similar records who haven't been faced
        for candidate in sorted_agents:
            if (candidate.agent_id != agent.agent_id and 
                candidate.agent_id not in used_agents and
                candidate.agent_id not in agent_standing.opponents_faced):
                return candidate
        
        # If no unfaced opponents, find closest available opponent
        for candidate in sorted_agents:
            if (candidate.agent_id != agent.agent_id and 
                candidate.agent_id not in used_agents):
                return candidate
        
        return None
    
    def _play_round(self, pairings: List[Tuple], match_runner_func) -> List[TournamentResult]:
        """Play all matches in a round"""
        round_results = []
        
        for i, (agent1, agent2) in enumerate(pairings):
            if agent2 is None:
                # Bye round - agent gets automatic win
                result = TournamentResult(
                    agent1_id=agent1.agent_id,
                    agent2_id="BYE",
                    agent1_score=1.0,
                    agent2_score=0.0,
                    agent1_fitness=0.0,  # No fitness gain from bye
                    agent2_fitness=0.0,
                    games_played=0,
                    metadata={'bye': True}
                )
                print(f"   Match {i+1}: {agent1.agent_id} gets BYE")
            else:
                # Regular match
                print(f"   Match {i+1}: {agent1.agent_id} vs {agent2.agent_id}")
                result = match_runner_func(agent1, agent2)
            
            round_results.append(result)
            self.all_results.append(result)
        
        return round_results
    
    def _update_standings(self, round_results: List[TournamentResult]):
        """Update agent standings with round results"""
        for result in round_results:
            # Update agent 1
            standing1 = self.standings[result.agent1_id]
            standing1.wins += result.agent1_score
            standing1.games_played += 1 if result.agent2_id != "BYE" else 0
            standing1.total_fitness += result.agent1_fitness
            if result.agent2_id != "BYE":
                standing1.opponents_faced.add(result.agent2_id)
            standing1.match_history.append(result)
            
            # Update agent 2 (if not bye)
            if result.agent2_id != "BYE":
                standing2 = self.standings[result.agent2_id]
                standing2.wins += result.agent2_score
                standing2.games_played += 1
                standing2.total_fitness += result.agent2_fitness
                standing2.opponents_faced.add(result.agent1_id)
                standing2.match_history.append(result)
    
    def _update_strength_of_schedule(self):
        """Update strength of schedule for all agents"""
        # Calculate win rates first
        win_rates = {}
        for agent_id, standing in self.standings.items():
            win_rates[agent_id] = standing.win_rate
        
        # Calculate strength of schedule
        for agent_id, standing in self.standings.items():
            if standing.opponents_faced:
                sos = sum(win_rates[opp_id] for opp_id in standing.opponents_faced)
                sos /= len(standing.opponents_faced)
                standing._strength_of_schedule = sos
            else:
                standing._strength_of_schedule = 0.0
    
    def _get_final_rankings(self) -> List[Tuple[str, AgentStanding]]:
        """Get final tournament rankings"""
        self._update_strength_of_schedule()
        
        # Sort by wins, then strength of schedule, then average fitness
        ranked_standings = sorted(
            self.standings.items(),
            key=lambda x: (x[1].wins, x[1].strength_of_schedule, x[1].avg_fitness),
            reverse=True
        )
        
        return ranked_standings
    
    def _print_round_summary(self):
        """Print summary of current round"""
        # Get top 5 agents
        current_rankings = sorted(
            self.standings.items(),
            key=lambda x: (x[1].wins, x[1].avg_fitness),
            reverse=True
        )[:5]
        
        print(f"   Top 5 after round {self.current_round}:")
        for i, (agent_id, standing) in enumerate(current_rankings):
            print(f"     {i+1}. {agent_id}: {standing.wins:.1f} wins, "
                  f"{standing.avg_fitness:.1f} avg fitness")
    
    def _print_final_results(self, top_agents: List[Tuple[str, AgentStanding]]):
        """Print final tournament results"""
        print(f"\n🥇 Final Rankings (Top {len(top_agents)}):")
        for i, (agent_id, standing) in enumerate(top_agents):
            print(f"  {i+1:2d}. {agent_id:20s} | "
                  f"Wins: {standing.wins:4.1f} | "
                  f"Games: {standing.games_played:2d} | "
                  f"Win Rate: {standing.win_rate:5.1%} | "
                  f"Avg Fitness: {standing.avg_fitness:6.1f} | "
                  f"SoS: {standing.strength_of_schedule:5.3f}")

    def get_tournament_stats(self) -> Dict:
        """Get comprehensive tournament statistics"""
        return {
            'total_agents': self.n_agents,
            'total_rounds': self.rounds,
            'total_matches': len(self.all_results),
            'matches_per_agent': sum(s.games_played for s in self.standings.values()) / self.n_agents,
            'final_rankings': self._get_final_rankings()
        }
