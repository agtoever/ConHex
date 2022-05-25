import constants as ct
import logging


class Conhex_game:
    """Representation of a Conhex Game and its state during a game
    """

    def __init__(self) -> None:
        """Initializes an empty Conhex board

        Returns: None
        """
        self.logger = logging.getLogger(ct.LOGGER)
        self.logger.info(f'Started logger for {self.__class__.__name__}')
        self.current_player = ct.BoardPosValue.PLAYER1
        self._board = {pos: ct.BoardPosValue.EMPTY
                       for pos in ct.POSITIONS}
        self.cells_conquered = {
            ct.BoardPosValue.PLAYER1: set(),
            ct.BoardPosValue.PLAYER2: set(),
            ct.BoardPosValue.EMPTY: set(ct.CELLS)
        }
        self.winner = ct.BoardPosValue.EMPTY
        self.moves = []
        self.player_names = dict(ct.DEFAULT_PLAYER_NAMES)

    def set_player_names(self, player1_name: str, player2_name: str) -> None:
        self.player_names[ct.BoardPosValue.PLAYER1] = player1_name
        self.player_names[ct.BoardPosValue.PLAYER2] = player2_name

    def next_player(self) -> ct.enum.Enum:
        """Makes the next player the current player

        Returns: the new current player
        """
        if self.current_player == ct.BoardPosValue.PLAYER1:
            self.current_player = ct.BoardPosValue.PLAYER2
        else:
            self.current_player = ct.BoardPosValue.PLAYER1

        self.logger.debug(f'Switched player: {self.current_player=}')
        return self.current_player

    def play_move(self, position: str) -> bool:
        """Play the given move on the board

        Args:
            position (str): position - capital letter + numer
                            MUST be one of ct.POSITIONS
                            the position on the board MUST be empty

        Returns:
            bool: True if the game is won; False if it isn't

        Raises:
            ValueError: if position is not one of ct.POSITIONS
            ValueError: if a move is placed at an empty spot
        """
        self.logger.debug(f'Playing move: {position=}')
        if position not in ct.POSITIONS:
            raise ValueError(f'{position} is not a valid position.')

        if self._board[position] != ct.BoardPosValue.EMPTY:
            raise ValueError(f"Can't play {position}; this position is already"
                             f" taken by {str(self.board[position])}")

        self._board[position] = self.current_player
        self.moves.append(position)
        self._update_cells_conquered(position)
        self.next_player()
        return self.game_won()

    def undo_move(self) -> None:
        """Undoes one move
        """
        if not self.moves:
            return

        position = self.moves.pop()
        self.logger.debug(f'Undoing move: {position}')
        self._board[position] = ct.BoardPosValue.EMPTY
        self.winner = ct.BoardPosValue.EMPTY
        self.next_player()
        self._full_update_cells_conquered()

    def reset(self) -> None:
        """Resets the board to its initial (empty) position
        """
        self.logger.debug('Resetting board')
        self.__init__()

    def _update_cells_conquered(self, position: str) -> None:
        """Updates the conquered cells after position is played

        Args:
            position (str): last played position
        """
        self.logger.debug(f'Updating conquered cells after playing {position}')
        # Check all cells
        for cell, cell_poss in ct.CELLS.items():

            # If the move is in the cell and the cell is not taken yet...
            if (position in cell_poss and
                cell not in (self.cells_conquered[ct.BoardPosValue.PLAYER1] |
                             self.cells_conquered[ct.BoardPosValue.PLAYER2])):

                # Count the number of positions for current player
                positions = sum(self._board[pos] == self._board[position]
                                for pos in cell_poss)

                # If this is more than half of the positions, claim it!
                if positions * 2 >= len(cell_poss):
                    self.cells_conquered[self._board[position]].add(cell)
                    self.cells_conquered[ct.BoardPosValue.EMPTY].remove(cell)

                    self.logger.info(
                        f'After {position=}, {cell=} with points '
                        f'{cell_poss} is added for {self.current_player}; '
                        f'player controls {positions=} points of that cell.'
                        f' Conquered cells are now: {self.cells_conquered=}')

    def _full_update_cells_conquered(self) -> None:
        """Makes a full update of the conquered cells by replaying the game
        """
        self.logger.debug('Replaying game to update conquered cells...')

        stored_moves = list(self.moves)
        self.reset()
        for move in stored_moves:
            self.play_move(move)

    def game_won(self) -> bool:
        """ Checks if the game is won by one of the players
            Winning player is stored in self.winner

        Returns:
            bool: True if the game is won; False if it isn't
        """
        if self.winner is not ct.BoardPosValue.EMPTY:
            return True

        for player, cell_dim in [(ct.BoardPosValue.PLAYER1, 1),
                                 (ct.BoardPosValue.PLAYER2, 0)]:
            self.logger.debug(f'Checking if {player=} has won...')
            player_cells = self.cells_conquered[player]

            # Do a quick check to see if player has a cell in exactly 2 sides
            if len({cell[cell_dim] for cell in player_cells
                   if (cell[cell_dim] <= ct.CELL_LOW_DIM
                       or cell[cell_dim] >= ct.CELL_HIGH_DIM)}) == 2:
                self.logger.debug(f'{player} had no cells at both borders')
                continue  # go to the next player in the for loop

            # Loop over each of the player's cell in the top or left row
            for cell in (cell for cell in player_cells
                         if cell[cell_dim] <= ct.CELL_LOW_DIM):
                # Keep adding points to the set of positions that are adjacent
                # to the cell until no more cells can be added. Also keep
                # track of the connected cells.
                connected_cells = set()
                pos_cloud = set(ct.CELLS[cell])
                cell_count = -1

                # Loop while cells are added in the loop
                while len(connected_cells) > cell_count:
                    cell_count = len(connected_cells)

                    # Loop over all the player's cells
                    for other_cell in player_cells:
                        # Loop over all positions of that player's cell
                        for pos in ct.CELLS[other_cell]:
                            # check if other_cell is adjacent to the cells
                            # connected to cell - we check this by matching
                            # positions iteratively between cell and other_cell
                            if pos in pos_cloud:
                                # Add position
                                pos_cloud |= set(ct.CELLS[other_cell])

                                # Add cell
                                connected_cells.add(other_cell)

                                # Break the loop; cell and pos's already added
                                break

                self.logger.debug(f'For {player=}, all points connected to '
                                  f'{cell} are: {connected_cells}')

                # Check if we can reach the other side
                if any(True for cell in connected_cells
                       if cell[cell_dim] == ct.CELL_HIGH_DIM):
                    self.logger.info(f'{player} has won!')
                    self.winner = player
                    return True

        self.logger.info('None of the players has won yet...')
        return False

    def free_positions(self) -> list:
        """Gives a list of free (non-empty) positions

        Returns:
            list: list of positions (capital letter + number)
        """
        return [pos for pos in ct.POSITIONS
                if self._board[pos] == ct.BoardPosValue.EMPTY]

    def __str__(self) -> str:
        """Returns a string representation of the board

        Returns:
            str: string representation of the board
        """
        result = ''

        # Generate board and plot positions
        for segment, pos in zip(ct.BOARD_ASCII_SEGMENTS, ct.POSITIONS):
            result += segment
            if self._board[pos] == ct.BoardPosValue.EMPTY:
                pos_char = 'O'
            else:
                pos_char = str(self._board[pos])[-1]
            result += pos_char

        # Replace cell coordinates with correct string values
        for x, y in ct.CELLS:
            for owner in ct.BoardPosValue:
                if (x, y) in self.cells_conquered[owner]:
                    result = result.replace(f'{x},{y}', ct.ASCII_CELL[owner])
                    break  # break out of inner for loop

        return result + '\n'

    def load(self, filename: str) -> None:
        """Loads a game from a txt file in LittleGolem format

        Args:
            filename (str): file name of the file to be loaded

        Raises:
            ValueError: if the signature is not found in the file
            ValueError: if file is empty
            ValueError: if the player names or moves could not be read
        """

        # Only first (and only) line is relevant
        with open(filename, 'r') as file:
            content = file.readline()
            self.logger.debug(f'Read file {filename}: {content}')

        if not content:
            raise ValueError(f'Could not read file {filename}; no content.')

        if ct.READ_MARKERS['SIGNATURE'] not in content:
            raise ValueError(f"Signature '{ct.READ_MARKERS['SIGNATURE']}' not "
                             f"found in file {filename}")

        # Parse player names
        try:
            # Find indices where player names start
            player_idx = [content.find(key)
                          for key in ct.READ_MARKERS['PLAYERS'].values()]

            # Extract player names
            player_names = [content[idx + 3:content.find(']', idx)]
                            for idx in player_idx]

            self.logger.debug(f'Read player names: {player_names}')

        except Exception:
            raise ValueError(f'Could not read player names from {filename}')

        # Parse moves
        try:
            # Split the content in fields; then check if the turn markers
            # are in a field. If so, extract the move and put it in the list.
            # This gives a list of moves like ['H5', 'I7', 'H7']
            fields = content.split(ct.READ_MARKERS['FIELD_SEPARATOR'])
            moves = [field[2:field.find(']')] for field in fields
                     if field[:2] in ct.READ_MARKERS['TURNS']]
        except Exception:
            raise ValueError(f'Could not read moves from {filename}')

        # File is read. Now set the player names and replay the game
        self.reset()
        self.set_player_names(*player_names)
        for move in moves:
            self.play_move(move)

        self.logger.info(f'Successfully read file {filename}')

    def save(self, filename: str) -> None:
        raise NotImplementedError


def main():
    import random
    b = Conhex_game()
    while not b.game_won():
        pos = random.choice(b.free_positions())
        print(f'Playing {pos=} for {str(b.current_player)}')
        b.play_move(pos)

    print(f'The game is won by {b.winner}')
    print(b)

    b.load('/Users/agtoever/Downloads/game2312755.txt')
    print(b)


if __name__ == "__main__":
    main()
