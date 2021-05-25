import socket
import re
from threading import Thread
import threading
import FSChunk
import FastFileServeTable
import pickle
import math
import constants
import http.client


# Os prints começados por '++' são referentes à ligação UDP, e os '--' são TCP


fastFileServList = FastFileServeTable.FastFileServeTable()     # 'ffs': ['(file,size)']     -> Lista de FFSs com uma lista de files                      
listaPedidos     = FastFileServeTable.ListaPedidos()           # 'iphttp': 'filename'       -> Lista de pedidos de ficheiros
fileToGo         = b''

# Faz a ligação UDP
def UDPListen(lock):
    IP_ADDRESS  = "127.0.0.1"
    UDP_PORT_NO = 8888

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP
    UDPServerSocket.bind((IP_ADDRESS, UDP_PORT_NO))

    print("++HTTPGateway a escutar em UDP com sucesso")

    while True:

        # Recebe uma mensagem por UDP de um novo FFS
        data, addr = UDPServerSocket.recvfrom(constants.MAX_BUFFER)
        mensagem = pickle.loads(data).data
        nrMsg, files = re.split("__",mensagem.decode("utf-8"))
        print("++Message",mensagem)

        # Caso os files não caibam numa mensagem, ler até ter os files todos
        while int(nrMsg) > 1:
            data2, addr = UDPServerSocket.recvfrom(constants.MAX_BUFFER)
            _ , files2 = re.split("__",pickle.loads(data2).data.decode("utf-8"))
            files += files2
            nrMsg-=1
            print("++ Mais 1")

        # Adiconar files e FFS
        files = files[1:-1]
        files_tuples = list(eval(files))
        fastFileServList.adicionaFFS(addr[0],addr[1],files_tuples)

        print(f"++FastFileServ {addr} Ligado", nrMsg, files_tuples)
        print("++Lista de servers", fastFileServList.servidores)

        # Trata pedidos
        print("++Lista Pedidos", listaPedidos.isNotEmpty())

        if listaPedidos.isNotEmpty():
            
            print("++ENTROU")
            # Vai buscar o filename do pedido de cima
            f = listaPedidos.primeiroPedido()
            #print(f)

            # Vê que ffs têm o file para transferir
            disponiveis = fastFileServList.procuraFile(f)
            print("++Disponiveis:", disponiveis)

            # Selecionar um ffs para pedir um file
            ffs_selecionado = disponiveis[0]
            pedir_file = "Ficheiro: " + f
            print("++Cenas",pedir_file, ffs_selecionado)
            file_bytes = pedir_file.encode()
            fschunk = FSChunk.FSChunk(IP_ADDRESS,ffs_selecionado,file_bytes)
            UDPServerSocket.sendto(pickle.dumps(fschunk), (ffs_selecionado[0],ffs_selecionado[1].porta))

            chunkList = []
            # Receber o file 
            i = fastFileServList.tamanhoFile(addr[0],f)
            print(i)

            nrMsg = math.ceil(i/constants.MAX_CHUNKSIZE)

            while nrMsg > 0:
                data, addr = UDPServerSocket.recvfrom(constants.MAX_BUFFER)
                msg = pickle.loads(data).data.decode("utf-8")
                chunkList.append(msg)
                nrMsg -= 1

            # Tratar das exceções caso o ficheiro não chegue com sucesso
            # Verificar nr de msg recebidas e verificar nr de bytes:
                # Se estiver OK, continuar
                # Se não, voltar a pedir a outro FFS
            
            print("++fora")

            # Dar locks e finalizar file
            lock.acquire()
            teste = ''.join([str(elem) for elem in chunkList])
            fileTeste = teste
            fileToGo = teste.encode("utf-8")
            lock.release()

            # Remover Pedido da lista
            listaPedidos.removePedido(ffs_selecionado[0])
            print("++ Removido pedido", fileToGo)


# Faz a ligação TCP
def TCPListen(lock):
    
    IP_ADDRESS  = "localhost"
    TCP_PORT_NO = 8080

    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
    TCPServerSocket.bind((IP_ADDRESS, TCP_PORT_NO))

    print("--HTTPGateway a escutar em TCP com sucesso")

    while True:
        # Faz a conexão TCP
        TCPServerSocket.listen(1)
        conn, address = TCPServerSocket.accept()
        print("--TCP connection from", address)

        # Parsing do HTTP request
        data = conn.recv(constants.MAX_BUFFER)
        stringdata = data.decode('utf-8')
        filename = re.sub('/','',stringdata).split(' ')
        ip = f"{address[0]}"#":{address[1]}"
        print("--Filename Requested:", filename[1],ip)

        # Acrescentar pedido à listaPedidos
        listaPedidos.adicionaPedido(ip,TCP_PORT_NO,filename[1])

        print("-- Vamos esperar")
        # Verificar o filesToGo até ter lá o ficheiro
        while listaPedidos.procuraPedido(ip):
           1
        
        print("-- Parei de esperar")

        # Ler o ficheiro e enviar o ficheiro
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_socket.connect((ip,constants.TCP_PORT))


        # BODY = "***filecontents***"
        # print("aquiaaaaaaa")
        # conn = http.client.HTTPConnection("localhost", 8080)
        # print(str(conn))
        # conn.request("PUT", "/teste.txt", BODY)
        # print("aquiaaaaaaabbbbbbbbb")
        # response = conn.getresponse()

        # print(response.status, response.reason)


        lock.acquire()
        
        # print("Vamos enviar?", address, str(conn), fileToGo)
        conn.send(fileToGo)

        lock.release()

        conn.close()
 
def main():
    global fileToGo

    fileToGo = b''

    lock = threading.Lock()

    ThreadUDP = Thread(target=UDPListen, args=(lock,))
    ThreadTCP = Thread(target=TCPListen, args=(lock,))

    ThreadUDP.start()
    ThreadTCP.start()
    
    print("Servidor Ligado!")


if __name__ == "__main__":
    main()