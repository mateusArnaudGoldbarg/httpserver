# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP (python 3)
#

# importacao das bibliotecas
import socket

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ('Serving HTTP on port %s ...' % PORT)


while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    request = request.decode('utf-8')
    print("Requisição do cliente {} - {}".format(client_address,request))
    request = request.split(" ")

    #request = GET /index.html HTTP/1.1
    #request = GET /favicon.ico HTTP/1.1
    #request = GET / HTTP/1.1

    '''
    request[0] = 'GET'
    request[1] = '/' ou request[1] = '/index.html' ou request[1] = '/favicon.ico'
    request[2][:8] = 'HTTP/1.1'
    '''

    # declaracao da resposta do servidor
    http_response = """\
    HTTP/1.1 200 OK

    """
    if request[0] == 'GET':
        if ((request[1] == '/index.html' or request[1] == '/') and request[2][:8] == 'HTTP/1.1'):
            client_connection.send(http_response.encode('utf-8'))
            file = open('index.html', 'r')
            client_connection.send(file.read().encode('utf-8'))

        elif request[1] == '/favicon.ico' and request[2][:8] == 'HTTP/1.1':
            image = open(r'favicon.ico','rb')
            client_connection.send(image.read())

        else:
            #client_connection.send(http_response.encode('utf-8'))
            not_found = open('notfound.html', 'r')
            client_connection.send(not_found.read().encode('utf-8'))

    else:
        #client_connection.send(http_response.encode('utf-8'))
        bad_request = open('bad_request.html', 'r')
        client_connection.send(bad_request.read().encode('utf-8'))

    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()
