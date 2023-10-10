""" 
    Aluno: Alan Lima Marques
    Atividade 02 , Exercicio 02
    Data de Criação: 07/10/2023
    Descrição: 
        Neste programa há um cliente que se conecta à um servidor usando sockets UDP , 
        e manda arquivos, que são verificados no servidor por meio de um Checksum.

        
PROTOCOLO : 
    Request :
    [FILENAME] [CHECKSUM]           [NUMBER_BLOCKS]  
    (255 bytes) (40 byte, SHA1)     (2 byte) -> Capacidade máxima de arquivo = 64MB 

    Response:
    [OP_STATUS] 
    (1 byte)   

    Status 1 : SUCESSO 
    Status 2 : FALHA
    Status 3 : CHECKSUM ERRADO
"""


import hashlib
import socket
import os
from _thread import *

ADDR='127.0.0.1'
PORT = 6666

def thread_envia(client_socket):
    while (True):
        arquivo=b''
        #Abrindo conexão e recebendo primeiro pacote com as informações do arquivo
        print("Esperando conexão")
        data,addr=client_socket.recvfrom(1024)
        request=data.decode().split(';')

        #Carregando as informações nas variáveis
        nome_arquivo=request[0]
        checksum=request[1]
        quantidade_datagramas=int(request[2])

        #Copia-se o arquivo em blocos de 1024 bytes
        # for i in range (quantidade_datagramas):
        #     data,_ = client_socket.recvfrom(1024)
        #     arquivo+=data

        arquivo = open('server_directory/'+nome_arquivo,'wb')
        for i in range(quantidade_datagramas):
            print(f"Recebendo bloco {i}/{quantidade_datagramas}")
            data, _ = client_socket.recvfrom(1024)
            if data == b"":
                break
            arquivo.write(data)
        arquivo.close()
        
        print("Fazendo hash")

        response=bytearray(1)
        response[0]=2

        if nome_arquivo in os.listdir('client_directory'):


            #Fazendo um hash do arquivo e comparando com o recebido
            arquivo = open('server_directory/'+nome_arquivo,'rb')
            sha1_hash = hashlib.sha1()
            while True:
                checksum_server=arquivo.read(1024)
                if not checksum_server:break
                sha1_hash.update(checksum_server)

            checksum_server= sha1_hash.hexdigest()
            arquivo.close()
            
            #Caso o checksum confira, escreve o arquivo
            if checksum_server==checksum:
                response[0]= 1
                print("arquivo recebido com sucesso")
            else : response[0]= 3

        else : response[0]=2

        #envia resposta do status da operação 
        client_socket.sendto(response,addr)

def main():
    endereco=(ADDR,PORT)

    #despacha as threads
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(endereco)
    #start_new_thread(thread_envia, (client_socket,))
    thread_envia(client_socket)


main()