from BaseServer import BaseServer
from time import sleep

HOST = '127.0.0.1'
PORT = 9000


class GameServer(BaseServer):
    def __init__(self, host, port, num_players):
        super().__init__(host, port)
        self.num_players = num_players
        self.game = []
        self.turn = "White"
        self.generate_board()

    def generate_board(self, string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        # capital is White, lowercase is black
        # r is rook
        # k is king
        # q is queen
        # p is pawn
        # b is bishop
        # n is knight

        # generate empty grid
        for _ in range(8):
            self.game.append(["" for _ in range(8)])

        # generate special black pieces
        self.game[0][0] = "r"
        self.game[0][1] = "n"
        self.game[0][2] = "b"
        self.game[0][3] = "q"
        self.game[0][4] = "k"
        self.game[0][5] = "b"
        self.game[0][6] = "n"
        self.game[0][7] = "r"

        # generate black pawns
        for i in range(8):
            self.game[1][i] = "p"

        # generate special white pieces
        self.game[7][0] = "R"
        self.game[7][1] = "N"
        self.game[7][2] = "B"
        self.game[7][3] = "Q"
        self.game[7][4] = "K"
        self.game[7][5] = "B"
        self.game[7][6] = "N"
        self.game[7][7] = "R"

        # generate white pawns
        for i in range(8):
            self.game[6][i] = "P"

    def on_server_init(self):
        print("Server initialized")

    def on_client_connect(self, client, address):
        if self.num_players > len(self.players):
            self.broadcast(f"NewPlayerConnectionEvent:Client at {address} joined the game", client)
            client.send("SuccessfulConnectionEvent:Joined the game successfully".encode('utf-8'))
            player_type = "White" if len(self.players) == 0 else "Black"
            # sleep needed otherwise the messages get sent as one message
            # TODO use asynccore rather than threading for more reliable messaging
            sleep(0.001)
            client.send(f"PlayerType:{player_type}".encode('utf-8'))
            return True
        else:
            client.send(f"ServerFullError:already {self.num_players} in the game".encode('utf-8'))
            return False

    def on_client_disconnect(self, client, address):
        self.broadcast(f"DisconnectEvent:Client at {address} left the game", client)

    def on_receive_msg(self, client, address, msg):
        if "UpdateGame:" in msg:
            type_length = 11
            turn = "Black" if self.turn == "White" else "White"
            self.turn = turn
            new_game = "UpdateGame:" + msg[type_length:] + "*" + turn

            # update the other player
            self.broadcast(new_game, client)


if __name__ == "__main__":
    server = GameServer(HOST, PORT, 2)
    server.start()
