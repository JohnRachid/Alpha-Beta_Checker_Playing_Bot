from checkers.game import Game
import numpy as np
import copy
import operator
import random

max_depth = 7


def main():
    game = Game()
    game.consecutive_noncapture_move_limit = 100
    while (not game.is_over()):
        if game.whose_turn() == 1:
            human_move(game) #if you want the bot to play for the human replace this line with bot_move(game,desired_depth)
            # bot_move(game, 1)
        else:
            bot_move(game,5)
        print_game_to_console(game)


def human_move(game):
    print("Possible moves for human ", game.get_possible_moves())
    prompt ="insert move number from list 0 - " + str(len(game.get_possible_moves())-1)
    move_number = int(input(prompt))
    if move_number >= len(game.get_possible_moves()):
        print("number out of bounds please provide a number within 0 - ", len(game.get_possible_moves())-1)
        move_number = int(input(prompt))

    print("player moved to ", game.get_possible_moves()[move_number])
    game.move(game.get_possible_moves()[move_number])


def bot_move(game,depth):
    print("Possible moves for bot ", game.get_possible_moves())
    first_moves = []

    for i in range(0, len(game.get_possible_moves())):
        new_game = copy.deepcopy(game)
        new_game.move(game.get_possible_moves()[i])
        val,best_move = alphabeta(new_game, depth, float("-inf"), float("inf"), True,game.get_possible_moves()[0])
        # print(val)
        first_moves.append(val)
    index, value = max(enumerate(first_moves), key=operator.itemgetter(1))
    duplicates = [i for i, x in enumerate(first_moves) if x == value]#isint python just the best?
    print("bot moved to ", game.get_possible_moves()[random.choice(duplicates)])#picks randomly between the elements with the highest values

    # print(val)
    game.move(game.get_possible_moves()[index])


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
                # print(best_move, value)
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
    if game.get_winner() == player_num:
        total_score = total_score + 500
    elif game.is_over():
        total_score = total_score - 500
    for piece in game.board.pieces:
        if not piece.captured:
            if len(piece.get_possible_capture_moves()) > 1:
                total_score = total_score + 20
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
