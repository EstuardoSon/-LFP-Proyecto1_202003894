from cairosvg import svg2png
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import Image
import Analizador
import os

class Ventana:
    def __init__(self, ventana):
        self.lienzo=None
        self.contenido=""
        self.procesar=None
        self.ventana = ventana
        self.ventana.title("Bitxelart")
        self.ventana.iconbitmap("icono.ico")
        self.frame = Frame(self.ventana,bg="grey",width=750,height=600)
        self.frame.pack()
        self.listaImagen= ttk.Combobox(self.frame, state="readonly")
        self.listaImagen.place(height=20, width=115,x=291,y=1)

    def crearBoton(self, texto, alto, ancho,X,Y,color="white"):
        if texto=="Cargar Archivos":
            self.listaImagen["values"] = []
            btn=Button(self.frame,text=texto,bg=color,command=self.cargarArchivo)
        elif texto=="Analizar Archivos":
            btn=Button(self.frame,text=texto,bg=color,command=self.analizarTexto)
        elif texto == "Ver Reportes":
            btn = Button(self.frame, text=texto, bg=color, command=self.crearHTML)
        elif texto == "Ver Reportes":
            btn = Button(self.frame, text=texto, bg=color, command=self.crearHTML)
        elif texto == "Original":
            btn = Button(self.frame, text=texto, bg=color, command=self.verOriginal)
        elif texto == "Mirror X":
            btn = Button(self.frame, text=texto, bg=color, command=self.verX)
        elif texto == "Mirror Y":
            btn = Button(self.frame, text=texto, bg=color, command=self.verY)
        elif texto == "Double Mirror":
            btn = Button(self.frame, text=texto, bg=color, command=self.verD)
        else:
            btn = Button(self.frame, text=texto, bg=color,command=self.ventana.destroy)
        btn.place(x=X,y=Y,width=ancho,height=alto)
        return btn

    def crearLienzo(self, imagen=None):
        self.lienzo=Label(self.frame,image=imagen)
        self.lienzo.place(x=196,y=50,width=500,height=500)
        self.ventana.mainloop()

    def cargarArchivo(self):
        try:
            self.listaImagen["values"] = []
            nameFile = filedialog.askopenfilename(initialdir="/",title="Seleccione un archivo",filetypes=(("PXLA files","*.pxla"),("all files","*.*")))
            file=open(nameFile,"r",encoding="utf-8")
            self.contenido=file.read()

            file.close()
        except:
            print("No se pudo leer el archivo")

    def analizarTexto(self):
        self.procesar=Analizador.Analizador(self.contenido)
        self.procesar.reconocerTokens()
        print("Tokens Reconocidos!!!")

        for imagen in self.procesar.listaImagenes:
            values = list(self.listaImagen["values"])
            self.listaImagen["values"] = values + [imagen.titulo]


    def crearHTML(self):
        try:
            file=open("Reportes\Tokens.html","w",encoding="utf-8")
            css='''<style type="text/css">
            border-collapse: collapse;
            width: 100%;
            }

            th, td {
            text-align: center;
            padding: 8px;
            }

            tr:nth-child(even){background-color: #f2f2f2}

            th {
            background-color: #04AA6D;
            color: white;
            }
            </style>'''

            file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Tokens e Imagenes</title>\n<meta charset='utf-8'>\n"+css+"\n</head>\n<body>")
            file.write("<H1>Lista de Tokens</H1> \n")
            file.write("<table border='2'> \n<tr>\n<th>Tipo</th>\n<th>Lexema</th>\n<th>Patron</th>\n<th>Linea</th>\n<th>No. Caracter</th>\n</tr>\n")
            for token in self.procesar.getTokens():
                file.write("<tr>\n<td>"+str(token.tipo)+"</td>\n<td>"+str(token.lexema)+"</td>\n<td>"+str(token.patron)+"</td>\n<td>"+str(token.linea)+"</td>\n<td>"+str(token.noCaracter)+"</td>\n</tr>\n")

            file.write("</table>\n<H1>Lista de Errores</H1> \n")
            file.write("<table border='2'> \n<tr>\n<th>Tipo</th>\n<th>Lexema</th>\n<th>Linea</th>\n<th>No. Caracter</th>\n</tr>\n")
            for error in self.procesar.getErrores():
                file.write("<tr>\n<td>" + str(error.tipo) + "</td>\n<td>" + str(error.lexema)+ "</td>\n<td>" + str(error.linea) + "</td>\n<td>" + str(error.noCaracter) + "</td>\n</tr>\n")

            file.write("</table>\n<br/>\n")
            for imagen in self.procesar.listaImagenes:
                file.write("<H2>"+imagen.titulo+"<H2>\n")
                file.write("<table cellspacing='5'>\n<tr>\n")
                file.write("<td>\n<H3> Original <H3>\n"+imagen.crearImagen()+"</td>\n")
                if imagen.mirrorX==True:
                    file.write("<td>\n<H3> MirrorX <H3>\n")
                    file.write(imagen.crearMirrorX()+"</td>\n")
                if imagen.mirrorY==True:
                    file.write("<td>\n<H3> MirrorY <H3>\n")
                    file.write(imagen.crearMirrorY()+"</td>\n")
                if imagen.doubleMirror==True:
                    file.write("<td>\n<H3> DoubleMirror <H3>\n")
                    file.write(imagen.crearMirrorD()+"</td>\n")
                file.write("</tr>\n</table>\n")

            file.write("</body>\n</html>")
            file.close()
            os.system("Reportes\Tokens.html")

        except:
            print("Ocurrio un error en al crear el archivo!!!")

    def verOriginal(self):
        for imagen in self.procesar.listaImagenes:
            if imagen.titulo==self.listaImagen.get():
                svg2png(bytestring=imagen.crearImagen(), write_to='Reportes\imagen.png')
                redimensionar=Image.open("Reportes\imagen.png")
                redimensionar = redimensionar.resize((500, 500), Image.ANTIALIAS)
                redimensionar.save("Reportes\imagen.png","png")
                imagens = PhotoImage(file="Reportes\imagen.png")
                self.crearLienzo(imagens)

    def verX(self):
        for imagen in self.procesar.listaImagenes:
            if imagen.titulo==self.listaImagen.get() and imagen.mirrorX==True:
                svg2png(bytestring=imagen.crearMirrorX(), write_to='Reportes\imagen.png')
                redimensionar = Image.open("Reportes\imagen.png")
                redimensionar = redimensionar.resize((500, 500), Image.ANTIALIAS)
                redimensionar.save("Reportes\imagen.png", "png")
                imagens = PhotoImage(file="Reportes\imagen.png")
                self.crearLienzo(imagens)

    def verY(self):
        for imagen in self.procesar.listaImagenes:
            if imagen.titulo==self.listaImagen.get() and imagen.mirrorY==True:
                svg2png(bytestring=imagen.crearMirrorY(), write_to='Reportes\imagen.png')
                redimensionar = Image.open("Reportes\imagen.png")
                redimensionar = redimensionar.resize((500, 500), Image.ANTIALIAS)
                redimensionar.save("Reportes\imagen.png", "png")
                imagens = PhotoImage(file="Reportes\imagen.png")
                self.crearLienzo(imagens)

    def verD(self):
        for imagen in self.procesar.listaImagenes:
            if imagen.titulo==self.listaImagen.get() and imagen.doubleMirror==True:
                svg2png(bytestring=imagen.crearMirrorD(), write_to='Reportes\imagen.png')
                redimensionar = Image.open("Reportes\imagen.png")
                redimensionar = redimensionar.resize((500, 500), Image.ANTIALIAS)
                redimensionar.save("Reportes\imagen.png", "png")
                imagens = PhotoImage(file="Reportes\imagen.png")
                self.crearLienzo(imagens)

