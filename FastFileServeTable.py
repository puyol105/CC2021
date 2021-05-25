class FastFileServeTableEntry:
    def __init__(self, ip, porta, files):
        self.ip = ip
        self.porta = porta
        self.files = files

    def encontra(self, filename):
        for i in self.files:
          if i[0] == filename:
            return True
        return False
    
    def tamanhoFile(self, filename):
        for i in self.files:
            if i[0] == filename:
                return i[1]


class FastFileServeTable:
    def __init__(self):
        self.servidores = {}

    def procuraFile(self, filename):
        res = []
        print(self.servidores)
        for key, value in self.servidores.items():
            if self.servidores[key].encontra(filename):
                res.append((key,value))
        return res

    def adicionaFFS(self, ip, porta, files):
        self.servidores[ip] = FastFileServeTableEntry(ip, porta, files) #files

    def removeFFS(self, ip):
        self.servidores.pop(ip)

    def tamanhoFile(self, ffs, filename):
        return self.servidores[ffs].tamanhoFile(filename)
        

class ListaPedidos:
    def __init__(self):
        self.pedidos = {}

    def adicionaPedido(self, ip, porta, filename):
        self.pedidos[ip] = filename

    def removePedido(self, ip):
        self.pedidos.pop(ip)

    def procuraPedido(self, ip):
        if ip in self.pedidos:
            return True
        return False

    def primeiroPedido(self):
        values_view = self.pedidos.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        return first_value

    def isNotEmpty(self):
        return bool(self.pedidos)

    