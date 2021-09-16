class Imagen:
    def __init__(self):
        self.titulo=""
        self.mirrorX=False
        self.mirrorY=False
        self.doubleMirror=False
        self.width=0
        self.height=0
        self.filas=0
        self.columnas=0
        self.listaPosiciones=list()

    def setTitulo(self, titulo):
        self.titulo=titulo

    def setWidth(self, width):
        self.width=width

    def setHeight(self, height):
        self.height=height

    def setFilas(self, fila):
        self.filas=fila

    def setColumnas(self, columnas):
        self.columnas=columnas

    def crearImagen(self):
        cWidth=int(self.width/self.columnas)
        cHeigth=int(self.height/self.filas)
        imagen='<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="'+str(int(self.width))+'" height="'+str(int(self.height))+'" viewBox="0 0 '+str(int(self.width))+' '+str(int(self.height))+'">\n'
        y=0

        for i in range(int(self.filas)):
            x = 0
            for j in range(int(self.columnas)):
                verificar = False
                for p in self.listaPosiciones:
                    if p.x==j and p.y==i and p.pintar==True:
                        imagen+='<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(cWidth)+'" height="'+str(cHeigth)+'" fill="'+p.color+'" stroke-width="1" stroke="black"/>\n'
                        verificar=True
                        break
                if not verificar:
                    imagen += '<rect x="'+str(x)+'" y="'+str(y)+'" width="' + str(cWidth) + '" height="' + str(cHeigth) + '" fill="#ffffff" stroke-width="1" stroke="black"/>\n'
                x+=cWidth
            y+=cHeigth


        imagen+="</svg>\n"
        return imagen

    def crearMirrorX(self):
        cWidth=int(self.width/self.columnas)
        cHeigth=int(self.height/self.filas)
        imagen='<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="'+str(int(self.width))+'" height="'+str(int(self.height))+'" viewBox="0 0 '+str(int(self.width))+' '+str(int(self.height))+'">\n'
        y=0

        for i in range(int(self.filas)):
            x = self.width-cWidth
            for j in range(int(self.columnas)):
                verificar = False
                for p in self.listaPosiciones:
                    if p.x==j and p.y==i and p.pintar==True:
                        imagen+='<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(cWidth)+'" height="'+str(cHeigth)+'" fill="'+p.color+'" stroke-width="1" stroke="black"/>\n'
                        verificar=True
                        break
                if not verificar:
                    imagen += '<rect x="'+str(x)+'" y="'+str(y)+'" width="' + str(cWidth) + '" height="' + str(cHeigth) + '" fill="#ffffff" stroke-width="1" stroke="black"/>\n'
                x-=cWidth
            y+=cHeigth


        imagen+="</svg>\n"
        return imagen

    def crearMirrorY(self):
        cWidth=int(self.width/self.columnas)
        cHeigth=int(self.height/self.filas)
        imagen='<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="'+str(int(self.width))+'" height="'+str(int(self.height))+'" viewBox="0 0 '+str(int(self.width))+' '+str(int(self.height))+'">\n'
        y=self.height-cHeigth

        for i in range(int(self.filas)):
            x = 0
            for j in range(int(self.columnas)):
                verificar = False
                for p in self.listaPosiciones:
                    if p.x==j and p.y==i and p.pintar==True:
                        imagen+='<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(cWidth)+'" height="'+str(cHeigth)+'" fill="'+p.color+'" stroke-width="1" stroke="black"/>\n'
                        verificar=True
                        break
                if not verificar:
                    imagen += '<rect x="'+str(x)+'" y="'+str(y)+'" width="' + str(cWidth) + '" height="' + str(cHeigth) + '" fill="#ffffff" stroke-width="1" stroke="black"/>\n'
                x+=cWidth
            y-=cHeigth


        imagen+="</svg>\n"
        return imagen

    def crearMirrorD(self):
        cWidth=int(self.width/self.columnas)
        cHeigth=int(self.height/self.filas)
        imagen='<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="'+str(int(self.width))+'" height="'+str(int(self.height))+'" viewBox="0 0 '+str(int(self.width))+' '+str(int(self.height))+'">\n'
        y=self.height-cHeigth

        for i in range(int(self.filas)):
            x = self.width-cWidth
            for j in range(int(self.columnas)):
                verificar = False
                for p in self.listaPosiciones:
                    if p.x==j and p.y==i and p.pintar==True:
                        imagen+='<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(cWidth)+'" height="'+str(cHeigth)+'" fill="'+p.color+'" stroke-width="1" stroke="black"/>\n'
                        verificar=True
                        break
                if not verificar:
                    imagen += '<rect x="'+str(x)+'" y="'+str(y)+'" width="' + str(cWidth) + '" height="' + str(cHeigth) + '" fill="#ffffff" stroke-width="1" stroke="black"/>\n'
                x-=cWidth
            y-=cHeigth


        imagen+="</svg>\n"
        return imagen

    def __str__(self):
        return self.titulo+" "+str(self.filas)+" "+str(self.columnas)+" "+str(self.width)+" "+str(self.height)+" "+str(self.mirrorY)+" "+str(self.mirrorX)+" "+str(self.doubleMirror)