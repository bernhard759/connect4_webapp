class ConnectFourGame:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)] # (6,7) gameboard

    def make_move(self, column, player):
        """
        Makes a move on the gameboard and returns True if the move was valid and could be made.
        """
        for row in reversed(self.board):
            if row[column] == 0:
                row[column] = player
                return True
        return False

    def undo_move(self, column):
        """
        Reverts the most recent move in the specified column.
        """
        for row in self.board:
            if row[column] != 0:
                row[column] = 0
                break

    def check_win(self):
        """
        Check if a player won the game.
        """
        the_board = list(reversed(self.board))
        # check if any player has four tokens in a row
        for c in range(len(the_board[0])):
            for r in range(len(the_board)):
                # do not check empty cells
                if the_board[r][c] == 0:
                    continue
                # check for horizontal lines
                if c >= 3 and the_board[r][c] == the_board[r][c-1] == the_board[r][c-2] == the_board[r][c-3]:
                    return True
                # check for vertical lines
                if r >= 3 and the_board[r][c] == the_board[r-1][c] == the_board[r-2][c] == the_board[r-3][c]:
                    return True
                # check for diagonal lines (type 1)
                if c >= 3 and r >= 3 and the_board[r][c] == the_board[r-1][c-1] == the_board[r-2][c-2] == the_board[r-3][c-3]:
                    return True
                # check for diagonal lines (type 2)
                if c <= 3 and r >= 3 and the_board[r][c] == the_board[r-1][c+1] == the_board[r-2][c+2] == the_board[r-3][c+3]:
                    return True
        return False
        

    def check_draw(self):
        """
        Check if the game is a draw then return True else False.
        """
        for col in range(len(self.board[0])):
            if self.board[0][col] == 0:
                return False
        return True


    def evaluate_board(self):
        """
        Evaluate the board's current state and return a score.
        This is a basic heuristic evaluation function.
        """
        # Basic heuristic: +100 for a win, -10 for a loss, 0 otherwise
        if self.check_win():
            return 100
        elif self.check_draw():
            return 0
        else:
            return -10


    def is_full(self, column):
        """
        Check if a column is full.
        """
        return self.board[0][column] != 0


    def get_valid_moves(self):
        """
        Return a list of columns that are not full.
        """
        return [c for c in range(7) if not self.is_full(c)]

