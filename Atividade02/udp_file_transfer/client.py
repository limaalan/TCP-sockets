""" 
    Aluno: Alan Lima Marques
    Atividade 02 , Exercicio 02
    Data de Criação: 07/10/2023
    Descrição: 
        Neste programa há um cliente que se conecta à um servidor usando sockets UDP , 
        e manda arquivos, que são verificados no servidor por meio de um Checksum.

        
PROTOCOLO : 
    Request :
    [FILENAME]; [CHECKSUM]; [NUMBER_BLOCKS]  
    (255 bytes) (40 bytes)   (2 byte) -> Capacidade máxima de arquivo = 64MB 

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

ADDR='127.0.0.1'
PORT = 6666

def envia_arquivo(server_socket,endereco):
    while(True):
        arquivos = os.listdir("client_directory")
        print(arquivos)

        nome_arquivo = input("Escolha o arquivo a ser enviado:")

        #Checa existência do arquivo
        if nome_arquivo not in arquivos:
            print("Arquivo não existe!")
            continue

        #Checa o tamanho do nome do arquivo
        if len(nome_arquivo) >255:
            print("Nome do arquivo excede o limite de 255 bytes!")
            continue
        
        #Cacula a quantidade de blocos a serem enviados
        tamanho_arquivo=os.stat("client_directory/"+nome_arquivo).st_size
        quantidade_datagramas = math.ceil(tamanho_arquivo/1024)
        
        #Checa se o arquivo não é grande demais
        if quantidade_datagramas>65536 :
            print("Tamanho do arquivo excede 64MB",quantidade_datagramas)
            continue
        
        sha1_hash=hashlib.sha1()

        #Faz o checksum e manda as informações
        with open ("client_directory/"+nome_arquivo,'rb') as file:
            checksum=file.read()
            sha1_hash.update(checksum)
            checksum=sha1_hash.hexdigest()

            #Envia primeiro datagrama com as informações do arquivo

            request = nome_arquivo +';'+\
                checksum +';'+\
                str(quantidade_datagramas)
            
            server_socket.sendto(request.encode(),endereco)

        #Envia os blocos
        with open("client_directory/"+nome_arquivo,'rb') as file:
            arq_byte=file.read(1024)
            cont=0
            while arq_byte != b'':
                server_socket.sendto(arq_byte,endereco)
                
                print(f"Enviando um pedaço {cont} do arquivo...")
                cont+=1

                arq_byte= file.read(1024)
        
        status, _= server_socket.recvfrom(1)

        print("Operação realizada com sucesso" if status[0]==1 else "Erro ao realizar operação!")



def main():
    endereco = (ADDR, PORT)

    # Cria o socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    envia_arquivo(client_socket, endereco)

main()