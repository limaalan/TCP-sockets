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
        -> GETFILESLIST (3): retorna uma lista com o nome dos arquivos.
        -> GETFILE (4): faz download de um arquivo.


PROTOCOLO : 
    Request :
    [Message Type] [Command ident]  [Filename Size] [Filename]  + Específicos
    (1 byte)            (1 byte)        (1 byte)   (0-255 bytes)

    Response:
    [Message Type] [Command ident]  [Status Code] + Específicos 
    (1 byte)            (1 byte)        (1 byte)  

Status 1 : SUCESS 
Status 2 : FAILED
Status 3 : NO FILES TO DELETE / LIST  
"""
import socket
import os
from _thread import *

ADDR = 'localhost'
PORT = 6666
commands={1:"addfile",2:"delete",3:"getfileslist",4:"getfile"}


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reusa porta
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

        # nome_arquivo = b''
        # for _ in range(fileNameSize):
        #     bytes = clientsocket.recv(1)
        #     nome_arquivo += bytes
        # nome_arquivo=nome_arquivo.decode()
        nome_arquivo = clientsocket.recv(fileNameSize).decode()

        #print(f"Messagetype {messageType}, command {commandIdentif}, fnsize {fileNameSize}, nome_arquivo {nome_arquivo}")
        print("-"*20)
        print(f"Received:\nType:{'request'if messageType==1 else 'response' } cmd:{commands[commandIdentif]} {nome_arquivo}")
        
        # ADDFILE
        if(messageType == 1 and commandIdentif == 1):
            tamanho_arquivo = int.from_bytes(clientsocket.recv(4), byteorder='big')
            print(f"Tamanho do arquivo : {tamanho_arquivo}")
            # Recebe o arquivo
            arquivo = b''
            for _ in range(tamanho_arquivo):
                bytes = clientsocket.recv(1)
                arquivo += bytes
            
            # Salva o arquivo
            with open('server_directory/' + nome_arquivo, 'w+b') as file:
                file.write(arquivo)

            # Preparo a resposta
            resposta = bytearray(3)
            resposta[0] = 2 #MESSAGE TYPE = RESPONSE
            resposta[1] = 1 #COMMAND IDENTIF = 1 ( ADD )
            resposta[2] = 1 if os.path.isfile('/server_directory'+nome_arquivo) else 2
            
            clientsocket.send(resposta)

        # DELETE
        if(messageType == 1 and commandIdentif == 2):
            
            resposta = bytearray(3)
            resposta[0] = 2  #MESSAGE TYPE = RESPONSE
            resposta[1] = 2  #COMMAND IDENTIF = 2 ( DELETE )

            # caso o arquivo exista no diretorio
            print(f"Deleting {nome_arquivo}...")
            if (os.path.isfile('server_directory/'+nome_arquivo)): 
                # remove arquivo  
                os.remove('server_directory/' + nome_arquivo)
                # verifica se realmente foi excluido
                resposta[2] = 2 if os.path.isfile('server_directory/'+nome_arquivo) else 1
            else :
                resposta[2]=3
            if(resposta[2]==1):print(f"\"{nome_arquivo}\" deleted.")

            clientsocket.send(resposta)

        # GETFILESLIST
        if(messageType == 1 and commandIdentif == 3):
            resposta=bytearray(3)
            resposta[0]=2#MESSAGE TYPE = RESPONS
            resposta[1]=3#COMMAND IDENTIF = 2 ( GETFILESLIST )

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
            arquivos = os.listdir(path='server_directory')

            resposta = bytearray(3)
            resposta[0] = 2
            resposta[1] = commandIdentif
            
            # se o arquivo existir
            if nome_arquivo in arquivos:
                resposta[2] = 1 #status ok
                clientsocket.send(resposta)

                # envia o tamanho do arquivo .st_size = tamanho em bytes
                tamanho_arquivo = (os.stat('server_directory/' + nome_arquivo).st_size).to_bytes(4, "big")
                clientsocket.send(tamanho_arquivo)
                
                # envia o arquivo byte a byte
                # with open('./server_directory/' + nome_arquivo, 'rb') as file:
                #     byte = file.read(1)
                #     while byte != b'':
                #         con.send(byte)
                #         byte = file.read(1)
                file = open('server_directory/'+nome_arquivo,'rb')
                #print(file.read())
                clientsocket.send(file.read())
            else:
                resposta[2] = 2 #Status 2 = arquivo não existe

    clientsocket.close()



# ------  Server Main Loop ------
while True:
    print("waiting...")
    (clientsocket, address) = serversocket.accept()

    print("Connected to :", address)

    start_new_thread(threaded_client, (clientsocket,))
