""" 
    Aluno: Alan Lima Marques
    Atividade 02 , Exercicio 02
    Data de Criação: 07/10/2023
    Descrição: 
        Neste programa há um cliente que se conecta à um servidor usando sockets UDP , 
        e manda arquivos, que são verificados no servidor por meio de um Checksum.

        
PROTOCOLO : 
    Request :
    [FILENAME] [CHECKSUM] [NUMBER_BLOCKS]  
    (255 bytes) (1 byte)   (2 byte) -> Capacidade máxima de arquivo = 64MB 

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
import math
from _thread import *

ADDR='localhost'
PORT = 6666

def envia_arquivo(server_socket,endereco):
    while(True):
        nome_arquivo = input("Escolha o arquivo a ser enviado:")
        arquivos = os.listdir("client_directory")

        if nome_arquivo  in arquivos:

            if len(nome_arquivo) <255:

                tamanho_arquivo=os.stat("client_directory/"+nome_arquivo).st_size
                quantidade_datagramas = math.ceil(tamanho_arquivo/1024)
                sha1_hash=hashlib.sha1()

            with open ("client_directory/",+nome_arquivo,'rb') as file:
                checksum=file.read()
                sha1_hash.update(checksum)
                checksum=sha1_hash.hexdigest()

                #Envia primeiro datagrama com as informações do arquivo

                request = nome_arquivo +';'+\
                    checksum +';'+\
                    str(quantidade_datagramas)

                server_socket.sendto(request.encode,endereco)

            with open("client_directory/"+nome_arquivo,'rb') as file:
                arq_byte=file.read(1024)

                while arq_byte != b'':
                    server_socket.sendto(arq_byte,endereco)

                    print("Enviando um pedaço do arquivo...")
                    arq_byte= file.read(1024)
            
            status, endereco_receive= server_socket.recvfrom(1)

            print("Operação realizada com sucesso" if status[0]==1 else "Erro ao realizar operação!")



def main():
    endereco=(ADDR,PORT)

    #despacha as threads
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(endereco)

    start_new_thread(envia_arquivo, (server_socket,endereco))

main()