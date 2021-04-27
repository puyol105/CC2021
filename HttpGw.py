# SERVIDOR

import socket
import re
from threading import Thread
import FSChunk
import FastFileServeTable

BUFFER_SIZE  = 1024


fastFileServList = FastFileServeTable.FastFileServeTable()
fileToGo = b''
listaPedidos = {
    "127.0.0.1": "teste.txt"
}


# Faz a ligação UDP
def UDPListen():
    IP_ADDRESS  = "127.0.0.1"
    UDP_PORT_NO = 8888

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP
    UDPServerSocket.bind((IP_ADDRESS, UDP_PORT_NO))

    print("HTTPGateway a escutar em UDP com sucesso")

    while True:
        data, addr = UDPServerSocket.recvfrom(BUFFER_SIZE)


        print(f"FastFileServ {addr} Ligado", data)
        print("Lista de server", fastFileServList)

        msgFromServer       = b"olaola"
        UDPServerSocket.sendto(msgFromServer,(IP_ADDRESS, UDP_PORT_NO))



# Faz a ligação TCP
def TCPListen():
    IP_ADDRESS  = "localhost"
    TCP_PORT_NO = 8080

    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
    TCPServerSocket.bind((IP_ADDRESS, TCP_PORT_NO))

    print("HTTPGateway a escutar em TCP com sucesso")

    while True:
        TCPServerSocket.listen(1)
        conn, address = TCPServerSocket.accept()
        print("TCP connection from", address)
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