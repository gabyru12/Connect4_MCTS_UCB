from ConnectState import ConnectState
from mcts import MCTS

# |---------------------------------------------------------|
# | https://www.harrycodes.com/blog/monte-carlo-tree-search |
# |---------------------------------------------------------|

def play():
    state = ConnectState()
    mcts = MCTS(state)

    while not state.game_over():
        print("Current state:")
        state.print()

        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        state.move(user_move)
        mcts.move(user_move)

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search(3)
        for child in mcts.root.children.values():
            print(f"{child.Q} / {child.N}")

        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.move(move)
        mcts.move(move)

        if state.game_over():
            state.print()
            print("Player two won!")
            break

if __name__ == "__main__":
    play()
