""" 
    Aluno: Alan Lima Marques
    Atividade 01 , Exercicio 01
    Data de Criação: 11/09/2023
    Descrição: 
        Neste programa há um servidor que se conecta a um cliente usando sockets TCP , 
        e responde as requisições do cliente. Os comandos disponíveis são :
        CONNECT user, senha - Usuário se autentica e consegue acesso à outros comandos.
        PWD - Caminho absoluto do diretório do servidor.
        CHDIR path - Altera o diretorio em uso
        GETFILES - Recebe uma lista com todos os arquivos no diretorio atual do servidor.
        GETDIRS - Recebe uma lista com todos os diretorios no diretorio atual do servidor.
        EXIT - Finaliza a sessão e a conexao com o servidor.
"""
import socket
import os
from _thread import *

ADDR = 'localhost'
PORT = 6666
senha=1234
userDict={"alan":"1234","teste":"0000","batata":"frita"}

COMMANDS=["connect user,password","pwd","chdir path","getfiles","getdirs","exit"]



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((ADDR, PORT))
serversocket.listen(5)

def handle_commands(received):

    if received =='pwd':
        response = os.getcwd()

    elif "chdir" in received:
        dir = received.split()[1]
        try :
            os.chdir(dir)
            response="SUCCESS"
        except:
            response="ERROR"

    elif "getfiles" in received:
        filecount=0
        files=[]
        for entry in os.scandir():
            if entry.is_file(): 
                filecount+=1
                files.append(entry.name)

        response=str(filecount)+" ".join(files)

    elif "getdirs" in received:
        dircount=0
        dirs=[]
        
        for entry in os.scandir():
            if entry.is_dir(): 
                dircount+=1
                dirs.append(entry.name)

        response=str(dircount)+" ".join(dirs)

    else:
        response= "Command list :\n->"+("\n->".join(COMMANDS))
    
    
    return response



def handle_login(received):
    response=" "
    logged=0

    #while logged==0  and received != "exit" :
    
    if (received.split()[0]!="connect") or (len(received.split())!=2):
        response="Connect user first with .'connect user,senha' "
    else:
        user =  received.split()[1].split(',')[0]
        senha = received.split()[1].split(',')[1]
        #Auth user
        if user in userDict :
            if senha==userDict[user]:
                response=f"User {user} logged sucessfully"
                logged=1 
            else: 
                response="Wrong password" 

        else :
            response=f"User {user} not found"
            
    return response,logged


def threaded_client(clientsocket):
    logged=0
    received=' '
    current_path=os.getcwd()


    while True:
            
        try:
            received = clientsocket.recv(2048).decode()
        except socket.error as e:
            print(e)
            print("CONEXÃO FECHADA")
            clientsocket.close()
        if received=="exit": break
        print(f"Received : {received}")

        if not logged:
            response,logged = handle_login(received)
            clientsocket.sendall(str.encode(response))
        else :
            #User logged, now we handle the commands
            
            response=handle_commands(received)
            clientsocket.sendall(str.encode(response))
    
    print("Connection Closed")
    clientsocket.close()



# ------ Main Server Loop ------
while True:
    print("waiting...")
    (clientsocket, address) = serversocket.accept()

    print("Connected to :", address)

    start_new_thread(threaded_client, (clientsocket,))
