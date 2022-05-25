import enum
import logging

#
# User adjustable configuration settings
#
LOG_LEVEL = logging.ERROR


#
# Logging
#
LOGGER = 'conhex'
LOG_FORMAT = ('[%(levelname)s] [%(asctime)s] [%(filename)s:(%(lineno)d] '
              '%(message)s')
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)


#
# Board layout: cells and positions, board dimensions
#
CELLS = {
    (1, 1): ['A1', 'B3', 'C2'],
    (1, 3): ['B3', 'B4', 'B5'],
    (1, 5): ['B5', 'B6', 'B7'],
    (1, 7): ['B7', 'B8', 'B9'],
    (1, 9): ['A11', 'B9', 'C10'],
    (2, 2): ['B3', 'B4', 'C2', 'C4', 'D2', 'D3'],
    (2, 4): ['B4', 'B5', 'B6', 'C4', 'C5', 'C6'],
    (2, 6): ['B6', 'B7', 'B8', 'C6', 'C7', 'C8'],
    (2, 8): ['B8', 'B9', 'C10', 'C8', 'D10', 'D9'],
    (3, 1): ['C2', 'D2', 'E2'],
    (3, 3): ['C4', 'C5', 'D3', 'D5', 'E3', 'E4'],
    (3, 5): ['C5', 'C6', 'C7', 'D5', 'D6', 'D7'],
    (3, 7): ['C7', 'C8', 'D7', 'D9', 'E8', 'E9'],
    (3, 9): ['C10', 'D10', 'E10'],
    (4, 2): ['D2', 'D3', 'E2', 'E3', 'F2', 'F3'],
    (4, 4): ['D5', 'D6', 'E4', 'E6', 'F4', 'F5'],
    (4, 6): ['F4', 'F5', 'G4', 'G6', 'H5', 'H6'],
    (4, 8): ['D10', 'D9', 'E10', 'E9', 'F10', 'F9'],
    (5, 1): ['E2', 'F2', 'G2'],
    (5, 3): ['E3', 'E4', 'F3', 'F4', 'G3', 'G4'],
    (5, 5): ['E6', 'F5', 'F6', 'F7', 'G6'],
    (5, 7): ['E8', 'E9', 'F8', 'F9', 'G8', 'G9'],
    (5, 9): ['E10', 'F10', 'G10'],
    (6, 2): ['F2', 'F3', 'G2', 'G3', 'H2', 'H3'],
    (6, 4): ['D6', 'D7', 'E6', 'E8', 'F7', 'F8'],
    (6, 6): ['F7', 'F8', 'G6', 'G8', 'H6', 'H7'],
    (6, 8): ['F10', 'F9', 'G10', 'G9', 'H10', 'H9'],
    (7, 1): ['G2', 'H2', 'I2'],
    (7, 3): ['G3', 'G4', 'H3', 'H5', 'I4', 'I5'],
    (7, 5): ['H5', 'H6', 'H7', 'I5', 'I6', 'I7'],
    (7, 7): ['G8', 'G9', 'H7', 'H9', 'I7', 'I8'],
    (7, 9): ['G10', 'H10', 'I10'],
    (8, 2): ['H2', 'H3', 'I2', 'I4', 'J3', 'J4'],
    (8, 4): ['I4', 'I5', 'I6', 'J4', 'J5', 'J6'],
    (8, 6): ['I6', 'I7', 'I8', 'J6', 'J7', 'J8'],
    (8, 8): ['H10', 'H9', 'I10', 'I8', 'J8', 'J9'],
    (9, 1): ['I2', 'J3', 'K1'],
    (9, 3): ['J3', 'J4', 'J5'],
    (9, 5): ['J5', 'J6', 'J7'],
    (9, 7): ['J7', 'J8', 'J9'],
    (9, 9): ['I10', 'J9', 'K11']
}

POSITIONS = sorted({position for cell in CELLS.values() for position in cell},
                   key=lambda p: (int(p[1:]), p[0]))

CELL_LOW_DIM = 2   # Row/column 1 *and* 2 lie at the border
CELL_HIGH_DIM = 8  # Row/column 8 *and* 9 lie at the border


#
# Players, default player names and possible values of the board positions
#
class BoardPosValue(enum.Enum):
    """Enum class for defining the state of a position on the board
    """

    def _generate_next_value_(name: str, *_) -> str:
        return name

    EMPTY = enum.auto()
    PLAYER1 = enum.auto()
    PLAYER2 = enum.auto()


DEFAULT_PLAYER_NAMES = {
    BoardPosValue.PLAYER1: 'Player 1',
    BoardPosValue.PLAYER2: 'Player 2',
}


#
# ASCII representation of the board
#
__ASCII_BOARD__ = \
    """   A     B     C     D     E     F     G     H     I     J     K
 1 #-----------+-----------+-----------+-----------+-----------#
   |           |    3,1    |    5,1    |    7,1    |           |
   |           |           |           |           |           |
 2 |   1,1     #-----#-----#-----#-----#-----#-----#     9,1   |
   |         /       |    4,2    |    6,2    |       \         |
   |       /         |           |           |         \       |
 3 +-----#    2,2    #-----#-----#-----#-----#    8,2    #-----+
   |     |         /       |    5,3    |       \         |     |
   |     |       /         |           |         \       |     |
 4 | 1,3 #-----#    3,3    #-----#-----#    7,3    #-----# 9,3 |
   |     |     |         /       |       \         |     |     |
   |     |     |       /         |         \       |     |     |
 5 +-----# 2,4 #-----#    4,4    #    6,4   #------# 8,4 #-----+
   |     |     |     |         /   \        |      |     |     |
   |     |     |     |       /  5,5  \      |      |     |     |
 6 | 1,5 #-----# 3,5 #------#    #    #-----# 7,5  #-----# 9,5 |
   |     |     |     |       \       /      |      |     |     |
   |     |     |     |         \   /        |      |     |     |
 7 +-----# 2,6 #-----#     4,6   #    6,6   #------# 8,6 #-----+
   |     |     |       \         |         /       |     |     |
   |     |     |         \       |       /         |     |     |
 8 | 1,7 #-----#    3,7    #-----#-----#    7,7    #-----# 9,7 |
   |     |       \         |           |         /       |     |
   |     |         \       |    5,7    |       /         |     |
 9 +-----#    2,8    #-----#-----#-----#-----#    8,8    #-----+
   |       \         |           |           |         /       |
   |         \       |    4,8    |    6,8    |       /         |
10 |   1,9     #-----#-----#-----#-----#-----#-----#    9,9    |
   |           |           |           |           |           |
   |           |    3,9    |    5,9    |    7,9    |           |
11 #-----------+-----------+-----------+-----------+-----------#""" \
# noqa: W605  - ignore escape sequence warming for the ascii board

BOARD_ASCII_SEGMENTS = __ASCII_BOARD__.split('#')

ASCII_CELL = {
    BoardPosValue.PLAYER1: '-1-',
    BoardPosValue.PLAYER2: '-2-',
    BoardPosValue.EMPTY: '   ',
}


#
# String markers for reading and writing files
#
READ_MARKERS = {
    'SIGNATURE': 'FF[CONHEX]VA[CONHEX]EV[conhex.ld.CONHEX]',
    'PLAYERS': {
        BoardPosValue.PLAYER1: 'PW',
        BoardPosValue.PLAYER2: 'PB',
    },
    'TURNS': ('B[', 'R['),
    'FIELD_SEPARATOR': ';',
}

#
# GUI strings and board settings
#
CANVAS_SIZE = 800
GRAPH_SCALAR = 10
GRAPH_BOTTOM_LEFT = (0, -12 * GRAPH_SCALAR)
GRAPH_TOP_RIGHT = (12 * GRAPH_SCALAR, 0)
GRAPH_BACKGROUND_COLOR = 'white'
MAIN_WINDOW_TITLE = 'ConHex - a connected game'
CELL_POLYS = {
    (1, 1): [(1, -1), (3, -1), (3, -2), (2, -3), (1, -3), (1, -1)],
    (1, 3): [(1, -3), (2, -3), (2, -5), (1, -5), (1, -3)],
    (1, 5): [(1, -5), (2, -5), (2, -7), (1, -7), (1, -5)],
    (1, 7): [(1, -7), (2, -7), (2, -9), (1, -9), (1, -7)],
    (1, 9): [(1, -9), (2, -9), (3, -10), (3, -11), (1, -11), (1, -9)],
    (2, 2): [(3, -2), (4, -2), (4, -3), (3, -4), (2, -4), (2, -3), (3, -2)],
    (2, 4): [(2, -4), (3, -4), (3, -6), (2, -6), (2, -4)],
    (2, 6): [(2, -6), (3, -6), (3, -8), (2, -8), (2, -6)],
    (2, 8): [(2, -8), (3, -8), (4, -9), (4, -10), (3, -10), (2, -9), (2, -8)],
    (3, 1): [(3, -1), (5, -1), (5, -2), (3, -2), (3, -1)],
    (3, 3): [(4, -3), (5, -3), (5, -4), (4, -5), (3, -5), (3, -4), (4, -3)],
    (3, 5): [(3, -5), (4, -5), (4, -7), (3, -7), (3, -5)],
    (3, 7): [(3, -7), (4, -7), (5, -8), (5, -9), (4, -9), (3, -8), (3, -7)],
    (3, 9): [(3, -10), (5, -10), (5, -11), (3, -11), (3, -10)],
    (4, 2): [(4, -2), (6, -2), (6, -3), (4, -3), (4, -2)],
    (4, 4): [(5, -4), (6, -4), (6, -5), (5, -6), (4, -6), (4, -5), (5, -4)],
    (4, 6): [(4, -6), (5, -6), (6, -7), (6, -8), (5, -8), (4, -7), (4, -6)],
    (4, 8): [(4, -9), (6, -9), (6, -10), (4, -10), (4, -9)],
    (5, 1): [(5, -1), (7, -1), (7, -2), (5, -2), (5, -1)],
    (5, 3): [(5, -3), (7, -3), (7, -4), (5, -4), (5, -3)],
    (5, 5): [(6, -5), (7, -6), (6, -7), (5, -6), (6, -5)],
    (5, 7): [(5, -8), (7, -8), (7, -9), (5, -9), (5, -8)],
    (5, 9): [(5, -10), (7, -10), (7, -11), (5, -11), (5, -10)],
    (6, 2): [(6, -2), (8, -2), (8, -3), (6, -3), (6, -2)],
    (6, 4): [(6, -4), (7, -4), (8, -5), (8, -6), (7, -6), (6, -5), (6, -4)],
    (6, 6): [(7, -6), (8, -6), (8, -7), (7, -8), (6, -8), (6, -7), (7, -6)],
    (6, 8): [(6, -9), (8, -9), (8, -10), (6, -10), (6, -9)],
    (7, 1): [(7, -1), (9, -1), (9, -2), (7, -2), (7, -1)],
    (7, 3): [(7, -3), (8, -3), (9, -4), (9, -5), (8, -5), (7, -4), (7, -3)],
    (7, 5): [(8, -5), (9, -5), (9, -7), (8, -7), (8, -5)],
    (7, 7): [(8, -7), (9, -7), (9, -8), (8, -9), (7, -9), (7, -8), (8, -7)],
    (7, 9): [(7, -10), (9, -10), (9, -11), (7, -11), (7, -10)],
    (8, 2): [(8, -2), (9, -2), (10, -3), (10, -4), (9, -4), (8, -3), (8, -2)],
    (8, 4): [(9, -4), (10, -4), (10, -6), (9, -6), (9, -4)],
    (8, 6): [(9, -6), (10, -6), (10, -8), (9, -8), (9, -6)],
    (8, 8): [(9, -8), (10, -8), (10, -9), (9, -10),
             (8, -10), (8, -9), (9, -8)],
    (9, 1): [(9, -1), (11, -1), (11, -3), (10, -3), (9, -2), (9, -1)],
    (9, 3): [(10, -3), (11, -3), (11, -5), (10, -5), (10, -3)],
    (9, 5): [(10, -5), (11, -5), (11, -7), (10, -7), (10, -5)],
    (9, 7): [(10, -7), (11, -7), (11, -9), (10, -9), (10, -7)],
    (9, 9): [(10, -9), (11, -9), (11, -11), (9, -11), (9, -10), (10, -9)]
}

BORDER_POLYS = {
    BoardPosValue.PLAYER1: [
        [(0, 0), (12, 0), (11, -1), (1, -1), (0, 0)],
        [(1, -11), (11, -11), (12, -12), (0, -12), (1, -11)]
    ],
    BoardPosValue.PLAYER2: [
        [(0, 0), (1, -1), (1, -11), (0, -12), (0, 0)],
        [(11, -1), (12, 0), (12, -12), (11, -11), (11, -1)]
    ]
}

CELL_FILL_COLORS = {
    BoardPosValue.PLAYER1: 'cornflower blue',  # 'slateblue1',
    BoardPosValue.PLAYER2: 'light coral',
    BoardPosValue.EMPTY: 'white',
}

POSITION_FILL_COLORS = {
    BoardPosValue.PLAYER1: 'blue',  # 'slateblue1',
    BoardPosValue.PLAYER2: 'red',
    BoardPosValue.EMPTY: 'white',
}

LINE_COLOR = 'grey'
LINE_WIDTH = 4
POSITION_RADIUS = 0.25 * GRAPH_SCALAR
BOARDNAME = 'ConHex board'

MENU_EXIT = 'Exit'
BUTTON_RESET = 'Reset'
BUTTON_SIZE = (8, 1)


def scale_poly(poly: list) -> list:
    return [(x * GRAPH_SCALAR, y * GRAPH_SCALAR)
            for x, y in poly]


def position_to_xy(position: str) -> tuple:
    return ((ord(position[0]) - 64) * GRAPH_SCALAR,
            -int(position[1:]) * GRAPH_SCALAR)


def xy_to_position(xy: tuple) -> str:
    result = chr(64 + int(xy[0] / GRAPH_SCALAR + .5))
    result += str(-int(xy[1] / GRAPH_SCALAR - 0.5))
    return result


if __name__ == "__main__":
    pass
