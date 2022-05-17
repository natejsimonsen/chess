import socket
import threading


class BaseServer:
    """Class that creates a server which can listen to messages and send messages"""
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.players = []

    def broadcast(self, message, ignore_client = None):
        for client in self.players:
            if ignore_client and client != ignore_client:
                client.send(message.encode('utf-8'))

    def handle_messages(self, client, address):
        connected = True
        while connected:
            message = client.recv(1024).decode('utf-8')

            # if the client disconnects
            if len(message) == 0:
                print("Disconnected")
                if client in self.players:
                    self.players.remove(client)
                client.close()
                connected = False
            else:
                self.on_receive_msg(client, address, message)

        self.on_client_disconnect(client, address)

    def on_server_init(self):
        pass

    def on_client_connect(self, client, address):
        pass

    def on_client_disconnect(self, client, address):
        pass

    def on_receive_msg(self, client, address, msg):
        pass

    def start(self):
        # start server
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.on_server_init()

        # listen for connections to server
        while True:
            client, address = self.server.accept()

            connected = self.on_client_connect(client, address)

            if connected:
                self.players.append(client)
                thread = threading.Thread(target=self.handle_messages, args=(client, address))
                thread.start()
