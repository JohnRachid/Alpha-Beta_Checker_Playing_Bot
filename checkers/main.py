from checkers.game import Game
import numpy as np
import copy
from anytree import Node, RenderTree,AnyNode

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
    move_number = int(input("insert move number from list (EX 0)"))

    print("player moved to ", game.get_possible_moves()[move_number])
    game.move(game.get_possible_moves()[move_number])


def bot_move(game):
    print("Possible moves for bot ", game.get_possible_moves())
    print("bot moved to ", game.get_possible_moves()[0])
    alpha_beta_main(game)
    game.move(game.get_possible_moves()[0])

def alpha_beta_main(game):
    root = AnyNode(game)
    construct_tree(root,0)

def construct_tree(parent,current_depth):
    if current_depth >= max_depth or parent.is_over():
        return
    
    current_depth = current_depth + 1
    for i in range(0, len(parent.get_possible_moves())):
        new_game = copy.deepcopy(parent)
        new_game.move(parent.get_possible_moves()[i])
        new_parent = AnyNode(new_game, parent=parent)
        construct_tree(new_parent,current_depth)

def alphabeta(node, depth, alpha, beta, maximizingPlayer): #used the psudocode provided at: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    # possible_scores
    if depth == 0 or node.is_over():
        return get_game_score(node)
    if maximizingPlayer:
        value = float("inf")
        for child in node.children:
            value = max(value, alphabeta(child,depth-1,alpha,beta,False))
            alpha = max(alpha,value)
            if alpha >= beta:
                break
        return value
    else:
        value = float("-inf")
        for child in node.children:
            value = min(value,alphabeta(child,depth-1,alpha,beta,True))
            beta = min(beta,value)
            if alpha >= beta:
                break
        return value

def get_game_score(game):
    total_score = 0
    for piece in game.board.pieces:
        if not piece.captured and piece.player == 2:
            if piece.king:
                total_score = total_score + 20
            if not piece.king:
                total_score = total_score + 5
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
                print(piece.get_adjacent_positions(), "", piece.get_row(), piece.get_column())
                if piece.get_row() % 2 == 0:
                    game_state[piece.get_row()][piece.get_column() * 2 + 1] = checker_symbol
                else:
                    game_state[piece.get_row()][piece.get_column() * 2] = checker_symbol

    print(game_state)


if __name__ == "__main__":
    main()
