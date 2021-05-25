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
import signal
import sys


IP_ADDRESS  = "127.0.0.1"
UDP_PORT_NO = 8888


UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #IPv4, UDP

# Ir buscar os nomes dos ficheiros do FFS e o seu tamanho
onlyFiles = [(f, os.stat(f).st_size) for f in listdir("../CC2021") if isfile(join("../CC2021", f))]
print("Meus Ficheiros:", onlyFiles,len(onlyFiles))

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
    print("Enviei os meus ficheiros ao HttpGw")
    UDPClientSocket.sendto(pickle.dumps(fschunk),(IP_ADDRESS, UDP_PORT_NO))
    nrMsg-=1

# O FFS fica à espera de receber um nome de ficheiro para mandar
while True:

    try:
        # Recebe mensagem do HttpGw com nome do file
        data2, addr = UDPClientSocket.recvfrom(constants.MAX_BUFFER)
        msg = pickle.loads(data2).data.decode("utf-8")
        print("Message from Server",msg)
        _, filename = re.split("Ficheiro: ",msg)

        if msg.startswith('Ficheiro: '):
            # Enviar ficheiro
            # Verificar tamanho
            fileSize = [item for item in onlyFiles if item[0] == filename][0][1]

            # Abrir ficheiro em modo de leitura em bytes
            in_file = open(filename, "rb")
            while (data := in_file.read(constants.MAX_CHUNKSIZE)): # Ir buscar file em bytes
                print(data)                
                fschunk2 = FSChunk.FSChunk(addr,IP_ADDRESS,data)
                print("addr: ", addr)
                UDPClientSocket.sendto(pickle.dumps(fschunk2),addr)
                print("sent filechunk")

            in_file.close()
        
        print('Pressione \'Ctrl+C\' para desligar o FFS ou aguarde novo pedido de ficheiro')

    # Trata de desligar a ligação
    except KeyboardInterrupt:
        print('\nA desligar FastFileServ...')
        UDPClientSocket.close()
        sys.exit(0)

