import os
import socket
import errno
import select
from makeResponse import do_response


childrens_pull = []


def start(host, port, root, cores):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((host, port))
    soc.listen(5)
    for i in range(cores):
        pid = os.fork()
        if pid:
            childrens_pull.append(pid)
            while True:
                try:
                    connection, address = soc.accept()
                except IOError as e:
                    code, msg = e.args
                    if code == errno.EINTR:
                        continue
                    else:
                        raise
                do_response(connection, root)
                connection.close()

    soc.close()
    for pid in childrens_pull:
        os.waitpid(pid, 0)