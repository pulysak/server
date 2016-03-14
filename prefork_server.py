import os
import socket
import time
from makeResponse import do_response


childrens_pull = []


def create_child(listen_sock, root):
    pid = os.fork()
    if pid == 0:
        while True:
            connection, adress = listen_sock.accept()
            do_response(connection, root)
            connection.close()


def start(host, port, root, cores):
        soc = socket.socket()
        soc.bind((host, port))
        soc.listen(1024)
        for i in range(cores):
            create_child(soc, root)
        while True:
            time.sleep(5)


