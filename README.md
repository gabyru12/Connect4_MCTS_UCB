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
- **Decision Tree vs AI**: Given a generated dataset, this Descision Tree will learn from it and play against the MCTS AI, 1000x faster
- **Benchmarking**: Benchmark different AI configurations and save results for analysis.

## Project Structure

- **src/jupyter_presentation/jupyter_presentation.ipynb**: Jupyter notebook with Cython-accelerated Connect4 logic, MCTS implementation, and interactive experiments.
- **src/development_files/connect4API.pyx**: Cython implementation of the Connect4 board and game logic.
- **src/development_files/mcts_ucb.py**: Python implementation of the MCTS algorithm with UCB.
- **src/development_files/main.py**: Entry point for running the game, AI matches, and benchmarking from the command line.
- **src/development_files/[MULTIPROCESSING]generateConnect4Data.py**: Generate random boards for early, mid and late stages, and apply mcts to get the best move.
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
- Datasets can be generated using MCTS without or with softmax + datasets can also be generate creating random boards and applying MCTS to them.
- Datasets are saved as CSV files in the `datasets/` folder.

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
    cd other_version/development_files/src
    python setup.py build_ext --inplace
    ```

## Usage

### Play the Game
Run the main script and select a mode:
```bash
python other_version/src/development_files/main.py
```
You will be prompted to choose between User vs AI, AI vs User, AI vs AI, DT vs AI or Benchmarking.

### Generate Datasets
- To create a dataset with randomly generated boards:
    ```bash
    python other_version/src/development_files/[MULTIPROCESSING]generateConnect4Data.py
    ```
- To create a dataset generated while two mcts AI play against each other
    To activate softmax make sure that in the configs file activateSoftmax = True
    ```bash
    python other_version/src/development_files/main.py
    ```

### Benchmarking
- Select option 5 in the main script to run concurrent AI vs AI matches and save results to a CSV file.

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
- [src/development_files/connect4API.pyx](other_version/src/development_files/connect4API.pyx)
- [src/development_files/mcts_ucb.py](other_version/src/development_files/mcts_ucb.py)
- [src/development_files/main.py](other_version/src/development_files/main.py)
- [src/development_files/[MULTIPROCESSING]generateConnect4Data.py](other_version/src/development_files/[MULTIPROCESSING]generateConnect4Data.py)
- [configs/configs.txt](other_version/configs/configs.txt)
