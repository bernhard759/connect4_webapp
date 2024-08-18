import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import MIN_PLAYER, MAX_PLAYER, SCORE_MATRIX


class ConnectFourGame:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)]  # (6,7) gameboard

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
        Check if a player won the game and return the player number, or return None if there's no winner.
        """
        the_board = list(reversed(self.board))
        for c in range(len(the_board[0])):
            for r in range(len(the_board)):
                if the_board[r][c] == 0:
                    continue
                # Check horizontal
                if (
                    c >= 3
                    and the_board[r][c]
                    == the_board[r][c - 1]
                    == the_board[r][c - 2]
                    == the_board[r][c - 3]
                ):
                    return the_board[r][c]
                # Check vertical
                if (
                    r >= 3
                    and the_board[r][c]
                    == the_board[r - 1][c]
                    == the_board[r - 2][c]
                    == the_board[r - 3][c]
                ):
                    return the_board[r][c]
                # Check diagonal (type 1)
                if (
                    c >= 3
                    and r >= 3
                    and the_board[r][c]
                    == the_board[r - 1][c - 1]
                    == the_board[r - 2][c - 2]
                    == the_board[r - 3][c - 3]
                ):
                    return the_board[r][c]
                # Check diagonal (type 2)
                if (
                    c <= 3
                    and r >= 3
                    and the_board[r][c]
                    == the_board[r - 1][c + 1]
                    == the_board[r - 2][c + 2]
                    == the_board[r - 3][c + 3]
                ):
                    return the_board[r][c]
        return None

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
        Evaluate the board state and return a score.
        """
        winner = self.check_win()
        if winner is not None:
            return 200 if winner == 2 else -100
        elif self.check_draw():
            return 0
        else:
            return self.simple_heuristic_score()

    def simple_heuristic_score(self):
        """
        Simple heuristic to evaluate the board based on potential two-in-a-rows
        and the centrality of the move (fields in the middle are more valuable).
        """
        score = 0
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == MAX_PLAYER:
                    score += SCORE_MATRIX[r][c]  # Add base score for position
                elif self.board[r][c] == MIN_PLAYER:
                    score -= SCORE_MATRIX[r][
                        c
                    ]  # Subtract base score for opponent position
        return score

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
