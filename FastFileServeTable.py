class FastFileServeTableEntry:
    def __init__(self, ip, porta, files):
        self.ip = ip
        self.porta = porta
        self.files = files

    def encontra(self, file):
        if file[0] in self.files:
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

    