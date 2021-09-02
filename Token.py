class Token:
    def __init__(self, tipo, lexema, patron, linea, noCaracter):
        self.tipo=tipo
        self.lexema=lexema
        self.patron=patron
        self.linea=linea
        self.noCaracter=noCaracter

    def __str__(self):
        return self.tipo+" "+self.lexema+" "+self.patron+" "+str(self.linea)+" "+str(self.noCaracter)
