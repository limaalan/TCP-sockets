import socket
ADDR = 'localhost'
PORT = 6666

COMMANDS=["connect user,password","pwd","chdir path","getfiles","getdirs","exit"]


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ADDR, PORT))

#------- CLIENT MAIN LOOP ----------
print("'help' for commands")

while True:
    msg = str(input("=>"))
    if not msg : continue
    print(f"Sent:{msg}")
    try:
        clientsocket.sendall(str.encode(msg))
        receiving = clientsocket.recv(2048).decode()
        print(f"Received:{receiving}")
    except socket.error as e:
        print(e, "Falha")
        break
