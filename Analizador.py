import Token
import Errores
import Posicion
import Imagen
import re

class Analizador:
    def __init__(self, contenido):
        self.contenido = contenido
        self.listaTokens = list()
        self.listaErrores = list()
        self.listaImagenes = list()
        self.imagen=Imagen.Imagen()
        self.comprobar=""
        self.posicion=None

    def reconocerTokens(self):
        centinela="°"
        texto=self.contenido+centinela
        linea=1
        noCaracter=1
        cadena=""
        estado=0
        i=0

        while i<len(texto):
            c=texto[i]
            if estado==0:
                if c=="{":
                    if self.comprobar=="CELDAS=":
                        self.comprobar+="{"

                    self.listaTokens.append(Token.Token("Llave Agrupacion", c, "{ o }", linea, noCaracter))
                    noCaracter+=1

                elif c=="}":
                    self.listaTokens.append(Token.Token("Llave Agrupacion", c, "{ o }", linea, noCaracter))
                    noCaracter+=1

                elif re.match("[A-Z]",c):
                    cadena += c
                    noCaracter += 1
                    estado=1

                elif c==";":
                    self.listaTokens.append(Token.Token("Punto y Coma", c, ";", linea, noCaracter))
                    noCaracter += 1

                elif c=="@":
                    estado=5
                    cadena+=c
                    noCaracter += 1

                elif c=="=":
                    if self.comprobar=="TITULO" or self.comprobar=="ALTO" or self.comprobar=="ANCHO" or self.comprobar=="FILAS" or self.comprobar=="COLUMNAS" or self.comprobar=="CELDAS" or self.comprobar=="FILTROS":
                        self.comprobar+="="

                    self.listaTokens.append(Token.Token("Igual", c, "=", linea, noCaracter))
                    noCaracter += 1

                elif c=="[":
                    if re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE)|(FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*",self.comprobar):
                        self.comprobar+=c
                        self.posicion=Posicion.Posicion()


                    self.listaTokens.append(Token.Token("Corchetes", c, "[ o ]", linea, noCaracter))
                    noCaracter += 1

                elif c=="]":
                    self.imagen.listaPosiciones.append(self.posicion)
                    self.posicion=Posicion.Posicion()
                    self.comprobar+=c
                    self.listaTokens.append(Token.Token("Corchetes", c, "[ o ]", linea, noCaracter))
                    noCaracter += 1

                elif c==",":
                    if re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[(([0-9]+)?,)?([0-9]+)?", self.comprobar) or re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[([0-9]+)?,([0-9]+),(TRUE|FALSE)", self.comprobar) or re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\]", self.comprobar):
                        self.comprobar+=c

                    self.listaTokens.append(Token.Token("Coma", c, ",", linea, noCaracter))
                    noCaracter += 1

                elif c=='"':
                    cadena += c
                    estado = 4
                    noCaracter += 1

                elif c=='#':
                    cadena+=c
                    estado=2
                    noCaracter += 1

                elif c == ' ':
                    noCaracter += 1

                elif c == '\t':
                    noCaracter += 1

                elif c == '\r':
                    continue

                elif c=="\n":
                    linea+=1
                    noCaracter=1

                elif re.match("[0-9]",c):
                    estado=3
                    cadena+=c
                    noCaracter+=1

                elif c==centinela:
                    self.listaImagenes.append(self.imagen)
                    self.imagen = Imagen.Imagen()
                    break

                else:
                    self.listaErrores.append(Errores.Error("El caracter no forma parte del lenguaje", c, linea, noCaracter))
                    noCaracter+=1

            elif estado==1:
                if re.match("[A-Z]",c):
                    cadena+=c
                    noCaracter+=1

                else:
                    noCaracter -= 1
                    if cadena=="TITULO":
                        self.comprobar="TITULO"
                        self.listaTokens.append(Token.Token("TITULO", cadena, "TITULO", linea, noCaracter))

                    elif cadena=="ANCHO":
                        self.comprobar="ANCHO"
                        self.listaTokens.append(Token.Token("ANCHO", cadena, "ANCHO", linea, noCaracter))

                    elif cadena=="ALTO":
                        self.comprobar="ALTO"
                        self.listaTokens.append(Token.Token("ALTO", cadena, "ALTO", linea, noCaracter))

                    elif cadena=="FILAS":
                        self.comprobar="FILAS"
                        self.listaTokens.append(Token.Token("FILAS", cadena, "FILAS", linea, noCaracter))

                    elif cadena=="COLUMNAS":
                        self.comprobar="COLUMNAS"
                        self.listaTokens.append(Token.Token("COLUMNAS", cadena, "COLUMNAS", linea, noCaracter))

                    elif cadena=="CELDAS":
                        self.comprobar = "CELDAS"
                        self.listaTokens.append(Token.Token("CELDAS", cadena, "CELDAS", linea, noCaracter))

                    elif cadena=="FALSE":
                        if re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[([0-9]+)?,([0-9]+)?,",self.comprobar):
                            self.posicion.pintar=False
                            self.comprobar+=cadena
                        self.listaTokens.append(Token.Token("Booleano", cadena, "FALSE o TRUE", linea, noCaracter))

                    elif cadena=="TRUE":
                        if re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[([0-9]+)?,([0-9]+)?,",self.comprobar):
                            self.posicion.pintar=True
                            self.comprobar+=cadena
                        self.listaTokens.append(Token.Token("Booleano", cadena, "FALSE o TRUE", linea, noCaracter))

                    elif cadena=="FILTROS":
                        self.comprobar="FILTROS"
                        self.listaTokens.append(Token.Token("FILTROS", cadena, "FILTROS", linea, noCaracter))

                    elif cadena=="MIRRORX":
                        if self.comprobar=="FILTROS=":
                            self.imagen.mirrorX=True
                        self.listaTokens.append(Token.Token("Filtro", cadena, "MIRRORX | MIRRORY | DOUBLEMIRROR", linea, noCaracter))

                    elif cadena=="MIRRORY":
                        if self.comprobar == "FILTROS=":
                            self.imagen.mirrorY = True
                        self.listaTokens.append(Token.Token("Filtro", cadena, "MIRRORX | MIRRORY | DOUBLEMIRROR", linea, noCaracter))

                    elif cadena=="DOUBLEMIRROR":
                        if self.comprobar == "FILTROS=":
                            self.imagen.doubleMirror = True
                        self.listaTokens.append(Token.Token("Filtro", cadena, "MIRRORX | MIRRORY | DOUBLEMIRROR", linea, noCaracter))

                    else:
                        self.listaErrores.append(Errores.Error("Token no reconocido", cadena, linea, noCaracter))

                    noCaracter += 1
                    cadena=""
                    estado=0
                    i-=1

            elif estado==2:
                if re.match("[a-zA-Z0-9]",c):
                    cadena += c
                    noCaracter += 1

                else:
                    noCaracter -= 1

                    if re.fullmatch("#[abcdefABCDEF0-9]{6}",cadena):
                        if re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,",self.comprobar):
                            self.comprobar+=cadena
                            self.posicion.color=cadena

                        self.listaTokens.append(Token.Token("Codigo Color Hex", cadena, "#[a-zA-Z0-9]]{6}", linea, noCaracter))

                    else:
                        self.listaErrores.append(Errores.Error("Token no reconocido", cadena, linea, noCaracter))

                    noCaracter += 1
                    cadena = ""
                    estado = 0
                    i -= 1

            elif estado==3:
                if re.match("[0-9]",c):
                    cadena += c
                    noCaracter += 1

                else:
                    if re.match("[a-zA-Z]", c):
                        cadena += c
                        noCaracter += 1
                        i += 1
                        continue

                    noCaracter -= 1

                    if re.fullmatch("[0-9]+",cadena):
                        if self.comprobar == "ALTO=":
                            self.imagen.setHeight(float(cadena))
                            self.comprobar = ""

                        elif self.comprobar == "ANCHO=":
                            self.imagen.setWidth(float(cadena))
                            self.comprobar = ""

                        elif self.comprobar == "FILAS=":
                            self.imagen.setFilas(float(cadena))
                            self.comprobar = ""

                        elif self.comprobar == "COLUMNAS=":
                            self.imagen.setColumnas(float(cadena))
                            self.comprobar = ""

                        elif re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[",self.comprobar):
                            self.posicion.x=(int(cadena))
                            self.comprobar+=cadena

                        elif re.fullmatch("CELDAS=\{(\[([0-9]+)?,([0-9]+)?,((TRUE|FALSE))?,(\#[0-9A-Za-z]{6})?\],?)*\[([0-9]+)?,",self.comprobar):
                            self.posicion.y=(int(cadena))
                            self.comprobar+=cadena

                        self.listaTokens.append(Token.Token("Entero", cadena, "[0-9]+", linea, noCaracter))

                    else:
                        self.listaErrores.append(Errores.Error("Token no reconocido", cadena, linea, noCaracter))

                    noCaracter += 1
                    cadena = ""
                    estado = 0
                    i -= 1

            elif estado==4:
                if c!='"':
                    cadena += c
                    noCaracter += 1

                else:
                    cadena += c

                    if re.fullmatch('"[^"]*"',cadena):
                        if self.comprobar == "TITULO=":
                            self.imagen.setTitulo(cadena)
                            self.comprobar = ""

                        self.listaTokens.append(Token.Token("String", cadena, '"[^"]*"', linea, noCaracter))

                    else:
                        self.listaErrores.append(Errores.Error("Token no reconocido", cadena, linea, noCaracter))

                    cadena = ""
                    estado = 0

            elif estado==5:
                if c=="@":
                    cadena += c
                    noCaracter += 1

                else:
                    noCaracter -= 1

                    if re.match("\@{4,}",cadena):
                        self.listaImagenes.append(self.imagen)
                        self.imagen = Imagen.Imagen()
                        self.listaTokens.append(Token.Token("Separador de Imagen", cadena, "@{4}", linea, noCaracter))

                        if not re.fullmatch("\@{4}",cadena):
                            self.listaErrores.append(Errores.Error("Excedente de separador", cadena, linea, noCaracter))

                    noCaracter += 1
                    cadena = ""
                    estado = 0
                    i -= 1

            i+=1

    def getTokens(self):
        return self.listaTokens

    def getErrores(self):
        return self.listaErrores
