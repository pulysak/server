import socket
from makeResponse import do_response

def start(host, port, root, cores):
    soc = socket.socket()
    soc.bind((host, port))
    # max connections in q
    soc.listen(1)
    while True:
        client_connection, client_address = soc.accept()
        request = client_connection.recv(1024)
        print request
        do_response(client_connection, request, root)
