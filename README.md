# Connect4 with Monte Carlo Tree Search (MCTS) and UCB

## Overview
This project is an implementation of the classic Connect4 game, enhanced with an AI player powered by **Monte Carlo Tree Search (MCTS)** and the **Upper Confidence Bound (UCB)** algorithm. The AI uses advanced reinforcement learning techniques to play optimally against human players or other AI opponents simulating many games in order to choose the highest win-rate path to beating the oposing player.

## Features
- **Interactive Gameplay**: Play Connect4 against the AI or another human player or let an AI play against another AI
- **AI with MCTS and UCB**: The AI uses Monte Carlo simulations and UCB to evaluate the best moves.
- **Scalable AI**: Adjust the time given to generate simulations for the AI to balance between performance and computation time.

## How It Works
1. **Monte Carlo Tree Search (MCTS)**:
   - Simulates multiple random games from the current state.
   - Uses the results of these simulations to estimate the value of each possible move.
2. **Upper Confidence Bound (UCB)**:
   - Balances exploration (trying new moves) and exploitation (choosing moves with known good results).
   - Ensures the AI efficiently explores the game tree.

## Installation
1. Clone the repository:
    git clone https://github.com/gabyru12/Connect4_MCTS_UCB.git

2. Navigate to the project directory:
    cd Connect4_MCTS_UCB

## Usage
1. Run the game
    python game.py

## Project Structure
- game.py: Entry point for the game
- mcts.py: Algorithm that implements the Monte Carlo Tree Search
- ConnectState.py: Implementation of the rules and board to play Connect4 

## Future Improvements (Destined for my project group)
- Add a graphical interface 
- Optimize AI
- Implement additional difficulty levels for AI:
    - AI inicia o mcts desde o root Node vs a partir do Node atual do jogo
    - AI com mais tempo para pensar
- Display the tree like structure of the AI