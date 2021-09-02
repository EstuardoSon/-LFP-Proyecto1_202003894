class Posicion:
    def __init__(self):
        self.x=float('inf')
        self.y=float('inf')
        self.pintar=False
        self.color="#ffffff"

    def __str__(self):
        return str(self.x)+" "+str(self.y)+" "+str(self.pintar)+" "+self.color