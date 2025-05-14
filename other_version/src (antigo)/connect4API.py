from copy import deepcopy
import random
import time

class Connect4:
    def __init__(self, MAX_ROWS: int, MAX_COLS: int):
        self.MAX_ROWS = MAX_ROWS
        self.MAX_COLS = MAX_COLS
        self.turn = "O"
        self.state = [["-"] * self.MAX_COLS for row in range(self.MAX_ROWS)]
        self.lastMovementRow = None
        self.lastMovementCol = None

    def printState(self):
        print("===========================")
        for row in range(self.MAX_ROWS):
            for col in range(self.MAX_COLS - 1):
                if self.state[row][col] == "O":
                    print(f" \033[94m{self.state[row][col]}\033[0m |", end="")
                elif self.state[row][col] == "X":
                    print(f" \033[91m{self.state[row][col]}\033[0m |", end="")
                else:
                    print(f" {self.state[row][col]} |", end="")
            if self.state[row][self.MAX_COLS-1] == "O":
                print(f" \033[94m{self.state[row][self.MAX_COLS-1]}\033[0m")
            elif self.state[row][self.MAX_COLS-1] == "X":
                print(f" \033[91m{self.state[row][self.MAX_COLS-1]}\033[0m")
            else:
                print(f" {self.state[row][self.MAX_COLS-1]}")
        print("===========================")
        print(' 1 | 2 | 3 | 4 | 5 | 6 | 7 ')

    def reset(self, connect4ActualState: list[list[str]], connect4ActualTurn: str):
        self.turn = connect4ActualTurn
        self.state = deepcopy(connect4ActualState)

    def checkPlayerWon(self, player: str, speed: str, row: int = None, col: int = None) -> bool:
        if speed.lower() == "fast":
            # Horizontal
            line = ''.join(self.state[row])
            if player * 4 in line:
                return True

            # Vertical
            line = ''.join(self.state[r][col] for r in range(self.MAX_ROWS))
            if player * 4 in line:
                return True

            # Diagonal (\)
            start_row = row
            start_col = col
            while start_row > 0 and start_col > 0:
                start_row -= 1
                start_col -= 1
            line = ''
            while start_row < self.MAX_ROWS and start_col < self.MAX_COLS:
                line += self.state[start_row][start_col]
                start_row += 1
                start_col += 1
            if player * 4 in line:
                return True

            # Anti-diagonal (/)
            start_row = row
            start_col = col
            while start_row < self.MAX_ROWS - 1 and start_col > 0:
                start_row += 1
                start_col -= 1
            line = ''
            while start_row >= 0 and start_col < self.MAX_COLS:
                line += self.state[start_row][start_col]
                start_row -= 1
                start_col += 1
            if player * 4 in line:
                return True

            return False

        elif speed.lower() == "slow":
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
        if any(self.state[0][col] == "-" for col in range(self.MAX_COLS)):
            return False
        return True

    def checkGameOver(self, speed: str) -> bool:
        if speed.lower() == "fast":
            return self.checkPlayerWon(row=self.lastMovementRow, col=self.lastMovementCol, player="O", speed="fast") or self.checkPlayerWon(row=self.lastMovementRow, col=self.lastMovementCol, player="X", speed="fast") or self.checkTie()
        elif speed.lower() == "slow":
            return self.checkPlayerWon(player="O", speed="slow") or self.checkPlayerWon(player="X", speed="slow") or self.checkTie()

    def checkGameResult(self, speed: str) -> str:
        if speed.lower() == "fast":
            if self.checkTie():
                return "-"
            elif self.checkPlayerWon(row=self.lastMovementRow, col=self.lastMovementCol, player="O", speed="fast"):
                return "O"
            else:
                return "X"
        elif speed.lower() == "slow":
            if self.checkTie():
                return "-"
            elif self.checkPlayerWon(player="O", speed="slow"):
                return "O"
            else:
                return "X"

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
                self.lastMovementRow = row
                self.lastMovementCol = move-1
                break
        self.turn = "X" if self.turn == "O" else "O"
        return True

    def getIntoDesiredState(self, turn: str, gameState: list[list[str]]):
        self.turn = turn
        self.state = deepcopy(gameState)