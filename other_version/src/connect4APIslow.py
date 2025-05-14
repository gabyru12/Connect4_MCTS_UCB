from copy import deepcopy
import random
import time

class Connect4:
    def __init__(self):
        self.bitboards = [0, 0]  # Two players: bitboards[0] for player 1, bitboards[1] for player 2
        self.heights = [0, 7, 14, 21, 28, 35, 42]  # Bit index of next available cell in each column
        self.counter = 0         # Total number of moves made

    def printState(self):
        print("===========================")
        for row in reversed(range(6)):  # Top to bottom
            for col in range(7):
                bit_index = col * 7 + row  # Position in bitboard
                bit_mask = 1 << bit_index

                if self.bitboards[0] & bit_mask:
                    cell = f"\033[94mO\033[0m"  # Red for Player 1
                elif self.bitboards[1] & bit_mask:
                    cell = f"\033[91mX\033[0m"  # Blue for Player 2
                else:
                    cell = " "

                if col < 6:
                    print(f" {cell} |", end="")
                else:
                    print(f" {cell} ")

        print("===========================")
        print(" 1 | 2 | 3 | 4 | 5 | 6 | 7 ")


    def reset(self, connect4):
        self.heights = deepcopy(connect4.heights)
        self.counter = connect4.counter
        self.bitboards = deepcopy(connect4.bitboards)

    def updateGameState(self, move: int):
        """Apply a move in the given column."""
        if move not in self.checkAvailableMoves():
            raise ValueError(f"Invalid move")
        move1 = 1 << self.heights[move-1]  # Get the bit index for the current top of the column
        self.heights[move-1] += 1         # Update height to the next position
        self.bitboards[self.counter & 1] ^= move1  # XOR sets the bit for current player
        self.counter += 1

    def checkPlayerWon(self, player: str) -> bool:
        """Check if a given bitboard has a 4-in-a-row."""
        if player == "O":
            bitboard = self.bitboards[0]
        else:
            bitboard = self.bitboards[1]
        directions = [1, 7, 6, 8]  # Horizontal, vertical, diagonal /
        for d in directions:
            bb = bitboard & (bitboard >> d)
            if bb & (bb >> (2 * d)):
                return True
        return False

    def checkTie(self):
        """Return True if the board is full and no one has won."""
        return not self.checkAvailableMoves() and self.checkPlayerWon("O") == False and self.checkPlayerWon("X") == False

    def checkGameResult(self) -> str:
        if self.checkPlayerWon("O"):
            return "O"
        elif self.checkTie():
            return "-"
        else:
            return "X"

    def checkGameOver(self) -> bool:
        last_player = "O" if self.current_player() == 1 else "X"
        return self.checkPlayerWon(player=last_player) or self.checkTie()

    def checkAvailableMoves(self):
        """Return a list of valid columns where a move can be made."""
        valid_moves = []
        TOP = 0b1000000_1000000_1000000_1000000_1000000_1000000_1000000
        for col in range(7):
            if (TOP & (1 << self.heights[col])) == 0:
                valid_moves.append(col+1)
        return valid_moves

    def current_player(self):
        """Return the current player (0 or 1)."""
        return self.counter & 1

def matrix_to_bitboard(matrix: list[list[str]]) -> tuple[list[int], int]:
    """
    Converts a 6x7 matrix to bitboards.
    Returns:
        - bitboards: [bitboard_O, bitboard_X]
        - counter: number of total pieces (used to determine current player)
    """
    bitboards = [0, 0]  # bitboards[0] = O, bitboards[1] = X
    counter = 0
    matrix_reverse = list(reversed(matrix))
    heights = []

    for col in range(7):
        for row in range(6):
            if matrix_reverse[row][col] == "-":
                heights.append(col * 7 + row)
                break
            if row == 6:
                heights.append(col * 7 + row)

    for row in range(6):
        for col in range(7):
            piece = matrix_reverse[row][col]
            if piece not in ('O', 'X'):
                continue
            bit_index = col * 7 + row
            if piece == 'O':
                bitboards[0] |= 1 << bit_index
            elif piece == 'X':
                bitboards[1] |= 1 << bit_index
            counter += 1

    return bitboards, counter, heights