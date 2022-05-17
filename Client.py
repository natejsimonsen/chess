import socket
import sys
import threading


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
            self.connected = True
            self.on_connect()
        except ConnectionRefusedError:
            print("The server refused the connection")
            self.stop()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def write(self, msg):
        self.on_write_msg(msg)
        message = msg.encode('utf-8')
        self.sock.send(message)

    def stop(self):
        self.sock.close()
        self.connected = False
        self.on_disconnect()
        sys.exit(0)

    def on_write_msg(self, msg):
        pass

    def on_disconnect(self):
        pass

    def on_connect(self):
        pass

    def on_receive_msg(self, msg):
        pass

    def receive(self):
        while self.connected:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                self.on_receive_msg(msg)
            except OSError:
                self.connected = False
