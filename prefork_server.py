import os
import socket
import select
import signal
from makeResponse import do_response


childrens_pull = []


class ChildController:
    def __init__(self, pipe):
        self.is_free = True
        self.pipe = pipe


def create_child(listen_sock, root):
    child_pipe, parent_pipe = socket.socketpair()
    pid = os.fork()
    if pid == 0:
        child_pipe.close()
        while True:
            connection, adress = listen_sock.accept()
            do_response(connection, root)
            connection.close()
    childrens_pull.append(ChildController(child_pipe))
    parent_pipe.close()


def start(host, port, root, cores):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((host, port))
        soc.listen(1)
        for i in range(cores):
            create_child(soc, root)
        while True:
            to_read = [soc] + [c.pipe.fileno() for c in childrens_pull]
            readables, writables, exceptions = select.select(to_read, [], [])
            if soc in readables:
                for c in childrens_pull:
                    if c.is_free:
                        c.is_free = False
                        break
            for c in childrens_pull:
                if c.pipe.fileno() in readables:
                    c.is_free = True



