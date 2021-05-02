import socket
from os import listdir
from os.path import isfile, join
import os
import random
import FSChunk
import pickle



IP_ADDRESS  = "127.0.0.1"
UDP_PORT_NO = 8888
BUFFER_SIZE = 1024
CHUNK_SIZE = 500


UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ir buscar os nomes dos ficheiros do FFS e o seu tamanho
onlyfiles = [(f, os.stat(f).st_size) for f in listdir("../CC2021") if isfile(join("../CC2021", f))]
print(onlyfiles,len(onlyfiles))

# Primeiro envio é a dizer os nomes dos ficheiros, ou no caso de não caber tudo numa mensagem
# tem de se enviar um marcador a dizer que vão ser enviadas mais X mensagens com nomes.
nrMsg = 1
nrFiles = len(onlyfiles)
nrFilesChars = len(str(onlyfiles))

if(nrFilesChars >= CHUNK_SIZE):
    nrMsg+=(nrFilesChars/CHUNK_SIZE)

while nrMsg > 0:
    msg = f"{nrMsg}__{onlyfiles}"
    fschunk = FSChunk.FSChunk(IP_ADDRESS,IP_ADDRESS,str.encode(msg))
    UDPClientSocket.sendto(pickle.dumps(fschunk),(IP_ADDRESS, UDP_PORT_NO))
    nrMsg-=1


while True:
    
    

    msgFromServer = UDPClientSocket.recvfrom(BUFFER_SIZE)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)


UDPClientSocket.close()