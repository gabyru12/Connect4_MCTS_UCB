from copy import deepcopy
class Connect4:
    def __init__(self, MAX_ROWS: int, MAX_COLS: int):
        self.MAX_ROWS = MAX_ROWS
        self.MAX_COLS = MAX_COLS
        self.turn = "X"
        self.state = [["-"] * self.MAX_COLS for row in range(self.MAX_ROWS)]

    def printState(self):
        print("==========================")
        for row in range(self.MAX_ROWS):
            for col in range(self.MAX_COLS - 1):
                print(f"{self.state[row][col]} | ", end="")
            print(f"{self.state[row][self.MAX_COLS-1]}")
        print("==========================")

    def reset(self, connect4ActualState: list[int], connect4ActualTurn: str):
        self.turn = connect4ActualTurn
        self.state = deepcopy(connect4ActualState)

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
        return self.checkPlayerWon("X") or self.checkPlayerWon("O") or self.checkTie()

    def checkGameResult(self):
        if self.checkTie():
            return "-"
        elif self.checkPlayerWon("X"):
            return "X"
        else:
            return "O"

    def checkAvailableMoves(self) -> list[int]:
        availableMoves = []
        for col in range(self.MAX_COLS):
            if self.state[0][col] == "-":
                availableMoves.append(col+1)
        return availableMoves

    def updateGameState(self, move: int) -> bool:
        if move < 1 or move > self.MAX_COLS:
            raise ValueError(f"Invalid move: {move}. Must be between 1 and {self.MAX_COLS}.")
        if self.state[0][move-1] != "-":
            raise ValueError(f"Column {move} is full.")
        for row in range(self.MAX_ROWS - 1, -1, -1):
            if self.state[row][move-1] == "-":
                self.state[row][move-1] = self.turn
                break
        self.turn = "O" if self.turn == "X" else "X"
        return True

    def getIntoDesiredState(self, turn: str, gameState: list[list[int]]):
        for row in range(self.MAX_ROWS):
            for col in range(self.MAX_COLS):
                self.state[row][col] = gameState[row][col]
        self.turn = turn
            

