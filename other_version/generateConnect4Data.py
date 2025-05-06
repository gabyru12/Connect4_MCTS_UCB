import random
import pandas as pd
from copy import deepcopy
from mcts_ucb import MctsAlgo, Node
from connect4API import Connect4
import math
import time

C0 = math.sqrt(2)
iterations0 = 2
resetTree0 = True
drawValue0 = 0

# Assumimos que você já tem estas funções:
# is_terminal(board) -> bool
# run_mcts(board, num_simulations) -> str  # retorna: 'win', 'lost', 'draw'

ROWS = 6
COLS = 7
MAX_MOVES = ROWS * COLS

# Distribuição sugerida
GAMESTATES = {
    "early": (4, 14),   # evitamos jogos com menos de 4 peças
    "mid": (15, 28),
    "final": (29, 41)   # até 41 para garantir que não é empate (42)
}

ITERATIONS_PER_GAMESTATE = 10000
TOTAL_ITERATIONS = ITERATIONS_PER_GAMESTATE * 3

def create_empty_board():
    return [['-' for _ in range(COLS)] for _ in range(ROWS)]

def make_random_move(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == '-':
            board[row][col] = player
            return True
    return False

def generate_valid_board(num_moves):
    board = create_empty_board()
    current_player = 'O'
    move_count = 0
    while move_count < num_moves:
        col = random.randint(0, COLS - 1)
        if make_random_move(board, col, current_player):
            move_count += 1
            current_player = 'X' if current_player == 'O' else 'O'
    return board, current_player

def flatten_board(board):
    return [cell for row in board for cell in row]

def generate_dataset():
    dataset = []
    mcts = MctsAlgo(C=C0, reset=resetTree0, drawValue=drawValue0)
    connect4 = Connect4(6, 7)
    for gamestate, (min_moves, max_moves) in GAMESTATES.items():
        print(f"Generating {gamestate} states...")
        count = 0
        while count < ITERATIONS_PER_GAMESTATE:
            print(f"{round(count/ITERATIONS_PER_GAMESTATE*100,2)}%")
            num_moves = random.randint(min_moves, max_moves)
            board,turn = generate_valid_board(num_moves)
            connect4.getIntoDesiredState(turn, gameState=board)

            if connect4.checkGameOver():  # IGNORA estados terminados
                continue

            # MCTS para determinar resultado provável
            mcts.run_mcts(iterations0, connect4)
            bestMove = mcts.choose_best_move()

            flat_board = flatten_board(board)
            flat_board.append(bestMove)
            dataset.append(flat_board)
            count += 1
        break
    return dataset

def save_to_excel(dataset, filename="connect4_dataset.xlsx"):
    col_names = [f"cell_{i}" for i in range(42)] + ["result"]
    df = pd.DataFrame(dataset, columns=col_names)
    df.to_excel(filename, index=False)
    print(f"Dataset salvo como {filename}")

# Executar geração
if __name__ == "__main__":
    start = time.time()
    all_states = generate_dataset()
    end = time.time()
    print(f"Run time: {round(end - start, 4)/60}m")
    save_to_excel(all_states)