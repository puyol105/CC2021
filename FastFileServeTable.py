class FastFileServeTableEntry:
    def __init__(self, ip, porta, files):
        self.ip = ip
        self.porta = porta
        self.files = files

    def encontra(self, file):
        if file in self.files:
            return True
        return False

class FastFileServeTable:
    def __init__(self):
        self.servidores = {}

    def procuraFile(self, filename):
        res = []
        for s in self.servidores:
            if s.encontra(filename):
                res.append(s)
        return res

    def adicionaFFS(self, ip, porta, files):
        self.servidores[ip] = FastFileServeTableEntry(ip, porta, files) #files
    
    def mostra(self):
        for s in self.servidores:
            print(s.ip, ":", s.files)

class ListaPedidos:
    def __init__(self):
        self.pedidos = {}

    def adicionaPedido(self, ip, porta, file):
        self.pedidos[ip] = file

    