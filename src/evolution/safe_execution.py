#!/usr/bin/env python3
"""
Safe Execution Environment for Evolutionary Agents

Provides isolated execution of LLM-generated agent code with
timeout protection, resource limits, and error handling.
"""
import signal
import sys
import time
import traceback
import numpy as np
from typing import Any, Dict, Optional, Callable
from contextlib import contextmanager

class TimeoutError(Exception):
    """Raised when code execution times out"""
    pass

class SafeExecutionError(Exception):
    """Raised when safe execution fails"""
    pass

class SafeAgent:
    """
    Safely executes LLM-generated agent code with protection mechanisms
    """

    def __init__(self, agent_id: str, code: str, timeout_seconds: float = 1.0):
        """
        Initialize safe agent

        Args:
            agent_id: Unique identifier for the agent
            code: Validated Python code string
            timeout_seconds: Maximum execution time per action
        """
        self.agent_id = agent_id
        self.code = code
        self.timeout_seconds = timeout_seconds

        # Execution statistics
        self.total_calls = 0
        self.total_errors = 0
        self.total_timeouts = 0
        self.avg_execution_time = 0.0
        self.is_disabled = False

        # Compile the agent code
        self.get_action_func = None
        self._compile_agent()

    def _compile_agent(self):
        """Compile agent code into executable function"""
        try:
            # Create safe execution environment
            safe_globals = self._create_safe_globals()

            # Execute the code to define functions
            exec(self.code, safe_globals)

            # Extract the get_action function
            if 'get_action' in safe_globals:
                self.get_action_func = safe_globals['get_action']
                print(f"✅ Agent {self.agent_id} compiled successfully")
            else:
                raise SafeExecutionError("No get_action function found")

        except Exception as e:
            print(f"❌ Agent {self.agent_id} compilation failed: {e}")
            self.is_disabled = True
            self.get_action_func = None

    def get_action(self, state: np.ndarray) -> int:
        """
        Safely execute agent's get_action function

        Args:
            state: Game state vector

        Returns:
            Action integer (0-9), defaults to 0 on error
        """
        if self.is_disabled or self.get_action_func is None:
            return 0

        self.total_calls += 1

        try:
            start_time = time.time()

            # Execute with timeout protection
            with self._timeout_context(self.timeout_seconds):
                action = self.get_action_func(state)

            execution_time = time.time() - start_time
            self._update_timing_stats(execution_time)

            # Validate and return action
            return self._validate_action(action)

        except TimeoutError:
            self.total_timeouts += 1
            self._handle_timeout()
            return 0

        except Exception as e:
            self.total_errors += 1
            self._handle_error(e)
            return 0

    def _create_safe_globals(self) -> Dict[str, Any]:
        """Create restricted global environment for code execution"""
        import numpy as np
        import random
        import math

        # Restricted builtins
        safe_builtins = {
            # Basic types
            'int': int,
            'float': float,
            'bool': bool,
            'str': str,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,

            # Basic functions
            'len': len,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'round': round,
            'sorted': sorted,
            'reversed': reversed,
            'pow': pow,

            # Type checking
            'isinstance': isinstance,
            'type': type,

            # Safe exceptions
            'Exception': Exception,
            'ValueError': ValueError,
            'TypeError': TypeError,
            'IndexError': IndexError,
            'KeyError': KeyError,

            # Import functionality (needed for agent code)
            '__import__': __import__,
        }

        return {
            '__builtins__': safe_builtins,
            'np': np,
            'numpy': np,
            'random': random,
            'math': math,
        }

    @contextmanager
    def _timeout_context(self, seconds: float):
        """Context manager for timeout protection"""
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Agent {self.agent_id} execution timed out after {seconds}s")

        # Set up signal handler (Unix/Linux/Mac only)
        if hasattr(signal, 'SIGALRM'):
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)

            try:
                yield
            finally:
                signal.alarm(0)  # Cancel the alarm
                signal.signal(signal.SIGALRM, old_handler)
        else:
            # Fallback for Windows (no signal support)
            # Use simple time-based check (less precise)
            start_time = time.time()
            yield
            if time.time() - start_time > seconds:
                raise TimeoutError(f"Agent {self.agent_id} execution took too long")

    def _validate_action(self, action: Any) -> int:
        """Validate and normalize action output"""
        try:
            # Convert to integer
            if isinstance(action, (int, float, np.integer, np.floating)):
                action_int = int(action)
                # Clamp to valid range
                return max(0, min(9, action_int))
            else:
                # Invalid type, return idle
                return 0
        except (ValueError, TypeError):
            return 0

    def _update_timing_stats(self, execution_time: float):
        """Update execution timing statistics"""
        if self.total_calls == 1:
            self.avg_execution_time = execution_time
        else:
            # Running average
            alpha = 0.1  # Smoothing factor
            self.avg_execution_time = (alpha * execution_time +
                                     (1 - alpha) * self.avg_execution_time)

    def _handle_timeout(self):
        """Handle timeout errors"""
        if self.total_timeouts > 10:
            print(f"⚠️  Agent {self.agent_id} disabled due to excessive timeouts")
            self.is_disabled = True

    def _handle_error(self, error: Exception):
        """Handle execution errors"""
        # Only print first few errors to avoid spam
        if self.total_errors <= 3:
            print(f"⚠️  Agent {self.agent_id} error: {error}")

        # Disable agent if too many errors
        if self.total_errors > 20:
            print(f"❌ Agent {self.agent_id} disabled due to excessive errors")
            self.is_disabled = True

    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return {
            'agent_id': self.agent_id,
            'total_calls': self.total_calls,
            'total_errors': self.total_errors,
            'total_timeouts': self.total_timeouts,
            'error_rate': self.total_errors / max(1, self.total_calls),
            'timeout_rate': self.total_timeouts / max(1, self.total_calls),
            'avg_execution_time': self.avg_execution_time,
            'is_disabled': self.is_disabled
        }

    @property
    def is_valid(self) -> bool:
        """Check if agent is valid and can execute"""
        return not self.is_disabled and self.get_action_func is not None

class AgentPool:
    """
    Manages a pool of safe agents with monitoring and cleanup
    """

    def __init__(self):
        self.agents: Dict[str, SafeAgent] = {}
        self.creation_time = time.time()

    def add_agent(self, agent_id: str, code: str, timeout_seconds: float = 1.0) -> bool:
        """
        Add a new agent to the pool

        Returns:
            True if agent was successfully added, False otherwise
        """
        try:
            agent = SafeAgent(agent_id, code, timeout_seconds)
            if agent.is_valid:
                self.agents[agent_id] = agent
                return True
            else:
                print(f"❌ Failed to add invalid agent {agent_id}")
                return False
        except Exception as e:
            print(f"❌ Failed to create agent {agent_id}: {e}")
            return False

    def get_agent(self, agent_id: str) -> Optional[SafeAgent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)

    def remove_agent(self, agent_id: str):
        """Remove agent from pool"""
        if agent_id in self.agents:
            del self.agents[agent_id]

    def get_valid_agents(self) -> Dict[str, SafeAgent]:
        """Get all valid (non-disabled) agents"""
        return {aid: agent for aid, agent in self.agents.items() if agent.is_valid}

    def cleanup_invalid_agents(self):
        """Remove disabled agents from pool"""
        invalid_agents = [aid for aid, agent in self.agents.items() if not agent.is_valid]
        for agent_id in invalid_agents:
            print(f"🧹 Removing invalid agent {agent_id}")
            del self.agents[agent_id]

    def get_pool_stats(self) -> Dict[str, Any]:
        """Get statistics for the entire agent pool"""
        valid_agents = self.get_valid_agents()

        if not self.agents:
            return {'total_agents': 0, 'valid_agents': 0}

        all_stats = [agent.get_stats() for agent in self.agents.values()]

        return {
            'total_agents': len(self.agents),
            'valid_agents': len(valid_agents),
            'avg_error_rate': np.mean([s['error_rate'] for s in all_stats]),
            'avg_timeout_rate': np.mean([s['timeout_rate'] for s in all_stats]),
            'avg_execution_time': np.mean([s['avg_execution_time'] for s in all_stats]),
            'pool_uptime': time.time() - self.creation_time
        }

def test_safe_execution():
    """Test the safe execution system"""
    print("🧪 Testing Safe Execution System")
    print("=" * 50)

    # Test 1: Valid agent
    valid_code = """
def get_action(state):
    distance = state[22]
    if distance < 0.3:
        return 4  # punch
    else:
        return 2  # move right
"""

    agent = SafeAgent("test_valid", valid_code)
    test_state = np.zeros(26)
    test_state[22] = 0.2  # Close distance

    action = agent.get_action(test_state)
    print(f"Valid agent test: {'✅ PASS' if action == 4 else '❌ FAIL'} (action: {action})")

    # Test 2: Timeout protection
    timeout_code = """
def get_action(state):
    import time
    time.sleep(2)  # This should timeout
    return 0
"""

    timeout_agent = SafeAgent("test_timeout", timeout_code, timeout_seconds=0.1)
    start_time = time.time()
    action = timeout_agent.get_action(test_state)
    duration = time.time() - start_time

    print(f"Timeout test: {'✅ PASS' if duration < 0.5 and action == 0 else '❌ FAIL'} (duration: {duration:.2f}s)")

    # Test 3: Error handling
    error_code = """
def get_action(state):
    return state[100]  # Index error
"""

    error_agent = SafeAgent("test_error", error_code)
    action = error_agent.get_action(test_state)
    print(f"Error handling test: {'✅ PASS' if action == 0 else '❌ FAIL'} (action: {action})")

    # Test 4: Agent pool
    pool = AgentPool()
    pool.add_agent("agent1", valid_code)
    pool.add_agent("agent2", error_code)

    stats = pool.get_pool_stats()
    print(f"Agent pool test: {'✅ PASS' if stats['total_agents'] == 2 else '❌ FAIL'}")

    print(f"\n📊 Safe Execution Tests Complete")

if __name__ == "__main__":
    test_safe_execution()
