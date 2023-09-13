import socket
from _thread import *

ADDR = 'localhost'
PORT = 6666
COMMANDS=["connect user,password","pwd","chdir path","getfiles","getdirs","exit"]



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((ADDR, PORT))
serversocket.listen(5)

def handle_response(received):
    response=" "

    if received =="exit":
        clientsocket.close()
    elif received =="connect":
        response = "conected"
    else:
        response= " ".join(COMMANDS)

    return response


def threaded_client(clientsocket):
    while True:
        try:
            received = clientsocket.recv(2048).decode()
            if not received:
                continue

            enviado = handle_response(received)
            clientsocket.sendall(str.encode(enviado))

            print(f"Recebido : {received}")

        except socket.error as e:
            print(e)
            print("CONEXÃO FECHADA")
            clientsocket.close()
            break

# ------ Main Server Loop ------
while True:
    print("waiting...")
    (clientsocket, address) = serversocket.accept()

    print("Connected to :", address)

    start_new_thread(threaded_client, (clientsocket,))
