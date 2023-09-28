""" 
    Aluno: Alan Lima Marques
    Atividade 01 , Exercicio 02
    Data de Criação: 24/09/2023
    Descrição: 
        Neste programa há um cliente que se conecta à um servidor usando sockets TCP , 
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
"""

import socket
import os
ADDR = 'localhost'
PORT = 6666

COMMANDS=["addfile","delete","getfileslist","getfile"]


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ADDR, PORT))


#Gerencia o envio do cabeçalho em comum à todos os comandos
def enviar_cabecalho(entrada, nomeArquivo, comandIdentif):
    func = entrada.split()[0]

    if(func == "addfile"):
        arquivos = os.listdir(path='./client_directory')

    # Checa se o arquivo existe
        if nomeArquivo not in arquivos:
            print('O arquivo solicitado não existe')
            return False
    
    fileNameSize = len(nomeArquivo)
        
    # Verifica se o nome não passa de 255 bytes
    if fileNameSize < 256:
        messageType = 1
        
            
        # Header
        cabecalho = bytearray(3)
        cabecalho[0] = messageType
        cabecalho[1] = comandIdentif
        cabecalho[2] = fileNameSize

        clientsocket.send(cabecalho)
        # Filename
        # for nome in nomeArquivo:
        #     byte = str.encode(nome)
        #     clientsocket.send(byte) 
        clientsocket.send(nomeArquivo.encode())
        
        return True
    else:
        print('O tamanho do nome do arquivo excedeu o limite de 255 caracteres')
        return False


#------- CLIENT MAIN LOOP ----------
while True:
    msg = str(input("=>"))
    if not msg : continue
    #print(f"Sent:{msg}")
    if ( msg.split()[0] == "addfile"):
        nome_arquivo=msg.split()[1]

        if ( enviar_cabecalho(msg,nome_arquivo,1)):
            #Campos específicos do cabeçalho do ADD 
            tamanho_arquivo=(os.stat('client_directory/' + nome_arquivo).st_size).to_bytes(4, "big") 
            clientsocket.send(tamanho_arquivo)

            with open('client_directory/' + nome_arquivo, 'rb') as file:
                    byte = file.read(1)
                    while byte != b'':
                        clientsocket.send(byte)
                        byte = file.read(1)

            # Espera a resposta
            resposta = clientsocket.recv(3)
            respostaTipo = int(resposta[0])
            respostaComando = int(resposta[1])
            respostaStatus = int(resposta[2])
            
            if(respostaTipo == 2 and respostaComando == 1):
                if(respostaStatus == 1):
                    print('Arquivo copiado com sucesso')
                elif(respostaStatus == 2):
                    print('Erro ao copiar arquivo')
        else :
            print(f"FALHA AO REALIZAR COMANDO \"{msg}\"" )

    elif ( msg.split()[0] == "delete"):
        nome_arquivo=msg.split()[1]
        if ( enviar_cabecalho(msg,nome_arquivo,2)):
                # Espera a resposta
                resposta = clientsocket.recv(3)
                respostaTipo = int(resposta[0])
                respostaComando = int(resposta[1])
                respostaStatus = int(resposta[2])
                
                if(respostaTipo == 2 and respostaComando == 2):
                    if(respostaStatus == 1):
                        print('Arquivo deletado com sucesso')
                    elif(respostaStatus == 2):
                        print('Erro ao deletar arquivo')
                    elif(respostaStatus == 3):
                        print('Arquivo não existe !')
                        


    elif ( msg.split()[0] == "getfileslist"):
        nome_arquivo=""
        listagem_arquivos=[]

        if enviar_cabecalho(msg,nome_arquivo,3):
            resposta=clientsocket.recv(3)
            respostaTipo=int(resposta[0])
            respostaComando=int(resposta[1])
            respostaStatus=int(resposta[2])

            if (respostaTipo==2 and respostaComando==3):
                if (respostaStatus==1):
                    n_arquivos=int.from_bytes(clientsocket.recv(2),byteorder='big')
                    print(f"numero de arquivos {n_arquivos}")

                    for _ in range ( n_arquivos):
                        tamanho_nome_arquivo=int.from_bytes(clientsocket.recv(1),byteorder='big')
                        print(f"tamanho do arquivo {tamanho_nome_arquivo}")

                        # for _ in range(tamanho_nome_arquivo):
                        #     char_nome_arq = clientsocket.recv(1)
                        #     nome_arquivo+=char_nome_arq.decode()
                        
                        nome_arquivo=clientsocket.recv(tamanho_nome_arquivo).decode()

                        listagem_arquivos.append(nome_arquivo)
                        print(f"Nome arquivo: {nome_arquivo}")
                        nome_arquivo =""
                elif(respostaStatus==2):
                    print("Erro na listagem de arquivos")
                elif(respostaStatus==3):
                    print("Não há arquivos para serem listados")

    elif ( msg.split()[0] == "getfile"):
        nome_arquivo = msg.split()[1]
            
            #Caso o retorno da função enviaCabecalho seja verdadeira
        if enviar_cabecalho(msg, nome_arquivo, 4):
            #Resposta do servidor
            resposta = clientsocket.recv(3)
            respostaTipo = int(resposta[0])
            respostaComando = int(resposta[1])
            respostaStatus = int(resposta[2])

            if respostaTipo == 2 and respostaComando == 4:
                #Status 1 = ok, Status 2 = falha
                if respostaStatus == 1:
                    tamanho_arquivo = int.from_bytes(clientsocket.recv(4), byteorder='big')

                    #Recebe byte a byte
                    # arquivo = b''
                    # for _ in range(tamanhoArquivo):
                    #     byte = clientsocket.recv(1)
                    #     arquivo += byte
                    print(f"Tamanho arquivo : {tamanho_arquivo}")
                    arquivo = clientsocket.recv(tamanho_arquivo)
                    print(f"arquivo recebido :{arquivo}")

                    #Cria arquivo w=write b=binary 
                    with open ('client_directory/' + nome_arquivo, 'w+b') as file:
                        file.write(arquivo)
                        print("Arquivo obtido e gravado com sucesso")
                
                elif respostaStatus==2:
                    print("Arquivo não encontrado")