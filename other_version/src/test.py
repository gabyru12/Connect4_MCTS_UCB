from connect4API import Connect4

game = Connect4()
game.updateGameState(4)
game.updateGameState(4)
matrix = game.bitboard_to_matrix()
for row in matrix:
    print(row)
flatted = game.flatten_board(matrix)
print(flatted)
