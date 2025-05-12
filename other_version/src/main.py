from mcts_ucb import *
from connect4API import *
import math
import gc
from multiprocessing import Process, Manager
from tqdm import tqdm  
import os  # Add this import at the top of the file

def user_first_vs_AI(c_constant_mcts: float, iterations: int, reset: bool, drawValue: float, showMCTSTime: bool, showNodesStats: bool, speed: str):
    mcts = MctsAlgo(C=c_constant_mcts, reset=reset, drawValue=drawValue, speed=speed)
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

        mcts.updateAfterAdversaryTurn(connect4, move)
        
        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="O", speed="fast"):
            connect4.printState()
            print("You win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

        connect4.printState()
        print("AI is thinking...")
        mcts.run_mcts(iterations, connect4)
        bestMove = mcts.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="X", speed="fast"):
            connect4.printState()
            print("AI win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

    if showMCTSTime:
        print(f"MCTS: {mcts.runTimes}")

    del mcts
    del connect4
    gc.collect()

def AI_first_vs_user(c_constant_mcts: float, iterations: int, reset: bool, drawValue: float, showMCTSTime: bool, showNodesStats: bool, speed: str):
    mcts = MctsAlgo(C=c_constant_mcts, reset=reset, drawValue=drawValue, speed=speed)
    connect4 = Connect4(6, 7)
    while True:
        connect4.printState()
        print("AI is thinking...")
        mcts.run_mcts(iterations, connect4)
        bestMove = mcts.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="O", speed="fast"):
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
        
        mcts.updateAfterAdversaryTurn(connect4, move)

        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="X", speed="fast"):
            connect4.printState()
            print("You win")
            break
        elif connect4.checkTie():
            print("Tie")
            break

    if showMCTSTime:
        print(f"MCTS: {mcts.runTimes}")
        
    del mcts
    del connect4
    gc.collect()

def AI_vs_AI(c_constant_mcts_1st: float, iterations_1st: int, reset1: bool, drawValue1: float, speed1: str, c_constant_mcts_2nd: float, iterations_2nd: int, reset2: bool, drawValue2: float, speed2: str, showMCTSTime: bool, showNodesStats: bool, benchMarkingList = None):
    connect4 = Connect4(6, 7)
    mcts1 = MctsAlgo(C=c_constant_mcts_1st, reset=reset1, drawValue=drawValue1, speed=speed1)
    mcts2 = MctsAlgo(C=c_constant_mcts_2nd, reset=reset2, drawValue=drawValue2, speed=speed2)
    mcts1.run_mcts(0, connect4)
    mcts2.run_mcts(0, connect4)
    
    while True:
        connect4.printState()
        print("AI_1st is thinking...")
        mcts1.run_mcts(iterations_1st, connect4)
        bestMove = mcts1.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)
        mcts2.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="O", speed="fast"):
            connect4.printState()
            print("AI_1st win")
            if benchMarkingList:
                benchMarkingList.append("1")
            break
        elif connect4.checkTie():
            print("Tie")
            if benchMarkingList:
                benchMarkingList.append("-")
            break

        connect4.printState()
        print("AI_2nd is thinking...")
        mcts2.run_mcts(iterations_2nd, connect4)
        bestMove = mcts2.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)
        mcts1.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="X", speed="fast"):
            connect4.printState()
            print("AI_2nd win")
            if benchMarkingList:
                benchMarkingList.append("2")
            break
        elif connect4.checkTie():
            print("Tie")
            if benchMarkingList:
                benchMarkingList.append("-")
            break
    
    if showMCTSTime:
        print(f"MCTS1: {mcts1.runTimes}")
        print(f"MCTS2: {mcts2.runTimes}")

    mcts1.currentState.children = {}   
    mcts1.actualState.children = {}   
    mcts2.currentState.children = {} 
    mcts2.actualState.children = {}  
    del mcts1
    del mcts2
    del connect4
    gc.collect()

def Benchmarking_AI_vs_AI(c_constant_mcts_1st: float, iterations_1st: int, reset1: bool, drawValue1: float, speed1: str, c_constant_mcts_2nd: float, iterations_2nd: int, reset2: bool, drawValue2: float, speed2: str, showMCTSTime: bool, showNodesStats: bool, benchMarkingList):
    connect4 = Connect4(6, 7)
    mcts1 = MctsAlgo(C=c_constant_mcts_1st, reset=reset1, drawValue=drawValue1, speed=speed1)
    mcts2 = MctsAlgo(C=c_constant_mcts_2nd, reset=reset2, drawValue=drawValue2, speed=speed2)
    mcts1.run_mcts(0, connect4)
    mcts2.run_mcts(0, connect4)
    while True:
        mcts1.run_mcts(iterations_1st, connect4)
        bestMove = mcts1.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)
        mcts2.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="O", speed="fast"):
            benchMarkingList.append("1")
            break
        elif connect4.checkTie():
            benchMarkingList.append("-")
            break


        mcts2.run_mcts(iterations_2nd, connect4)
        bestMove = mcts2.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)
        mcts1.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(row=connect4.lastMovementRow, col=connect4.lastMovementCol, player="X", speed="fast"):
            benchMarkingList.append("2")
            break
        elif connect4.checkTie():
            benchMarkingList.append("-")
            break
    
    if showMCTSTime:
        print(f"MCTS1: {mcts1.runTimes}")
        print(f"MCTS2: {mcts2.runTimes}")

    mcts1.currentState.children = {}   
    mcts1.actualState.children = {}   
    mcts2.currentState.children = {} 
    mcts2.actualState.children = {}  
    del mcts1
    del mcts2
    del connect4
    gc.collect()

def read_input(config_filePath: str):
    resets = []
    Cs = []
    with open(config_filePath, "r") as file:
        lines = file.readlines()
        C0 = lines[1].strip().split(" = ")[1]
        Cs.append(C0)
        iterations0 = int(lines[2].strip().split(" = ")[1])
        resetTree0 = lines[3].strip().split(" = ")[1]
        resets.append(resetTree0)
        drawValue0 = float(lines[4].strip().split(" = ")[1])
        speed0 = lines[5].strip().split(" = ")[1]
        C1 = lines[8].strip().split(" = ")[1]
        Cs.append(C1)
        iterations1 = int(lines[9].strip().split(" = ")[1])
        resetTree1 = lines[10].strip().split(" = ")[1]
        resets.append(resetTree1)
        drawValue1 = float(lines[11].strip().split(" = ")[1])
        speed1 = lines[12].strip().split(" = ")[1]
        C2 = lines[13].strip().split(" = ")[1]
        Cs.append(C2)
        iterations2 = int(lines[14].strip().split(" = ")[1])
        resetTree2 = lines[15].strip().split(" = ")[1]
        resets.append(resetTree2)
        drawValue2 = float(lines[16].strip().split(" = ")[1])
        speed2 = lines[17].strip().split(" = ")[1]
        showMCTSTime = lines[20].strip().split(" = ")[1]
        showNodesStats = lines[23].strip().split(" = ")[1]
        benchmarkingFile = lines[26].strip().split(" = ")[1]

    for i in range(len(Cs)):
        if Cs[i][0:5] == "sqrt_":
            Cs[i] = math.sqrt(int(Cs[i][5]))
        else:
            Cs[i] = float(C)

    for i in range(len(resets)):
        if resets[i].lower() == "true":
            resets[i] = True
        else:
            resets[i] = False

    if showMCTSTime.lower() == "true":
        showMCTSTime = True
    else:
        showMCTSTime = False

    if showNodesStats.lower() == "true":
        showNodesStats = True
    else:
        showNodesStats = False

    return {"C0": Cs[0], "iterations0": iterations0, "resetTree0": resets[0], "drawValue0": drawValue0, "speed0": speed0,
            "C1": Cs[1], "iterations1": iterations1, "resetTree1": resets[1], "drawValue1": drawValue1, "speed1": speed1,
            "C2": Cs[2], "iterations2": iterations2, "resetTree2": resets[2], "drawValue2": drawValue2, "speed2": speed2,
            "showMCTSTime": showMCTSTime, "showNodesStats": showNodesStats, "benchmarkingFile": benchmarkingFile}

if __name__ == "__main__":
    typeOfGame = ""
    config = read_input(r"C:\Users\arcan\OneDrive\Ambiente de Trabalho\My apps\python\connect4Project\other_version\configs\configs.txt")
    showMCTSTime = config["showMCTSTime"]
    showNodesStats = config["showNodesStats"]
    while typeOfGame.lower() != "exit":
        print("""
<---------------------------------------->
        What do you want to play:

            1. User vs AI
            2. AI vs User
             3. AI vs AI
         4. Benchmarking AIs

              -- Exit --
<---------------------------------------->
""")
        typeOfGame = input("Choose: ")
        if typeOfGame == "1":
            C_constant, nIterations, reset, drawValue, speed = config["C0"], config["iterations0"], config["resetTree0"], config["drawValue0"], config["speed0"] 
            user_first_vs_AI(C_constant, nIterations, reset, drawValue, showMCTSTime, showNodesStats, speed)

        elif typeOfGame == "2":
            C_constant, nIterations, reset, drawValue, speed = config["C0"], config["iterations0"], config["resetTree0"], config["drawValue0"], config["speed0"]
            AI_first_vs_user(C_constant, nIterations, reset, drawValue, showMCTSTime, showNodesStats, speed)

        elif typeOfGame == "3":
            C_constant1, nIterations1, reset1, drawValue1, speed1 = config["C1"], config["iterations1"], config["resetTree1"], config["drawValue1"], config["speed1"]
            C_constant2, nIterations2, reset2, drawValue2, speed2 = config["C2"], config["iterations2"], config["resetTree2"], config["drawValue2"], config["speed2"]

            AI_vs_AI(C_constant1, nIterations1, reset1, drawValue1, speed1, C_constant2, nIterations2, reset2, drawValue2, speed2, showMCTSTime, showNodesStats)


        elif typeOfGame == "4":
            # Concurrent AI vs AI
            C_constant1, nIterations1, reset1, drawValue1, speed1 = config["C1"], config["iterations1"], config["resetTree1"], config["drawValue1"], config["speed1"]
            C_constant2, nIterations2, reset2, drawValue2, speed2 = config["C2"], config["iterations2"], config["resetTree2"], config["drawValue2"], config["speed2"]
            
            manager = Manager()
            return_list = manager.list()
            total_iterations = 20

            with tqdm(total=total_iterations, desc="Benchmarking Progress", unit="iteration") as pbar:
                for i in range(total_iterations):
                    # Create and start 5 processes
                    processes = []
                    for _ in range(5):
                        p = Process(target=Benchmarking_AI_vs_AI, args=(C_constant1, nIterations1, reset1, drawValue1, speed1, C_constant2, nIterations2, reset2, drawValue2, speed2, showMCTSTime, showNodesStats, return_list))
                        processes.append(p)
                        p.start()
                    # Wait for all processes to complete
                    for p in processes:
                        p.join()
                    # Update the progress bar
                    pbar.update(1)
            
            # Ensure the directory exists
            output_dir = r"other_version\AI_vs_AI_statistics"
            os.makedirs(output_dir, exist_ok=True)

            # Write the results to a file
            output_file_path = os.path.join(output_dir, config["benchmarkingFile"])
            with open(output_file_path, "w") as file:
                for result in return_list:
                    file.write(f"{result}\n")
            print(f"Results written to {output_file_path}")

        else:
            if typeOfGame.lower() != "exit":
                print("\nPlease choose between the options available!\n")