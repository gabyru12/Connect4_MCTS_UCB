import math

# |---------------------------------------------------------|
# | https://www.harrycodes.com/blog/monte-carlo-tree-search |
# |---------------------------------------------------------|

class GameMeta:
    PLAYERS = {'none': 0, 'one': 1, 'two': 2}
    OUTCOMES = {'none': 0, 'one': 1, 'two': 2, 'draw': 3}
    INF = float('inf')
    ROWS = 6
    COLS = 7


class MCTSMeta:
    EXPLORATION = math.sqrt(2)
