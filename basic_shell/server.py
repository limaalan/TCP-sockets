import socket
from _thread import *

ADDR = 'localhost'
PORT = 6666
senha=1234
userDict={"alan":"1234","teste":"0000","batata":"frita"}

COMMANDS=["connect user,password","pwd","chdir path","getfiles","getdirs","exit"]



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((ADDR, PORT))
serversocket.listen(5)

def handle_login(received):
    response=" "
    logged=0

    #while logged==0  and received != "exit" :
    
    if received.split()[0]!="connect":
        response="Conecte o usuario primeiro.'connect user,senha' "
    else:
        user =  received.split()[1].split(',')[0]
        senha = received.split()[1].split(',')[1]
        #Faz autenticacao
        if user in userDict :
            if senha==userDict[user]:
                response=f"Usuario {user} logado com sucesso"
                logged=1 
            else: 
                response="senha incorreta" 

        else :
            response=f"Usuario {user} não encontrado"
            
    # Uma vez autenticado, realiza comandos
    return response,logged


def threaded_client(clientsocket):
    logged=0
    received=' '

    while received!="exit":
    
        try:
            received = clientsocket.recv(2048).decode()
        except socket.error as e:
            print(e)
            print("CONEXÃO FECHADA")
            clientsocket.close()
            
        print(f"Recebido : {received}")

        if not logged:
            response,logged = handle_login(received)
            clientsocket.sendall(str.encode(response))
        else :
            #Já está logado, agora realizamos os comandos
            response= "Logou!!!"
            if received not in COMMANDS:
               response= "All commands are :"+("\n\t".join(COMMANDS))
            clientsocket.sendall(str.encode(response))



# ------ Main Server Loop ------
while True:
    print("waiting...")
    (clientsocket, address) = serversocket.accept()

    print("Connected to :", address)

    start_new_thread(threaded_client, (clientsocket,))
