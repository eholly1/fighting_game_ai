#!/usr/bin/env python3
"""
Performance benchmarking for fighting game AI components
"""
import time
import numpy as np
from environment import FightingGameEnv
from models import SimplePolicy, FighterPolicy
import torch

def benchmark_performance():
    print('🔍 Performance Benchmarking:')
    print('=' * 50)

    # Setup
    env = FightingGameEnv(headless=True)
    rule_based = SimplePolicy('medium')

    # Load neural network policy
    try:
        nn_policy = FighterPolicy()
        checkpoint = torch.load('experiments/long_training_100M_001/policies/policy_step_92502016_step_92502016.pth', map_location='cpu')
        nn_policy.load_state_dict(checkpoint['model_state_dict'])
        nn_policy.eval()
        print('✅ Loaded neural network policy')
        nn_available = True
    except Exception as e:
        print(f'❌ Could not load neural network policy: {e}')
        nn_policy = None
        nn_available = False

    # Benchmark environment step time
    print('\n1. Environment Step Time:')
    state = env.reset()
    times = []
    for i in range(1000):
        start = time.time()
        next_state, reward, done, info = env.step(0, 0)  # Both idle
        times.append(time.time() - start)
        if done:
            state = env.reset()
        else:
            state = next_state

    env_step_time = np.mean(times) * 1000  # Convert to milliseconds
    print(f'  Average step time: {env_step_time:.3f} ms')

    # Benchmark rule-based inference
    print('\n2. Rule-Based AI Inference:')
    state = env.reset()
    times = []
    for i in range(1000):
        start = time.time()
        action = rule_based.get_action(state)
        times.append(time.time() - start)

    rule_inference_time = np.mean(times) * 1000
    print(f'  Average inference time: {rule_inference_time:.3f} ms')

    # Benchmark neural network inference
    if nn_available:
        print('\n3. Neural Network Inference:')
        state = env.reset()
        times = []
        for i in range(1000):
            start = time.time()
            action = nn_policy.get_action(state, deterministic=True)
            times.append(time.time() - start)
        
        nn_inference_time = np.mean(times) * 1000
        print(f'  Average inference time: {nn_inference_time:.3f} ms')
    else:
        nn_inference_time = 0

    # Summary
    print('\n📊 Performance Summary:')
    print(f'  Environment step: {env_step_time:.3f} ms')
    print(f'  Rule-based AI:   {rule_inference_time:.3f} ms')
    if nn_available:
        print(f'  Neural network:   {nn_inference_time:.3f} ms')

    print('\n🎯 Bottleneck Analysis:')
    total_rule = env_step_time + 2 * rule_inference_time
    if nn_available:
        total_nn = env_step_time + rule_inference_time + nn_inference_time
        print(f'  Rule vs Rule:     {total_rule:.3f} ms per step')
        print(f'  NN vs Rule:       {total_nn:.3f} ms per step')
        print(f'  NN overhead:      {((total_nn/total_rule - 1) * 100):.1f}%')
    else:
        print(f'  Rule vs Rule:     {total_rule:.3f} ms per step')

    # Games per second calculation
    print('\n⚡ Throughput Analysis:')
    steps_per_game = 3600  # Max game length
    print(f'  Rule vs Rule:     {1000 / (total_rule * steps_per_game):.2f} games/second')
    if nn_available:
        print(f'  NN vs Rule:       {1000 / (total_nn * steps_per_game):.2f} games/second')

    env.close()

if __name__ == "__main__":
    benchmark_performance()
