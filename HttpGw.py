import socket
from threading import Thread
# import time

BUFFER_SIZE  = 1024

fastFileServList = []

# Faz a ligação UDP
def UDPListen():
    IP_ADDRESS  = "localhost"
    UDP_PORT_NO = 8888

    msgFromServer       = "Ola FastFileServ"
    bytesToSend         = str.encode(msgFromServer)

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind((IP_ADDRESS, UDP_PORT_NO))

    print("HTTPGateway a escutar em UDP com sucesso")

    while True:
        data, addr = UDPServerSocket.recvfrom(BUFFER_SIZE)
        print ("Message: ", data)
        UDPServerSocket.sendto(bytesToSend, addr)

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
        print("Mesage: ", data)
        conn.close()

def main():
    ThreadUDP = Thread(target=UDPListen)
    ThreadTCP = Thread(target=TCPListen)

    ThreadUDP.start()
    ThreadTCP.start()
    print("Servidor Ligado!")


if __name__ == "__main__":
    main()