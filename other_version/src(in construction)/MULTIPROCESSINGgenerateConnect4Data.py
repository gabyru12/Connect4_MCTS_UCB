import random
import pandas as pd
from copy import deepcopy
from mcts_ucb import MctsAlgo, Node
from connect4API import Connect4
import math
import time
import os
from multiprocessing import Manager, Process, Queue
from tqdm import tqdm  # Add tqdm for the main progress bar

# Constants
C0 = math.sqrt(2)
iterations0 = 15000
resetTree0 = True
drawValue0 = 0

ROWS = 6
COLS = 7

GAMESTATES = {
    "early": (4, 14),
    "mid": (15, 28),
    "late": (29, 41)
}

ITERATIONS_PER_GAMESTATE = 3330

# === Helpers ===
def create_empty_board() -> list[list[str]]:
    return [['-' for _ in range(COLS)] for _ in range(ROWS)]

def make_random_move(board: list[list[str]], col: int, player: str) -> bool:
    for row in reversed(range(ROWS)):
        if board[row][col] == '-':
            board[row][col] = player
            return True
    return False

def generate_valid_board(num_moves: int) -> (list[list[str]], str):
    board = create_empty_board()
    current_player = 'O'
    move_count = 0
    while move_count < num_moves:
        col = random.randint(0, COLS - 1)
        if make_random_move(board, col, current_player):
            move_count += 1
            current_player = 'X' if current_player == 'O' else 'O'
    return board, current_player

def flatten_board(board: list[list[str]]) -> list[str]:
    return [cell for row in board for cell in row]

def save_to_csv(dataset: list[list[str]], saveFor: str):
    col_names = [f"cell_{i}" for i in range(42)] + ["result"]
    df = pd.DataFrame(dataset, columns=col_names)
    csv_path = f'other_version/datasets/connect4_{saveFor}.csv'
    df.to_csv(csv_path, index=False)
    print(f"\nDataset saved as connect4_{saveFor}.csv")

# === Dataset Generation (child process) ===
def generate_dataset(createFor: str, iterations: int, sendTo, progress_queue) -> None:
    dataset = []
    mcts = MctsAlgo(C=C0, reset=resetTree0, drawValue=drawValue0, speed="fast")
    connect4 = Connect4(6, 7)
    count = 0
    min_moves, max_moves = GAMESTATES[createFor]

    while count < iterations:
        num_moves = random.randint(min_moves, max_moves)
        board, turn = generate_valid_board(num_moves)
        connect4.getIntoDesiredState(turn, gameState=board)

        if connect4.checkGameOver(speed="slow"):
            continue

        mcts.run_mcts(iterations0, connect4)
        bestMove = str(mcts.choose_best_move())

        flat_board = flatten_board(board)
        flat_board.append(bestMove)
        dataset.append(flat_board)

        # Report progress to the main process
        if progress_queue:
            progress_queue.put(1)

        count += 1

    sendTo.extend(dataset)

# === Multiprocess Controller ===
def generate_dataset_multiprocess(process_count: int, createFor: str):
    iterations_per_process = ITERATIONS_PER_GAMESTATE // process_count

    manager = Manager()
    return_list = manager.list()
    progress_queue = Queue()

    processes = []
    for _ in range(process_count):
        process = Process(
            target=generate_dataset,
            args=(createFor, iterations_per_process, return_list, progress_queue)
        )
        processes.append(process)
        process.start()

    # Show progress in the main process
    with tqdm(total=ITERATIONS_PER_GAMESTATE, desc="Generating Dataset") as pbar:
        completed = 0
        while completed < ITERATIONS_PER_GAMESTATE:
            progress_queue.get()
            completed += 1
            pbar.update(1)

    for process in processes:
        process.join()

    combined_dataset = list(return_list)
    flattened_dataset = [inner for outer in combined_dataset for inner in outer]
    save_to_csv(combined_dataset, saveFor=createFor)

# === Entry Point ===
if __name__ == '__main__':
    #generate_dataset_early_multiprocess(process_count=5, createFor="early")
    generate_dataset_early_multiprocess(process_count=5, createFor="mid")
    #generate_dataset_multiprocess(process_count=5, createFor="late")
