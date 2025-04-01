from mcts_ucb import Node, MctsAlgo
from connect4API import Connect4
import math
import gc

def AI_first_vs_user(c_constant_mcts: int, iterations: int):
    mcts = MctsAlgo(c_constant_mcts)
    connect4 = Connect4(6, 7)
    move = None
    while not connect4.checkGameOver():
        connect4.printState()
        print("AI is thinking...")
        mcts.run_mcts(iterations, connect4, move)
        bestMove = mcts.choose_best_move()
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon("X"):
            connect4.printState()
            print("AI win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

        connect4.printState()
        move = int(input("Choose your move: "))
        connect4.updateGameState(move)

        if connect4.checkPlayerWon("O"):
            connect4.printState()
            print("You win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

def user_first_vs_AI(c_constant_mcts: int, iterations: int):
    mcts = MctsAlgo(c_constant_mcts)
    connect4 = Connect4(6, 7)
    while not connect4.checkGameOver():
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
        mcts.run_mcts(iterations, connect4, move)
        bestMove = mcts.choose_best_move()
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon("O"):
            connect4.printState()
            print("AI win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

def AI_vs_AI(c_constant_mcts_1st: int, iterations_1st: int, c_constant_mcts_2nd: int, iterations_2nd: int):
    connect4 = Connect4(6, 7)
    mcts1 = MctsAlgo(c_constant_mcts_1st)
    mcts2 = MctsAlgo(c_constant_mcts_2nd)
    bestMove = None
    mcts1.run_mcts(0, connect4, bestMove)
    mcts2.run_mcts(0, connect4, bestMove)
    
    while not connect4.checkGameOver():
        connect4.printState()
        print("AI_1st is thinking...")
        mcts1.run_mcts(iterations_1st, connect4, bestMove)
        bestMove = mcts1.choose_best_move()
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon("X"):
            connect4.printState()
            print("AI_1st win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

        connect4.printState()
        print("AI_2nd is thinking...")
        mcts2.run_mcts(iterations_2nd, connect4, bestMove)
        bestMove = mcts2.choose_best_move()
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon("O"):
            connect4.printState()
            print("AI_2nd win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

    mcts1.root = None
    mcts2.root = None
    mcts1.actualState = None
    mcts2.actualState = None
    del mcts1
    del mcts2
    del connect4
    gc.collect()

if __name__ == "__main__":
    typeOfGame = ""
    while True:
        print("""
<---------------------------------------->
        What do you want to play:

            1. User vs AI
            2. AI vs User
            3. AI vs AI

            -- Exit --
<---------------------------------------->
""")
        typeOfGame = input("Choose: ")
        if typeOfGame == "1":
            C_constant = input("Choose the value for the C constant for MCTS(eg. X, sqrt_X): ")
            if C_constant[0:5] == "sqrt_":
                C_constant = math.sqrt(int(C_constant[5]))
            else:
                C_constant = int(C_constant)
            nIterations = int(input("Choose the value for the number of iterations: "))    
            user_first_vs_AI(C_constant, nIterations)
        elif typeOfGame == "2":
            C_constant = input("Choose the value for the C constant for MCTS(eg. X, sqrt_X): ")
            if C_constant[0:5] == "sqrt_":
                C_constant = math.sqrt(int(C_constant[5]))
            else:
                C_constant = int(C_constant)
            nIterations = int(input("Choose the value for the number of iterations: "))
            AI_first_vs_user(C_constant, nIterations)
        elif typeOfGame == "3":
            C_constant1 = input("Choose the value for the C constant for MCTS_1st(eg. X, sqrt_X): ")
            if C_constant1[0:5] == "sqrt_":
                C_constant1 = math.sqrt(int(C_constant1[5]))
            else:
                C_constant1 = int(C_constant1)
            nIterations1 = int(input("Choose the value for the number of iterations for MCTS_1st: "))
            C_constant2 = input("Choose the value for the C constant for MCTS_2st(eg. X, sqrt_X): ")
            if C_constant2[0:5] == "sqrt_":
                C_constant2 = math.sqrt(int(C_constant2[5]))
            else:
                C_constant2 = int(C_constant2)
            nIterations2 = int(input("Choose the value for the number of iterations for MCTS_2st: "))
            AI_vs_AI(C_constant1, nIterations1, C_constant2, nIterations2)
        else:
            if typeOfGame.lower() != "exit":
                print("\nPlease choose between the options available!\n")


