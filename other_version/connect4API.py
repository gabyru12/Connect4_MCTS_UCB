from copy import deepcopy
import random
import numpy as np

class Connect4:
    def __init__(self, MAX_ROWS: int, MAX_COLS: int):
        self.MAX_ROWS = MAX_ROWS
        self.MAX_COLS = MAX_COLS
        self.turn = "O"
        self.state = [["-"] * self.MAX_COLS for row in range(self.MAX_ROWS)]

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
        return self.checkPlayerWon("O") or self.checkPlayerWon("X") or self.checkTie()

    def checkGameResult(self):
        if self.checkTie():
            return "-"
        elif self.checkPlayerWon("O"):
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
                break
        self.turn = "X" if self.turn == "O" else "O"
        return True

    def getIntoDesiredState(self, turn: str, gameState: list[list[int]]):
        for row in range(self.MAX_ROWS):
            for col in range(self.MAX_COLS):
                self.state[row][col] = gameState[row][col]
        self.turn = turn