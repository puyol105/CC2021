import socket
import re
from threading import Thread
import FSChunk
import FastFileServeTable
import pickle
import re

BUFFER_SIZE = 1024
CHUNK_SIZE = 500


fastFileServList = FastFileServeTable.FastFileServeTable()
fileToGo = b''
listaPedidos = FastFileServeTable.ListaPedidos()


# Faz a ligação UDP
def UDPListen():
    IP_ADDRESS  = "127.0.0.1"
    UDP_PORT_NO = 8888

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP
    UDPServerSocket.bind((IP_ADDRESS, UDP_PORT_NO))

    print("HTTPGateway a escutar em UDP com sucesso")

    while True:

        # Recebe uma mensagem por UDP de um novo FFS
        data, addr = UDPServerSocket.recvfrom(BUFFER_SIZE)
        mensagem = pickle.loads(data).data
        nrMsg, files = re.split("__",mensagem.decode("utf-8"))

        # Caso os files não caibam numa mensagem, ler até ter os files todos
        while int(nrMsg) > 1:
            data2, addr = UDPServerSocket.recvfrom(BUFFER_SIZE)
            _ , files2 = re.split("__",pickle.loads(data2).data.decode("utf-8"))
            files += files2
            nrMsg-=1

        #Adiconar files e FFS 
        fastFileServList.adicionaFFS(addr,UDP_PORT_NO,files)

        print(f"FastFileServ {addr} Ligado", nrMsg, files)
        print("Lista de servers", fastFileServList.servidores)

        # Trata pedidos
        if not bool(listaPedidos):
            # Vê que ffs têm o file para transferir
            disponiveis = fastFileServList.procuraFile()

            # divide os chunks a pedir




        msgFromServer       = b"olaola"
        UDPServerSocket.sendto(msgFromServer, addr)



# Faz a ligação TCP
def TCPListen():
    IP_ADDRESS  = "localhost"
    TCP_PORT_NO = 8080

    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
    TCPServerSocket.bind((IP_ADDRESS, TCP_PORT_NO))

    print("HTTPGateway a escutar em TCP com sucesso")

    while True:
        #Faz a conexão TCP
        TCPServerSocket.listen(1)
        conn, address = TCPServerSocket.accept()
        print("TCP connection from", address)
        # Parsing do HTTP request
        data = conn.recv(BUFFER_SIZE)
        stringdata = data.decode('utf-8')
        filename = re.sub('/','',stringdata).split(' ')
        ip = f"{address[0]}"#":{address[1]}"
        print("Filename Requested:", filename[1],ip)
        listaPedidos[ip]=filename[1]
        print(listaPedidos)
        f=open(filename[1],'rb')
        content=f.read()
        
        #fschunk = FSChunkProtocol(filename[1],)
        #Escrever ficheiro
        #filefinal = open(filename[1], 'wb')
        # meter while o ficheiro ainda não está completo

        #Fechar ficheiro e conexao    
        #filefinal.close()
        #conn.close()
 
def main():
    ThreadUDP = Thread(target=UDPListen)
    ThreadTCP = Thread(target=TCPListen)

    ThreadUDP.start()
    ThreadTCP.start()
    print("Servidor Ligado!")


if __name__ == "__main__":
    main()