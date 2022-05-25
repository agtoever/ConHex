import logging
import PySimpleGUI as sg
import conhex_board
import constants as ct


class ConHex_GUI:
    """GUI for the game ConHex
    """

    def __init__(self, board: conhex_board.Conhex_game) -> None:
        """Initializes the GUI. Needs an Conhex_game instance to display

        Args:
            board (conhex_board.Conhex_game): initialized game to display
        """
        self.logger = logging.getLogger(ct.LOGGER)
        self.logger.info(f'Started logger for {self.__class__.__name__}')

        self.board = board

        menu = sg.Menu([[ct.MENU_EXIT]])
        buttons = [[sg.Button(ct.BUTTON_RESET,  ct.BUTTON_SIZE)]]
        self.graph = sg.Graph(canvas_size=(ct.CANVAS_SIZE, ct.CANVAS_SIZE),
                              graph_bottom_left=ct.GRAPH_BOTTOM_LEFT,
                              graph_top_right=ct.GRAPH_TOP_RIGHT,
                              background_color=ct.GRAPH_BACKGROUND_COLOR,
                              key=ct.BOARDNAME,
                              enable_events=True)

        layout = [
            [menu],
            [self.graph],
            [buttons]
        ]

        self.window = sg.Window(ct.MAIN_WINDOW_TITLE, layout, finalize=True)
        self.draw_board()

    def draw_board(self):
        """Redraw the game board
        """
        logging.debug('Redrawing board...')
        # Draw the borders
        for player, poly_list in ct.BORDER_POLYS.items():
            for poly in poly_list:
                self.graph.draw_polygon(ct.scale_poly(poly),
                                        fill_color=ct.CELL_FILL_COLORS[player],
                                        line_color=ct.LINE_COLOR,
                                        line_width=ct.LINE_WIDTH)

        # Draw cells
        for player, cells in self.board.cells_conquered.items():
            for cell in cells:
                self.graph.draw_polygon(ct.scale_poly(ct.CELL_POLYS[cell]),
                                        fill_color=ct.CELL_FILL_COLORS[player],
                                        line_color=ct.LINE_COLOR,
                                        line_width=ct.LINE_WIDTH)

        # draw positions
        for pos, player in self.board._board.items():
            self.graph.draw_circle(center_location=ct.position_to_xy(pos),
                                   radius=ct.POSITION_RADIUS,
                                   fill_color=ct.POSITION_FILL_COLORS[player],
                                   line_color=ct.LINE_COLOR,
                                   line_width=ct.LINE_WIDTH)

        # draw labels
        for value in range(1, 12):
            loc1 = (ct.GRAPH_SCALAR // 2, -value * ct.GRAPH_SCALAR)
            loc2 = (value * ct.GRAPH_SCALAR, -ct.GRAPH_SCALAR // 2)
            self.graph.draw_text(str(value), location=loc1)
            self.graph.draw_text(chr(value + 64), location=loc2)

    def run_eventloop(self) -> None:
        """Event loop of the GUI
        """
        while True:
            event, values = self.window.read()
            self.logger.debug(f'Received {event=} with {values=}')

            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            elif event == ct.BUTTON_RESET:
                self.board.reset()
                self.draw_board()

            elif event == ct.BOARDNAME:
                move = ct.xy_to_position(values[ct.BOARDNAME])
                if move in self.board.free_positions():
                    self.board.play_move(move)
                    self.draw_board()


def main():
    """Mail programm. Creates a game, GUI and runs the GUI's event loop
    """
    game = conhex_board.Conhex_game()
    GUI = ConHex_GUI(game)
    GUI.run_eventloop()


if __name__ == "__main__":
    main()
