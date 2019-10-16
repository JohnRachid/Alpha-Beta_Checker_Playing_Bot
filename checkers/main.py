from checkers.game import Game
import numpy as np
import copy
from anytree import Node, RenderTree, AnyNode

max_depth = 5


def main():
    game = Game()
    while (not game.is_over()):
        if game.whose_turn() == 1:
            human_move(game)
        else:
            bot_move(game)
        print_game_to_console(game)


def human_move(game):
    print("Possible moves for human ", game.get_possible_moves())
    prompt ="insert move number from list 0 - " + str(len(game.get_possible_moves())-1)
    move_number = int(input(prompt))

    print("player moved to ", game.get_possible_moves()[move_number])
    game.move(game.get_possible_moves()[move_number])


def bot_move(game):
    print("Possible moves for bot ", game.get_possible_moves())

    val,best_move = alphabeta(game, max_depth, float("-inf"), float("inf"), True,game.get_possible_moves()[0])
    print(val)
    print("bot moved to ", best_move)
    print(val)
    game.move(best_move)


def alphabeta(node, depth, alpha, beta, maximizingPlayer,
              best_move):  # used the psudocode provided at: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    # possible_scores
    if depth == 0 or node.is_over():
        return get_game_score(node), best_move
    if maximizingPlayer:
        value = float("-inf")
        for i in range(0, len(node.get_possible_moves())):
            new_game = copy.deepcopy(node)
            new_game.move(node.get_possible_moves()[i])
            new_value,best_move = alphabeta(new_game, depth - 1, alpha, beta, False, best_move)

            value = max(value, new_value)
            if get_game_score(new_game) > value:
                best_move = node.get_possible_moves()[i]
                print(best_move, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = float("inf")
        for i in range(0, len(node.get_possible_moves())):
            new_game = copy.deepcopy(node)
            new_game.move(node.get_possible_moves()[i])
            new_value,best_move = alphabeta(new_game, depth - 1, alpha, beta, True, best_move)

            value = min(value, new_value)#need to do the same as above here
            beta = min(beta, value)
            if get_game_score(new_game) < value:
                best_move = node.get_possible_moves()[i]
            if alpha >= beta:
                break
        return value, best_move


def get_game_score(game):
    player_num = game.whose_turn()
    total_score = 0
    for piece in game.board.pieces:
        if not piece.captured:
            if piece.king and piece.player == player_num:
                total_score = total_score + 20
            elif piece.king:
                total_score = total_score - 20
            if not piece.king and piece.player == player_num:
                total_score = total_score + 5
            elif not piece.king:
                total_score = total_score - 5
    return total_score


def print_game_to_console(game):
    game_state = np.chararray((8, 8), unicode=True)
    game_state[:] = '_'
    for piece in game.board.pieces:
        if piece.player == 1:
            checker_symbol = '⛀'
            king_symbol = '⛁'
        else:
            checker_symbol = '⛂'
            king_symbol = '⛃'
        if not piece.captured:
            if piece.king == 1:
                if piece.get_row() % 2 == 0:
                    game_state[piece.get_row()][piece.get_column() * 2 + 1] = king_symbol
                else:
                    game_state[piece.get_row()][piece.get_column() * 2] = king_symbol
            else:
                # print(piece.get_adjacent_positions(), "", piece.get_row(), piece.get_column())
                if piece.get_row() % 2 == 0:
                    game_state[piece.get_row()][piece.get_column() * 2 + 1] = checker_symbol
                else:
                    game_state[piece.get_row()][piece.get_column() * 2] = checker_symbol

    print(game_state)


if __name__ == "__main__":
    main()
