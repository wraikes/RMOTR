import os
os.chdir('/home/wraikes/Programming/Dojo/RMOTR/tic-tac-toe')

from tic_tac_toe.exceptions import *

# internal helpers
def _position_is_empty_in_board(position, board):
    """
    Checks if given position is empty ("-") in the board.

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)
    :param board: Game board.

    Returns True if given position is empty, False otherwise.
    """    
    
    return board[position[0]][position[1]] == '-'


def _position_is_valid(position):
    """
    Checks if given position is a valid. To consider a position as valid, it
    must be a two-elements tuple, containing values from 0 to 2.
    Examples of valid positions: (0,0), (1,0)
    Examples of invalid positions: (0,0,1), (9,8), False

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)

    Returns True if given position is valid, False otherwise.
    """    
    
    if not isinstance(position, tuple):
        return False
    
    if len(position) != 2:
        return False
    
    return all([pos in range(3) for pos in position])

def _board_is_full(board):
    """
    Returns True if all positions in given board are occupied.

    :param board: Game board.
    """
    return all([pos != '-' for row in board for pos in row])

def _is_winning_combination(board, combination, player):
    """
    Checks if all 3 positions in given combination are occupied by given player.

    :param board: Game board.
    :param combination: Tuple containing three position elements.
                        Example: ((0,0), (0,1), (0,2))

    Returns True of all three positions in the combination belongs to given
    player, False otherwise.
    """
    return all([board[x][y] == player for x, y in combination])


def _check_winning_combinations(board, player):
    """
    There are 8 posible combinations (3 horizontals, 3, verticals and 2 diagonals)
    to win the Tic-tac-toe game.
    This helper loops through all these combinations and checks if any of them
    belongs to the given player.

    :param board: Game board.
    :param player: One of the two playing players.

    Returns the player (winner) of any of the winning combinations is completed
    by given player, or None otherwise.
    """
    
    diag_1 = tuple((i, i) for i in range(3))        
    diag_2 = tuple((i, 2-i) for i in range(3))
    if any([_is_winning_combination(board, x, player) for x in (diag_1, diag_2)]):
        return player
    
    for i in range(3):
        row_combo = tuple((i, col) for col in range(3))
        col_combo = tuple((row, i) for row in range(3))
         
        if any([_is_winning_combination(board, x, player) for x in (row_combo, col_combo)]):
            return player
       
    else:
        return None
    
# public interface
def start_new_game(player1, player2):
    """
    Creates and returns a new game configuration.
    """
    
    return {'player1': player1,
            'player2': player2,
            'board': [['-' for i in range(3)] for j in range(3)],
            'next_turn': player1,
            'winner': None
            }


def get_winner(game):
    """
    Returns the winner player if any, or None otherwise.
    """
    return game['winner']


def move(game, player, position):
    """
    Performs a player movement in the game. Must ensure all the pre requisites
    checks before the actual movement is done.
    After registering the movement it must check if the game is over.
    """
    if game['next_turn'] != player:
        raise InvalidMovement('"{}" moves next.'.format(game['next_turn']))
    
    if game['winner'] or _board_is_full(game['board']):
        raise InvalidMovement('Game is over.')

    if not _position_is_valid(position):
        raise InvalidMovement('Position out of range.')

    if not _position_is_empty_in_board(position, game['board']):
        raise InvalidMovement('Position already taken.')
            
    game['board'][position[0]][position[1]] = player
    game['winner'] = _check_winning_combinations(game['board'], player)
    game['next_turn'] = game['player1'] if player == game['player2'] else game['player2']    
    
    if game['winner']:
        raise GameOver('"{}" wins!'.format(player))        
        
    if _board_is_full(game['board']):
        raise GameOver('Game is tied!')
         
def get_board_as_string(game):
    """
    Returns a string representation of the game board in the current state.
    """
    
    return '\n' + '\n--------------\n'.join(['  |  '.join(game['board'][x]) for x in range(3)]) + '\n'
    

def get_next_turn(game):
    """
    Returns the player who plays next, or None if the game is already over.
    """
    return game['next_turn']
