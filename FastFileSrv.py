import socket
from os import listdir
from os.path import isfile, join
import os
import random
import FSChunk
import pickle
import re
import math
import constants



IP_ADDRESS  = "127.0.0.1"
UDP_PORT_NO = 8888
BUFFER_SIZE = 1024


UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ir buscar os nomes dos ficheiros do FFS e o seu tamanho
onlyFiles = [(f, os.stat(f).st_size) for f in listdir("../CC2021") if isfile(join("../CC2021", f))]
print(onlyFiles,len(onlyFiles))

# Primeiro envio é a dizer os nomes dos ficheiros, ou no caso de não caber tudo numa mensagem
# tem de se enviar um marcador a dizer que vão ser enviadas mais X mensagens com nomes.
nrMsg = 1
nrFiles = len(onlyFiles)
nrFilesChars = len(str(onlyFiles))



if(nrFilesChars >= constants.MAX_CHUNKSIZE):
    nrMsg+=(nrFilesChars/constants.MAX_CHUNKSIZE)

while nrMsg > 0:
    msg = f"{nrMsg}__{onlyFiles}"
    fschunk = FSChunk.FSChunk(IP_ADDRESS,IP_ADDRESS,str.encode(msg))
    print("Enviei")
    UDPClientSocket.sendto(pickle.dumps(fschunk),(IP_ADDRESS, UDP_PORT_NO))
    nrMsg-=1


while True:

    data2, addr = UDPClientSocket.recvfrom(BUFFER_SIZE)
    msg = pickle.loads(data2).data.decode("utf-8")
    print("Message from Server",msg)
    _, filename = re.split("Ficheiro: ",msg)

    if msg.startswith('Ficheiro: '):
        # Enviar ficheiro
        # Verificar tamanho
        print("ENTROU NO IF")
        fileSize = [item for item in onlyFiles if item[0] == filename][0][1]
        print(fileSize)

        # Enviar primeiro pedaço do céu
        in_file = open(filename, "rb")
        while (data := in_file.read(constants.MAX_CHUNKSIZE)):
            # Ir buscar file em bytes
            print(data)
            #data = in_file.read(CHUNK_SIZE) # if you only wanted to read 512 bytes, do .read(512)
            
            fschunk2 = FSChunk.FSChunk(addr,IP_ADDRESS,data)
            print("addr: ", addr)
            UDPClientSocket.sendto(pickle.dumps(fschunk2),addr)
            print("sent filechunk")

        in_file.close()

UDPClientSocket.close()