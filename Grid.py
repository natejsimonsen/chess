import pygame
from Client import Client
import json

images = {
    "b": pygame.image.load("assets/img/b_bishop_png_shadow_128px.png"),
    "k": pygame.image.load("assets/img/b_king_png_shadow_128px.png"),
    "n": pygame.image.load("assets/img/b_knight_png_shadow_128px.png"),
    "r": pygame.image.load("assets/img/b_rook_png_shadow_128px.png"),
    "p": pygame.image.load("assets/img/b_pawn_png_shadow_128px.png"),
    "q": pygame.image.load("assets/img/b_queen_png_shadow_128px.png"),
    "B": pygame.image.load("assets/img/w_bishop_png_shadow_128px.png"),
    "K": pygame.image.load("assets/img/w_king_png_shadow_128px.png"),
    "N": pygame.image.load("assets/img/w_knight_png_shadow_128px.png"),
    "P": pygame.image.load("assets/img/w_pawn_png_shadow_128px.png"),
    "R": pygame.image.load("assets/img/w_rook_png_shadow_128px.png"),
    "Q": pygame.image.load("assets/img/w_queen_png_shadow_128px.png"),
}


class Grid(Client):
    def __init__(self, screen, width, height, host, port):
        super().__init__(host, port)
        self.screen_width = width
        self.screen_height = height
        self.circle_color = pygame.color.Color("#777777")
        self.width = 8
        self.height = 8
        self.square_size = 70
        self.images = {key: pygame.transform.scale(images[key], (self.square_size - 5, self.square_size - 5)) for key in
                       images}
        self.offset_center = (
            (width - self.width * self.square_size) // 2, (height - self.height * self.square_size) // 2)
        self.color = pygame.color.Color("#a47449")
        self.offset_color = pygame.color.Color("#bd9573")
        self.highlight_color = pygame.color.Color("#999999")
        self.bg_color = pygame.color.Color("#000000")
        self.turn = "White"
        self.screen = screen
        self.highlighted_block = (-1, -1)
        self.selected_player = (-1, -1)
        self.type = None
        self.tf = pygame.font.SysFont("Arial", 14)
        self.valid_moves = []
        self.game = []

    # TODO use string param later
    def generate_board(self, string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        # capital is White, lowercase is black
        # r is rook
        # k is king
        # q is queen
        # p is pawn
        # b is bishop
        # n is knight

        # generate empty grid
        for i in range(self.height):
            self.game.append(["" for i in range(self.width)])

        # generate power pieces for black
        self.game[0][0] = "r"
        self.game[0][1] = "n"
        self.game[0][2] = "b"
        self.game[0][3] = "q"
        self.game[0][4] = "k"
        self.game[0][5] = "b"
        self.game[0][6] = "n"
        self.game[0][7] = "r"

        # generate pawns for black
        for i in range(self.width):
            self.game[1][i] = "p"

        # generate power pieces for white
        self.game[7][0] = "R"
        self.game[7][1] = "N"
        self.game[7][2] = "B"
        self.game[7][3] = "Q"
        self.game[7][4] = "K"
        self.game[7][5] = "B"
        self.game[7][6] = "N"
        self.game[7][7] = "R"

        # generate pawns for black
        for i in range(self.width):
            self.game[6][i] = "P"

    def on_write_msg(self, msg):
        pass

    def on_disconnect(self):
        pass

    def on_connect(self):
        pass

    def on_receive_msg(self, msg):
        type_len = len("PlayerType:")
        if "PlayerType:" == msg[:type_len]:
            player_type = msg[type_len:]
            self.type = player_type
            if self.type == "White":
                self.bg_color = pygame.color.Color("#567890")
            else:
                self.bg_color = pygame.color.Color("#a9876f")

        type_len = len("UpdateGame:")
        if "UpdateGame:" == msg[:type_len]:
            game_board, new_turn = msg[type_len:].split("*")
            self.game = json.loads(game_board)
            self.turn = new_turn

    def draw_board(self):
        self.screen.fill(self.bg_color)
        if self.type == "White":
            for row in range(self.width):
                for col in range(self.height):
                    width_offset, height_offset = self.offset_center
                    x, y = width_offset + col * self.square_size, height_offset + row * self.square_size
                    color = self.color if (row + col) % 2 != 0 else self.offset_color

                    # if the box is hovered
                    if row == self.highlighted_block[0] and col == self.highlighted_block[1]:
                        color = self.highlight_color

                    # if the player is selected by the mouse
                    if row == self.selected_player[0] and col == self.selected_player[1]:
                        color = self.highlight_color

                    cell = pygame.Rect(x, y, self.square_size, self.square_size)
                    pygame.draw.rect(self.screen, color, cell)

                    if self.game[row][col]:
                        image = self.images[self.game[row][col]]
                        image_rect = image.get_rect(center=cell.center)
                        self.screen.blit(image, image_rect)

                    if (row, col) in self.valid_moves:
                        pygame.draw.circle(self.screen, self.circle_color, cell.center, self.square_size // 6)

            # draw font for debug purposes
            font_surface = self.tf.render(f"{self.turn}'s turn", True, (0, 0, 0))
            self.screen.blit(font_surface, (10, 10))
        elif self.type == "Black":
            for row in range(self.width):
                for col in range(self.height):
                    width_offset, height_offset = self.offset_center
                    x, y = width_offset + (7 - col) * self.square_size, height_offset + (7 - row) * self.square_size
                    color = self.color if (row + col) % 2 != 0 else self.offset_color

                    # if the box is hovered
                    if row == self.highlighted_block[0] and col == self.highlighted_block[1]:
                        color = self.highlight_color

                    # if the player is selected by the mouse
                    if row == self.selected_player[0] and col == self.selected_player[1]:
                        color = self.highlight_color

                    cell = pygame.Rect(x, y, self.square_size, self.square_size)
                    pygame.draw.rect(self.screen, color, cell)

                    if self.game[row][col]:
                        image = self.images[self.game[row][col]]
                        image_rect = image.get_rect(center=cell.center)
                        self.screen.blit(image, image_rect)

                    if (row, col) in self.valid_moves:
                        pygame.draw.circle(self.screen, self.circle_color, cell.center, self.square_size // 6)

            # draw font for debug purposes
            font_surface = self.tf.render(f"{self.turn}'s turn", True, (0, 0, 0))
            self.screen.blit(font_surface, (10, 10))

    def on_hover(self, event):
        """Handles pygame mousemotion event and highlights a cell"""
        x, y = event.pos
        if pos := self.in_bounds(x, y):
            self.highlighted_block = pos
        else:
            self.highlighted_block = (-1, -1)

    def in_bounds(self, x, y):
        """Returns a boolean if the mouse location is in the viewport"""
        offset_x, offset_y = self.offset_center
        if offset_x < x < (self.screen_width - offset_x) and offset_y < y < (self.screen_height - offset_y):
            return (y - offset_y) // self.square_size, (x - offset_x) // self.square_size
        return None

    # next steps
    # if there are no moves that can save the king, then we have checkmate and end of game
    # I want a function that checks if the king can castle

    def is_in_check(self, board):
        # find the king's coords
        king_coords = None

        for row in range(len(board)):
            for col in range(len(board)):
                cell = board[row][col]
                if self.turn == "White":
                    # if turn is white and King is white, add to king coords
                    if cell == "K":
                        king_coords = (row, col)
                else:
                    if cell == "k":
                        king_coords = (row, col)

        turn = "White" if self.turn == "Black" else "Black"

        # check if any opponent pieces can attack king
        for row in range(len(board)):
            for col in range(len(board)):
                cell = board[row][col]
                if self.turn == "White":
                    if cell.islower():
                        cell_valid_moves = self.get_valid_moves_for_cell(row, col, turn, board)
                        if king_coords in cell_valid_moves:
                            return True
                else:
                    if cell.isupper():
                        cell_valid_moves = self.get_valid_moves_for_cell(row, col, turn, board)
                        if king_coords in cell_valid_moves:
                            return True

        return False

    # FUTURE TODOS
    # I want to eventually add en passant to the game
    # I want to be able to generate a chess game based on a fen string
    # I want to add sound effects
    # I want to add networking so gameplay can be over internet

    # helper function to get legal moves for a cell based on its role
    def get_valid_moves_for_cell(self, row, col, turn, board=None):
        game = self.game
        if board:
            game = board
        valid_coords = []

        def valid_cell(row, col):
            if -1 < row < 8 and -1 < col < 8:
                # if piece is on diff team add to valid coords and then stop
                if turn == "Black" and game[row][col].isupper():
                    valid_coords.append((row, col))
                    return False
                if turn == "White" and game[row][col].islower():
                    valid_coords.append((row, col))
                    return False
                # if piece is on the same team stop
                if turn == "Black" and game[row][col].islower():
                    return False
                if turn == "White" and game[row][col].isupper():
                    return False
                return True
            return False

        # if the row and col is inside the grid
        if -1 < row < 8 and -1 < col < 8:
            cell = game[row][col]
            # black pawn rulesets
            if cell == "p":
                if row == 1 and game[row + 2][col] == "":
                    valid_coords.append((row + 2, col))
                if row < 7:
                    if game[row + 1][col] == "":
                        valid_coords.append((row + 1, col))
                    if col != 7 and game[row + 1][col + 1].isupper():
                        valid_coords.append((row + 1, col + 1))
                    if col != 0 and game[row + 1][col - 1].isupper():
                        valid_coords.append((row + 1, col - 1))

            # white pawn rulesets
            if cell == "P":
                if row == 6 and game[row - 2][col] == "":
                    valid_coords.append((row - 2, col))
                if row > 0:
                    if game[row - 1][col] == "":
                        valid_coords.append((row - 1, col))
                    if col != 7 and game[row - 1][col + 1].islower():
                        valid_coords.append((row - 1, col + 1))
                    if col != 0 and game[row - 1][col - 1].islower():
                        valid_coords.append((row - 1, col - 1))

            # knight moves
            if cell.lower() == 'n':
                if valid_cell(row - 2, col + 1):
                    valid_coords.append((row - 2, col + 1))
                if valid_cell(row - 2, col - 1):
                    valid_coords.append((row - 2, col - 1))
                if valid_cell(row + 2, col + 1):
                    valid_coords.append((row + 2, col + 1))
                if valid_cell(row + 2, col - 1):
                    valid_coords.append((row + 2, col - 1))
                if valid_cell(row - 1, col + 2):
                    valid_coords.append((row - 1, col + 2))
                if valid_cell(row - 1, col - 2):
                    valid_coords.append((row - 1, col - 2))
                if valid_cell(row + 1, col + 2):
                    valid_coords.append((row + 1, col + 2))
                if valid_cell(row + 1, col - 2):
                    valid_coords.append((row + 1, col - 2))

            # bishop moves
            if cell.lower() == "b" or cell.lower() == "q":
                new_row = row
                new_col = col
                while valid_cell(new_row - 1, new_col - 1):
                    valid_coords.append((new_row - 1, new_col - 1))
                    new_row -= 1
                    new_col -= 1
                new_row = row
                new_col = col
                while valid_cell(new_row + 1, new_col + 1):
                    valid_coords.append((new_row + 1, new_col + 1))
                    new_row += 1
                    new_col += 1
                new_row = row
                new_col = col
                while valid_cell(new_row + 1, new_col - 1):
                    valid_coords.append((new_row + 1, new_col - 1))
                    new_row += 1
                    new_col -= 1
                new_row = row
                new_col = col
                while valid_cell(new_row - 1, new_col + 1):
                    valid_coords.append((new_row - 1, new_col + 1))
                    new_row -= 1
                    new_col += 1

            # rook moves
            if cell.lower() == "r" or cell.lower() == "q":
                new_row = row
                new_col = col
                while valid_cell(new_row + 1, new_col):
                    valid_coords.append((new_row + 1, new_col))
                    new_row += 1
                new_row = row
                new_col = col
                while valid_cell(new_row - 1, new_col):
                    valid_coords.append((new_row - 1, new_col))
                    new_row -= 1
                new_row = row
                new_col = col
                while valid_cell(new_row, new_col + 1):
                    valid_coords.append((new_row, new_col + 1))
                    new_col += 1
                new_row = row
                new_col = col
                while valid_cell(new_row, new_col - 1):
                    valid_coords.append((new_row, new_col - 1))
                    new_col -= 1

            # king moves
            if cell.lower() == "k":
                if valid_cell(row + 1, col):
                    valid_coords.append((row + 1, col))
                if valid_cell(row + 1, col + 1):
                    valid_coords.append((row + 1, col + 1))
                if valid_cell(row + 1, col - 1):
                    valid_coords.append((row + 1, col - 1))
                if valid_cell(row - 1, col):
                    valid_coords.append((row - 1, col))
                if valid_cell(row - 1, col + 1):
                    valid_coords.append((row - 1, col + 1))
                if valid_cell(row - 1, col - 1):
                    valid_coords.append((row - 1, col - 1))
                if valid_cell(row, col + 1):
                    valid_coords.append((row, col + 1))
                if valid_cell(row, col - 1):
                    valid_coords.append((row, col - 1))

            return valid_coords

    def simulate_move(self, row, col, new_row, new_col):
        game_copy = [row[:] for row in self.game]

        game_copy[new_row][new_col] = self.game[row][col]
        game_copy[row][col] = ""
        return game_copy

    def check_moves(self, row, col):
        validated_moves = []
        valid_moves = self.get_valid_moves_for_cell(row, col, self.turn)
        for new_row, new_col in valid_moves:
            new_board = self.simulate_move(row, col, new_row, new_col)
            if not self.is_in_check(new_board):
                validated_moves.append((new_row, new_col))
        return validated_moves

    def on_click(self, event):
        # new on_click structure needs to do something like this and only this, it's confusing as hell
        # if pos in bounds
        # set_selected_player()
        # valid_moves = get_valid_moves()
        # self.valid_moves = valid_moves
        # move_player(row, col)

        x, y = event.pos
        if pos := self.in_bounds(x, y):
            new_row, new_col = pos
            if self.turn != self.type:
                pass
            elif self.turn == "White" and self.type == "White":
                # if the piece is white
                if self.game[new_row][new_col].isupper():
                    self.selected_player = pos
                else:
                    pass

                # if the piece is a valid coordinate but doesn't do any player movement validation yet
                if self.selected_player[0] != -1:
                    selected_row, selected_col = self.selected_player
                    valid_moves = self.check_moves(selected_row, selected_col)
                    self.valid_moves = valid_moves

                    # move the player
                    if pos in self.valid_moves and self.type == "White":
                        row, col = self.selected_player
                        player = self.game[row][col]
                        self.game[new_row][new_col] = player
                        self.game[row][col] = ""
                        self.selected_player = (-1, -1)
                        self.valid_moves = []
                        self.turn = "Black"
                        self.write(f"UpdateGame:{json.dumps(self.game)}")

            elif self.turn == "Black" and self.type == "Black":
                # if the piece is black
                if self.game[new_row][new_col].islower():
                    self.selected_player = pos
                else:
                    pass

                # if the piece is a valid coordinate but doesn't do any player movement validation yet
                if self.selected_player[0] != -1:
                    selected_row, selected_col = self.selected_player
                    valid_moves = self.check_moves(selected_row, selected_col)
                    self.valid_moves = valid_moves

                    # move the player
                    if pos in valid_moves and self.type == "Black":
                        row, col = self.selected_player
                        player = self.game[row][col]
                        self.game[new_row][new_col] = player
                        self.game[row][col] = ""
                        self.selected_player = (-1, -1)
                        self.valid_moves = []
                        self.turn = "White"
                        self.write(f"UpdateGame:{json.dumps(self.game)}")

            # destroy test super secret win tactic
            # if self.game[row][col].islower():
            #     self.game[row][col] = ""
