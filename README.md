# Connect4 with Monte Carlo Tree Search (MCTS) and UCB

## Overview
This project is an implementation of the classic Connect4 game, enhanced with an AI player powered by **Monte Carlo Tree Search (MCTS)** and the **Upper Confidence Bound (UCB)** algorithm. The AI uses advanced reinforcement learning techniques to play optimally against human players or other AI opponents by simulating many games to choose the highest win-rate path.

## Features
- **Interactive Gameplay**: Play Connect4 against the AI, another human player, or let two AIs play against each other.
- **AI with MCTS and UCB**: The AI uses Monte Carlo simulations and UCB to evaluate the best moves.
- **Cython-Accelerated Connect4**: The Connect4 game logic is implemented in Cython for high performance.
- **Configurable AI**: Adjust parameters like exploration constant, number of iterations, and tie handling to customize AI behavior.
- **Concurrent AI Matches**: Run multiple AI vs. AI matches concurrently using multiprocessing.
- **Dataset Generation**: Generate datasets for Connect4 game states using MCTS for training or analysis.
- **Benchmarking**: Benchmark different AI configurations and save results for analysis.

## Project Structure

- **src/jupyter_presentation/jupyter_presentation.ipynb**: Jupyter notebook with Cython-accelerated Connect4 logic, MCTS implementation, and interactive experiments.
- **src/connect4API.pyx**: Cython implementation of the Connect4 board and game logic.
- **src/mcts_ucb.py**: Python implementation of the MCTS algorithm with UCB.
- **src/main.py**: Entry point for running the game, AI matches, and benchmarking from the command line.
- **src/[INDIVIDUAL]generateConnect4Data.ipynb**: Notebook for generating datasets using MCTS.
- **src/[MULTIPROCESSING]generateConnect4Data.py**: Script for fast, multiprocessed dataset generation.
- **configs/configs.txt**: Configuration file for AI parameters and game settings.
- **datasets/**: Folder for generated datasets.
- **ideas/**: Contains notes and experiments for future improvements.

## How It Works

### Connect4 Game Logic
- The Connect4 board is represented using two bitboards (one for each player) for efficient computation.
- The Cython class `Connect4` provides methods for updating the game state, checking for wins/ties, and converting between matrix and bitboard representations.
- The board is displayed in the terminal with colored pieces for each player.

### Monte Carlo Tree Search (MCTS)
- The `MctsAlgo` class implements the MCTS algorithm with UCB for move selection.
- The search tree is built dynamically as the AI simulates games, balancing exploration and exploitation.
- Tie results can be configured to count as win, loss, or custom value via the `drawValue` parameter.

### Game Modes
- **User vs AI**: Play against the AI, with the user moving first.
- **AI vs User**: Play against the AI, with the AI moving first.
- **AI vs AI**: Watch two AIs play against each other with different configurations.
- **Benchmarking**: Run multiple concurrent AI vs AI matches and save results for analysis.

### Dataset Generation
- Datasets can be generated for early, mid, and late game states using MCTS.
- Use the Jupyter notebook or the multiprocessing script to generate large datasets for training or research.
- Datasets are saved as CSV or Excel files in the `datasets/` folder.

### Configuration
- All AI parameters (exploration constant, number of iterations, tie value, etc.) are set in [other_version/configs/configs.txt](other_version/configs/configs.txt).
- The main script reads these settings and applies them to the AI and benchmarking routines.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/gabyru12/Connect4_MCTS_UCB.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Connect4_MCTS_UCB
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Build the Cython extension:
    ```bash
    cd other_version/src
    python setup.py build_ext --inplace
    ```

## Usage

### Play the Game
Run the main script and select a mode:
```bash
python other_version/src/main.py
```
You will be prompted to choose between User vs AI, AI vs User, AI vs AI, or Benchmarking.

### Generate Datasets
- Open [other_version/src/[INDIVIDUAL]generateConnect4Data.ipynb](other_version/src/[INDIVIDUAL]generateConnect4Data.ipynb) and execute the cells to generate datasets for early, mid, or late game states.
- Or run the multiprocessing script for faster generation:
    ```bash
    python other_version/src/[MULTIPROCESSING]generateConnect4Data.py
    ```

### Benchmarking
- Select option 4 in the main script to run concurrent AI vs AI matches and save results to a CSV file.

## Customization

- Edit [other_version/configs/configs.txt](other_version/configs/configs.txt) to change AI parameters, such as the exploration constant, number of iterations, and tie handling.
- You can experiment with different MCTS settings and observe their impact on gameplay and dataset generation.

## Future Improvements

- Add a graphical interface for better user experience.
- Optimize AI performance for faster decision-making.
- Implement additional difficulty levels for AI.
- Visualize the MCTS tree structure during gameplay.
- Explore adaptive exploration constants for different game phases.

## References

- [src/jupyter_presentation/jupyter_presentation.ipynb](other_version/src/jupyter_presentation/jupyter_presentation.ipynb)
- [src/connect4API.pyx](other_version/src/connect4API.pyx)
- [src/mcts_ucb.py](other_version/src/mcts_ucb.py)
- [src/main.py](other_version/src/main.py)
- [src/[INDIVIDUAL]generateConnect4Data.ipynb](other_version/src/[INDIVIDUAL]generateConnect4Data.ipynb)
- [src/[MULTIPROCESSING]generateConnect4Data.py](other_version/src/[MULTIPROCESSING]generateConnect4Data.py)
- [configs/configs.txt](other_version/configs/configs.txt)