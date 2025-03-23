class Connect4:
    def __init__(self, MAX_ROWS: int, MAX_COLS: int, state: list[str] = None):
        self.MAX_ROWS = MAX_ROWS
        self.MAX_COLS = MAX_COLS
        self.turn = "X"
        if(state != None):
            self.state = state
        else:
            self.state = [["-"] * self.MAX_COLS for row in range(self.MAX_ROWS)]


    def printState(self):
        print("==========================")
        for row in range(self.MAX_ROWS):
            for col in range(self.MAX_COLS - 1):
                print(f"{self.state[row][col]} | ", end="")
            print(f"{self.state[row][self.MAX_COLS-1]}")
        print("==========================")

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

    def checkAvailableMoves(self) -> list[int]:
        availableMoves = []
        for col in range(self.MAX_COLS):
            if self.state[0][col] == "-":
                availableMoves.append(col+1)
        return availableMoves

    def updateState(self, move: int) -> bool:
        if move not in range(1,8):
            return False
        if self.state[0][move-1] != "-":
            return False
        for row in range(self.MAX_ROWS - 1, -1, -1):
            if self.state[row][move-1] == "-":
                self.state[row][move-1] = self.turn
                break
        self.turn = "O" if self.turn == "X" else "X"
        return True

    def getIntoDesiredState(self, movesPlayed: list[int]) -> list[list[str]]:
        for i in range(len(movesPlayed)):
            updateState(movesPlayed[i])
        return self.state

board = [["-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-"]]
                
connect4 = Connect4(6, 7)
print(connect4.checkAvailableMoves())

