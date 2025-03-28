import math
import graphviz
from connect4API import *
import random

class Node:
    def __init__(self, parent: 'Node', move: int, depth: int):
        self.Q = 0
        self.N = 0
        self.depth = depth
        if self.depth % 2 == 1:
            self.playerTurn = "X"
        else:
            self.playerTurn = "O"
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
        while self.currentState != self.actualState.parent:
            self.currentState.N += 1
            if(self.currentState.playerTurn == gameResult):
                self.currentState.Q += 1
            self.currentState = self.currentState.parent
        self.iteration += 1

    def updateMCTSState(self, move: int):
        self.currentState = self.currentState.children[move]
        
    def upper_confidence_bound(self, node: Node) -> int:
        return (node.Q / node.N) + (self.C * math.sqrt((math.log(node.parent.N) / node.N)))

    def run_mcts(self, iterations: int, connect4Actual: Connect4, moveBefore: int = None):
        if(self.iteration == 0): 
            self.expansion_phase()
        if moveBefore != None:
            self.actualState = self.actualState.children[moveBefore]
        for i in range(iterations):
            self.reset(connect4Actual)
            self.selection_phase()
            wasExpansionSuccessful = self.expansion_phase()
            gameResult = self.simulation_phase(wasExpansionSuccessful)
            self.backPropagation_phase(gameResult)

    def choose_best_move(self) -> int:
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

    def visualize_mcts_tree_graphviz(self, root: Node, max_depth=1):
        dot = graphviz.Digraph(comment="MCTS Tree")

        def traverse(node, parent_name=None, depth=0):
            if node is None or depth > max_depth:  # Ensure depth is an integer
                return
            node_label = f"Move: {node.move}\nQ: {node.Q:.1f} / N: {node.N}"
            node_name = f"{node.move}_{depth}_{id(node)}"
            dot.node(node_name, node_label)
            if parent_name:
                dot.edge(parent_name, node_name)
            for child in node.children.values():
                traverse(child, node_name, depth + 1)  # Increment depth correctly

        traverse(root)
        dot.render("mcts_tree", format="png", view=True)  # Saves and opens the tree

if __name__ == "__main__":
    mcts = MctsAlgo(2)
    connect4 = Connect4(6, 7)
    mcts.run_mcts(10000, connect4)
    mcts.visualize_mcts_tree_graphviz(mcts.root)