# CLIENTE

import socket
from os import listdir
from os.path import isfile, join
import random

# Ir buscar os nomes dos ficheiros do FFS
onlyfiles = [f for f in listdir("/Users/puyol/Desktop/CC2021") if isfile(join("/Users/puyol/Desktop/CC2021", f))]
print(onlyfiles,len(onlyfiles))


IP_ADDRESS  = "127.0.0.1"
UDP_PORT_NO = 8888
BUFFER_SIZE = 1024
nrFiles = 0

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Primeiro envio é a dizer os nomes dos ficheiros, ou no caso de não caber tudo numa mensagem
# tem de se enviar um marcador a dizer que vão ser enviadas mais X mensagens com nomes.

while True:
    msg = "ola httpgw"
    UDPClientSocket.sendto(str.encode(msg),(IP_ADDRESS, UDP_PORT_NO))


    msgFromServer = UDPClientSocket.recvfrom(BUFFER_SIZE)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)


UDPClientSocket.close()