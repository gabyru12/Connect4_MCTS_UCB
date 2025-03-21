MAX_ROWS = 7
MAX_COLS = 8

#correct
def empty_board():
    board = [[] for _ in range(MAX_ROWS)]
    for row in range(MAX_ROWS):
        for col in range(MAX_COLS):
            board[row].append("-")
    return board

#correct
def create_new_board(new_board):
    board = empty_board()
    for row in range(MAX_ROWS):
        for col in range(MAX_COLS):
            board[row][col] = new_board[row][col]
    return board

#correct
def check_win(board, player):
    # Check horizontal
    for row in range(MAX_ROWS):
        for col in range(MAX_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True
    # Check vertical
    for row in range(MAX_ROWS - 3):
        for col in range(MAX_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True
    # Check diagonal
    for row in range(MAX_ROWS - 3):
        for col in range(MAX_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True
    for row in range(3, MAX_ROWS):
        for col in range(MAX_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True
    return False

#correct
def check_tie(board):
    for col in range(MAX_COLS):
        if board[0][col] == "-":
            return False
    return True

#correct
def check_game_over(board):
    return check_win(board, player="X") or check_tie(board) or check_win(board, player="O")

#correct
def move(board, col, player):
    for row in range(MAX_ROWS - 1, -1, -1):
        if board[row][col-1] == "-":
            board[row][col-1] = player
            return True
    return False

#correct
def get_valid_moves(board):
    valid_moves = []
    for col in range(MAX_COLS):
        if board[0][col] == "-":
            valid_moves.append(col+1) 
    return valid_moves

#correct
def get_next_state(board, col, player):
    new_board = create_new_board(board)
    move(new_board, col, player)
    return new_board

def get_current_player(board):
    x_count = 0
    o_count = 0
    for row in range(MAX_ROWS):
        for col in range(MAX_COLS):
            if board[row][col] == "X":
                x_count += 1
            elif board[row][col] == "O":
                o_count += 1
    if x_count == o_count:
        return "X"
    return "O"

#correct
def get_winner(board):
    if check_win(board, "X"):
        return "X"
    if check_win(board, "O"):
        return "O"
    return None

#correct
def get_board_string(board):
    board_string = ""
    for row in range(MAX_ROWS):
        for col in range(MAX_COLS):
            board_string += board[row][col]
        board_string += "\n"
    return board_string

new_board = [['-', '-', '-', '-', '-', '-', '-'],
['-', '-', '-', '-', '-', '-', '-'],
['-', '-', '-', '-', '-', '-', '-'],
['-', '-', '-', '-', '-', '-', '-'],
['-', '-', '-', '-', 'O', '-', '-'],
['-', '-', '-', 'X', 'O', '-', '-'],
['-', '-', '-', 'X', '-', '-', '-']]