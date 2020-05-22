class TicTacToe:

    def __init__(self, n: int):
        """
        Initialize your data structure here.
        """
        self._size = n
        self._rows = [[0,0] for _ in range(n)]
        self._cols = [[0,0] for _ in range(n)]
        self._diagonal = [0,0]
        self._anti_diagonal = [0,0]
        

    def move(self, row: int, col: int, player: int) -> int:
        """
        Player {player} makes a move at ({row}, {col}).
        @param row The row of the board.
        @param col The column of the board.
        @param player The player, can be either 1 or 2.
        @return The current winning condition, can be either:
                0: No one wins.
                1: Player 1 wins.
                2: Player 2 wins.
        """
        p = player - 1
        self._rows[row][p] += 1
        self._cols[col][p] += 1
        if row == col:
            self._diagonal[p] += 1
        if col == len(self._rows) - row - 1:
            self._anti_diagonal[p] += 1
        if any([self._rows[row][p] == self._size,
                    self._cols[col][p] == self._size,
                    self._diagonal[p] == self._size,
                    self._anti_diagonal[p] == self._size]):
                    return player         
        return 0
        


toe = TicTacToe(3)
print(toe.__dict__)
assert toe.move(0, 0, 1) == 0


