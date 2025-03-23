import math
import connect4API

class Node:
    def __init__(self, parent: Node, move: int):
        self.Q = 0
        self.N = 0
        self.move = move
        self.parent = parent
        self.children = {}

class MctsAlgo:
    def __init__(self, C: int):
        self.C = C
        self.root = Node(None, None)
        self.nodeState = self.root
        self.iteration = 0
        self.depth = 0

    def selection_phase(self, connect4: Connect4):
        if connect4.checkGameOver():
            backPropagation_phase()
            return
        self.depth += 1
        moveValues = {}
        movesWithHighesValue = []
        maxValue = -1
        if len(self.nodeState.children) > 0:
            for move in self.children.keys():
                moveValues[move] = upper_confidence_bound(self.children[move])
                if(moveValues[move] > maxValue): 
                    maxValue = moveValues[move]
            for move, value in moveValues.items():
                if value == maxValue:
                    movesWithHighesValue.append(move)
            chosenMove = random.choice(movesWithHighesValue)
            self.nodeState = self.nodeState.children[chosenMove] 
            selection_phase(connect4)
        else:
            expansion_phase()

    def expansion_phase(self, connect4: Connect4):
        availableMoves = connect4.checkAvailableMoves()
        for move in availableMoves:
            self.nodeState.children[move] = Node(self.state, move)
        simulation_phase()

    def simulation_phase(self, connect4: Connect4):
        boardState = connect4.state
        for move in self.nodeState.children.keys():
            connect4.state = boardState
            connect4.updateState(move)
            newNodeState = self.nodeState.children[move] 
            while not connect4.checkGameOver():
                availableMoves = connect4.checkAvailableMoves()
                chosenMove = random.choice(availableMoves)
                connect4.updateState(chosenMove)
            backPropagation_phase(newBoardState)

    def backPropagation_phase(self, newNodeState: Node):
        pass
        
    def upper_confidence_bound(self, node: Node):
        return node.Q / node.N + self.C * math.sqrt(math.log(node.parent.N) / node.N)
        
            