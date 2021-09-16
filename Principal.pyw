from tkinter import *
import Ventana

if __name__=="__main__":
    listaTokens=list()
    ventana=Tk()
    Interfaz=Ventana.Ventana(ventana)

    btnCargar = Interfaz.crearBoton("Cargar Archivos",20,95,1,1)
    btnAnalizar = Interfaz.crearBoton("Analizar Archivos", 20, 100,96,1)
    btnReportes = Interfaz.crearBoton("Ver Reportes", 20, 95,196,1)
    btnSalir = Interfaz.crearBoton("Salir", 20, 70,406,1)

    btnOriginal= Interfaz.crearBoton("Original", 80, 116, 40, 80,"#CBCFCA")
    btnMirrorX = Interfaz.crearBoton("Mirror X", 80, 116, 40, 160,"#CBCFCA")
    btnMirrorY = Interfaz.crearBoton("Mirror Y", 80, 116, 40, 240,"#CBCFCA")
    btnDMirror = Interfaz.crearBoton("Double Mirror", 80, 116, 40, 320,"#CBCFCA")

    Interfaz.crearLienzo();

    ventana.mainloop()
