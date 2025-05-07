import math
from connect4API import *
import random
import gc
import time


class Node:
    def __init__(self, parent: 'Node', move: int, depth: int):
        self.Q = 0
        self.N = 0
        self.depth = depth
        if self.depth % 2 == 1:
            self.playerTurn = "O"
        else:
            self.playerTurn = "X"
        self.move = move
        self.parent = parent
        self.children = {}

class MctsAlgo:
    def __init__(self, C: float = math.sqrt(2), reset: bool = True, connect4: Connect4 = Connect4(6, 7), drawValue: float = 0):
        self.C = C
        self.root = Node(None, None, 0)
        self.connect4 = connect4
        self.currentState = self.root
        self.iteration = 0
        self.actualState = self.root
        self.resetTree = reset
        self.drawValue = drawValue
        self.runTimes = []

    def reset(self, connect4Actual: Connect4):
        self.connect4.reset(connect4Actual.state, connect4Actual.turn)
        self.currentState = self.actualState

    def selection_phase(self) -> None:
        valuesForEachChildren = {}
        promissingChildren = []
        childrenWithNZero = []
        self.currentState = self.actualState

        #trying to find a node without children
        while len(self.currentState.children) != 0:
            valuesForEachChildren = {}
            promissingChildren = []
            childrenWithNZero = []
            bestValue = -1
            for move in self.currentState.children.keys():
                if self.currentState.children[move].N > 0:
                    valuesForEachChildren[move] = self.upper_confidence_bound(self.currentState.children[move])
                    if valuesForEachChildren[move] > bestValue:
                        promissingChildren.clear()
                        promissingChildren.append(move)
                        bestValue = valuesForEachChildren[move]
                    elif valuesForEachChildren[move] == bestValue:
                        promissingChildren.append(move)
                else:
                    childrenWithNZero.append(move)
            if len(childrenWithNZero) > 0:
                randomChoice = random.choice(childrenWithNZero)    
                self.updateMCTSState(randomChoice)
                self.connect4.updateGameState(randomChoice)
                return
            randomChoice = random.choice(promissingChildren)
            self.updateMCTSState(randomChoice)
            self.connect4.updateGameState(randomChoice)

        return

    def expansion_phase(self, checkIfGameFinished: bool) -> bool:
        if checkIfGameFinished:
            isGameFinished = self.connect4.checkGameOver()
            if isGameFinished:
                return False
        availableMoves = self.connect4.checkAvailableMoves()
        for move in availableMoves:
            self.currentState.children[move] = Node(self.currentState, move, self.currentState.depth + 1)
        return True

    def simulation_phase(self, wasExpansionSuccessful: bool) -> str:
        if wasExpansionSuccessful == False:
            gameResult = self.connect4.checkGameResult()
            return gameResult
        moves = [key for key in self.currentState.children.keys()]
        randomChoice = random.choice(moves)
        self.updateMCTSState(randomChoice)
        self.connect4.updateGameState(randomChoice)
        while not self.connect4.checkGameOver():
            self.connect4.updateGameState(random.choice(self.connect4.checkAvailableMoves()))
        gameResult = self.connect4.checkGameResult()
        return gameResult
        
    def backPropagation_phase(self, gameResult: str):
        while self.currentState != self.actualState:
            self.currentState.N += 1
            if self.currentState.playerTurn == gameResult:
                self.currentState.Q += 1
            elif gameResult == "-":
                self.currentState.Q += self.drawValue
            self.currentState = self.currentState.parent
        self.currentState.N += 1
        if self.currentState.playerTurn == gameResult:
            self.currentState.Q += 1
        elif gameResult == "-":
            self.currentState.Q += self.drawValue
        self.iteration += 1

    def updateMCTSState(self, move: int):
        self.currentState = self.currentState.children[move]
        
    def upper_confidence_bound(self, node: Node) -> int:
        return (node.Q / node.N) + (self.C * math.sqrt((math.log(node.parent.N) / node.N)))

    def updateAfterAdversaryTurn(self, connect4Actual: Connect4, moveBefore: int):
        if len(self.actualState.children) == 0: 
            self.reset(connect4Actual)
            self.expansion_phase(checkIfGameFinished=False)                
        self.actualState = self.actualState.children[moveBefore]
    
    def run_mcts(self, iterations: int, connect4Actual: Connect4):
        start_time = time.time()  # Start timing
        if self.resetTree:
            self.actualState.children = {}   # Resets tree by clearing every child node
            self.currentState.children = {}  # Definetely resets tree by clearing every child node
            gc.collect()
        if len(self.actualState.children) == 0: 
            self.reset(connect4Actual)
            self.expansion_phase(checkIfGameFinished=False)
        for i in range(iterations):
            self.reset(connect4Actual)
            self.selection_phase()
            wasExpansionSuccessful = self.expansion_phase(checkIfGameFinished=True)
            gameResult = self.simulation_phase(wasExpansionSuccessful)
            self.backPropagation_phase(gameResult)
        end_time = time.time()  # End timing
        self.runTimes.append(round(end_time - start_time, 4))

    def choose_best_move(self, showStats: bool = False) -> int:
        bestMove = None
        highestN = 0
        for move in self.actualState.children.keys():
            if self.actualState.children[move].N > highestN:
                highestN = self.actualState.children[move].N
                bestMove = move
        if showStats:
            self.print_childrenStats(bestMove)
        self.actualState = self.actualState.children[bestMove]
        self.actualState.parent = None    # Clears the parent Node from memory
        self.currentState.parent = None   # Definetely clears the parent Node from memory  
        gc.collect()
        return bestMove

    def print_childrenStats(self, bestMove: int):
        for move, child in self.actualState.children.items():
            if move == bestMove:
                print(f"\033[93m{move}: {child.Q} / {child.N}\033[0m")
            else:
                print(f"{move}: {child.Q} / {child.N}")

class Node1:
    def __init__(self, parent: 'Node', move: int, depth: int):
        self.Q = 0
        self.N = 0
        self.depth = depth
        if self.depth % 2 == 1:
            self.playerTurn = "O"
        else:
            self.playerTurn = "X"
        self.move = move
        self.parent = parent
        self.children = {}

class MctsAlgo1:
    def __init__(self, C: float = math.sqrt(2), reset: bool = True, connect4: Connect41 = Connect41(6, 7), drawValue: float = 0):
        self.C = C
        self.root = Node1(None, None, 0)
        self.connect4 = connect4
        self.currentState = self.root
        self.iteration = 0
        self.actualState = self.root
        self.resetTree = reset
        self.drawValue = drawValue
        self.runTimes = []

    def reset(self, connect4Actual: Connect4):
        self.connect4.reset(connect4Actual.state, connect4Actual.turn)
        self.currentState = self.actualState

    def selection_phase(self) -> None:
        valuesForEachChildren = {}
        promissingChildren = []
        childrenWithNZero = []
        self.currentState = self.actualState

        #trying to find a node without children
        while len(self.currentState.children) != 0:
            valuesForEachChildren = {}
            promissingChildren = []
            childrenWithNZero = []
            bestValue = -1
            for move in self.currentState.children.keys():
                if self.currentState.children[move].N > 0:
                    valuesForEachChildren[move] = self.upper_confidence_bound(self.currentState.children[move])
                    if valuesForEachChildren[move] > bestValue:
                        promissingChildren.clear()
                        promissingChildren.append(move)
                        bestValue = valuesForEachChildren[move]
                    elif valuesForEachChildren[move] == bestValue:
                        promissingChildren.append(move)
                else:
                    childrenWithNZero.append(move)
            if len(childrenWithNZero) > 0:
                randomChoice = random.choice(childrenWithNZero)    
                self.updateMCTSState(randomChoice)
                self.connect4.updateGameState(randomChoice)
                return
            randomChoice = random.choice(promissingChildren)
            self.updateMCTSState(randomChoice)
            self.connect4.updateGameState(randomChoice)

        return

    def expansion_phase(self) -> bool:
        isGameFinished = self.connect4.checkGameOver()
        if isGameFinished:
            return False
        availableMoves = self.connect4.checkAvailableMoves()
        for move in availableMoves:
            self.currentState.children[move] = Node1(self.currentState, move, self.currentState.depth + 1)
        return True

    def simulation_phase(self, wasExpansionSuccessful: bool) -> str:
        if wasExpansionSuccessful == False:
            gameResult = self.connect4.checkGameResult()
            return gameResult
        moves = [key for key in self.currentState.children.keys()]
        randomChoice = random.choice(moves)
        self.updateMCTSState(randomChoice)
        self.connect4.updateGameState(randomChoice)
        while not self.connect4.checkGameOver():
            self.connect4.updateGameState(random.choice(self.connect4.checkAvailableMoves()))
        gameResult = self.connect4.checkGameResult()
        return gameResult
        
    def backPropagation_phase(self, gameResult: str):
        while self.currentState != self.actualState:
            self.currentState.N += 1
            if self.currentState.playerTurn == gameResult:
                self.currentState.Q += 1
            elif gameResult == "-":
                self.currentState.Q += self.drawValue
            self.currentState = self.currentState.parent
        self.currentState.N += 1
        if self.currentState.playerTurn == gameResult:
            self.currentState.Q += 1
        elif gameResult == "-":
            self.currentState.Q += self.drawValue
        self.iteration += 1

    def updateMCTSState(self, move: int):
        self.currentState = self.currentState.children[move]
        
    def upper_confidence_bound(self, node: Node1) -> int:
        return (node.Q / node.N) + (self.C * math.sqrt((math.log(node.parent.N) / node.N)))

    def updateAfterAdversaryTurn(self, connect4Actual: Connect4, moveBefore: int):
        if len(self.actualState.children) == 0: 
            self.reset(connect4Actual)
            self.expansion_phase()                
        self.actualState = self.actualState.children[moveBefore]
    
    def run_mcts(self, iterations: int, connect4Actual: Connect4, moveBefore: int = None):
        start_time = time.time()  # Start timing
        if self.resetTree:
            self.actualState.children = {}   # Resets tree by clearing every child node
            self.currentState.children = {}  # Definetely resets tree by clearing every child node
            gc.collect()
        if len(self.actualState.children) == 0: 
            self.reset(connect4Actual)
            self.expansion_phase()
        for i in range(iterations):
            self.reset(connect4Actual)
            self.selection_phase()
            wasExpansionSuccessful = self.expansion_phase()
            gameResult = self.simulation_phase(wasExpansionSuccessful)
            self.backPropagation_phase(gameResult)
        end_time = time.time()  # End timing
        self.runTimes.append(round(end_time - start_time, 4))
        print(f"{round(end_time - start_time, 4)}")

    def choose_best_move(self, showStats: bool = False) -> int:
        bestMove = None
        highestN = 0
        for move in self.actualState.children.keys():
            if self.actualState.children[move].N > highestN:
                highestN = self.actualState.children[move].N
                bestMove = move
        if showStats:
            self.print_childrenStats(bestMove)
        self.actualState = self.actualState.children[bestMove]
        self.actualState.parent = None    # Clears the parent Node from memory
        self.currentState.parent = None   # Definetely clears the parent Node from memory  
        gc.collect()
        return bestMove

    def print_childrenStats(self, bestMove: int):
        for move, child in self.actualState.children.items():
            if move == bestMove:
                print(f"\033[93m{move}: {child.Q} / {child.N}\033[0m")
            else:
                print(f"{move}: {child.Q} / {child.N}")