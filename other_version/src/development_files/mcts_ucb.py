import math
from connect4API import *
#from connect4APIslow import *
from copy import deepcopy
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
    def __init__(self, C: float = math.sqrt(2), reset: bool = True, connect4: Connect4 = Connect4(), drawValue: float = 0):
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
        self.connect4.reset(connect4Actual)
        self.currentState = self.actualState

    def updateMCTSState(self, move: int):
        self.currentState = self.currentState.children[move]

    def updateAfterAdversaryTurn(self, connect4Actual: Connect4, moveBefore: int):
        if len(self.actualState.children) == 0: 
            self.reset(connect4Actual)
            self.expansion_phase(checkIfGameFinished=False)          
        self.actualState = self.actualState.children[moveBefore]

    def selection_phase(self) -> None:
        self.currentState = self.actualState

        while self.currentState.children:
            children = self.currentState.children
            unexplored = [move for move, node in children.items() if node.N == 0]
            if unexplored:
                randomChoice = random.choice(unexplored)
                self.updateMCTSState(randomChoice)
                self.connect4.updateGameState(randomChoice)
                return

            # Compute UCB values for all children
            ucb_values = {move: (node.Q / node.N) + (self.C * math.sqrt((math.log(node.parent.N) / node.N))) for move, node in children.items()}
            max_ucb = max(ucb_values.values())
            # In case of ties, randomly choose among the best
            best_moves = [move for move, val in ucb_values.items() if val == max_ucb]
            randomChoice = random.choice(best_moves)
            self.updateMCTSState(randomChoice)
            self.connect4.updateGameState(randomChoice)

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

    def run_mcts(self, iterations: int, connect4Actual: Connect4, dataset = None):
        start_time = time.time()  # Start timing
        if self.resetTree:
            self.actualState.children = {}   # Resets tree by clearing every child node
            self.currentState.children = {}  # Definetely resets tree by clearing every child node
            gc.collect()
        if len(self.actualState.children) == 0: 
            self.reset(connect4Actual)
            self.expansion_phase(checkIfGameFinished=False)
        if dataset is None:
            for i in range(iterations):
                self.reset(connect4Actual)
                self.selection_phase()
                wasExpansionSuccessful = self.expansion_phase(checkIfGameFinished=True)
                gameResult = self.simulation_phase(wasExpansionSuccessful)
                self.backPropagation_phase(gameResult)
        else:
            matrix = self.connect4.bitboard_to_matrix()
            flat_board = self.connect4.flatten_board(matrix)
            for i in range(iterations):
                if i == iterations//5:
                    bestMove = self.choose_best_move(datasetFlag=True)
                    flat_board.append(str(bestMove))
                elif i == iterations//5*2:
                    bestMove = self.choose_best_move(datasetFlag=True)
                    flat_board.append(str(bestMove))
                elif i == iterations//5*3:
                    bestMove = self.choose_best_move(datasetFlag=True)
                    flat_board.append(str(bestMove))
                elif i == iterations//5*4:
                    bestMove = self.choose_best_move(datasetFlag=True)
                    flat_board.append(str(bestMove))
                elif i == iterations//5*5-1:
                    bestMove = self.choose_best_move(datasetFlag=True)
                    flat_board.append(str(bestMove))
    
                self.reset(connect4Actual)
                self.selection_phase()
                wasExpansionSuccessful = self.expansion_phase(checkIfGameFinished=True)
                gameResult = self.simulation_phase(wasExpansionSuccessful)
                self.backPropagation_phase(gameResult)
            dataset.append(flat_board)
        end_time = time.time()  # End timing
        self.runTimes.append(round(end_time - start_time, 4))

    def choose_best_move(self, showStats: bool = False, datasetFlag: bool = False, testSoftMax: bool = False, temperature: float = 0.5) -> int:
        def stable_softmax(visits, temperature):
            if temperature == 0:
                max_index = visits.index(max(visits))
                return [1 if i == max_index else 0 for i in range(len(visits))]

            # Apply log for better smoothing and scaling
            scaled = [math.log(v + 1) / temperature for v in visits]
            max_scaled = max(scaled)
            exp_values = [math.exp(s - max_scaled) for s in scaled]
            total = sum(exp_values)
            return [ev / total for ev in exp_values]

        if testSoftMax:
            # Use softmax sampling
            moves = list(self.actualState.children.keys())
            visit_counts = [self.actualState.children[move].N for move in moves]
            probabilities = stable_softmax(visit_counts, temperature)
            bestMove = random.choices(moves, weights=probabilities, k=1)[0]
            if showStats:
                self.print_childrenStats(bestMove, probabilities)
            self.actualState = self.actualState.children[bestMove]
            self.actualState.parent = None
            self.currentState.parent = None
            gc.collect()
        elif datasetFlag:
            # Use softmax sampling
            bestMove = max(self.actualState.children.items(), key=lambda item: item[1].N)[0]
        else:
            # Choose the move with highest visit count
            bestMove = max(self.actualState.children.items(), key=lambda item: item[1].N)[0]
            if showStats:
                self.print_childrenStats(bestMove)
            # Update internal state
            self.actualState = self.actualState.children[bestMove]
            self.actualState.parent = None
            self.currentState.parent = None
            gc.collect()

        return bestMove

    def print_childrenStats(self, bestMove: int, probabilities: list[int] = None):
        for move, child in self.actualState.children.items():
            if move == bestMove:
                if probabilities is None:
                    print(f"\033[93m{move}: {child.Q:>7} / {child.N:<7}\033[0m")
                else:
                    print(f"\033[93m{move}: {child.Q:>7} / {child.N:<7}\t{round(probabilities[list(self.actualState.children).index(move)], 2)}%\033[0m")
            else:
                if probabilities is None:
                    print(f"{move}: {child.Q:>7} / {child.N:<7}")
                else:
                    print(f"{move}: {child.Q:>7} / {child.N:<7}\t{round(probabilities[list(self.actualState.children).index(move)], 2)}%")
