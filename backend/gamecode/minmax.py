import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import MIN_PLAYER, MAX_PLAYER
from game_logic import ConnectFourGame
from copy import deepcopy
import math


class MinimaxAI:
    def __init__(self, depth=4):
        self.depth = depth  # Depth of search for minimax

    def find_best_move(self, board):
        """
        Find the best move using the minimax algorithm.
        Returns a tuple: (best_move, move_scores) where move_scores is a list of tuples (column, score).
        """
        # AI is maximizing player
        best_score = -math.inf
        best_move = None
        move_scores = []

        # Get the game and a copy of the board
        game = ConnectFourGame()
        game.board = deepcopy(board)

        # Try out all valid moves
        for move in game.get_valid_moves():
            # Make move
            game.make_move(move, MAX_PLAYER)
            # Calculate the score
            score = self.minimax(game, self.depth, False)  # Minimize the opponent score
            # Undo move
            game.undo_move(move)

            move_scores.append((move, score))

            # Update score if improvement
            if score > best_score:
                best_score = score
                best_move = move

        return best_move, move_scores

    def minimax(self, game, depth, is_maximizing):
        """
        Minimax algorithm with depth limitation.
        """
        if depth == 0 or game.check_win() or game.check_draw():
            score = game.evaluate_board(MAX_PLAYER if is_maximizing else MIN_PLAYER)
            if not is_maximizing:
                score = -score # Flip score because we always evaluate from the maximizing player view
            # print(f"Depth: {depth}, Is Maximizing: {is_maximizing}, Score: {score}")
            return score

        # Maximizing player
        if is_maximizing:
            best_score = -math.inf
            # Check out all the moves
            for move in game.get_valid_moves():
                # Make move calculate score and then undo
                game.make_move(move, MAX_PLAYER)
                score = self.minimax(game, depth - 1, False)
                game.undo_move(move)
                best_score = max(score, best_score)
            return best_score

        # Minimizing player
        else:
            best_score = math.inf
            for move in game.get_valid_moves():
                # Make move calculate score and then undo
                game.make_move(move, MIN_PLAYER)
                score = self.minimax(game, depth - 1, True)
                game.undo_move(move)
                best_score = min(score, best_score)
            return best_score
