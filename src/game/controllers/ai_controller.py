"""
AI Controller for fighting game
Handles both rule-based and RL-based AI decision making
"""
import random
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../core')))
import config

# Try to import PyTorch for RL policies
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available - RL policies disabled")

class DummyAI:
    def __init__(self):
        self.decision_timer = 0
        self.current_action = "idle"
        self.action_duration = 0
        self.target_distance = 150  # Preferred distance from opponent
        self.behavior_mode = config.AIBehavior.DEFAULT  # Current behavior mode
        self.is_charging_projectile = False
        self.charge_start_distance = 0

    def set_behavior_mode(self, mode):
        """Set the AI behavior mode"""
        self.behavior_mode = mode
        print(f"AI behavior changed to: {self._get_behavior_name(mode)}")

    def _get_behavior_name(self, mode):
        """Get human-readable name for behavior mode"""
        if mode == config.AIBehavior.DEFAULT:
            return "Default AI"
        elif mode == config.AIBehavior.IDLE:
            return "Idle (Stand Still)"
        elif mode == config.AIBehavior.BLOCK:
            return "Constant Block"
        return "Unknown"

    def update_fighter(self, fighter, opponent, audio_manager=None):
        """Update fighter based on current behavior mode"""
        self.audio_manager = audio_manager  # Store for use in actions
        if self.behavior_mode == config.AIBehavior.IDLE:
            self._idle_behavior(fighter)
            return None
        elif self.behavior_mode == config.AIBehavior.BLOCK:
            self._block_behavior(fighter)
            return None
        else:  # DEFAULT
            return self._default_behavior(fighter, opponent)

    def _idle_behavior(self, fighter):
        """Idle behavior - do nothing"""
        # Don't interfere with knockback state
        if fighter.state != config.FighterState.KNOCKBACK:
            fighter.stop_moving()
            if fighter.is_blocking:
                fighter.stop_blocking()

    def _block_behavior(self, fighter):
        """Constant blocking behavior"""
        # Don't interfere with knockback state
        if fighter.state != config.FighterState.KNOCKBACK:
            fighter.stop_moving()
            fighter.block()

    def _default_behavior(self, fighter, opponent):
        """Original AI behavior"""
        self.decision_timer += 1

        # Make new decision every AI_DECISION_INTERVAL frames
        if self.decision_timer >= config.AI_DECISION_INTERVAL:
            self.decision_timer = 0
            self._make_decision(fighter, opponent)

        # Execute current action and check for projectile
        projectile = self._execute_action(fighter, opponent)

        # Decrease action duration
        if self.action_duration > 0:
            self.action_duration -= 1

        return projectile

    def _make_decision(self, fighter, opponent):
        """Make a new AI decision based on game state"""
        distance = abs(fighter.x - opponent.x)

        # Check if we should continue charging projectile
        if self.is_charging_projectile:
            # Check if fully charged
            is_fully_charged = (fighter.charging_orb and
                              fighter.charging_orb.get_charge_percent() >= 1.0)

            # Continue charging if distance hasn't changed significantly and not fully charged
            distance_change = abs(distance - self.charge_start_distance)
            if distance_change < 50 and fighter.is_charging_projectile and not is_fully_charged:
                # Keep charging
                self.current_action = "charge_projectile"
                self.action_duration = 10  # Continue for a bit longer
                return
            else:
                # Stop charging (distance changed, fully charged, or charging stopped)
                self.is_charging_projectile = False
                self.current_action = "fire_projectile"
                self.action_duration = 5
                return

        # Calculate probabilities based on distance and situation
        if distance < 100:  # Close range
            if random.random() < config.AI_ATTACK_CHANCE:
                # Choose random attack
                if random.random() < 0.5:
                    self.current_action = "punch"
                else:
                    self.current_action = "kick"
                self.action_duration = 20
            elif random.random() < config.AI_BLOCK_CHANCE:
                self.current_action = "block"
                self.action_duration = 30
            else:
                # Move away
                if fighter.x < opponent.x:
                    self.current_action = "move_left"
                else:
                    self.current_action = "move_right"
                self.action_duration = 40

        elif distance > 300:  # Far range
            # Consider projectile charging (30% chance) or move closer
            if random.random() < 0.3 and fighter.can_charge_projectile():
                self.current_action = "start_projectile"
                self.action_duration = 5
                self.is_charging_projectile = True
                self.charge_start_distance = distance
            else:
                # Move closer
                if fighter.x < opponent.x:
                    self.current_action = "move_right"
                else:
                    self.current_action = "move_left"
                self.action_duration = 60

        else:  # Medium range (100-300 pixels)
            # Consider projectile charging (20% chance) or random behavior
            if random.random() < 0.2 and fighter.can_charge_projectile():
                self.current_action = "start_projectile"
                self.action_duration = 5
                self.is_charging_projectile = True
                self.charge_start_distance = distance
            elif random.random() < config.AI_JUMP_CHANCE:
                self.current_action = "jump"
                self.action_duration = 10
            else:
                # Random behavior
                actions = ["move_left", "move_right", "idle", "jump"]
                weights = [0.25, 0.25, 0.3, 0.2]
                self.current_action = random.choices(actions, weights=weights)[0]
                self.action_duration = random.randint(20, 60)

    def _execute_action(self, fighter, opponent):
        """Execute the current AI action"""
        projectile = None

        if self.current_action == "move_left":
            fighter.move_left(getattr(self, 'audio_manager', None))
        elif self.current_action == "move_right":
            fighter.move_right(getattr(self, 'audio_manager', None))
        elif self.current_action == "jump":
            fighter.jump(getattr(self, 'audio_manager', None))
        elif self.current_action == "punch":
            fighter.punch(getattr(self, 'audio_manager', None))
        elif self.current_action == "kick":
            fighter.kick(getattr(self, 'audio_manager', None))
        elif self.current_action == "block":
            fighter.block()
        elif self.current_action == "start_projectile":
            # Start charging projectile
            if fighter.can_charge_projectile():
                fighter.start_charging_projectile()
        elif self.current_action == "charge_projectile":
            # Continue charging (fighter should already be charging)
            pass  # Just wait, charging happens automatically
        elif self.current_action == "fire_projectile":
            # Fire the projectile if we're charging
            if fighter.is_charging_projectile:
                projectile = fighter.stop_charging_projectile(getattr(self, 'audio_manager', None))
            self.is_charging_projectile = False
        elif self.current_action == "idle":
            fighter.stop_moving()
            if fighter.is_blocking:
                fighter.stop_blocking()

        # Stop action if duration expired
        if self.action_duration <= 0:
            self.current_action = "idle"

        return projectile


class BalancedAI:
    """
    Balanced AI with phase-based personality system

    Uses top-level parameters to modify behavior:
    - current_phase: "aggressive", "defensive", "neutral"
    - aggression_level: 0.0-1.0 (defensive to aggressive)
    - adaptation_factor: 0.0-1.0 (ignore to heavily adapt to opponent)
    """

    def __init__(self, personality="aggressive", difficulty="easy"):
        # AI Configuration
        self.personality = personality  # "aggressive", "defensive", "zoner", "balanced"
        self.difficulty = difficulty    # "easy", "medium", "hard"

        # Strategic level (5-10 seconds)
        # Set initial intent based on personality
        if personality == "aggressive":
            self.current_intent = "pressure"
        elif personality == "defensive":
            self.current_intent = "counter"
        elif personality == "zoner":
            self.current_intent = "zone"
        else:  # balanced
            self.current_intent = "pressure"

        self.intent_timer = 0
        self.intent_duration = 300  # 5 seconds at 60fps
        self.last_intent_switch = 0

        # Tactical level (1-3 seconds)
        self.current_sequence = []
        self.sequence_index = 0
        self.sequence_timer = 0
        self.sequence_complete = True
        self.first_sequence_selected = False

        # Execution level (frame-by-frame)
        self.current_action = "idle"
        self.action_duration = 0
        self.decision_timer = 0

        # Legacy phase system (for compatibility)
        self.current_phase = "neutral"  # "aggressive", "defensive", "neutral"
        self.last_attacks = []  # Track recent attacks for variety

        # Opponent analysis
        self.opponent_patterns = {
            'block_frequency': 0.5,
            'aggression': 0.5,
            'movement_frequency': 0.5
        }

        # Pattern tracking
        self.opponent_action_history = []
        self.frame_count = 0

        # Projectile evasion cooldown to prevent spam jumping
        self.last_evasion_frame = -100  # Frame when we last evaded
        self.last_evasion_type = None   # Type of last evasion (charging vs projectile)

        # Configure AI based on personality and difficulty
        self._configure_ai()

        # Tactical sequences (simplified for debugging)
        self.tactical_sequences = {
            "pressure_close": ["punch", "kick", "punch"],
            "pressure_far": ["move_toward", "punch", "kick"],
            "zone_basic": ["projectile", "move_away", "projectile"],
            "zone_defensive": ["block", "projectile", "move_away"],
            "counter_bait": ["block", "punch", "kick"],
            "counter_punish": ["punch", "kick", "block"],
            "reset_neutral": ["idle", "move_toward", "punch"],
            "reset_reposition": ["jump", "punch", "kick"]
        }

    def _configure_ai(self):
        """Configure AI parameters based on personality and difficulty"""

        # Difficulty settings
        difficulty_settings = {
            "easy": {
                "decision_interval": 20,  # Slower decisions
                "action_duration_multiplier": 1.5,  # Longer actions
                "adaptation_speed": 0.3,  # Slow learning
                "reaction_time": 15  # Delayed reactions
            },
            "medium": {
                "decision_interval": 15,
                "action_duration_multiplier": 1.0,
                "adaptation_speed": 0.6,
                "reaction_time": 8
            },
            "hard": {
                "decision_interval": 10,  # Faster decisions
                "action_duration_multiplier": 0.8,  # Shorter actions
                "adaptation_speed": 1.0,  # Fast learning
                "reaction_time": 3  # Quick reactions
            }
        }

        # Personality tactical preferences
        personality_tactics = {
            "aggressive": {"pressure": 0.85, "counter": 0.1, "zone": 0.05},  # Much more pressure-focused
            "defensive": {"counter": 0.8, "zone": 0.15, "pressure": 0.05},  # Much more counter-focused
            "zoner": {"zone": 0.7, "counter": 0.2, "pressure": 0.1},
            "balanced": {"pressure": 0.33, "zone": 0.33, "counter": 0.33}
        }

        # Personality characteristics
        personality_traits = {
            "aggressive": {
                "preferred_range": "close",
                "aggression_level": 0.8,
                "adaptation_factor": 0.5,  # Less adaptive, more aggressive
                "variety_enforcement": 0.6  # Less variety, more aggression
            },
            "defensive": {
                "preferred_range": "medium",
                "aggression_level": 0.2,
                "adaptation_factor": 0.9,  # Highly adaptive
                "variety_enforcement": 0.8
            },
            "zoner": {
                "preferred_range": "far",
                "aggression_level": 0.3,
                "adaptation_factor": 0.7,
                "variety_enforcement": 0.5  # Focus on projectiles
            },
            "balanced": {
                "preferred_range": "medium",
                "aggression_level": 0.5,
                "adaptation_factor": 0.7,
                "variety_enforcement": 0.8
            }
        }

        # Apply difficulty settings
        diff_config = difficulty_settings[self.difficulty]
        self.base_decision_interval = diff_config["decision_interval"]
        self.action_duration_multiplier = diff_config["action_duration_multiplier"]
        self.adaptation_speed = diff_config["adaptation_speed"]
        self.reaction_time = diff_config["reaction_time"]

        # Apply personality settings
        personality_config = personality_traits[self.personality]
        self.preferred_range = personality_config["preferred_range"]
        self.aggression_level = personality_config["aggression_level"]
        self.adaptation_factor = personality_config["adaptation_factor"]
        self.variety_enforcement = personality_config["variety_enforcement"]

        # Store tactical preferences
        self.tactical_preferences = personality_tactics[self.personality]

        print(f"🤖 AI configured: {self.personality.title()} ({self.difficulty.title()})")
        print(f"   Range: {self.preferred_range}, Aggression: {self.aggression_level:.1f}")
        print(f"   Initial Intent: {self.current_intent.upper()}")
        print(f"   Tactical Preferences: {self.tactical_preferences}")

    def update_fighter(self, fighter, opponent, audio_manager=None):
        """Simplified update method with better action flow"""
        self.audio_manager = audio_manager
        self.frame_count += 1

        # Update opponent pattern tracking
        self._track_opponent_patterns(opponent)

        # Make decisions at regular intervals, but don't interrupt movement
        self.decision_timer += 1
        decision_interval = self.base_decision_interval  # Use configured interval

        # Use longer intervals for movement to make it more fluid
        if self.current_action in ["move_toward", "move_away"]:
            decision_interval = int(self.base_decision_interval * 1.5)  # 1.5x longer for movement

        if self.decision_timer >= decision_interval:
            self.decision_timer = 0
            # Don't interrupt movement unless action is complete or urgent
            if (self.action_duration <= 0 or
                self.current_action not in ["move_toward", "move_away"] or
                self._is_urgent_situation(fighter, opponent)):
                self._make_simple_decision(fighter, opponent)

        # Execute current action
        projectile = self._execute_action(fighter, opponent)

        # Decrease action duration
        if self.action_duration > 0:
            self.action_duration -= 1
        else:
            self.current_action = "idle"

        return projectile

    def _track_opponent_patterns(self, opponent):
        """Track opponent behavior patterns"""
        # Record current opponent state
        opponent_state = {
            'is_attacking': opponent.is_attacking,
            'is_blocking': opponent.is_blocking,
            'is_moving': abs(opponent.velocity_x) > 0.1
        }

        self.opponent_action_history.append(opponent_state)

        # Keep only recent history (last 5 seconds)
        max_history = 300  # 5 seconds at 60fps
        if len(self.opponent_action_history) > max_history:
            self.opponent_action_history = self.opponent_action_history[-max_history:]

        # Update patterns every 60 frames (1 second)
        if self.frame_count % 60 == 0 and len(self.opponent_action_history) > 60:
            recent_history = self.opponent_action_history[-60:]

            # Calculate frequencies
            self.opponent_patterns['block_frequency'] = sum(1 for h in recent_history if h['is_blocking']) / len(recent_history)
            self.opponent_patterns['aggression'] = sum(1 for h in recent_history if h['is_attacking']) / len(recent_history)
            self.opponent_patterns['movement_frequency'] = sum(1 for h in recent_history if h['is_moving']) / len(recent_history)

    def _update_phase(self, fighter, opponent):
        """Update current tactical phase"""
        # Check if it's time to switch phases
        if self.frame_count - self.last_phase_switch > self.phase_duration:
            self._switch_phase(fighter, opponent)

        # Emergency phase switches based on situation
        health_ratio = fighter.health / 100.0
        opponent_health_ratio = opponent.health / 100.0

        # Switch to defensive if health is low
        if health_ratio < 0.3 and self.current_phase != "defensive":
            self.current_phase = "defensive"
            self.last_phase_switch = self.frame_count

        # Switch to aggressive if opponent health is low
        elif opponent_health_ratio < 0.3 and self.current_phase != "aggressive":
            self.current_phase = "aggressive"
            self.last_phase_switch = self.frame_count

    def _switch_phase(self, fighter, opponent):
        """Switch to a new tactical phase"""
        phases = ["aggressive", "defensive", "neutral"]

        # Remove current phase from options for variety
        available_phases = [p for p in phases if p != self.current_phase]

        # Weight phases based on situation
        weights = []
        for phase in available_phases:
            if phase == "aggressive":
                # More likely if we're winning or opponent is passive
                weight = 1.0
                if fighter.health > opponent.health:
                    weight += 0.5
                if self.opponent_patterns['aggression'] < 0.3:
                    weight += 0.3
            elif phase == "defensive":
                # More likely if we're losing or opponent is aggressive
                weight = 1.0
                if fighter.health < opponent.health:
                    weight += 0.5
                if self.opponent_patterns['aggression'] > 0.6:
                    weight += 0.3
            else:  # neutral
                weight = 1.0

            weights.append(weight)

        # Select new phase
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        import random
        self.current_phase = random.choices(available_phases, weights=normalized_weights)[0]
        self.last_phase_switch = self.frame_count

        print(f"🤖 AI switched to {self.current_phase} phase")

    def _update_strategic_intent(self, fighter, opponent):
        """Update strategic intent (high-level strategy)"""
        # Check if it's time to switch intent
        if self.frame_count - self.last_intent_switch > self.intent_duration:
            self._switch_strategic_intent(fighter, opponent)

        # Emergency intent switches based on critical situations
        health_ratio = fighter.health / 100.0
        opponent_health_ratio = opponent.health / 100.0
        distance = abs(fighter.x - opponent.x)

        # Switch to counter if opponent is very aggressive
        if (self.opponent_patterns.get('aggression', 0.5) > 0.7 and
            self.current_intent != "counter"):
            self.current_intent = "counter"
            self.last_intent_switch = self.frame_count
            self.sequence_complete = True  # Force new sequence
            print(f"🛡️ AI switching to COUNTER intent (opponent aggressive)")

        # Switch to pressure if opponent is very passive
        elif (self.opponent_patterns.get('aggression', 0.5) < 0.2 and
              distance < 200 and self.current_intent != "pressure"):
            self.current_intent = "pressure"
            self.last_intent_switch = self.frame_count
            self.sequence_complete = True
            print(f"⚔️ AI switching to PRESSURE intent (opponent passive)")

    def _switch_strategic_intent(self, fighter, opponent):
        """Switch to a new strategic intent"""
        distance = abs(fighter.x - opponent.x)
        health_ratio = fighter.health / 100.0
        health_advantage = (fighter.health - opponent.health) / 100.0

        # Calculate intent weights based on situation
        intent_weights = {
            "pressure": 1.0,
            "zone": 1.0,
            "counter": 1.0,
            "reset": 0.3
        }

        # Distance-based modifications
        if distance > 250:
            intent_weights["pressure"] *= 1.5  # Want to close gap
            intent_weights["zone"] *= 0.7
        elif distance < 100:
            intent_weights["zone"] *= 1.4     # Want to create space
            intent_weights["pressure"] *= 0.8

        # Health-based modifications
        if health_ratio < 0.4:
            intent_weights["counter"] *= 1.4   # More defensive when low health
            intent_weights["pressure"] *= 0.6
        elif health_advantage > 0.3:
            intent_weights["pressure"] *= 1.3  # More aggressive when winning

        # Opponent pattern adaptations
        if self.opponent_patterns.get('block_frequency', 0.5) > 0.6:
            intent_weights["zone"] *= 1.3      # Zone against defensive opponent
            intent_weights["pressure"] *= 0.7

        if self.opponent_patterns.get('aggression', 0.5) > 0.6:
            intent_weights["counter"] *= 1.4   # Counter aggressive opponent
            intent_weights["pressure"] *= 0.8

        # Avoid repeating the same intent
        if self.current_intent in intent_weights:
            intent_weights[self.current_intent] *= 0.5

        # Select new intent
        total_weight = sum(intent_weights.values())
        normalized_weights = {k: v / total_weight for k, v in intent_weights.items()}

        import random
        new_intent = random.choices(
            list(normalized_weights.keys()),
            weights=list(normalized_weights.values())
        )[0]

        self.current_intent = new_intent
        self.last_intent_switch = self.frame_count
        self.sequence_complete = True  # Force new sequence selection

        print(f"🧠 AI switching to {new_intent.upper()} intent")

    def _make_simple_decision(self, fighter, opponent):
        """Simplified decision making with better action flow"""
        distance = abs(fighter.x - opponent.x)

        # Check for incoming projectiles and jump if needed
        projectile_action = self._check_projectile_evasion(fighter, opponent)
        if projectile_action:
            self.current_action = projectile_action["action"]
            self.action_duration = int(projectile_action["duration"] * self.action_duration_multiplier)
            print(f"🎮 AI: {projectile_action['action']} (evading projectile)")
            return

        # Update current intent occasionally
        if self.frame_count % 180 == 0:  # Every 3 seconds
            self._update_simple_intent(fighter, opponent, distance)

        # Choose action based on intent and distance
        if self.current_intent == "pressure":
            # Defensive personalities are much more reluctant to pressure
            if self.personality == "defensive":
                pressure_range = 180 if self.difficulty == "hard" else 160 if self.difficulty == "medium" else 140
            else:
                pressure_range = 120

            if distance > pressure_range:
                action = "move_toward"
                duration = 25  # Longer for fluid movement
            elif distance < 60:
                # Close combat - heavily favor attacks for aggressive personalities
                if self.personality == "aggressive":
                    # Aggressive personalities attack much more frequently
                    attack_chance = 0.9 if self.difficulty == "hard" else 0.8 if self.difficulty == "medium" else 0.7
                    if self.frame_count % 30 < 30 * attack_chance:
                        if self.frame_count % 20 < 10:
                            action = "punch"
                            duration = 8
                        else:
                            action = "kick"
                            duration = 10
                    else:
                        action = "block"
                        duration = 8  # Shorter block duration for aggressive
                elif self.personality == "defensive":
                    # Defensive personalities want to escape close range!
                    escape_chance = 0.7 if self.difficulty == "hard" else 0.6 if self.difficulty == "medium" else 0.5
                    if self.frame_count % 30 < 30 * escape_chance:
                        action = "move_away"
                        duration = 20  # Try to escape
                    else:
                        # When forced to fight close, mostly block
                        if self.frame_count % 40 < 10:
                            action = "punch"  # Occasional counter
                            duration = 8
                        else:
                            action = "block"
                            duration = 15  # Long defensive blocks
                else:
                    # Non-aggressive, non-defensive personalities use original pattern
                    if self.frame_count % 60 < 20:
                        action = "punch"
                        duration = 8
                    elif self.frame_count % 60 < 40:
                        action = "kick"
                        duration = 10
                    else:
                        action = "block"
                        duration = 12
            else:
                # Medium range - aggressive personalities attack more
                if self.personality == "aggressive":
                    attack_chance = 0.8 if self.difficulty == "hard" else 0.7 if self.difficulty == "medium" else 0.6
                    if self.frame_count % 30 < 30 * attack_chance:
                        if self.frame_count % 20 < 10:
                            action = "punch"
                            duration = 8
                        else:
                            action = "kick"
                            duration = 10
                    else:
                        action = "move_toward"
                        duration = 15  # Shorter movement for more aggression
                else:
                    # Non-aggressive personalities use original pattern
                    if self.frame_count % 40 < 15:
                        action = "punch"
                        duration = 8
                    else:
                        action = "move_toward"
                        duration = 20  # Longer for fluid movement

        elif self.current_intent == "zone":
            # Defensive personalities want much more space
            if self.personality == "defensive":
                zone_distance = 200 if self.difficulty == "hard" else 180 if self.difficulty == "medium" else 160
            else:
                zone_distance = 150

            if distance < zone_distance:
                action = "move_away"
                duration = 25  # Longer for fluid movement
            else:
                # Far range - defensive personalities block more, attack less
                if self.personality == "defensive":
                    if self.frame_count % 60 < 20:  # Only 33% projectiles
                        action = "projectile"
                        duration = 15
                    else:
                        action = "block"  # 67% blocking
                        duration = 15  # Longer blocks for defensive
                else:
                    # Non-defensive personalities use original pattern
                    if self.frame_count % 50 < 25:
                        action = "projectile"
                        duration = 15
                    else:
                        action = "block"
                        duration = 12

        elif self.current_intent == "counter":
            if opponent.is_attacking:
                # Aggressive personalities block less, attack more even when opponent attacks
                if self.personality == "aggressive" and self.difficulty == "hard":
                    # 30% chance to attack instead of block (risky but aggressive)
                    if self.frame_count % 10 < 3:
                        action = "punch" if self.frame_count % 20 < 10 else "kick"
                        duration = 8
                    else:
                        action = "block"
                        duration = 8  # Shorter block
                else:
                    action = "block"
                    duration = 12
            elif self.personality == "defensive":
                # Defensive personalities in COUNTER mode should counter-attack when in range
                # Hard mode is more precise with ranges, Easy mode makes more mistakes

                if self.difficulty == "hard":
                    # Hard mode: precise range awareness
                    punch_range = 45  # Very precise punch range
                    kick_range = 85   # Precise kick range
                elif self.difficulty == "medium":
                    # Medium mode: decent range awareness
                    punch_range = 55  # Slightly less precise
                    kick_range = 95
                else:  # easy
                    # Easy mode: poor range awareness, makes mistakes
                    punch_range = 70  # Often tries punches too far
                    kick_range = 110  # Often tries kicks too far

                if distance < punch_range:
                    # Punch range - counter with punches only
                    counter_chance = 0.7 if self.difficulty == "hard" else 0.6 if self.difficulty == "medium" else 0.5
                    if self.frame_count % 30 < 30 * counter_chance:
                        action = "punch"  # Counter-attack with punch
                        duration = 8
                    else:
                        action = "move_away"  # Back away if not countering
                        duration = 20
                elif distance < kick_range:
                    # Kick range - counter with kicks only
                    counter_chance = 0.8 if self.difficulty == "hard" else 0.7 if self.difficulty == "medium" else 0.6
                    if self.frame_count % 30 < 30 * counter_chance:
                        action = "kick"  # Counter-attack with kick
                        duration = 10
                    else:
                        action = "block"  # Block if not countering
                        duration = 15
                elif distance < 150:
                    # Medium range - only kicks (no punches that will miss)
                    if self.frame_count % 60 < 15:  # 25% counter chance
                        action = "kick"  # Only kicks at this range
                        duration = 10
                    else:
                        action = "block"  # Mostly blocking
                        duration = 18
                elif distance > 250:
                    # Very far - use projectiles from safe distance
                    action = "projectile"
                    duration = 15
                else:
                    # Far range - mostly block and wait
                    if self.frame_count % 80 < 10:  # 12.5% projectile chance
                        action = "projectile"
                        duration = 15
                    else:
                        action = "block"
                        duration = 20
            elif distance > 100:
                # Non-defensive personalities move toward when far
                action = "move_toward"
                duration = 20  # Longer for fluid movement
            else:
                # Counter attack - aggressive personalities attack more frequently
                if self.personality == "aggressive":
                    attack_chance = 0.85 if self.difficulty == "hard" else 0.75 if self.difficulty == "medium" else 0.65
                    if self.frame_count % 25 < 25 * attack_chance:
                        if self.frame_count % 20 < 10:
                            action = "punch"
                            duration = 8
                        else:
                            action = "kick"
                            duration = 10
                    else:
                        action = "block"
                        duration = 8
                else:
                    # Non-aggressive personalities use original pattern
                    if self.frame_count % 30 < 15:
                        action = "punch"
                        duration = 8
                    else:
                        action = "kick"
                        duration = 10
        else:  # reset or fallback
            if distance < 80:
                action = "punch"
                duration = 8
            elif distance > 250:
                action = "projectile"
                duration = 15
            else:
                action = "move_toward"
                duration = 20  # Longer for fluid movement

        # Set the action with difficulty-adjusted duration
        self.current_action = action
        self.action_duration = int(duration * self.action_duration_multiplier)

        # Track attacks for variety
        if action in ['punch', 'kick', 'projectile']:
            self.last_attacks.append(action)
            if len(self.last_attacks) > 5:
                self.last_attacks = self.last_attacks[-5:]

        print(f"🎮 AI: {action} (intent: {self.current_intent}, distance: {distance:.0f})")

    def _update_simple_intent(self, fighter, opponent, distance):
        """Intent switching based on personality and situation"""
        health_ratio = fighter.health / 100.0

        # Get personality preferences
        pressure_weight = self.tactical_preferences["pressure"]
        zone_weight = self.tactical_preferences["zone"]
        counter_weight = self.tactical_preferences["counter"]

        # Situational modifiers
        if health_ratio < 0.4:
            counter_weight *= 2.0  # More defensive when low health

        if distance > 200:
            pressure_weight *= 1.5  # Want to close gap
            zone_weight *= 0.7
        elif distance < 80:
            zone_weight *= 1.5  # Want to create space
            pressure_weight *= 0.7

        if self.opponent_patterns.get('aggression', 0.5) > 0.6:
            counter_weight *= 1.5  # Counter aggressive opponent

        # Aggressive personalities strongly favor pressure, especially on hard difficulty
        if self.personality == "aggressive":
            pressure_multiplier = 2.5 if self.difficulty == "hard" else 2.0 if self.difficulty == "medium" else 1.5
            pressure_weight *= pressure_multiplier
            # Reduce other intents for aggressive personalities
            counter_weight *= 0.5
            zone_weight *= 0.3

        # Defensive personalities strongly avoid pressure and heavily favor counter
        elif self.personality == "defensive":
            # Massive boost to counter intent for defensive personalities
            counter_multiplier = 5.0 if self.difficulty == "hard" else 4.0 if self.difficulty == "medium" else 3.0
            counter_weight *= counter_multiplier

            # Moderate boost to zone, but much less than counter
            zone_weight *= 1.5

            # Heavily reduce pressure for defensive personalities
            pressure_weight *= 0.1

        # Select intent based on weighted preferences
        import random
        intents = ["pressure", "zone", "counter"]
        weights = [pressure_weight, zone_weight, counter_weight]

        # Avoid repeating same intent too much
        if self.current_intent in intents:
            current_index = intents.index(self.current_intent)
            weights[current_index] *= 0.5

        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        self.current_intent = random.choices(intents, weights=normalized_weights)[0]

        print(f"🧠 AI intent: {self.current_intent.upper()} ({self.personality})")

    def _is_urgent_situation(self, fighter, opponent):
        """Check if situation requires immediate action change"""
        # Urgent if opponent is attacking and we're not blocking
        if opponent.is_attacking and self.current_action != "block":
            return True

        # Urgent if we're very close and moving toward (might want to attack)
        distance = abs(fighter.x - opponent.x)
        if distance < 50 and self.current_action == "move_toward":
            return True

        # Urgent if we're very far and moving away (might want to approach)
        if distance > 300 and self.current_action == "move_away":
            return True

        return False

    def _check_projectile_evasion(self, fighter, opponent):
        """Check for incoming projectiles and decide on evasion with difficulty-based timing"""
        # Only certain personalities and intents care about projectile evasion
        if self.current_intent not in ["counter", "zone"] and self.personality not in ["defensive", "balanced"]:
            return None

        # Check for projectiles in the air and distance-based threats
        projectile_threat = False
        projectile_urgency = 0  # 0 = no threat, 1 = charging, 2 = just fired, 3 = projectile in air
        projectile_distance = None

        # Check for projectiles in the air (from game state)
        # Try multiple ways to detect projectiles
        projectiles_found = []



        # Method 1: Check opponent.projectiles
        if hasattr(opponent, 'projectiles') and opponent.projectiles:
            for projectile in opponent.projectiles:
                if hasattr(projectile, 'x') and hasattr(projectile, 'y'):
                    # These should be opponent's projectiles, so they're threats
                    proj_distance = abs(fighter.x - projectile.x)
                    projectiles_found.append(proj_distance)

        # Method 2: Check game engine projectiles (if available)
        if hasattr(self, 'game_engine') and hasattr(self.game_engine, 'projectiles'):
            for projectile in self.game_engine.projectiles:
                if hasattr(projectile, 'x') and hasattr(projectile, 'y') and hasattr(projectile, 'owner'):
                    # Only evade projectiles that are NOT owned by this fighter
                    if projectile.owner != fighter:
                        proj_distance = abs(fighter.x - projectile.x)
                        projectiles_found.append(proj_distance)

        # Method 3: Check fighter's game reference
        if hasattr(fighter, 'game') and hasattr(fighter.game, 'projectiles'):
            if self.difficulty == "hard" and self.personality == "defensive":
                print(f"[DEBUGGING PROJECTILE EVASION] Found {len(fighter.game.projectiles)} projectiles in fighter.game.projectiles")
            for projectile in fighter.game.projectiles:
                if hasattr(projectile, 'x') and hasattr(projectile, 'y') and hasattr(projectile, 'owner'):
                    # Only evade projectiles that are NOT owned by this fighter
                    if projectile.owner != fighter:
                        proj_distance = abs(fighter.x - projectile.x)
                        projectiles_found.append(proj_distance)
                        if self.difficulty == "hard" and self.personality == "defensive":
                            print(f"[DEBUGGING PROJECTILE EVASION] Method 3 - Enemy projectile at distance: {proj_distance}px")
                    elif self.difficulty == "hard" and self.personality == "defensive":
                        print(f"[DEBUGGING PROJECTILE EVASION] Ignoring own projectile")

        # Use closest projectile if any found
        if projectiles_found:
            projectile_distance = min(projectiles_found)
            projectile_threat = True
            projectile_urgency = 3  # Projectile in air

        # Detect if opponent is charging a projectile
        if hasattr(opponent, 'is_charging_projectile') and opponent.is_charging_projectile:
            projectile_threat = True
            if projectile_urgency < 1:  # Don't override projectile in air
                projectile_urgency = 1
            if self.difficulty == "hard" and self.personality == "defensive":
                print(f"[DEBUGGING PROJECTILE EVASION] Opponent is charging projectile!")

        # Detect if opponent just fired (check recent actions or state)
        if hasattr(opponent, 'state') and hasattr(opponent, 'attack_timer'):
            # If opponent is in projectile state or just finished projectile
            if (str(opponent.state).lower().find('projectile') != -1 or
                (opponent.attack_timer > 0 and opponent.attack_timer < 10)):
                projectile_threat = True
                if projectile_urgency < 2:  # Don't override projectile in air
                    projectile_urgency = 2  # Just fired
                if self.difficulty == "hard" and self.personality == "defensive":
                    print(f"[DEBUGGING PROJECTILE EVASION] Opponent just fired! State: {opponent.state}, Timer: {getattr(opponent, 'attack_timer', 'N/A')}")

        # [DEBUGGING PROJECTILE EVASION] - Final threat assessment
        if self.difficulty == "hard" and self.personality == "defensive":
            print(f"[DEBUGGING PROJECTILE EVASION] Final assessment - Threat: {projectile_threat}, Urgency: {projectile_urgency}, Distance: {projectile_distance}")

        if not projectile_threat:
            if self.difficulty == "hard" and self.personality == "defensive" and self.frame_count % 60 == 0:
                print(f"[DEBUGGING PROJECTILE EVASION] No projectile threat detected")
            return None

        # Difficulty-based timing and decision making
        if self.difficulty == "hard":
            # Hard mode: Precise timing - jump when projectile is exactly 240px away
            if projectile_urgency == 3 and projectile_distance is not None:
                # Projectile in air - precise distance-based timing
                # Hard mode: Realistic jump timing based on projectile speed
                if 150 <= projectile_distance <= 200:  # Optimal jump window
                    evasion_chance = 0.95  # Very high chance - this is the right time
                elif 130 <= projectile_distance <= 220:  # Good window
                    evasion_chance = 0.7  # Good chance
                elif 110 <= projectile_distance <= 240:  # Acceptable window
                    evasion_chance = 0.4  # Moderate chance
                else:
                    evasion_chance = 0.0  # Never jump at wrong time
            elif projectile_urgency == 1:
                # Opponent is charging - Hard mode should be smart about timing
                if hasattr(opponent, 'charging_orb') and opponent.charging_orb:
                    charge_level = getattr(opponent.charging_orb, 'size', 10)
                    # [DEBUGGING PROJECTILE EVASION] Check more attributes
                    if self.personality == "defensive":
                        print(f"[DEBUGGING PROJECTILE EVASION] Charge orb found - size: {charge_level}")
                        print(f"[DEBUGGING PROJECTILE EVASION] Orb attributes: {dir(opponent.charging_orb)}")

                    # Hard mode: wait for larger charges, but not too long
                    if charge_level > 20:  # Large charge
                        evasion_chance = 0.95
                        if self.personality == "defensive":
                            print(f"[DEBUGGING PROJECTILE EVASION] Large charge detected: {charge_level} - HIGH EVASION!")
                    elif charge_level > 12:  # Medium charge
                        evasion_chance = 0.7
                        if self.personality == "defensive":
                            print(f"[DEBUGGING PROJECTILE EVASION] Medium charge: {charge_level} - MODERATE EVASION!")
                    else:
                        evasion_chance = 0.3  # Small charge, but still some chance
                        if self.personality == "defensive":
                            print(f"[DEBUGGING PROJECTILE EVASION] Small charge: {charge_level} - LOW EVASION!")
                else:
                    # No charge orb visible - assume it's about to fire
                    evasion_chance = 0.8  # High chance since we detected charging
                    if self.personality == "defensive":
                        print(f"[DEBUGGING PROJECTILE EVASION] Charging detected but no orb - HIGH EVASION!")
            elif projectile_urgency == 2:
                # Just fired - moderate chance (prefer distance-based timing)
                evasion_chance = 0.3
            else:
                evasion_chance = 0.02

        elif self.difficulty == "medium":
            # Medium mode: Tries to time precisely but mistimes often
            if projectile_urgency == 3 and projectile_distance is not None:
                # Projectile in air - attempts precise timing but with errors
                if 220 <= projectile_distance <= 260:  # Wider window, less precise
                    evasion_chance = 0.7  # Good but not perfect
                elif 200 <= projectile_distance <= 280:  # Even wider mistiming
                    evasion_chance = 0.4  # Sometimes mistimes
                else:
                    evasion_chance = 0.1  # Usually doesn't jump at wrong time
            elif projectile_urgency == 1:
                evasion_chance = 0.5  # Decent anticipation
            elif projectile_urgency == 2:
                evasion_chance = 0.6  # Good reaction
            else:
                evasion_chance = 0.2

        else:  # easy
            # Easy mode: Sporadic jumping while projectile is in air
            if projectile_urgency == 3:
                # Projectile in air - sporadic jumping throughout flight
                evasion_chance = 0.6  # Jumps frequently while projectile flies
            elif projectile_urgency >= 1:
                evasion_chance = 0.7  # Jumps a lot when sees any threat
            else:
                evasion_chance = 0.3  # Even jumps sometimes without clear threat

        # Apply personality modifiers
        if self.personality == "defensive":
            evasion_chance *= 1.2  # More cautious
        elif self.personality == "balanced":
            evasion_chance *= 1.0  # Normal
        else:
            evasion_chance *= 0.8  # Less evasive

        # Cap at 1.0
        evasion_chance = min(1.0, evasion_chance)

        # Check cooldown to prevent spam jumping - different cooldowns for different threats
        current_threat_type = "charging" if projectile_urgency == 1 else "projectile" if projectile_urgency == 3 else "other"

        # Shorter cooldown for different threat types, longer for same type
        if self.last_evasion_type == current_threat_type:
            evasion_cooldown = 45  # 0.75 second cooldown for same threat type
        else:
            evasion_cooldown = 20  # 0.33 second cooldown for different threat type

        frames_since_last_evasion = self.frame_count - self.last_evasion_frame

        if frames_since_last_evasion < evasion_cooldown:
            if self.difficulty == "hard" and self.personality == "defensive":
                print(f"[DEBUGGING PROJECTILE EVASION] Evasion on cooldown: {frames_since_last_evasion}/{evasion_cooldown} frames (type: {current_threat_type})")
            return None

        # Check if we should evade based on timing
        timing_check = 20 if self.difficulty == "easy" else 30 if self.difficulty == "medium" else 40
        timing_result = self.frame_count % timing_check < timing_check * evasion_chance

        # [DEBUGGING PROJECTILE EVASION] - Final decision
        if self.difficulty == "hard" and self.personality == "defensive":
            print(f"[DEBUGGING PROJECTILE EVASION] Evasion chance: {evasion_chance:.2f}, Timing check: {timing_result}, Frame: {self.frame_count % timing_check}/{timing_check}")

        if timing_result:
            # Record this evasion to prevent spam
            self.last_evasion_frame = self.frame_count
            self.last_evasion_type = current_threat_type

            distance = abs(fighter.x - opponent.x)

            # [DEBUGGING PROJECTILE EVASION] - Action selection
            if self.difficulty == "hard" and self.personality == "defensive":
                print(f"[DEBUGGING PROJECTILE EVASION] EVADING! Fighter distance from opponent: {distance}px")

            # Choose evasion method based on distance and personality
            if distance > 200:
                # Far away - can try to jump over
                if self.difficulty == "hard" and self.personality == "defensive":
                    print(f"[DEBUGGING PROJECTILE EVASION] Choosing JUMP (far distance)")
                return {"action": "jump", "duration": 20}
            elif distance > 100:
                # Medium distance - jump or move away
                if self.difficulty == "hard":
                    # Hard mode prefers precise jumping
                    if self.difficulty == "hard" and self.personality == "defensive":
                        print(f"[DEBUGGING PROJECTILE EVASION] Choosing JUMP (hard mode precision)")
                    return {"action": "jump", "duration": 20}
                elif self.frame_count % 40 < 20:
                    return {"action": "jump", "duration": 20}
                else:
                    return {"action": "move_away", "duration": 15}
            else:
                # Close distance - move away or jump
                if self.personality == "defensive":
                    if self.difficulty == "hard" and self.personality == "defensive":
                        print(f"[DEBUGGING PROJECTILE EVASION] Choosing MOVE_AWAY (defensive close)")
                    return {"action": "move_away", "duration": 15}
                else:
                    return {"action": "jump", "duration": 20}

        if self.difficulty == "hard" and self.personality == "defensive":
            print(f"[DEBUGGING PROJECTILE EVASION] Not evading this frame")

        return None

    def _update_tactical_sequence(self, fighter, opponent):
        """Update tactical sequence based on current intent"""
        # If sequence is complete or empty, select a new one
        if self.sequence_complete or not self.current_sequence or not self.first_sequence_selected:
            self._select_tactical_sequence(fighter, opponent)
            self.first_sequence_selected = True

    def _select_tactical_sequence(self, fighter, opponent):
        """Select appropriate tactical sequence for current intent"""
        distance = abs(fighter.x - opponent.x)

        if self.current_intent == "pressure":
            if distance > 150:
                sequence_name = "pressure_far"
            else:
                sequence_name = "pressure_close"

        elif self.current_intent == "zone":
            if self.opponent_patterns.get('aggression', 0.5) > 0.6:
                sequence_name = "zone_defensive"  # More blocking against aggressive opponent
            else:
                sequence_name = "zone_basic"

        elif self.current_intent == "counter":
            if distance > 120:
                sequence_name = "counter_punish"  # Punish from distance
            else:
                sequence_name = "counter_bait"    # Bait and counter up close

        elif self.current_intent == "reset":
            if abs(fighter.x - 400) > 200:  # Far from center
                sequence_name = "reset_reposition"
            else:
                sequence_name = "reset_neutral"
        else:
            sequence_name = "pressure_close"  # Fallback

        # Get the sequence
        self.current_sequence = self.tactical_sequences[sequence_name].copy()
        self.sequence_index = 0
        self.sequence_complete = False

        print(f"🎯 AI starting {sequence_name}: {self.current_sequence}")

    def _execute_sequence_action(self, fighter, opponent):
        """Execute current action in the tactical sequence"""
        # If no sequence or sequence complete, fall back to old decision making
        if self.sequence_complete or not self.current_sequence:
            return self._execute_fallback_action(fighter, opponent)

        # Get current action from sequence
        if self.sequence_index < len(self.current_sequence):
            action = self.current_sequence[self.sequence_index]
        else:
            # Sequence completed
            self.sequence_complete = True
            return self._execute_fallback_action(fighter, opponent)

        # Set action if we don't have one or current one is done
        if self.action_duration <= 0:
            self.current_action = action
            self.action_duration = self._get_action_duration(action)
            print(f"🎮 AI executing: {action} (step {self.sequence_index + 1}/{len(self.current_sequence)})")

            # Track attacks for variety
            if action in ['punch', 'kick', 'projectile']:
                self.last_attacks.append(action)
                if len(self.last_attacks) > 5:
                    self.last_attacks = self.last_attacks[-5:]

        # Execute the action
        return self._execute_action(fighter, opponent)

    def _execute_fallback_action(self, fighter, opponent):
        """Fallback to old decision making when no sequence is active"""
        # Use simplified decision making for fallback
        distance = abs(fighter.x - opponent.x)

        if distance < 80:
            self.current_action = "punch"
            self.action_duration = 15
        elif distance > 300:
            self.current_action = "projectile"
            self.action_duration = 30
        else:
            self.current_action = "move_toward"
            self.action_duration = 20

        return self._execute_action(fighter, opponent)

    def _make_decision(self, fighter, opponent):
        """Make tactical decision based on current state and phase"""
        # Get base action probabilities
        probs = self._get_action_probabilities(fighter, opponent)

        # Apply range-based filtering
        distance = abs(fighter.x - opponent.x)
        probs = self._filter_by_range(probs, distance)

        # Enforce attack variety
        probs = self._enforce_variety(probs)

        # Adapt to opponent patterns
        probs = self._adapt_to_opponent(probs, opponent)

        # Apply situational modifiers
        probs = self._apply_situational_modifiers(probs, fighter, opponent)

        # Select action
        action = self._weighted_random_choice(probs)

        # Set action and duration
        self.current_action = action
        self.action_duration = self._get_action_duration(action)

        # Track attacks for variety enforcement
        if action in ['punch', 'kick', 'projectile']:
            self.last_attacks.append(action)
            if len(self.last_attacks) > 5:  # Keep last 5 attacks
                self.last_attacks = self.last_attacks[-5:]

    def _get_action_probabilities(self, fighter, opponent):
        """Get base action probabilities based on current phase"""
        # Base balanced probabilities
        base_probs = {
            'punch': 0.15,
            'kick': 0.10,
            'projectile': 0.10,
            'block': 0.15,
            'move_toward': 0.20,
            'move_away': 0.10,
            'jump': 0.05,
            'idle': 0.15
        }

        # Apply phase modifiers
        if self.current_phase == "aggressive":
            base_probs['punch'] *= 1.8      # More punches
            base_probs['kick'] *= 1.5       # More kicks
            base_probs['move_toward'] *= 1.6 # Close distance
            base_probs['block'] *= 0.4      # Less blocking
            base_probs['move_away'] *= 0.3  # Less retreating
            base_probs['idle'] *= 0.5       # Less waiting

        elif self.current_phase == "defensive":
            base_probs['block'] *= 2.0      # More blocking
            base_probs['move_away'] *= 1.8  # More retreating
            base_probs['projectile'] *= 1.4 # More zoning
            base_probs['punch'] *= 0.6      # Fewer attacks
            base_probs['kick'] *= 0.5
            base_probs['move_toward'] *= 0.4 # Less advancing

        # Apply aggression_level (0.0-1.0)
        attack_multiplier = 0.5 + (self.aggression_level * 1.0)
        defense_multiplier = 1.5 - (self.aggression_level * 0.5)

        base_probs['punch'] *= attack_multiplier
        base_probs['kick'] *= attack_multiplier
        base_probs['block'] *= defense_multiplier

        return base_probs

    def _filter_by_range(self, probs, distance):
        """Modify probabilities based on current distance"""
        current_range = self._classify_range(distance)

        # Range-appropriate actions
        if current_range == "close":
            probs['punch'] *= 2.0
            probs['kick'] *= 1.5
            probs['projectile'] *= 0.1  # Can't use projectiles up close
            probs['move_away'] *= 1.3   # Sometimes back off

        elif current_range == "medium":
            # Medium range is good for all actions
            probs['move_toward'] *= 1.2  # Slight preference to close
            probs['projectile'] *= 1.1   # Good projectile range

        elif current_range == "far":
            probs['projectile'] *= 2.5
            probs['move_toward'] *= 1.8  # Need to close distance
            probs['punch'] *= 0.1  # Can't punch from far
            probs['kick'] *= 0.1
            probs['block'] *= 0.7  # Less need to block at range

        # Adjust movement based on preferred range
        if current_range != self.preferred_range:
            if self.preferred_range == "close" and current_range in ["medium", "far"]:
                probs['move_toward'] *= 1.5
            elif self.preferred_range == "far" and current_range in ["close", "medium"]:
                probs['move_away'] *= 1.5
                probs['jump'] *= 1.3  # Jump back

        return probs

    def _enforce_variety(self, probs):
        """Prevent spam by reducing probability of recently used attacks"""
        # Check last 3 attacks
        recent_attacks = self.last_attacks[-3:] if len(self.last_attacks) >= 3 else self.last_attacks

        for attack in recent_attacks:
            if attack in probs:
                # Reduce probability based on how recently it was used
                recency_penalty = 0.7 ** recent_attacks.count(attack)
                probs[attack] *= recency_penalty

        # Boost unused attacks
        all_attacks = ['punch', 'kick', 'projectile']
        for attack in all_attacks:
            if attack not in recent_attacks:
                probs[attack] *= 1.2  # Slight boost to unused attacks

        return probs

    def _adapt_to_opponent(self, probs, opponent):
        """Modify behavior based on opponent patterns"""
        # If opponent is attacking, increase blocking
        if opponent.is_attacking:
            probs['block'] *= 1.8
            probs['move_away'] *= 1.4
            probs['punch'] *= 0.3
            probs['kick'] *= 0.3

        # If opponent blocks frequently, use more movement/projectiles
        if self.opponent_patterns.get('block_frequency', 0) > 0.6:
            if 'move_toward' in probs:
                probs['move_toward'] *= 0.7  # Don't rush into blocks
            if 'projectile' in probs:
                probs['projectile'] *= 1.4   # Use ranged attacks
            if 'jump' in probs:
                probs['jump'] *= 1.3         # Use aerial approaches

        # If opponent is passive, be more aggressive
        if self.opponent_patterns.get('aggression', 0.5) < 0.3:
            if 'punch' in probs:
                probs['punch'] *= 1.3
            if 'kick' in probs:
                probs['kick'] *= 1.2
            if 'move_toward' in probs:
                probs['move_toward'] *= 1.4

        return probs

    def _apply_situational_modifiers(self, probs, fighter, opponent):
        """Apply situational modifiers based on health, position, etc."""
        # Health-based modifications
        health_ratio = fighter.health / 100.0
        health_advantage = (fighter.health - opponent.health) / 100.0

        # If low health, be more defensive
        if health_ratio < 0.3:
            probs['block'] *= 1.5
            probs['move_away'] *= 1.3
            probs['punch'] *= 0.8
            probs['kick'] *= 0.8

        # If winning by a lot, be more aggressive
        if health_advantage > 0.4:
            probs['punch'] *= 1.3
            probs['kick'] *= 1.2
            probs['move_toward'] *= 1.2

        # Edge avoidance
        stage_width = config.STAGE_WIDTH
        if fighter.x < 100:  # Near left edge
            probs['move_away'] *= 0.3  # Don't move further left
            probs['move_toward'] *= 1.5  # Move toward center
        elif fighter.x > stage_width - 100:  # Near right edge
            probs['move_away'] *= 0.3  # Don't move further right
            probs['move_toward'] *= 1.5  # Move toward center

        return probs

    def _classify_range(self, distance):
        """Classify distance as close, medium, or far"""
        if distance < 80:
            return "close"
        elif distance < 200:
            return "medium"
        else:
            return "far"

    def _weighted_random_choice(self, probs):
        """Select action based on weighted probabilities"""
        import random

        # Normalize probabilities
        total = sum(probs.values())
        if total == 0:
            return "idle"

        normalized_probs = {k: v/total for k, v in probs.items()}

        # Create cumulative distribution
        actions = list(normalized_probs.keys())
        weights = list(normalized_probs.values())

        return random.choices(actions, weights=weights)[0]

    def _get_action_duration(self, action):
        """Get duration for action in frames (shortened for faster sequences)"""
        durations = {
            'punch': 8,
            'kick': 10,
            'projectile': 15,
            'block': 12,
            'move_toward': 10,
            'move_away': 10,
            'jump': 15,
            'idle': 5
        }
        return durations.get(action, 5)

    def _execute_action(self, fighter, opponent):
        """Execute the current action"""
        projectile = None

        if self.current_action == "punch":
            fighter.punch(self.audio_manager)
        elif self.current_action == "kick":
            fighter.kick(self.audio_manager)
        elif self.current_action == "projectile":
            if fighter.can_charge_projectile():
                fighter.start_charging_projectile()
                # For AI, immediately fire a quick projectile (minimal charge)
                if fighter.charging_orb:
                    fighter.charging_orb.charge_time = 10  # Small charge
                    projectile = fighter.stop_charging_projectile(self.audio_manager)
        elif self.current_action == "block":
            fighter.block()
        elif self.current_action == "move_toward":
            # Move toward opponent
            if fighter.x < opponent.x:
                fighter.move_right(self.audio_manager)
            else:
                fighter.move_left(self.audio_manager)
        elif self.current_action == "move_away":
            # Move away from opponent
            if fighter.x < opponent.x:
                fighter.move_left(self.audio_manager)
            else:
                fighter.move_right(self.audio_manager)
        elif self.current_action == "jump":
            fighter.jump(self.audio_manager)
        elif self.current_action == "idle":
            fighter.stop_moving()
            if fighter.is_blocking:
                fighter.stop_blocking()

        return projectile


# RL-based AI Controller
class FighterPolicy(nn.Module):
    """Neural network policy for RL-trained AI"""

    def __init__(self, state_size=26, action_size=10, hidden_size=128):
        super(FighterPolicy, self).__init__()

        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch required for RL policies")

        self.state_size = state_size
        self.action_size = action_size

        # Policy network
        self.policy_net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_size)
        )

        # Value network (for actor-critic)
        self.value_net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, state):
        """Forward pass - returns action logits and value"""
        action_logits = self.policy_net(state)
        value = self.value_net(state)
        return action_logits, value

    def get_action(self, state, deterministic=False):
        """Get action from state"""
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state)

        if len(state.shape) == 1:
            state = state.unsqueeze(0)

        with torch.no_grad():
            action_logits, _ = self.forward(state)
            action_probs = F.softmax(action_logits, dim=-1)

            if deterministic:
                action = torch.argmax(action_probs, dim=-1)
            else:
                action = torch.multinomial(action_probs, 1).squeeze(-1)

            return action.item() if action.numel() == 1 else action.cpu().numpy()


class RLAIController:
    """RL-based AI controller that can load trained policies"""

    def __init__(self, policy_path=None, personality_config=None):
        self.policy = None
        self.personality = personality_config or {}
        self.action_mapping = {
            0: 'idle',
            1: 'move_left',
            2: 'move_right',
            3: 'jump',
            4: 'punch',
            5: 'kick',
            6: 'block',
            7: 'move_left_block',
            8: 'move_right_block',
            9: 'projectile'
        }

        # Fallback to dummy AI if RL not available
        self.fallback_ai = DummyAI()

        if policy_path and TORCH_AVAILABLE:
            self.load_policy(policy_path)
        elif not TORCH_AVAILABLE:
            print("Using fallback rule-based AI (PyTorch not available)")

    def load_policy(self, policy_path):
        """Load trained policy from file"""
        if not TORCH_AVAILABLE:
            print("Cannot load RL policy - PyTorch not available")
            return False

        try:
            # Handle relative paths from game directory
            if not os.path.isabs(policy_path):
                # Try relative to training directory
                training_path = os.path.join(os.path.dirname(__file__), '..', '..', 'training', policy_path)
                if os.path.exists(training_path):
                    policy_path = training_path
                else:
                    # Try relative to current directory
                    if not os.path.exists(policy_path):
                        print(f"Policy file not found: {policy_path}")
                        return False

            checkpoint = torch.load(policy_path, map_location='cpu')
            self.policy = FighterPolicy()
            self.policy.load_state_dict(checkpoint['model_state_dict'])
            self.policy.eval()
            print(f"✅ Loaded RL policy from {policy_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to load policy: {e}")
            self.policy = None
            return False

    def get_state_vector(self, fighter, opponent):
        """Convert game state to ML format with mirroring"""
        # Determine if we need to mirror (player is on the right)
        if fighter.x > opponent.x:
            mirror = True
        else:
            mirror = False

        # Build state with consistent perspective (player on left, opponent on right)
        if mirror:
            # Mirror positions and velocities
            player_x = 1.0 - (fighter.x / config.STAGE_WIDTH)
            opponent_x = 1.0 - (opponent.x / config.STAGE_WIDTH)
            player_vel_x = -fighter.velocity_x / config.FIGHTER_SPEED
            opponent_vel_x = -opponent.velocity_x / config.FIGHTER_SPEED
            relative_x = (opponent_x - player_x)  # opponent relative to player
        else:
            # Normal positions
            player_x = fighter.x / config.STAGE_WIDTH
            opponent_x = opponent.x / config.STAGE_WIDTH
            player_vel_x = fighter.velocity_x / config.FIGHTER_SPEED
            opponent_vel_x = opponent.velocity_x / config.FIGHTER_SPEED
            relative_x = (opponent_x - player_x)  # opponent relative to player

        state = [
            # Player state (always "on the left" in representation)
            player_x,
            fighter.y / config.STAGE_HEIGHT,
            fighter.health / 100.0,
            player_vel_x,
            float(fighter.is_grounded),
            float(fighter.is_attacking),
            float(fighter.is_blocking),
            fighter.attack_cooldown / config.ATTACK_COOLDOWN,
            # Projectile state for player
            fighter.projectile_cooldown / config.PROJECTILE_COOLDOWN,
            float(fighter.is_charging_projectile),
            fighter.charging_orb.get_charge_percent() if fighter.charging_orb else 0.0,

            # Opponent state (always "on the right" in representation)
            opponent_x,
            opponent.y / config.STAGE_HEIGHT,
            opponent.health / 100.0,
            opponent_vel_x,
            float(opponent.is_grounded),
            float(opponent.is_attacking),
            float(opponent.is_blocking),
            opponent.attack_cooldown / config.ATTACK_COOLDOWN,
            # Projectile state for opponent
            opponent.projectile_cooldown / config.PROJECTILE_COOLDOWN,
            float(opponent.is_charging_projectile),
            opponent.charging_orb.get_charge_percent() if opponent.charging_orb else 0.0,

            # Relative information (opponent relative to player)
            abs(relative_x),  # Distance (always positive)
            relative_x,       # Relative position (positive = opponent to right)
            (opponent.y - fighter.y) / config.STAGE_HEIGHT,  # Height difference
            (fighter.health - opponent.health) / 100.0,      # Health advantage
        ]
        return np.array(state, dtype=np.float32)

    def update_fighter(self, fighter, opponent, audio_manager=None):
        """Main update method - uses RL policy or falls back to rule-based"""
        if self.policy is None:
            # Fallback to rule-based AI
            self.fallback_ai.update_fighter(fighter, opponent, audio_manager)
            return

        # Get current state
        state = self.get_state_vector(fighter, opponent)

        # Get action from policy
        action_idx = self.policy.get_action(state, deterministic=False)
        action_name = self.action_mapping[action_idx]

        # Debug: Print action occasionally (every 60 frames = 1 second)
        if not hasattr(self, 'debug_counter'):
            self.debug_counter = 0
        self.debug_counter += 1

        if self.debug_counter % 60 == 0 and not config.TRAINING_MODE:
            print(f"AI Action: {action_name} (action_idx: {action_idx})")

        # Apply personality modifications (if any)
        action_name = self._apply_personality(action_name, state, fighter, opponent)

        # Execute action
        self._execute_action(action_name, fighter, audio_manager)

    def _apply_personality(self, action, state, fighter, opponent):
        """Modify action based on personality traits (future enhancement)"""
        if not self.personality:
            return action

        # Example personality modifications (can be expanded)
        aggression = self.personality.get('aggression', 0.5)
        defensiveness = self.personality.get('defensiveness', 0.5)

        # Aggressive personality: more likely to attack
        if aggression > 0.7 and action == 'idle':
            distance = abs(fighter.x - opponent.x)
            if distance < 100:  # Close range
                return random.choice(['punch', 'kick'])

        # Defensive personality: more likely to block
        if defensiveness > 0.7 and opponent.is_attacking and action in ['punch', 'kick']:
            return 'block'

        return action

    def _execute_action(self, action, fighter, audio_manager):
        """Execute the chosen action"""
        if action == 'move_left':
            fighter.move_left(audio_manager)
        elif action == 'move_right':
            fighter.move_right(audio_manager)
        elif action == 'jump':
            fighter.jump(audio_manager)
        elif action == 'punch':
            fighter.punch(audio_manager)
        elif action == 'kick':
            fighter.kick(audio_manager)
        elif action == 'block':
            fighter.block()
        elif action == 'move_left_block':
            fighter.move_left(audio_manager)
            fighter.block()
        elif action == 'move_right_block':
            fighter.move_right(audio_manager)
            fighter.block()
        elif action == 'projectile':
            # Simple projectile for AI - just fire immediately if possible
            if fighter.can_charge_projectile():
                fighter.start_charging_projectile()
                # For AI, immediately fire a quick projectile (minimal charge)
                if fighter.charging_orb:
                    # Give it a tiny bit of charge time for visual consistency
                    fighter.charging_orb.charge_time = 5  # Small charge
                    projectile = fighter.stop_charging_projectile(audio_manager)
                    # Note: Projectile would be handled by game engine in full game
        # 'idle' does nothing
