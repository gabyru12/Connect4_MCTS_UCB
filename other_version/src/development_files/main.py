from mcts_ucb import *
from connect4API import *
#from connect4APIslow import *
import math
import gc
from multiprocessing import Process, Manager
from tqdm import tqdm  
import os 
import pandas as pd
from DTID3 import *
from sklearn.model_selection import train_test_split

def user_first_vs_AI(c_constant_mcts: float, iterations: int, reset: bool, drawValue: float, showMCTSTime: bool, showNodesStats: bool):
    mcts = MctsAlgo(C=c_constant_mcts, reset=reset, drawValue=drawValue)
    connect4 = Connect4()
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
        
        if connect4.checkPlayerWon(player="O"):
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

        if connect4.checkPlayerWon(player="X"):
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

def AI_first_vs_user(c_constant_mcts: float, iterations: int, reset: bool, drawValue: float, showMCTSTime: bool, showNodesStats: bool):
    mcts = MctsAlgo(C=c_constant_mcts, reset=reset, drawValue=drawValue)
    connect4 = Connect4()
    while True:
        connect4.printState()
        print("AI is thinking...")
        mcts.run_mcts(iterations, connect4)
        bestMove = mcts.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon(player="O"):
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

        if connect4.checkPlayerWon(player="X"):
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

def AI_vs_AI(c_constant_mcts_1st: float, iterations_1st: int, reset1: bool, drawValue1: float, c_constant_mcts_2nd: float, iterations_2nd: int, reset2: bool, drawValue2: float, showMCTSTime: bool, showNodesStats: bool, activateSoftmax):
    connect4 = Connect4()
    mcts1 = MctsAlgo(C=c_constant_mcts_1st, reset=reset1, drawValue=drawValue1)
    mcts2 = MctsAlgo(C=c_constant_mcts_2nd, reset=reset2, drawValue=drawValue2)    
    while True:
        connect4.printState()
        print("AI_1st is thinking...")
        mcts1.run_mcts(iterations_1st, connect4)
        bestMove = mcts1.choose_best_move(showNodesStats, testSoftMax = activateSoftmax)
        connect4.updateGameState(bestMove)
        mcts2.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(player="O"):
            connect4.printState()
            print("AI_1st win")
            break
        elif connect4.checkTie():
            connect4.printState()
            print("Tie")
            break

        connect4.printState()
        print("AI_2nd is thinking...")
        mcts2.run_mcts(iterations_2nd, connect4)
        bestMove = mcts2.choose_best_move(showNodesStats, testSoftMax = activateSoftmax)
        connect4.updateGameState(bestMove)
        mcts1.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(player="X"):
            connect4.printState()
            print("AI_2nd win")
            break
        elif connect4.checkTie():
            connect4.printState()
            print("Tie")
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

def DT_vs_AI(c_constant_mcts_1st: float, iterations_1st: int, reset1: bool, drawValue1: float, showMCTSTime: bool, showNodesStats: bool, training_data_file: str, tree_max_depth: int):
    connect4 = Connect4()
    mcts = MctsAlgo(C=c_constant_mcts_1st, reset=reset1, drawValue=drawValue1)
    df = pd.read_csv(f"other_version/datasets/{training_data_file}").drop(columns=["10kIter","20kIter","30kIter","40kIter"])
    tree = ID3Tree(max_depth=tree_max_depth)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    tree.fit(df, X.columns)
    col_names = [f"cell_{i}" for i in range(42)]
    while True:
        connect4.printState()
        print("DT is thinking...")
        matrix = connect4.bitboard_to_matrix()
        flattened = connect4.flatten_board(matrix)
        row = pd.DataFrame([flattened], columns=col_names)  # <-- fix here
        bestMove = tree.classify(row)
        try:
            connect4.updateGameState(bestMove)
        except TypeError:
            print(bestMove)
        mcts.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(player="O"):
            connect4.printState()
            print("DT won")
            break
        elif connect4.checkTie():
            connect4.printState()
            print("Tie")
            break

        connect4.printState()
        mcts.run_mcts(iterations_1st, connect4)
        bestMove = mcts.choose_best_move(showNodesStats)
        connect4.updateGameState(bestMove)

        if connect4.checkPlayerWon(player="X"):
            connect4.printState()
            print("MCTS won")
            break
        elif connect4.checkTie():
            connect4.printState()
            print("Tie")
            break

    if showMCTSTime:
        print(f"MCTS: {mcts.runTimes}")
    mcts.currentState.children = {}   
    mcts.actualState.children = {}   
    del mcts
    del connect4
    gc.collect()

def Benchmarking_AI_vs_AI(c_constant_mcts_1st: float, iterations_1st: int, reset1: bool, drawValue1: float, c_constant_mcts_2nd: float, iterations_2nd: int, reset2: bool, drawValue2: float, showMCTSTime: bool, showNodesStats: bool, dataset, activateSoftmax):
    connect4 = Connect4()
    mcts1 = MctsAlgo(C=c_constant_mcts_1st, reset=reset1, drawValue=drawValue1)
    mcts2 = MctsAlgo(C=c_constant_mcts_2nd, reset=reset2, drawValue=drawValue2)
    while True:
        mcts1.run_mcts(iterations_1st, connect4, dataset)
        bestMove = mcts1.choose_best_move(showNodesStats, testSoftMax = activateSoftmax)
        connect4.updateGameState(bestMove)
        mcts2.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(player="O"):
            break
        elif connect4.checkTie():
            break

        mcts2.run_mcts(iterations_2nd, connect4, dataset)
        bestMove = mcts2.choose_best_move(showNodesStats, testSoftMax = activateSoftmax)
        connect4.updateGameState(bestMove)
        mcts1.updateAfterAdversaryTurn(connect4, bestMove)

        if connect4.checkPlayerWon(player="X"):
            break
        elif connect4.checkTie():
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
        C1 = lines[7].strip().split(" = ")[1]
        Cs.append(C1)
        iterations1 = int(lines[8].strip().split(" = ")[1])
        resetTree1 = lines[9].strip().split(" = ")[1]
        resets.append(resetTree1)
        drawValue1 = float(lines[10].strip().split(" = ")[1])
        C2 = lines[11].strip().split(" = ")[1]
        Cs.append(C2)
        iterations2 = int(lines[12].strip().split(" = ")[1])
        resetTree2 = lines[13].strip().split(" = ")[1]
        resets.append(resetTree2)
        drawValue2 = float(lines[14].strip().split(" = ")[1])
        showMCTSTime = lines[17].strip().split(" = ")[1]
        showNodesStats = lines[20].strip().split(" = ")[1]
        benchmarkingFile = lines[23].strip().split(" = ")[1]
        DTtrainfile = lines[26].strip().split(" = ")[1]
        activateSoftMax = lines[29].strip().split(" = ")[1]

    for i in range(len(Cs)):
        if Cs[i][0:5] == "sqrt_":
            Cs[i] = math.sqrt(int(Cs[i][5]))
        else:
            Cs[i] = float(Cs[i])

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

    if activateSoftMax.lower() == "true":
        activateSoftMax = True
    else:
        activateSoftMax = False

    return {"C0": Cs[0], "iterations0": iterations0, "resetTree0": resets[0], "drawValue0": drawValue0,
            "C1": Cs[1], "iterations1": iterations1, "resetTree1": resets[1], "drawValue1": drawValue1, 
            "C2": Cs[2], "iterations2": iterations2, "resetTree2": resets[2], "drawValue2": drawValue2,
            "showMCTSTime": showMCTSTime, "showNodesStats": showNodesStats, "benchmarkingFile": benchmarkingFile, "DTtrainfile": DTtrainfile, "activateSoftMax": activateSoftMax}

def save_to_csv(dataset: list[list[str]], filePath: str):
    col_names = [f"cell_{i}" for i in range(42)] + ["10kIter", "20kIter", "30kIter", "40kIter", "50kIter",]
    df_new = pd.DataFrame(dataset, columns=col_names)
    csv_path = f'other_version/datasets/{filePath}'

    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(csv_path, index=False)
        print(f"\nAppended to existing connect4_{filePath}.csv (total: {len(df_combined)} rows)")
    else:
        df_new.to_csv(csv_path, index=False)
        print(f"\nDataset saved as new connect4_{filePath}.csv")

if __name__ == "__main__":
    typeOfGame = ""
    config = read_input(r"other_version\configs\configs.txt")
    showMCTSTime = config["showMCTSTime"]
    showNodesStats = config["showNodesStats"]
    trainingDataFile = config["DTtrainfile"]
    activateSoftMax = config["activateSoftMax"]
    while typeOfGame.lower() != "exit":
        print("""
<---------------------------------------->
        What do you want to play:

            1. User vs AI
            2. AI vs User
             3. AI vs AI
             4. DT vs AI
         5. Benchmarking AIs

              -- Exit --
<---------------------------------------->
""")
        typeOfGame = input("Choose: ")
        if typeOfGame == "1":
            C_constant, nIterations, reset, drawValue = config["C0"], config["iterations0"], config["resetTree0"], config["drawValue0"]
            user_first_vs_AI(C_constant, nIterations, reset, drawValue, showMCTSTime, showNodesStats)

        elif typeOfGame == "2":
            C_constant, nIterations, reset, drawValue = config["C0"], config["iterations0"], config["resetTree0"], config["drawValue0"]
            AI_first_vs_user(C_constant, nIterations, reset, drawValue, showMCTSTime, showNodesStats)

        elif typeOfGame == "3":
            C_constant1, nIterations1, reset1, drawValue1 = config["C1"], config["iterations1"], config["resetTree1"], config["drawValue1"]
            C_constant2, nIterations2, reset2, drawValue2 = config["C2"], config["iterations2"], config["resetTree2"], config["drawValue2"]

            AI_vs_AI(C_constant1, nIterations1, reset1, drawValue1, C_constant2, nIterations2, reset2, drawValue2, showMCTSTime, showNodesStats, activateSoftMax)
        
        elif typeOfGame == "4":
            C_constant0, nIterations0, reset0, drawValue0 = config["C0"], config["iterations0"], config["resetTree0"], config["drawValue0"]

            DT_vs_AI(C_constant0, nIterations0, reset0, drawValue0, showMCTSTime, showNodesStats, trainingDataFile, 20)

        elif typeOfGame == "5":
            # Concurrent AI vs AI
            C_constant1, nIterations1, reset1, drawValue1 = config["C1"], config["iterations1"], config["resetTree1"], config["drawValue1"]
            C_constant2, nIterations2, reset2, drawValue2 = config["C2"], config["iterations2"], config["resetTree2"], config["drawValue2"]
            
            manager = Manager()
            dataset = manager.list()
            total_iterations = 20

            with tqdm(total=total_iterations, desc="Benchmarking Progress", unit="iteration") as pbar:
                for i in range(total_iterations):
                    # Create and start 5 processes
                    processes = []
                    for _ in range(5):
                        p = Process(target=Benchmarking_AI_vs_AI, args=(C_constant1, nIterations1, reset1, drawValue1, C_constant2, nIterations2, reset2, drawValue2, showMCTSTime, showNodesStats, dataset, activateSoftMax))
                        processes.append(p)
                        p.start()
                    # Wait for all processes to complete
                    for p in processes:
                        p.join()
                    # Update the progress bar
                    pbar.update(1)
            
            dataset = list(dataset)
            # Write results to csv file
            save_to_csv(dataset=dataset, filePath = config["benchmarkingFile"])

        else:
            if typeOfGame.lower() != "exit":
                print("\nPlease choose between the options available!\n")