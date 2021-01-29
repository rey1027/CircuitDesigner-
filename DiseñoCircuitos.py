"""
**********************************************************
Instituto Tecnológico de Costa Rica (TEC)
Área Académica de Ingeniería en Computadores
Algoritmos y Estructuras de Datos 1
II Semestre, 2020
Rachel Pereira González, Bryan Gomez Matamoros, Gabriel Cerdas Chinchilla
Proyecto 3: Circuit Designer
Main File
Python 3.8.2
**********************************************************
"""
#Bibliotecas Utilizadas
import pygame  
import sys    
import random 
import time    
import threading # hilos
import eztext
from FuentePoder import FuentePoder
from Resistencia import Resistencia
from collections import deque, namedtuple
from Graph import Graph

#Inicio del Programa 
pygame.init()

##FUNCIÓN PRINCIPAL DEL DISEÑADOR DE CIRCUITOS##
def menu():

    ##FUNCIÓN PARA LA IMPORTACIÓN DE CIRCUITO##
    def CargarCircuito(file):
            ruta=file+".txt"#ruta
            archivo=open(ruta)#abrir
            contenido=archivo.readlines()#lectura de las lineas
            archivo.close()#cerrar
            return contenido

   ##FUNCIÓN PARA LA EXPORTACION DE CIRCUITO##
    def GuardarCircuito(file,dato):
            ruta=file+".txt"
            archivo=open(ruta,"a")#a->append
            archivo.write(dato+"\n") # escribe el dato en el archivo
            archivo.close()

    
    #Colores utilizados
    negro = (0,0,0)
    blanco = (255,255,255)
    color = (255, 255, 255)
    colorPassive = pygame.Color("gray15")
    colo = colorPassive

    #Listas Utilizadas
    PuntosEnlace = []
    RectsList = []
    indicadorEstado = []
    ListaGrafo = []
    ListaConexiones = []
    NodoElectronico = []
    NodoElectronico2 = []
    NodosE = []
    NodosE2= []
    ListaTensiones = []
    NombresComponentes = []
    Grafo = []
    GrafoFinal = []

    #Coordenadas iniciales
    x1=15 # Position x initial 
    y1=-55 # Position y initial 

    ##ALGORITMO PARA CREAR EL ÁREA DE DISEÑO##
    for i in range(8): # Up to 5 per row
        y1+=71# Increase in the value of y1 (next box)
        x1=15 
        for j in range(13): # For each column up to 9
            RectsList.append(pygame.Rect(x1,y1,70,70)) # Adding the box to the list
            indicadorEstado.append(0)
            x1+=71 # Increase value of x1 (next box)
    print(indicadorEstado)

    # Ventana del diseñador con sus dimensiones
    Menu = pygame.display.set_mode([1098,650])      

    #Fuentes utilizadas en las palabras
    fuente = pygame.font.Font(None,25)
    fuente2 = pygame.font.Font(None,25)
    fuente3 = pygame.font.Font(None,38)
    back = fuente3.render("<<<",True,(255,227,82))
    
    # Nombre del elemento
    userText = ""
    # Valor del elementpo
    userText2 = ""
    #Nombre del archivo (Importar/Exportar)
    userText3 = ""

    #Indicadores
    textSeleccion = "Componente:"
    textSeleccion2 = " ------ "
    unid = "---"

    ##Imagenes Utilizadas
    Seleccion_Image = pygame.image.load("imagenesCD/resistencia1.png").convert()
    Seleccion_Image = pygame.transform.scale(Seleccion_Image, (55, 100))
    MainMenu_Image = pygame.image.load("imagenesCD/fondo1.png").convert()
    Resistencia_Image = pygame.image.load("imagenesCD/resistencia1.png").convert()
    ResistenciaH_Image = pygame.image.load("imagenesCD/resistencia2.png").convert()
    ResistenciaS_Image = pygame.image.load("imagenesCD/resistenciaS3.png").convert()
    FPoder_Image = pygame.image.load("imagenesCD/fuentepoder1.jpg").convert()
    FPoderH_Image = pygame.image.load("imagenesCD/fuentepoder2.jpg").convert()
    FPoderS_Image = pygame.image.load("imagenesCD/fuentepoderS3.jpg").convert()
    Slot = pygame.image.load("imagenesCD/Empty.png").convert()
    Borrar_Image = pygame.image.load("imagenesCD/Borrar.png").convert()
    Girar_Image = pygame.image.load("imagenesCD/Girar.png").convert()
    Importar_Image = pygame.image.load("imagenesCD/importar.png")
    Exportar_Image = pygame.image.load("imagenesCD/Exportar.png")
    Exportar_Image = pygame.transform.scale(Exportar_Image, (140, 38))
    Simulacion_Image = pygame.image.load("imagenesCD/Simulacion.png")
    
    #Grafo = nx.Graph()

    
    #Color de la venta
    Menu.fill((3, 152, 158))

    #Dibuja los cuadros blancos
    for recs in RectsList: # For the squares in the list
            Menu.blit(Slot,(recs[0],recs[1]))

    #Variables Globales
    global seleccionFPoder
    seleccionFPoder = [False]

    global seleccionResistencia
    seleccionResistencia = [False]

   #Rectangulos de diseño
    inputRect = pygame.Rect(962,249,112,22)
    inputRectValor = pygame.Rect(962,299,82,22)
    inputExpImp = pygame.Rect(956,519,125,22)
    seleccionRect =  pygame.Rect(957,170,120,161)
    seleccionRect2 = pygame.Rect(960,173,115,155)
    eliminarRect = pygame.Rect(981,500,70,70)
    infoEliminar = pygame.Rect(16,587,850,55)
    infoDijkstra = pygame.Rect(15,1,923,25)
    interfazRect = pygame.Rect(942,15,152,630)
    AtrasRect = pygame.Rect(868,587,69,55)

    #DIbujar rectangulo
    pygame.draw.rect(Menu,(76,36,147),interfazRect)
    pygame.draw.rect(Menu,(3,82,88),AtrasRect)
    Menu.blit(back,(AtrasRect.x+11,AtrasRect.y+14))

    #Controladores de las acciones
    activo = False
    activo2 = False
    activo3 = False
    eliminar = False
    voltear = False
    exportar = False
    importar = False
    conectar = 0
    simulacion = False
    contNodoE = 0
    MostrarTensiones = False
    conecta2 = False
    global contDijk
    contDijk=0
    detener = False
    cantidadNodosE = 0
    D1 = 0

    #Variable para el cambio de color de los nodos 
    colorNodoE = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    


    # we'll use infinity as a default distance to nodes.
    inf = float('inf')
    Edge = namedtuple('Edge', 'start, end, cost')


    def make_edge(start, end, cost=1):
        return Edge(start, end, cost)

    ##FUNCION PARA EL ORDEN ALFABETICO##
    def ord_alf(cadena):
       alfabeto = {
              "A":1, "a":1, "Á":1, "á":1,
              "B":2, "b":2,
              "C":3, "c":3,
              "D":4, "d":4,
              "E":5, "e":5, "É":5, "é":5,
              "F":6, "f":6,
              "G":7, "g":7,
              "H":8, "h":8,
              "I":9, "i":9, "Í":9, "í":9,
              "J":10, "j":10,
              "K":11, "k":11,
              "L":12, "l":12,
              "M":13, "m":13,
              "N":14, "n":14,
              "Ñ":15, "ñ":15,
              "O":16, "o":16, "Ó":16, "ó":16,
              "P":17, "p":17,
              "Q":18, "q":18,
              "R":19, "r":19,
              "S":20, "s":20,
              "T":21, "t":21,
              "U":22, "u":22, "Ú":22, "ú":22,
              "V":23, "v":23,
              "W":24, "w":24,
              "X":25, "x":25,
              "Y":26, "y":26,
              "Z":27, "z":27,
              }
       #Listas       
       codigos=[ ]

       ##ALGORITMO PARA INTERCAMBIAR LETRAS POR NUMEROS##
       for letra in cadena :
              codigos.append(alfabeto[letra])
       return codigos

    ##ALGORITMO DE QUICK SORT PARA ORDENAR ASCENDENTE LOS NOMBRES DE LAS RESISTENCIAS##
    def sort(lista):
        izquierda = []
        centro = []
        derecha = []
        if len(lista) > 1:
            pivote = lista[0]
            for i in lista:
                if i < pivote:
                    izquierda.append(i)
                elif i == pivote:
                    centro.append(i)
                elif i > pivote:
                    derecha.append(i)
            return sort(izquierda)+centro+sort(derecha)
        else:
            return lista

    ##ALGORITMO DE INSERTION SORT PARA ORDENAR DESCENDENTE LOS NOMBRES DE LAS RESISTENCIAS##
    def insertionSort(NombresComponentes):
        for index in range(1,len(NombresComponentes)):
            valor = NombresComponentes[index]
            posicion = index
            while posicion >0 and NombresComponentes[posicion-1]< valor:
                NombresComponentes[posicion]=NombresComponentes[posicion-1]
                posicion = posicion-1
            NombresComponentes[posicion]= valor
    insertionSort(NombresComponentes)

    #BUCLE PRINCIPAL DEL DISEÑADOR DE CIRCUITOS 
    while True:

        #BUCLE DE EVENTOS 
        for event in pygame.event.get():
            #Evento Salir
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Eventos de teclas  
            if event.type == pygame.KEYDOWN:

                #Para escribir en el nombre del componente
                if activo == True:
                    if event.key == pygame.K_BACKSPACE:
                        userText = userText[0:-1]
                    else:    
                        userText += event.unicode
                #Para escribir en el valor del componente
                if activo2 == True:
                    if event.key == pygame.K_BACKSPACE:
                        userText2 = userText2[0:-1]
                    else:    
                        userText2 += event.unicode
                #Para escribir en el nombre de circuito 
                if activo3 == True:
                    if event.key == pygame.K_BACKSPACE:
                        userText3 = userText3[0:-1]
                    else:    
                        userText3 += event.unicode

                #Evento de para que la tecla S hacer el cambio de nodo y de color 
                if event.key == pygame.K_s:
                    contNodoE+=1
                    colorNodoE = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    NodosE2.append(NodoElectronico2)
                    NodosE.append(NodoElectronico)
                    NodoElectronico = []
                    print (NodosE)
                    randomCorriente = random.randint(1,1000)
                    ListaTensiones += [[random.randint(1,10),randomCorriente]]
                    for num in range(cantidadNodosE,len(Grafo)): 
                        Grafo[num][2]= randomCorriente
                        cantidadNodosE+=1
                    print(Grafo)
                    

            
            #Eventos de click en pantanlla
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                ## Al seleccionar el segundo punto, se ejecuta el dijkstra
                if D1!=0:
                    for cadaNodo in NodosE:
                    #print(cadaNodo)
                        Pos+=1
                        for cadaPunto in cadaNodo:
                            if cadaPunto.collidepoint(event.pos):
                                for j in ListaGrafo:
                                    if j[5]==cadaPunto or j[6]==cadaPunto:
                                        D2 = j[0]
                                        pygame.draw.rect(Menu,(negro),infoDijkstra)
                                        activoDijk = fuente2.render("     Ruta mas corta de ("+str(D1)+") hacia ("+str(D2)+") : "+str(GrafoFinal.dijkstra(D1,D2)), True, (blanco))
                                        Menu.blit(activoDijk,infoDijkstra)
                                        print(GrafoFinal.dijkstra(D1,D2))
                                        D1=0

                #Posición del Mouse
                PositionMenu = pygame.mouse.get_pos()
                print(PositionMenu)


                #Colisiones con el rectagulo del nombre del elemento
                if inputRect.collidepoint(event.pos):
                    activo = True
                if not inputRect.collidepoint(event.pos):
                    activo = False

                #Colisiones con el rectagulo del valor del elemento
                if inputRectValor.collidepoint(event.pos):
                    activo2 = True
                if not inputRectValor.collidepoint(event.pos):
                    activo2 = False

                #Colisiones con el rectagulo del nombre del archivo
                if inputExpImp.collidepoint(event.pos):
                    activo3 = True
                    print(activo3,activo2,activo)
                if not inputExpImp.collidepoint(event.pos):
                    activo3 = False 

                if AtrasRect.collidepoint(event.pos):
                    return principal()

                if PositionMenu[0]>80 and PositionMenu[0]<930 and PositionMenu[1]<570:
                    
                    #Ubicar la fuente de poder en el area de diseño
                    if seleccionFPoder[0]:
                       
                       #Variable
                        seleccionFPoder[0]=False
                        Posicion = -1

                        ##ALGORITMO PARA AVERIGUAR RECTANGULO UTILIZADO##
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1

                            if recs.collidepoint(event.pos):

                                indicadorEstado[Posicion-1] = 5
                                indicadorEstado[Posicion] = 1
                                recs.x = recs[0]
                                recs.y = recs[1]

                                Menu.blit(FPoder_Image,recs)

                                InfoN = fuente2.render(userText, True, (negro))
                                InfoV = fuente2.render(userText2+" V", True, (negro))

                                Menu.blit(InfoN,(recs[0]-57,recs[1]-40))
                                Menu.blit(InfoV,(recs[0]-47,recs[1]-20))

                                #Dibujar los puntos de enlace de los componentes
                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))
                                a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                PuntosEnlace.append(a)
                                pygame.draw.rect(Menu, negro, a)
                                b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                PuntosEnlace.append(b)
                                pygame.draw.rect(Menu, negro, b)

                                #Agregar un nodo al grafo
                                ListaGrafo.append([userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b,a.x,a.y,b.x,b.y])
                                nFPoder = FuentePoder(userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b)

                        #Reiniciar los campos
                        textSeleccion2 = " ------ "
                        unid="---"
                        userText2=""
                        userText=""

                    #Eliminar todo lo relacionado a un componente
                    if eliminar:
                        eliminar = False

                        Posicion = -1

                        ##ALGORITMO PARA SABER QUE ELIMINAR EN EL AREA DE DISEÑO##
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1

                            if recs.collidepoint(event.pos):

                                #Indicar que todo lo del elemento este eliminado
                                indicadorEstado[Posicion-1] = 0
                                indicadorEstado[Posicion+1] = 0
                                indicadorEstado[Posicion-13] = 0
                                indicadorEstado[Posicion+13] = 0
                                indicadorEstado[Posicion-14] = 0
                                indicadorEstado[Posicion] = 0
                                recs.x = recs[0]
                                recs.y = recs[1]

                                #Poner los rectangulos en blanco
                                Menu.blit(Slot,recs)
                                Menu.blit(Slot,RectsList[Posicion-1])
                                Menu.blit(Slot,RectsList[Posicion+1])
                                Menu.blit(Slot,RectsList[Posicion+13])
                                Menu.blit(Slot,RectsList[Posicion-13])
                                Menu.blit(Slot,RectsList[Posicion-14])

                                #Remove todos los puntos de enlace del componente
                                for i in PuntosEnlace:
                                    if i == pygame.Rect(recs.x+31,recs.y-40,7,5):
                                        PuntosEnlace.remove(i)
                                for i in PuntosEnlace:
                                    if i == pygame.Rect(recs.x+31,recs.y+106,7,5):
                                        PuntosEnlace.remove(i)
                                for i in PuntosEnlace:
                                    if i == pygame.Rect(recs.x-40,recs.y+31,5,7):
                                        PuntosEnlace.remove(i)
                                for i in PuntosEnlace:
                                    if i == pygame.Rect(recs.x+106,recs.y+31,5,7):
                                        PuntosEnlace.remove(i)

                                #Remove el nodo del grafo
                                for nodo in ListaGrafo:
                                    if nodo[3] == recs.x and nodo[4] == recs.y:
                                        ListaGrafo.remove(nodo)
                                    for i in NombresComponentes:
                                        if nodo[0] == i:
                                                NombresComponentes.remove(i)

                        #Limpiar los campos
                        textSeleccion2 = " ------ "
                        unid="---"

                    #Girar el componente
                    if voltear:
                        voltear = False
                        Posicion = -1

                        ##ALGORITMO PARA SABER CUAL ELEMENTO DE GIRAR##
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1
                            if recs.collidepoint(event.pos):
                                #Fuente de Poder Horizontal 
                                if indicadorEstado[Posicion] == 2:

                                    #Indica la posicion a cambiar vertical
                                    indicadorEstado[Posicion] = 1
                                    recs.x = recs[0]
                                    recs.y = recs[1]

                                    #Cambia la imagen de la orientación indicada
                                    Menu.blit(FPoder_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-1])
                                    Menu.blit(Slot,RectsList[Posicion+1])
                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))

                                    #Eliminar puntos de enlace antiguos
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x-40,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+106,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)

                                    #Crear nuevos puntos de enlace
                                    a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    #Cambio de las coordenadas de los puntos de enlace 
                                    for recs in RectsList: # For the squares in the list
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 1 
                                                nodo[5] = a
                                                nodo[6] = b
                                                nodo[7] = a.x
                                                nodo[8] = a.y
                                                nodo[9] = b.x
                                                nodo[10] = b.y
                                
                                #Fuente de Poder Vertical
                                elif indicadorEstado[Posicion] == 1:

                                    #Indica la posicion a cambiar horizontal
                                    indicadorEstado[Posicion] = 2
                                    recs.x = recs[0]
                                    recs.y = recs[1]

                                    #Cambia la imagen de la orientación indicada
                                    Menu.blit(FPoderH_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-13])
                                    Menu.blit(Slot,RectsList[Posicion+13])

                                    pygame.draw.rect(Menu,(negro),(recs.x-40,recs.y+34,40,2))
                                    pygame.draw.rect(Menu,(negro),(recs.x+66,recs.y+34,40,2))
                                    
                                    #Eliminar puntos de enlace antiguos
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y-40,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y+106,7,5):
                                            PuntosEnlace.remove(i)

                                    #Crear nuevos puntos de enlace
                                    a = pygame.Rect(recs.x-40,recs.y+31,5,7)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+106,recs.y+31,5,7)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    #Cambio de las coordenadas de los puntos de enlace
                                    for recs in RectsList: 
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 2 
                                                nodo[5] = a
                                                nodo[6] = b
                                                nodo[7] = a.x
                                                nodo[8] = a.y
                                                nodo[9] = b.x
                                                nodo[10] = b.y

                                    print(ListaGrafo)

                                #Resistencia Horizontal
                                elif indicadorEstado[Posicion] == 4:

                                    #Indica la posicion a cambiar vertical
                                    indicadorEstado[Posicion] = 3
                                    recs.x = recs[0]
                                    recs.y = recs[1]

                                    #Cambia la imagen de la orientación indicada
                                    Menu.blit(Resistencia_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-1])
                                    Menu.blit(Slot,RectsList[Posicion+1])

                                    #Eliminar puntos de enlace antiguos
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x-40,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+106,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)

                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))

                                    #Crear nuevos puntos de enlace
                                    a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    #Cambio de las coordenadas de los puntos de enlace
                                    for recs in RectsList: 
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 3 
                                                nodo[5] = a
                                                nodo[6] = b
                                                nodo[7] = a.x
                                                nodo[8] = a.y
                                                nodo[9] = b.x
                                                nodo[10] = b.y

                                #Resistencia Vertical
                                elif indicadorEstado[Posicion] == 3:

                                    #Indica la posicion a cambiar horizontal
                                    indicadorEstado[Posicion] = 4
                                    recs.x = recs[0]
                                    recs.y = recs[1]

                                    #Cambia la imagen de la orientación indicada
                                    Menu.blit(ResistenciaH_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-13])
                                    Menu.blit(Slot,RectsList[Posicion+13])

                                    pygame.draw.rect(Menu,(negro),(recs.x-40,recs.y+34,40,2))
                                    pygame.draw.rect(Menu,(negro),(recs.x+66,recs.y+34,40,2))
                                    
                                    #Eliminar puntos de enlace antiguos
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y-40,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y+106,7,5):
                                            PuntosEnlace.remove(i)

                                    #Crear nuevos puntos de enlace
                                    a = pygame.Rect(recs.x-40,recs.y+31,5,7)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+106,recs.y+31,5,7)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    #Cambio de las coordenadas de los puntos de enlace
                                    for recs in RectsList: 
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 4 
                                                nodo[5] = a
                                                nodo[6] = b
                                                nodo[7] = a.x
                                                nodo[8] = a.y
                                                nodo[9] = b.x
                                                nodo[10] = b.y

                        #Limpiar el campo 
                        textSeleccion2 = " ------ "
                        unid="---"

                    #Colocar una resistencia
                    if seleccionResistencia[0]:
                        
                        seleccionResistencia[0]=False
                        Posicion = -1
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1
                            if recs.collidepoint(event.pos):

                                #Indica el elemento a colocar
                                indicadorEstado[Posicion-1] = 5
                                indicadorEstado[Posicion] = 3
                                recs.x = recs[0]
                                recs.y = recs[1]

                                #Dibuja la imagen de la orientación 
                                Menu.blit(Resistencia_Image,recs)
                                InfoN = fuente2.render(userText, True, (negro))
                                InfoV = fuente2.render(userText2+" Ω", True, (negro))
                                Menu.blit(InfoN,(recs[0]-57,recs[1]-40))
                                Menu.blit(InfoV,(recs[0]-47,recs[1]-20))
                                
                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))

                                #Crear nuevos puntos de enlace
                                a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                PuntosEnlace.append(a)
                                pygame.draw.rect(Menu, negro, a)
                                b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                PuntosEnlace.append(b)
                                pygame.draw.rect(Menu, negro, b)

                                #Agregar un nodo al grafo
                                ListaGrafo.append([userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b,a.x,a.y,b.x,b.y])
                                nResist = Resistencia(userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b)
                                print(ListaGrafo)

                        #Limpiar campos        
                        textSeleccion2 = " ------ "
                        unid="---"
                        userText2=""
                        userText=""

                    # Conexion entre puntos
                    Punto = -1
                    #conexion1=0
                    #enlazado1=0
                    print(PuntosEnlace)
                    
                    for puntos in PuntosEnlace: # For the squares in the list
                        Punto+=1

                        #Seleccionar el primer punto de conexión
                        if puntos.collidepoint(event.pos) and conectar == 0:
                            print("puntos[0]")
                            print(puntos[0])
                            for nodo in ListaGrafo:
                                if nodo[5][1] == puntos[1]:
                                    if nodo[5][0] == puntos[0]:
                                        x=nodo[5][0]
                                        print(x)
                                        y=nodo[5][1]
                                        enlazado1 = nodo[5]
                                        print(y)
                                        print("uno")
                                        nombre1=nodo[0]

                                if nodo[6][1] == puntos[1]:
                                    if nodo[6][0] == puntos[0]:
                                        x=nodo[6][0]
                                        print(x)
                                        y=nodo[6][1]
                                        enlazado1 = nodo[6]
                                        print(y)
                                        print("dos")
                                        nombre1=nodo[0]

                            ##ALGORITMO PARA SABER EL PUNTO DE ENLACE DEL COMPONENTE QUE SE UTILIZA##
                            pygame.draw.rect(Menu, (219, 177, 48), puntos)
                            p1=(puntos[0],puntos[1])
                            conectar = 1
                            break     

                        #Seleccionar otro punto de conexión y dibuja el cable 
                        elif puntos.collidepoint(event.pos) and conecta2:

                            ##ALGORITMO PARA SABER EL PUNTO DE ENLACE DEL COMPONENTE QUE SE UTILIZA Y AGREGARLO AL GRAFO DE NODOS ELECTRONICOS##
                            for nodo in ListaGrafo:
                                if nodo[5][0] == puntos[0] and nodo[5][1] == puntos[1]:
                                    conexion2 = nodo[5] 
                                    enlazado2 = nodo[5]
                                    print("tres")

                                    #ListaConexiones.append([conexion1,conexion2])
                                    
                                    NodoElectronico.append(enlazado1)
                                    NodoElectronico.append(enlazado2)
                                    print(NodoElectronico)
                                    Grafo.append([str(nombre1),str(nodo[0]),0])
                                    
                                    NodoElectronico2.append(enlazado1.x)
                                    NodoElectronico2.append(enlazado1.y)
                                    NodoElectronico2.append(enlazado2.x)
                                    NodoElectronico2.append(enlazado2.y)
                                    break

                                elif nodo[6][0] == puntos[0] and nodo[6][1] == puntos[1]:
                                    conexion2 = nodo[6]
                                    enlazado2 = nodo[6]
                                    print("cuatro")

                                    #ListaConexiones.append([conexion1,enlazado1,conexion2,enlazado2])

                                    NodoElectronico.append(enlazado1)
                                    NodoElectronico.append(enlazado2)
                                    print(NodoElectronico)
                                    Grafo.append([str(nombre1),str(nodo[0]),0])

                                    NodoElectronico2.append(enlazado1.x)
                                    NodoElectronico2.append(enlazado1.y)
                                    NodoElectronico2.append(enlazado2.x)
                                    NodoElectronico2.append(enlazado2.y)
                                    break
                                    
                            #Dibuja el cable de conexión
                            pygame.draw.line(Menu, colorNodoE, (p1[0],p1[1]), (puntos[0], puntos[1]),2)
                            pygame.draw.rect(Menu, (219, 177, 48), puntos)
                            conectar = 0
                            conecta2=False
                            break


                if conectar ==1:
                    conecta2=True
                #Al pulsar botón eliminar
                if PositionMenu[0]>948 and PositionMenu[0]<1028 and PositionMenu[1]>340 and PositionMenu[1]<410:
                    eliminar = True
                    print(NodoElectronico)

                #Al pulsar botón voltear
                if PositionMenu[0]>1021 and PositionMenu[0]<1091 and PositionMenu[1]>340 and PositionMenu[1]<410:
                    voltear = True

                #Al pulsar botón simular
                if PositionMenu[0]>950 and PositionMenu[0]<1085 and PositionMenu[1]>568 and PositionMenu[1]<640:
                    simulacion = True

                #Al pulsar botón de Fuente de Poder
                if PositionMenu[0]>981 and PositionMenu[0]<1051 and PositionMenu[1]>15 and PositionMenu[1]<85:
                    seleccionFPoder[0] = True
                    seleccionResistencia[0] = False
                    textSeleccion2 = "Fuente"
                    unid = "V"

                #Al pulsar botón de Resistencia
                if PositionMenu[0]>981 and PositionMenu[0]<1051 and PositionMenu[1]>90 and PositionMenu[1]<160:
                    seleccionResistencia[0] = True
                    seleccionFPoder[0] = False
                    textSeleccion2 = "Resistencia"
                    unid = "Ω"

                #Al pulsar botón de exponer
                if PositionMenu[0]>955 and PositionMenu[0]<1080 and PositionMenu[1]>474 and PositionMenu[1]<506:
                    exportar = True

                #Al pulsar botón de importar
                if PositionMenu[0]>955 and PositionMenu[0]<1080 and PositionMenu[1]>433 and PositionMenu[1]<465:
                    importar = True   

        #Pegar los botones
        Menu.blit(Borrar_Image,(948,340))
        Menu.blit(Girar_Image,(1021,340))
        pygame.draw.rect(Menu,(225, 227, 82),seleccionRect,5)
        pygame.draw.rect(Menu,(3,82,88),seleccionRect2)
        #´Funcion para la sinulacion del circuito  
        if simulacion:

            #Añadir los nombres de los componentes
            for i in ListaGrafo:
                if i[2] == 3 or i[2] == 4:
                    NombresComponentes.append(i[0])

            GrafoDijkstra = []
            for edge in Grafo:
                GrafoDijkstra.append((edge[0],edge[1],edge[2]))
            print(GrafoDijkstra)
            GrafoFinal = Graph(GrafoDijkstra)
            #Bloqueo de los botones
            eliminar = False
            voltear = False
            activo = False
            activo2 = False
            seleccionFPoder[0] = False
            seleccionResistencia[0] = False
            conectar = 0

            #Manejo de las coordenadas
            PositionSimulacion = pygame.mouse.get_pos()
            
            #Agregar un valor aleatorio al nodo electronico
            numNodo = 0
            
            #Controladores
            MostrarTensiones = True
            simulacion = False

        #Activar la función eliminar
        if eliminar:
            pygame.draw.rect(Menu,(255,255,255),infoEliminar)
            activoEliminar = fuente2.render("Seleccione el componente electronico que desea eliminar", True, (negro))
            Menu.blit(activoEliminar,infoEliminar)
        if not eliminar:
            pygame.draw.rect(Menu,(negro),infoEliminar)

        #Activar la función voltear
        if voltear:
            pygame.draw.rect(Menu,(255,255,255),infoEliminar)
            activoEliminar = fuente2.render("Seleccione el componente electronico que desea girar", True, (negro))
            Menu.blit(activoEliminar,infoEliminar)

        #Activar la función exportar
        if exportar:  
            for cadaComponente in ListaGrafo:
                GuardarCircuito(userText3,str(cadaComponente))
            for i in NodosE2:
                GuardarCircuito(userText3+"Nodos",str(i))
            
            userText3 = ""
            exportar = False

        #Activar la función importar
        #Se reinicia todo de nuevo 
        if importar:
            userText = ""
            # Valor
            userText2 = ""

            textSeleccion2 = " ------ "
            unid = "---"
            ListaGrafo = []
            ListaConexiones = []
            for recs in RectsList: # For the squares in the list
                    Menu.blit(Slot,(recs[0],recs[1]))
            for indicador in indicadorEstado:
                indicador = 0

            seleccionFPoder = [False]
            seleccionResistencia = [False]
            color = (255, 255, 255)
            colorPassive = pygame.Color("gray15")
            colo = colorPassive
            activo = False
            activo2 = False
            activo3 = False
            eliminar = False
            voltear = False
            exportar = False
            #importar = False
            conectar = 0
            simulacion = False
            contNodoE = 0
            colorNodoE = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            NodoElectronico = []
            NodosE = []
            ListaTensiones = []
            MostrarTensiones = False
            Cargando_Image = FPoder_Image
            InfoV = ""

            #Excepcion para detectar cuando no existe el archivo
            try:
                guardado = CargarCircuito(userText3) #test code
                guardadoNodos = CargarCircuito(userText3+"Nodos")
                #guardado2 = CargarCircuito(userText3+"Nodos")
                # ListaGrafo.append([userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b])
                for cadaLinea in guardado:

                    nombreCargado = cadaLinea.split(",")[0].split("'")[1]
                    valorCargado = cadaLinea.split(",")[1].split("'")[1]
                    indEstadoCargado = int(cadaLinea.split(",")[2])
                    XCargado = int(cadaLinea.split(",")[3])
                    YCargado = int(cadaLinea.split(",")[4])
                    #print(cadaLinea.split("]")[0].split(",")[16])
                    Xpunto1=int(cadaLinea.split(",")[13])
                    Ypunto1=int(cadaLinea.split(",")[14])
                    Xpunto2=int(cadaLinea.split(",")[15])
                    Xpunto2=int(cadaLinea.split("]")[0].split(",")[16])
                    simbolo = 0
                    if indEstadoCargado == 1:
                        Cargando_Image = FPoder_Image
                        simbolo = " V"
                    
                    if indEstadoCargado == 2:
                        Cargando_Image = FPoderH_Image
                        simbolo = " V"
                    
                    if indEstadoCargado == 3:
                        Cargando_Image = Resistencia_Image
                        simbolo = " Ω"

                    if indEstadoCargado == 4:
                        Cargando_Image = ResistenciaH_Image
                        simbolo = " Ω"
                    
                    Menu.blit(Cargando_Image,(XCargado,YCargado))

                    if indEstadoCargado == 2 or indEstadoCargado == 4:
                        pygame.draw.rect(Menu,(negro),(XCargado-40,YCargado+34,40,2))
                        pygame.draw.rect(Menu,(negro),(XCargado+66,YCargado+34,40,2))
                        a = pygame.Rect(XCargado-40,YCargado+31,5,7)
                        PuntosEnlace.append(a)
                        pygame.draw.rect(Menu, negro, a)
                        b = pygame.Rect(XCargado+106,YCargado+31,5,7)
                        PuntosEnlace.append(b)
                        pygame.draw.rect(Menu, negro, b)

                    if indEstadoCargado == 1 or indEstadoCargado == 3:
                        pygame.draw.rect(Menu,(negro),(XCargado+33,YCargado-40,2,40))
                        pygame.draw.rect(Menu,(negro),(XCargado+33,YCargado+69,2,40))
                        a = pygame.Rect(XCargado+31,YCargado-40,7,5)
                        PuntosEnlace.append(a)
                        pygame.draw.rect(Menu, negro, a)
                        b = pygame.Rect(XCargado+31,YCargado+106,7,5)
                        PuntosEnlace.append(b)
                        pygame.draw.rect(Menu, negro, b)

                    InfoN = fuente2.render(nombreCargado, True, (negro))
                    Menu.blit(InfoN,(XCargado-57,YCargado-40))
                    Menu.blit(fuente2.render(valorCargado+simbolo, True, (negro)),(XCargado-47,YCargado-20))

                    Posicion = -1
                    for recs in RectsList: # For the squares in the list
                        Posicion+=1
                        if recs.x == XCargado and recs.y == YCargado:
                            indicadorEstado[Posicion] = indEstadoCargado

                
                for cadaLinea2 in guardadoNodos:
                    #print(cadaLinea2)
                    #print(cadaLinea2.split("[")[1].split("]")[0])
                    lis = []
                    for j in cadaLinea2.split("[")[1].split("]")[0].split(","):
                        lis.append(int(j))
                    contNE = 0
                    for coordenada in lis:
                        print(contNE)
                        print(coordenada)
                        if contNE == 0:
                            punto1x = coordenada  
                            contNE+=1
                        elif contNE == 1:
                            punto1y = coordenada
                            contNE+=1
                        elif contNE ==2:
                            punto2x = coordenada
                            contNE+=1
                        elif contNE ==3:
                            punto2y = coordenada
                            colorAleatorio = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                            print(punto1x,punto1y,punto2x,punto2y)
                            pygame.draw.line(Menu, colorAleatorio, (punto1x,punto1y), (punto2x,punto2y),2)
                            contNE=0
                        
                    #for cadaCondectado in cadaLinea2:
                        #pygame.draw.line(Menu, colorAleatorio, (cadaCondectado[0][0],cadaCondectado[0][1]), (cadaCondectado[1][0], cadaCondectado[1][1]),2)

            except:
                print("Circuito inexistente")  
            
            importar = False

        #Muestra las tensiones de cada nodo y ordena los nombres de las resistecias en orden alfabetico 
        if MostrarTensiones:
            conectar = 0
            insertionSort(NombresComponentes)
            pygame.draw.rect(Menu,(255,255,255),infoEliminar)
            activoEliminar = fuente2.render("            Ascendente: "+str(sort(NombresComponentes))+"            " +"            Descendente: "+str(NombresComponentes), True, (negro))
            Menu.blit(activoEliminar,infoEliminar)
            try:
                PositionSimulacion = pygame.mouse.get_pos()
                Pos = -1
                for cadaNodo in NodosE:
                    #print(cadaNodo)
                    Pos+=1
                    for cadaPunto in cadaNodo:
                        if cadaPunto.collidepoint(event.pos):
                            #print(ListaTensiones[Pos])
                            pygame.draw.rect(Menu,(255,255,255),infoEliminar)
                            TensionActual = fuente2.render("      Voltaje: "+str(ListaTensiones[Pos][0])+" V     Corriente: "+str(ListaTensiones[Pos][1])+" mA", True, (negro))
                            Menu.blit(TensionActual,infoEliminar)

                            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and D1==0:
                                for j in ListaGrafo:
                                    if j[5]==cadaPunto or j[6]==cadaPunto:
                                        D1 = j[0]
                                        print(D1) 
                    #print(contDijk)
            except:
                print("Fuera de Posicion")  
        #print(contDijk)
                   
        #Colocar los botones en el tablero 
        Menu.blit(FPoder_Image,(981,15))
        if seleccionFPoder[0]:
            Menu.blit(FPoderS_Image,(981,15))
        Menu.blit(Resistencia_Image,(981,90))
        if seleccionResistencia[0]:
            Menu.blit(ResistenciaS_Image,(981,90))
        Menu.blit(Importar_Image,(943,428))
        Menu.blit(Exportar_Image,(949,470))
        Menu.blit(Simulacion_Image,(943,567))

        #Colocar los cuadros de textos 
        pygame.draw.rect(Menu,color,inputRect)
        textSurface = fuente.render(userText,True,(negro))
        Menu.blit(textSurface,inputRect)

        pygame.draw.rect(Menu,color,inputRectValor)
        textSurface2 = fuente.render(userText2,True,(negro))
        Menu.blit(textSurface2,inputRectValor)

        pygame.draw.rect(Menu,color,inputExpImp)
        textSurface3 = fuente.render(userText3,True,(negro))
        Menu.blit(textSurface3,inputExpImp)


        #Etiquetas de los cuadros de texto
        Nombre = fuente2.render("Nombre:", True, (255,255,255))
        Menu.blit(Nombre,(964,229))

        Valor = fuente2.render("Valor:", True, (255,255,255))
        Menu.blit(Valor,(964,283))

        Unidad = fuente2.render(unid, True, (219, 177, 48))
        Menu.blit(Unidad,(1050,300))

        #Imagenes de selección 
        seleccionado = fuente2.render(textSeleccion, True, (255,255,255))
        Menu.blit(seleccionado,(962,181))

        seleccionado2 = fuente2.render(textSeleccion2, True, (219, 177, 48))
        Menu.blit(seleccionado2,(975,201))

        #Actualizar la pantalla
        pygame.display.update()
        pygame.time.wait(50)

### MENU ### ===================================================================================================================
#Funcion que llama a la ventana de creditos del programa 
def credit():
    Credit = pygame.display.set_mode([700,550]) # Play window with its dimensions     

    Credits_Image = pygame.image.load("imagenesCD/Creditos.png").convert()

    while True:
        #Ciclo para cerrar la ventana
        for event in pygame.event.get():         
            if event.type == pygame.QUIT: 
                pygame.quit() # Cerrar

            #Evento para presionar el boton de volver
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                PositionMenu = pygame.mouse.get_pos()
                if PositionMenu[0]>38 and PositionMenu[0]<94 and PositionMenu[1]>450 and PositionMenu[1]<506: # Si se pulsa el boton Play
                    return principal()
        #Pone la imagen de los creditos         
        Credit.blit(Credits_Image,(0,0))
        pygame.time.wait(50) # Tiempo en milisegundos para una mejor funcionalidad
        pygame.display.update()

#Funcion que llama a la ventana del menu principal del programa     
def principal():

    Menu= pygame.display.set_mode([700,550]) # Play window with its dimensions     

    MainMenu_Image = pygame.image.load("imagenesCD/Circuit Designer.png").convert()
    
    while True:
        #Ciclo para cerrar el programa
        for event in pygame.event.get():         
            if event.type == pygame.QUIT: 
                pygame.quit() # Cerrar
                sys.exit()
            # Eventos de los botones  
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    PositionMenu = pygame.mouse.get_pos()
                
                    if PositionMenu[0]>277 and PositionMenu[0]<450 and PositionMenu[1]>325 and PositionMenu[1]<400 :
                        return menu()
                    elif PositionMenu[0]>279 and PositionMenu[0]<440 and PositionMenu[1]>439 and PositionMenu[1]<515 :
                        return credit()
                        
        #Pone la imagen del Menu 
        Menu.blit(MainMenu_Image,(0,0))
        pygame.time.wait(50) # Tiempo en milisegundos para una mejor funcionalida
        pygame.display.update() # Actualizar constantemente la pantalla        
principal()

