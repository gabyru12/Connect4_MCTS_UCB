from mcts_ucb import Node, MctsAlgo
from connect4API import Connect4

def play():
    mcts = MctsAlgo(2)
    connect4 = Connect4(6, 7)
    while not connect4.checkGameOver():
        print("Current state")
        connect4.printState()
        move = int(input("Choose your move: "))
        connect4.updateGameState(move)

        if connect4.checkPlayerWon("X"):
            connect4.printState()
            print("You win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

        connect4.printState()
        print("AI is thinking...")
        mcts.run_mcts(10000, connect4, move)
        bestMove = mcts.choose_best_move()
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon("O"):
            connect4.printState()
            print("AI win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

play()


