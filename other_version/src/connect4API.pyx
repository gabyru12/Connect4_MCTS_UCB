# connect4.pyx
cimport cython
from copy import deepcopy

cdef class Connect4:
    cdef public long long bitboards[2]
    cdef public int heights[7]
    cdef public int counter

    def __init__(self):
        self.bitboards[0] = 0
        self.bitboards[1] = 0
        self.heights[:] = [0, 7, 14, 21, 28, 35, 42]
        self.counter = 0
    
    def reset(self, Connect4 connect4):
        self.bitboards[0] = connect4.bitboards[0]
        self.bitboards[1] = connect4.bitboards[1]
        self.counter = connect4.counter
        for i in range(len(self.heights)):
            self.heights[i] = connect4.heights[i]

    def printState(self):
        print("===========================")
        for row in reversed(range(6)):
            for col in range(7):
                bit_index = col * 7 + row
                bit_mask = 1 << bit_index

                if self.bitboards[0] & bit_mask:
                    cell = f"\033[94mO\033[0m"
                elif self.bitboards[1] & bit_mask:
                    cell = f"\033[91mX\033[0m"
                else:
                    cell = " "

                if col < 6:
                    print(f" {cell} |", end="")
                else:
                    print(f" {cell} ")
        print("===========================")
        print(" 1 | 2 | 3 | 4 | 5 | 6 | 7 ")


    def updateGameState(self, int move):
        if move not in self.checkAvailableMoves():
            raise ValueError("Invalid move")
        move1 = 1LL << self.heights[move - 1]
        self.bitboards[self.counter & 1] ^= move1
        self.heights[move - 1] += 1
        self.counter += 1

    def checkPlayerWon(self, str player):
        cdef long long bitboard
        cdef long long bb
        cdef int d
        if player == "O":
            bitboard = self.bitboards[0]
        else:
            bitboard = self.bitboards[1]

        for d in [1, 7, 6, 8]:
            bb = bitboard & (bitboard >> d)
            if bb & (bb >> (2 * d)):
                return True
        return False

    def checkTie(self):
        return not self.checkAvailableMoves() and not self.checkPlayerWon("O") and not self.checkPlayerWon("X")

    def checkGameResult(self):
        if self.checkPlayerWon("O"):
            return "O"
        elif self.checkTie():
            return "-"
        else:
            return "X"

    def checkGameOver(self):
        last_player = "O" if self.current_player() == 1 else "X"
        return self.checkPlayerWon(last_player) or self.checkTie()

    def checkAvailableMoves(self):
        cdef int col
        cdef long long TOP = 0b1000000100000010000001000000100000010000001000000
        valid_moves = []
        for col in range(7):
            if (TOP & (1LL << self.heights[col])) == 0:
                valid_moves.append(col + 1)
        return valid_moves

    def current_player(self):
        return self.counter & 1

    def flatten_board(self, board: list[list[str]]) -> list[str]:
        return [cell for row in board for cell in row]

    def bitboard_to_matrix(self) -> list[list[str]]:
        cdef long long bitboardO = self.bitboards[0]
        cdef long long bitboardX = self.bitboards[1]
        cdef list matrix = [["-" for _ in range(7)] for _ in range(6)]
        cdef int col, row
        cdef long long bit_index, mask

        for col in range(7):
            for row in range(6):
                bit_index = col * 7 + row
                mask = 1LL << bit_index

                if bitboardO & mask:
                    matrix[5 - row][col] = "O"
                elif bitboardX & mask:
                    matrix[5 - row][col] = "X"

        return matrix
