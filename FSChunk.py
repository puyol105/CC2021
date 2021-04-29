class FSChunk:

    def __init__(self, ffs_IP, httpgw_IP, data):
        self.max_chunksize = 500         # bytes
        self.ffs_IP = ffs_IP             # IP do FastFileServ
        self.httpgw_IP = httpgw_IP       # IP do HttpGw
        self.data = data                 # Mensagem


# Fazer ligação, basicamente é tipo cabeçalho, leva porta destino e mensagem
# Se for a receber o fastfileserv é com o nome do ficheiro
# Se for o oposto é o ficheiro em si