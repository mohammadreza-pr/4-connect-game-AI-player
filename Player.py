from Board import BoardUtility
import numpy as np
import random

MIN = -1_000_000
MAX = 1_000_000


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return random.choice(BoardUtility.get_valid_locations(board))


class HumanPlayer(Player):
    def play(self, board):
        move = int(input("input the next column index 0 to 8:"))
        return move


def minimax(depth, max_depth, game_board: np.ndarray, maximizing_player, alpha, beta, player_piece, enemy_piece,
            last_move):
    if BoardUtility.is_terminal_state(game_board):
        return BoardUtility.score_position(game_board, player_piece), last_move

    if depth == max_depth:
        return BoardUtility.score_position(game_board, player_piece), last_move

    if maximizing_player:
        best = MIN
        best_move = BoardUtility.get_valid_locations(game_board)[0]

        for col in BoardUtility.get_valid_locations(game_board):
            new_board_game = game_board.copy()
            BoardUtility.make_move(new_board_game, col, player_piece)
            val, current_move = minimax(depth + 1, max_depth, new_board_game,
                                        False, alpha, beta, player_piece, enemy_piece, col)
            if val > best:
                best_move = col
            best = max(best, val)
            alpha = max(alpha, best)

            if beta <= alpha:
                break
        return best, best_move
    else:
        best = MAX
        best_move = BoardUtility.get_valid_locations(game_board)[0]

        for col in BoardUtility.get_valid_locations(game_board):
            new_board_game = game_board.copy()
            BoardUtility.make_move(new_board_game, col, enemy_piece)
            val, current_move = minimax(depth + 1, max_depth, new_board_game,
                                        True, alpha, beta, player_piece, enemy_piece, col)
            if val < best:
                best_move = col
            best = min(best, val)
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best, best_move


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def play(self, board: np.ndarray):
        """
        Inputs : 
           board : 7*9 numpy array. 0 for empty cell, 1 and 2 for cells containig a piece.
        return the next move(columns to play in) of the player based on minimax algorithm.
        """
        # Todo: implement minimax algorithm with alpha beta pruning
        enemy_piece = 0
        if self.piece == 1:
            enemy_piece = 2
        else:
            enemy_piece = 1

        val, move = minimax(0, self.depth, board, True, MIN, MAX, self.piece, enemy_piece, 0)
        return move


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def play(self, board):
        """
        Inputs : 
           board : 7*9 numpy array. 0 for empty cell, 1 and 2 for cells containig a piece.
        same as above but each time you are playing as max choose a random move instead of the best move
        with probability self.prob_stochastic.
        """
        # Todo: implement minimax algorithm with alpha beta pruning
        if self.piece == 1:
            enemy_piece = 2
        else:
            enemy_piece = 1
        move = -1
        prob = random.random()
        if prob > self.prob_stochastic:
            val, move = minimax(0, self.depth, board, True, MIN, MAX, self.piece, enemy_piece, 0)
        else:
            move = np.random.choice(BoardUtility.get_valid_locations(board)[:])

        return move
