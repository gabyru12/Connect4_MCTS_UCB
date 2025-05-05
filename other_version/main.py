from mcts_ucb import Node, MctsAlgo
from connect4API import Connect4
import math
import gc
from multiprocessing import Process

def user_first_vs_AI(c_constant_mcts: int, iterations: int, reset: bool, drawValue: float):
    mcts = MctsAlgo(C=c_constant_mcts, reset=reset, drawValue=drawValue)
    connect4 = Connect4(6, 7)
    while True:
        connect4.printState()
        while True: 
            try:
                move = int(input("Choose your move: "))
                connect4.updateGameState(move)
                break
            except ValueError as e:
                print(f"{e}")
                continue 

        if connect4.checkPlayerWon("O"):
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

        if connect4.checkPlayerWon("X"):
            connect4.printState()
            print("AI win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

    del mcts
    del connect4
    gc.collect()

def AI_first_vs_user(c_constant_mcts: int, iterations: int, reset: bool, drawValue):
    mcts = MctsAlgo(C=c_constant_mcts, reset=reset, drawValue=drawValue)
    connect4 = Connect4(6, 7)
    move = None
    while not connect4.checkGameOver():
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

        connect4.printState()
        while True: 
            try:
                move = int(input("Choose your move: "))
                connect4.updateGameState(move)
                break
            except ValueError as e:
                print(f"{e}")
                continue 

        if connect4.checkPlayerWon("X"):
            connect4.printState()
            print("You win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

    del mcts
    del connect4
    gc.collect()

def AI_vs_AI(c_constant_mcts_1st: int, iterations_1st: int, reset1: bool, drawValue1: float, c_constant_mcts_2nd: int, iterations_2nd: int, reset2: bool, drawValue2: float):
    connect4 = Connect4(6, 7)
    mcts1 = MctsAlgo(C=c_constant_mcts_1st, reset=reset1, drawValue=drawValue1)
    mcts2 = MctsAlgo(C=c_constant_mcts_2nd, reset=reset2, drawValue=drawValue2)
    bestMove = None
    mcts1.run_mcts(0, connect4, bestMove)
    mcts2.run_mcts(0, connect4, bestMove)
    
    while not connect4.checkGameOver():
        connect4.printState()
        print("AI_1st is thinking...")
        mcts1.run_mcts(iterations_1st, connect4, bestMove)
        bestMove = mcts1.choose_best_move()
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon("O"):
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

        if connect4.checkPlayerWon("X"):
            connect4.printState()
            print("AI_2nd win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

    del mcts1
    del mcts2
    del connect4
    gc.collect()

def read_input(config_filePath: str):
    with open(config_filePath, "r") as file:
        lines = file.readlines()
        C0 = lines[1].strip().split(" = ")[1]
        iterations0 = lines[2].strip().split(" = ")[1]
        resetTree0 = lines[3].strip().split(" = ")[1]
        drawValue0 = lines[4].strip().split(" = ")[1]
        C1 = lines[7].strip().split(" = ")[1]
        iterations1 = lines[8].strip().split(" = ")[1]
        resetTree1 = lines[9].strip().split(" = ")[1]
        drawValue1 = lines[10].strip().split(" = ")[1]
        C2 = lines[11].strip().split(" = ")[1]
        iterations2 = lines[12].strip().split(" = ")[1]
        resetTree2 = lines[13].strip().split(" = ")[1]
        drawValue2 = lines[14].strip().split(" = ")[1]
    
    return {"C0": C0, "iterations0": iterations0, "resetTree0": resetTree0, "drawValue0": drawValue0,
            "C1": C1, "iterations1": iterations1, "resetTree1": resetTree1, "drawValue1": drawValue1,
            "C2": C2, "iterations2": iterations2, "resetTree2": resetTree2, "drawValue2": drawValue2}

if __name__ == "__main__":
    typeOfGame = ""
    config = read_input(r"C:\Users\zebru\OneDrive\Desktop\FCUP\2ยบ ano\2ยบ semestre\IA\Connect4_MCTS\other_version\configs.txt")
    while typeOfGame.lower() != "exit":
        print("""
<---------------------------------------->
        What do you want to play:

            1. User vs AI
            2. AI vs User
             3. AI vs AI
        4. Run concurrently (5)

              -- Exit --
<---------------------------------------->
""")
        typeOfGame = input("Choose: ")
        if typeOfGame == "1":
            C_constant, nIterations, reset, drawValue = config["C0"], config["iterations0"], config["resetTree0"], config["drawValue0"] 
            if C_constant[0:5] == "sqrt_":
                C_constant = math.sqrt(int(C_constant[5]))
            else:
                C_constant = int(C_constant)
            if reset.lower() == "true":
                reset = True
            else:
                reset = False
            user_first_vs_AI(C_constant, int(nIterations), reset, float(drawValue))

        elif typeOfGame == "2":
            C_constant, nIterations, reset, drawValue = config["C0"], config["iterations0"], config["resetTree0"], config["drawValue0"]
            if C_constant[0:5] == "sqrt_":
                C_constant = math.sqrt(int(C_constant[5]))
            else:
                C_constant = int(C_constant)
            if reset.lower() == "true":
                reset = True
            else:
                reset = False
            AI_first_vs_user(C_constant, int(nIterations), reset, float(drawValue))

        elif typeOfGame == "3":
            C_constant1, nIterations1, reset1, drawValue1 = config["C1"], config["iterations1"], config["resetTree1"], config["drawValue1"]
            C_constant2, nIterations2, reset2, drawValue2 = config["C2"], config["iterations2"], config["resetTree2"], config["drawValue2"]
            if C_constant1[0:5] == "sqrt_":
                C_constant1 = math.sqrt(int(C_constant1[5]))
            else:
                C_constant1 = int(C_constant1)
            if reset1.lower() == "true":
                reset1 = True
            else:
                reset1 = False

            if C_constant2[0:5] == "sqrt_":
                C_constant2 = math.sqrt(int(C_constant2[5]))
            else:
                C_constant2 = int(C_constant2)
            if reset2.lower() == "true":
                reset2 = True
            else:
                reset2 = False

            nIterations1 = int(nIterations1)
            nIterations2 = int(nIterations2)
            drawValue1 = float(drawValue1)
            drawValue2 = float(drawValue2)
            AI_vs_AI(C_constant1, nIterations1, reset1, drawValue1, C_constant2, nIterations2, reset2, drawValue2)

        elif typeOfGame == "4":
            # Concurrent AI vs AI
            C_constant1, nIterations1, reset1, drawValue1 = config["C1"], config["iterations1"], config["resetTree1"], config["drawValue1"]
            C_constant2, nIterations2, reset2, drawValue2 = config["C2"], config["iterations2"], config["resetTree2"], config["drawValue2"]
            if C_constant1[0:5] == "sqrt_":
                C_constant1 = math.sqrt(int(C_constant1[5]))
            else:
                C_constant1 = int(C_constant1)
            if reset1.lower() == "true":
                reset1 = True
            else:
                reset1 = False
            if C_constant2[0:5] == "sqrt_":
                C_constant2 = math.sqrt(int(C_constant2[5]))
            else:
                C_constant2 = int(C_constant2)
            if reset2.lower() == "true":
                reset2 = True
            else:
                reset2 = False
            nIterations1 = int(nIterations1)
            nIterations2 = int(nIterations2)
            # Create and start 5 processes
            processes = []
            for _ in range(5):
                p = Process(target=AI_vs_AI, args=(C_constant1, nIterations1, reset1, drawValue1, C_constant2, nIterations2, reset2, drawValue2))
                processes.append(p)
                p.start()
            # Wait for all processes to complete
            for p in processes:
                p.join()

        else:
            if typeOfGame.lower() != "exit":
                print("\nPlease choose between the options available!\n")