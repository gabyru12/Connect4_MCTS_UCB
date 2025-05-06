import random
import pandas as pd
from copy import deepcopy
from tqdm import tqdm
import mcts_ucb as mcts
import connect4API as connect4
import math

C0 = math.sqrt(2)
iterations0 = 10000
resetTree0 = True
drawValue0 = 0

def checkPlayerWon(self, player: str) -> bool:
    #horizontal
    for row in range(self.MAX_ROWS - 1, -1, -1):
        for col in range(self.MAX_COLS - 3):
            if(self.state[row][col] == player and self.state[row][col+1] == player and self.state[row][col+2] == player and self.state[row][col+3] == player):
                return True

    #vertical
    for col in range(self.MAX_COLS - 1, -1, -1):
        for row in range(self.MAX_ROWS - 3):
            if(self.state[row][col] == player and self.state[row+1][col] == player and self.state[row+2][col] == player and self.state[row+3][col] == player):
                return True

    #diagonal
    for row in range(self.MAX_ROWS - 1, 2, -1):
        for col in range(self.MAX_COLS - 3):
            if(self.state[row][col] == player and self.state[row-1][col+1] == player and self.state[row-2][col+2] == player and self.state[row-3][col+3] == player):
                return True

    #anti diagonal
    for row in range(self.MAX_ROWS - 3):
        for col in range(self.MAX_COLS - 3):
            if(self.state[row][col] == player and self.state[row+1][col+1] == player and self.state[row+2][col+2] == player and self.state[row+3][col+3] == player):
                return True

    return False

def checkTie(self) -> bool:
    for row in range(self.MAX_ROWS):
        for col in range(self.MAX_COLS):
            if self.state[row][col] == "-":
                return False
    return True

def checkGameOver(self) -> bool:
        return self.checkPlayerWon("O") or self.checkPlayerWon("X") or self.checkTie()

# Assumimos que você já tem estas funções:
# is_terminal(board) -> bool
# run_mcts(board, num_simulations) -> str  # retorna: 'win', 'lost', 'draw'

connect = connect4.Connect4(6, 7)
ROWS = 6
COLS = 7
MAX_MOVES = ROWS * COLS

# Distribuição sugerida
CATEGORY_LIMITS = {
    "early": (4, 14),   # evitamos jogos com menos de 4 peças
    "mid": (15, 28),
    "final": (29, 41)   # até 41 para garantir que não é empate (42)
}

STATES_PER_CATEGORY = 10000
TOTAL_STATES = STATES_PER_CATEGORY * 3

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

def generate_dataset(mcts=mcts.MctsAlgo(C0,resetTree0,drawValue0)):
    dataset = []
    for category, (min_moves, max_moves) in CATEGORY_LIMITS.items():
        print(f"Generating {category} states...")
        count = 0
        while count < STATES_PER_CATEGORY:
            num_moves = random.randint(min_moves, max_moves)
            board,turn = generate_valid_board(num_moves)
            connect.getIntoDesiredState(turn, gameState=board)

            if checkGameOver(board):  # IGNORA estados terminados
                continue

            # MCTS para determinar resultado provável
            mcts.run_mcts(iterations0, connect, move)
            bestMove = mcts.choose_best_move()

            flat_board = flatten_board(board)
            flat_board.append(result)
            dataset.append(flat_board)
            count += 1
    return dataset

def save_to_excel(dataset, filename="connect4_dataset.xlsx"):
    col_names = [f"cell_{i}" for i in range(42)] + ["result"]
    df = pd.DataFrame(dataset, columns=col_names)
    df.to_excel(filename, index=False)
    print(f"Dataset salvo como {filename}")

# Executar geração
if __name__ == "__main__":
    all_states = generate_dataset()
    save_to_excel(all_states)