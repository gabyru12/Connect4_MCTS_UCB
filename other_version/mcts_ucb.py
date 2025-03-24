import math
from connect4API import *
import random

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
    def __init__(self, C: int, connect4: Connect4 = Connect4(6, 7)):
        self.C = C
        self.root = Node(None, None, 0)
        self.connect4 = connect4
        self.currentState = self.root
        self.iteration = 0
        self.actualState = self.root

    def reset(self):
        self.connect4.reset()
        self.currentState = self.root

    def selection_phase(self):
        valuesForEachChildren = {}
        promissingChildren = []
        childrenWithNZero = []
        bestValue = -1
        self.currentState = self.actualState

        #trying to find a node without children
        while len(self.currentState.children) != 0:
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
        while self.currentState != self.root:
            self.currentState.N += 1
            if(self.currentState.playerTurn == gameResult):
                self.currentState.Q += 1
            self.currentState = self.currentState.parent
        self.currentState.N += 1
        self.iteration += 1

    def updateMCTSState(self, move: int):
        self.currentState = self.currentState.children[move]
        
    def upper_confidence_bound(self, node: Node):
        return node.Q / node.N + self.C * math.sqrt(math.log(node.parent.N) / node.N)

    def run_mcts(self, iterations: int):
        for i in range(iterations):
            self.reset()
            self.selection_phase()
            wasExpansionSuccessful = self.expansion_phase()
            gameResult = self.simulation_phase(wasExpansionSuccessful)
            self.backPropagation_phase(gameResult)

    def choose_best_move(self):
        bestMove = None
        highestN = 0
        for move, child in self.actualState.children.items():
            print(f"{move}: {child.Q} / {child.N}")
        for move in self.actualState.children.keys():
            if self.actualState.children[move].N > highestN:
                highestN = self.actualState.children[move].N
                bestMove = move
        self.actualState = self.actualState.children[bestMove]
        return bestMove

# for move, child in mcts.currentState.children.items():
#     print(f"{move}: {child.Q} / {child.N}")
    
            