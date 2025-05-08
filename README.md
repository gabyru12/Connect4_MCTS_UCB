# Connect4 with Monte Carlo Tree Search (MCTS) and UCB

## Overview
This project is an implementation of the classic Connect4 game, enhanced with an AI player powered by **Monte Carlo Tree Search (MCTS)** and the **Upper Confidence Bound (UCB)** algorithm. The AI uses advanced reinforcement learning techniques to play optimally against human players or other AI opponents by simulating many games to choose the highest win-rate path.

## Features
- **Interactive Gameplay**: Play Connect4 against the AI, another human player, or let two AIs play against each other.
- **AI with MCTS and UCB**: The AI uses Monte Carlo simulations and UCB to evaluate the best moves.
- **Configurable AI**: Adjust parameters like exploration constant, number of iterations, and tie handling to customize AI behavior.
- **Concurrent AI Matches**: Run multiple AI vs. AI matches concurrently using multiprocessing.
- **Dataset Generation**: Generate datasets for Connect4 game states using MCTS for training or analysis.

## How It Works
1. **Monte Carlo Tree Search (MCTS)**:
   - Simulates multiple random games from the current state.
   - Uses the results of these simulations to estimate the value of each possible move.
2. **Upper Confidence Bound (UCB)**:
   - Balances exploration (trying new moves) and exploitation (choosing moves with known good results).
   - Ensures the AI efficiently explores the game tree.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/gabyru12/Connect4_MCTS_UCB.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Connect4_MCTS_UCB
    ```

## Usage
1. Run the game:
    ```bash
    python main.py
    ```

2. Generate datasets:
    Open the `generateConnect4Data.ipynb` notebook and execute the cells to generate datasets for early, mid, or late game states.

## Project Structure
- **src/main.py**: Entry point for the game, allowing different game modes (User vs AI, AI vs User, AI vs AI).
- **src/mcts_ucb.py**: Implementation of the Monte Carlo Tree Search algorithm with UCB.
- **src/connect4API.py**: Implementation of the Connect4 game logic and board management.
- **src/generateConnect4Data.ipynb**: Notebook for generating datasets using MCTS.
- **configs/configs.txt**: Configuration file for AI parameters and game settings.
- **ideas/**: Contains notes and experiments for future improvements.

## Future Improvements
- Add a graphical interface for better user experience.
- Optimize AI performance for faster decision-making.
- Implement additional difficulty levels for AI:
    - AI starts MCTS from the root node vs. the current game state.
    - AI with more time for simulations.
- Visualize the MCTS tree structure during gameplay.
- Explore adaptive exploration constants for different game phases.