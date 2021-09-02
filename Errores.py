class Error:
    def __init__(self, tipo, lexema, linea, noCaracter):
        self.tipo=tipo
        self.lexema=lexema
        self.linea=linea
        self.noCaracter=noCaracter

    def __str__(self):
        return self.tipo+" "+self.lexema+" "+str(self.linea)+" "+str(self.noCaracter)