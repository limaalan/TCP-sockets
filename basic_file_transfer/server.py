""" 
    Aluno: Alan Lima Marques
    Atividade 01 , Exercicio 02
    Data de Criação: 24/09/2023
    Descrição: 
         Descrição: 
        Neste programa há um servidor que se conecta à um servidor usando sockets TCP , 
        e manda mensagens para realizar requisições. Os comandos disponíveis são :
        -> ADDFILE (1): adiciona um arquivo novo.
        -> DELETE (2): remove um arquivo existente.
            Status : 1 ok , 2 erro , 3 no file to delete
        -> GETFILESLIST (3): retorna uma lista com o nome dos arquivos.
            Status : 1 ok , 2 erro , 3 no files to list
        -> GETFILE (4): faz download de um arquivo.


PROTOCOLO : 
    Request :
    [Message Type] [Command ident]  [Filename Size] [Filename]  + Específicos
    (1 byte)            (1 byte)        (1 byte)   (0-255 bytes)

    Response:
    [Message Type] [Command ident]  [Status Code] + Específicos 
    (1 byte)            (1 byte)        (1 byte)  

"""
import socket
import os
from _thread import *

ADDR = 'localhost'
PORT = 6666


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serversocket.bind((ADDR, PORT))
serversocket.listen(20)

# ---- A thread for each client ---
def threaded_client(clientsocket):

    while True:
        msg = clientsocket.recv(3)

        # Extraindo informacoes segundo o protocolo
        messageType = int(msg[0])
        commandIdentif = int(msg[1])
        fileNameSize = int(msg[2])

        nomeArquivo = b''
        for _ in range(fileNameSize):
            bytes = clientsocket.recv(1)
            nomeArquivo += bytes
        #nomeArquivo = nomeArquivo.decode('utf-8')
        nomeArquivo = nomeArquivo.decode()

        print(f"Messagetype {messageType}, command {commandIdentif}, fnsize {fileNameSize}, nome_arquivo {nomeArquivo}")

        # ADDFILE
        if(messageType == 1 and commandIdentif == 1):
            print("stop 1")
            debug = clientsocket.recv(4)
            print(f"recebido {debug}")
            tamanhoArquivo = int.from_bytes(debug, byteorder='big')
            print(f"tamanho arquivo {tamanhoArquivo}")
            # Recebe o arquivo
            arquivo = b''
            for _ in range(tamanhoArquivo):
                bytes = clientsocket.recv(1)
                print(f"stop 2 {bytes}")
                arquivo += bytes
            
            # Salva o arquivo
            print("stop 31")
            with open('server_directory/' + nomeArquivo, 'w+b') as file:
                file.write(arquivo)
            print("stop 32")

            # Preparo a resposta
            resposta = bytearray(3)
            resposta[0] = 2 #MESSAGE TYPE = RESPONSE
            resposta[1] = 1 #COMMAND IDENTIF = 1 ( ADD )
            
            #arquivos = os.listdir(path='./server_files')
            #resposta[2] = 1 if os.path.isfile('/server_directory'+nomeArquivo) else 2
            print("stop 4")
            if (os.path.isfile('server_directory/'+nomeArquivo)):
                resposta[2] = 1 # STATUS OK
            else:
                resposta[2] = 2 # STATUS FAILED
            print("stop 5")
            clientsocket.send(resposta)
            print("stop 6")

        # DELETE
        if(messageType == 1 and commandIdentif == 2):
            #arquivos = os.listdir(path='server_directory')
            print("a1")
            
            resposta = bytearray(3)
            resposta[0] = 2
            resposta[1] = 2
            print("a2")

            # caso o arquivo exista no diretorio
            if (os.path.isfile('server_directory/'+nomeArquivo)): 
                print("a3")               
                # remove arquivo  
                os.remove('server_directory/' + nomeArquivo)
                print("a4")
                # verifica se realmente foi excluido
                resposta[2] = 2 if os.path.isfile('server_directory/'+nomeArquivo) else 1
                print(f"a5{resposta[2]}")
            else :
                resposta[2]=3

            print(f"a6 {resposta[2]}")
            clientsocket.send(resposta)
            print("a7")

        # GETFILESLIST
        if(messageType == 1 and commandIdentif == 3):
            resposta=bytearray(3)
            resposta[0]=2
            resposta[1]=3

            arquivos=os.listdir("server_directory")
            resposta[2]=1 if len(arquivos)>0 else 3 # Status "no files to list"
            clientsocket.send(resposta)
            clientsocket.send(len(arquivos).to_bytes(2, byteorder='big'))
            
            for arquivo in arquivos:
                if len(arquivo)<256:
                    clientsocket.send(len(arquivo).to_bytes(1,byteorder='big'))
                    #for nome in arquivo:
                    #    byte=str.encode(nome)
                    #    clientsocket.send(byte)
                    
                    clientsocket.send(arquivo.encode())

        # GETFILE
        if(messageType == 1 and commandIdentif == 4):
            pass

    clientsocket.close()



# ------  Server Main Loop ------
while True:
    print("waiting...")
    (clientsocket, address) = serversocket.accept()

    print("Connected to :", address)

    start_new_thread(threaded_client, (clientsocket,))
