import socket

IP_ADDRESS  = "localhost"
UDP_PORT_NO = 8888
BUFFER_SIZE = 1024

Message = ("Ola HTTPGateway")

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDPClientSocket.sendto(Message.encode(),(IP_ADDRESS, UDP_PORT_NO))

msgFromServer = UDPClientSocket.recvfrom(BUFFER_SIZE)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)