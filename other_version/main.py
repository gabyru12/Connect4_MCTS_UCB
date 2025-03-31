from mcts_ucb import Node, MctsAlgo
from connect4API import Connect4
import math

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
    mcts1 = MctsAlgo(c_constant_mcts_1st)
    mcts2 = MctsAlgo(c_constant_mcts_2nd)
    connect4 = Connect4(6, 7)
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

if __name__ == "__main__":
    typeOfGame = ""
    while typeOfGame.lower() != "exit":
        print("<---------------------------------------->")
        print("What do you want to play:\n1. User vs AI\n2. AI vs User\n3. AI vs AI\n<-- Exit -->")
        print("<---------------------------------------->")
        typeOfGame = input("Choose: ")
        if typeOfGame == "1":
            user_first_vs_AI(math.sqrt(2), 10000)
        elif typeOfGame == "2":
            AI_first_vs_user(math.sqrt(2), 10000)
        elif typeOfGame == "3":
            AI_vs_AI(math.sqrt(2), 10000, math.sqrt(2), 10000)
        else:
            print("Please choose between the options available!\n")


