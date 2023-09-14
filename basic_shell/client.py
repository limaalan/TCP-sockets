""" 
    Aluno: Alan Lima Marques
    Exercicio 01
    Data de Criação: 11/09/2023
    Descrição: 
        Neste programa há um cliente se conecta à um servidor usando sockets TCP , 
        e manda mensagens para realizar requisições. Os comandos disponíveis são :
        CONNECT user, senha - Usuário se autentica e consegue acesso à outros comandos.
        PWD - Caminho absoluto do diretório do servidor.
        CHDIR path - Altera o diretorio em uso
        GETFILES - Recebe uma lista com todos os arquivos no diretorio atual do servidor.
        GETDIRS - Recebe uma lista com todos os diretorios no diretorio atual do servidor.
        EXIT - Finaliza a sessão e a conexao com o servidor.
"""

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
