import pygame  
import sys    
import random 
import time    
import threading # hilos
import eztext
import networkx as nx

pygame.init()


def menu():

    def CargarCircuito(file):
            ruta=file+".txt"#ruta
            archivo=open(ruta)#abrir
            contenido=archivo.readlines()#lectura de las lineas
            archivo.close()#cerrar
            return contenido
    ### ESCRITURA EN ARCHIVO (FACTURAS) ###
    def GuardarCircuito(file,dato):
            ruta=file+".txt"
            archivo=open(ruta,"a")#a->append
            archivo.write(dato+"\n") # escribe el dato en el archivo
            archivo.close()

    
    negro = (0,0,0)
    blanco = (255,255,255)

    PuntosEnlace = []
    
    RectsList = []

    indicadorEstado = []

    x1=15 # Position x initial 
    y1=-55 # Position y initial  

    for i in range(8): # Up to 5 per row
        y1+=71# Increase in the value of y1 (next box)
        x1=15 
        for j in range(13): # For each column up to 9
            RectsList.append(pygame.Rect(x1,y1,70,70)) # Adding the box to the list
            indicadorEstado.append(0)
            x1+=71 # Increase value of x1 (next box)
    print(indicadorEstado)


    Menu = pygame.display.set_mode([1098,650]) # Play window with its dimensions     

    fuente = pygame.font.Font(None,25)
    
    # Nombre
    userText = ""
    # Valor
    userText2 = ""

    userText3 = ""

    fuente2 = pygame.font.Font(None,25)

    textSeleccion = "Componente:"
    textSeleccion2 = " ------ "

    unid = "---"

    Seleccion_Image = pygame.image.load("resistencia1.png").convert()
    Seleccion_Image = pygame.transform.scale(Seleccion_Image, (55, 100))

    MainMenu_Image = pygame.image.load("fondo1.png").convert()
    Resistencia_Image = pygame.image.load("resistencia1.png").convert()
    ResistenciaH_Image = pygame.image.load("resistencia2.png").convert()
    ResistenciaS_Image = pygame.image.load("resistenciaS3.png").convert()
    FPoder_Image = pygame.image.load("fuentepoder1.jpg").convert()
    FPoderH_Image = pygame.image.load("fuentepoder2.jpg").convert()
    FPoderS_Image = pygame.image.load("fuentepoderS3.jpg").convert()
    Slot = pygame.image.load("Empty.png").convert()
    Borrar_Image = pygame.image.load("Borrar.png").convert()
    Girar_Image = pygame.image.load("Girar.png").convert()
    Importar_Image = pygame.image.load("importar.png")
    Exportar_Image = pygame.image.load("Exportar.png")
    Exportar_Image = pygame.transform.scale(Exportar_Image, (140, 38))
    Simulacion_Image = pygame.image.load("Simulacion.png")
    
    Grafo = nx.Graph()

    ListaGrafo = []

    ListaConexiones = []

    Menu.fill((13, 31, 74))

    for recs in RectsList: # For the squares in the list
            Menu.blit(Slot,(recs[0],recs[1]))

    global seleccionFPoder
    seleccionFPoder = [False]

    global seleccionResistencia
    seleccionResistencia = [False]

    #Menu.blit(MainMenu_Image,(10,5))

    inputRect = pygame.Rect(962,249,112,22)

    inputRectValor = pygame.Rect(962,299,82,22)

    inputExpImp = pygame.Rect(956,519,125,22)

    seleccionRect =  pygame.Rect(957,170,120,161)

    seleccionRect2 = pygame.Rect(960,173,115,155)

    eliminarRect = pygame.Rect(981,500,70,70)

    infoEliminar = pygame.Rect(16,587,922,55)


    color = (255, 255, 255)
    colorPassive = pygame.Color("gray15")
    colo = colorPassive

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

    colorNodoE = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    NodoElectronico = []

    NodosE = []

    ListaTensiones = []

    MostrarTensiones = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if activo == True:
                    if event.key == pygame.K_BACKSPACE:
                        userText = userText[0:-1]
                    else:    
                        userText += event.unicode
                if activo2 == True:
                    if event.key == pygame.K_BACKSPACE:
                        userText2 = userText2[0:-1]
                    else:    
                        userText2 += event.unicode
                if activo3 == True:
                    if event.key == pygame.K_BACKSPACE:
                        userText3 = userText3[0:-1]
                    else:    
                        userText3 += event.unicode


                if event.key == pygame.K_s:
                    contNodoE+=1
                    colorNodoE = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    NodosE.append(NodoElectronico)
                    NodoElectronico = []
                    print (NodosE)             
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:

                for i in ListaGrafo:
                    print (i[0])

                print(ListaGrafo)

                #print(ListaGrafo)
                PositionMenu = pygame.mouse.get_pos()
                print(PositionMenu)

                if inputRect.collidepoint(event.pos):
                    activo = True
                    #inputRect.x = 1100

                if not inputRect.collidepoint(event.pos):
                    activo = False

                if inputRectValor.collidepoint(event.pos):
                    activo2 = True

                if not inputRectValor.collidepoint(event.pos):
                    activo2 = False

                if inputExpImp.collidepoint(event.pos):
                    activo3 = True
                    print(activo3,activo2,activo)

                if not inputExpImp.collidepoint(event.pos):
                    activo3 = False              

                if PositionMenu[0]>80 and PositionMenu[0]<930 and PositionMenu[1]<570:
                    
                    if seleccionFPoder[0]:
                        #Menu.blit(FPoder_Image,(PositionMenu[0]-30,PositionMenu[1]-35))
                        seleccionFPoder[0]=False
                        #recto = FPoder_Image.get_rect()
                        #recto.x = PositionMenu[0]-30
                        #recto.y = PositionMenu[1]-35
                        #pygame.draw.rect(Menu,color,recto)
                        Posicion = -1
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1
                            if recs.collidepoint(event.pos):

                                indicadorEstado[Posicion-1] = 5
                                indicadorEstado[Posicion] = 1

                                #print(indicadorEstado)
                                recs.x = recs[0]
                                recs.y = recs[1]
                                Menu.blit(FPoder_Image,recs)
                                InfoN = fuente2.render(userText, True, (negro))
                                InfoV = fuente2.render(userText2+" V", True, (negro))
                                Menu.blit(InfoN,(recs[0]-57,recs[1]-40))
                                Menu.blit(InfoV,(recs[0]-47,recs[1]-20))

                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))

                                a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                PuntosEnlace.append(a)
                                pygame.draw.rect(Menu, negro, a)
                                b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                PuntosEnlace.append(b)
                                pygame.draw.rect(Menu, negro, b)

                                #Grafo.add_node(userText)
                                #Grafo.nodes[userText]["Valor"] = userText2
                                #Grafo.nodes[userText]["Valoar"] = userText2
                                #print(Grafo.nodes(data=True))

                                ListaGrafo.append([userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b])


                        textSeleccion2 = " ------ "
                        unid="---"
                        userText2=""
                        userText=""

                    if eliminar:
                        eliminar = False

                        Posicion = -1
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1
                            if recs.collidepoint(event.pos):

                                indicadorEstado[Posicion-1] = 0
                                indicadorEstado[Posicion+1] = 0
                                indicadorEstado[Posicion-13] = 0
                                indicadorEstado[Posicion+13] = 0
                                indicadorEstado[Posicion-14] = 0
                                indicadorEstado[Posicion] = 0


                                #print(indicadorEstado)
                                recs.x = recs[0]
                                recs.y = recs[1]
                                Menu.blit(Slot,recs)
                                Menu.blit(Slot,RectsList[Posicion-1])
                                Menu.blit(Slot,RectsList[Posicion+1])
                                Menu.blit(Slot,RectsList[Posicion+13])
                                Menu.blit(Slot,RectsList[Posicion-13])
                                Menu.blit(Slot,RectsList[Posicion-14])

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

                                for nodo in ListaGrafo:
                                    if nodo[3] == recs.x and nodo[4] == recs.y:
                                        ListaGrafo.remove(nodo)        


                        #print(indicadorEstado)
                        textSeleccion2 = " ------ "
                        unid="---"

                    if voltear:
                        voltear = False

                        Posicion = -1
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1
                            if recs.collidepoint(event.pos):
                                if indicadorEstado[Posicion] == 2:
                                    indicadorEstado[Posicion] = 1
                                    #print(indicadorEstado)
                                    recs.x = recs[0]
                                    recs.y = recs[1]
                                    Menu.blit(FPoder_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-1])
                                    Menu.blit(Slot,RectsList[Posicion+1])

                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))
                                    # eliminar puntos de enlace antiguos
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x-40,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+106,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)
                                    # crear nuevos puntos de enlace
                                    a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    for recs in RectsList: # For the squares in the list
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 1 
                                                nodo[5] = a
                                                nodo[6] = b
                                
                                elif indicadorEstado[Posicion] == 1:
                                    indicadorEstado[Posicion] = 2
                                    #print(indicadorEstado)
                                    recs.x = recs[0]
                                    recs.y = recs[1]
                                    Menu.blit(FPoderH_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-13])
                                    Menu.blit(Slot,RectsList[Posicion+13])

                                    pygame.draw.rect(Menu,(negro),(recs.x-40,recs.y+34,40,2))
                                    pygame.draw.rect(Menu,(negro),(recs.x+66,recs.y+34,40,2))
                                    
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y-40,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y+106,7,5):
                                            PuntosEnlace.remove(i)

                                    a = pygame.Rect(recs.x-40,recs.y+31,5,7)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+106,recs.y+31,5,7)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    for recs in RectsList: # For the squares in the list
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 2 
                                                nodo[5] = a
                                                nodo[6] = b


                                elif indicadorEstado[Posicion] == 4:
                                    indicadorEstado[Posicion] = 3
                                    #print(indicadorEstado)
                                    recs.x = recs[0]
                                    recs.y = recs[1]
                                    Menu.blit(Resistencia_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-1])
                                    Menu.blit(Slot,RectsList[Posicion+1])

                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x-40,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+106,recs.y+31,7,5):
                                            PuntosEnlace.remove(i)

                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                    pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))

                                    a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    for recs in RectsList: # For the squares in the list
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 3 
                                                nodo[5] = a
                                                nodo[6] = b


                                elif indicadorEstado[Posicion] == 3:
                                    indicadorEstado[Posicion] = 4
                                    #print(indicadorEstado)
                                    recs.x = recs[0]
                                    recs.y = recs[1]
                                    Menu.blit(ResistenciaH_Image,RectsList[Posicion])
                                    Menu.blit(Slot,RectsList[Posicion-13])
                                    Menu.blit(Slot,RectsList[Posicion+13])

                                    pygame.draw.rect(Menu,(negro),(recs.x-40,recs.y+34,40,2))
                                    pygame.draw.rect(Menu,(negro),(recs.x+66,recs.y+34,40,2))
                                    
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y-40,7,5):
                                            PuntosEnlace.remove(i)
                                    for i in PuntosEnlace:
                                        if i == pygame.Rect(recs.x+31,recs.y+106,7,5):
                                            PuntosEnlace.remove(i)

                                    a = pygame.Rect(recs.x-40,recs.y+31,5,7)
                                    PuntosEnlace.append(a)
                                    pygame.draw.rect(Menu, negro, a)
                                    b = pygame.Rect(recs.x+106,recs.y+31,5,7)
                                    PuntosEnlace.append(b)
                                    pygame.draw.rect(Menu, negro, b)

                                    for recs in RectsList: # For the squares in the list
                                        for nodo in ListaGrafo:
                                            if nodo[3] == recs.x and nodo[4] == recs.y:
                                                nodo[2] = 4 
                                                nodo[5] = a
                                                nodo[6] = b




                        #print(indicadorEstado)
                        textSeleccion2 = " ------ "
                        unid="---"


                    if seleccionResistencia[0]:
                        #Menu.blit(Resistencia_Image,(PositionMenu[0]-20,PositionMenu[1]-30))
                        seleccionResistencia[0]=False
                        Posicion = -1
                        for recs in RectsList: # For the squares in the list
                            Posicion+=1
                            if recs.collidepoint(event.pos):

                                indicadorEstado[Posicion-1] = 5
                                indicadorEstado[Posicion] = 3

                                #print(indicadorEstado)
                                recs.x = recs[0]
                                recs.y = recs[1]
                                Menu.blit(Resistencia_Image,recs)
                                InfoN = fuente2.render(userText, True, (negro))
                                InfoV = fuente2.render(userText2+" Ω", True, (negro))
                                Menu.blit(InfoN,(recs[0]-57,recs[1]-40))
                                Menu.blit(InfoV,(recs[0]-47,recs[1]-20))
                                
                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y-40,2,40))
                                pygame.draw.rect(Menu,(negro),(recs.x+33,recs.y+69,2,40))


                                a = pygame.Rect(recs.x+31,recs.y-40,7,5)
                                PuntosEnlace.append(a)
                                pygame.draw.rect(Menu, negro, a)
                                b = pygame.Rect(recs.x+31,recs.y+106,7,5)
                                PuntosEnlace.append(b)
                                pygame.draw.rect(Menu, negro, b)

                                ListaGrafo.append([userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b])
                                print(ListaGrafo)

                        textSeleccion2 = " ------ "
                        unid="---"
                        userText2=""
                        userText=""
                    # conexion entre puntos
                    Punto = -1
                    for puntos in PuntosEnlace: # For the squares in the list
                        Punto+=1
                        if puntos.collidepoint(event.pos) and conectar == 0:
                            
                            for nodo in ListaGrafo:
                                if nodo[5][0] == puntos[0] and nodo[5][1] == puntos[1]:
                                    conexion1 = nodo[0]
                                    enlazado1 = nodo[5]
                                elif nodo[6][0] == puntos[0] and nodo[6][1] == puntos[1]:
                                    conexion1 = nodo[0]
                                    enlazado1 = nodo[6]

                            pygame.draw.rect(Menu, (219, 177, 48), puntos)
                            p1=(puntos[0],puntos[1])
                            conectar = 1

                            break

                        if puntos.collidepoint(event.pos) and conectar == 1:

                            for nodo in ListaGrafo:


                                if nodo[5][0] == puntos[0] and nodo[5][1] == puntos[1]:
                                    conexion2 = nodo[0] 
                                    enlazado2 = nodo[5]
                                    ListaConexiones.append([conexion1,conexion2])

                                    NodoElectronico.append(enlazado1)
                                    NodoElectronico.append(enlazado2)


                                elif nodo[6][0] == puntos[0] and nodo[6][1] == puntos[1]:
                                    conexion2 = nodo[0]
                                    enlazado2 = nodo[6]
                                    ListaConexiones.append([conexion1,enlazado1,conexion2,enlazado2])

                                    NodoElectronico.append(enlazado1)
                                    NodoElectronico.append(enlazado2)
                                    

                            pygame.draw.line(Menu, colorNodoE, (p1[0],p1[1]), (puntos[0], puntos[1]),2)
                            pygame.draw.rect(Menu, (219, 177, 48), puntos)
                            conectar = 0


                if PositionMenu[0]>948 and PositionMenu[0]<1028 and PositionMenu[1]>340 and PositionMenu[1]<410:
                    eliminar = True
                    print(NodoElectronico)

                if PositionMenu[0]>1021 and PositionMenu[0]<1091 and PositionMenu[1]>340 and PositionMenu[1]<410:
                    voltear = True

                if PositionMenu[0]>950 and PositionMenu[0]<1085 and PositionMenu[1]>568 and PositionMenu[1]<640:
                    simulacion = True


                if PositionMenu[0]>981 and PositionMenu[0]<1051 and PositionMenu[1]>15 and PositionMenu[1]<85:
                    seleccionFPoder[0] = True
                    seleccionResistencia[0] = False
                    textSeleccion2 = "Fuente"
                    unid = "V"

                if PositionMenu[0]>981 and PositionMenu[0]<1051 and PositionMenu[1]>90 and PositionMenu[1]<160:
                    seleccionResistencia[0] = True
                    seleccionFPoder[0] = False
                    textSeleccion2 = "Resistencia"
                    unid = "Ω"

                if PositionMenu[0]>955 and PositionMenu[0]<1080 and PositionMenu[1]>474 and PositionMenu[1]<506:
                    exportar = True

                if PositionMenu[0]>955 and PositionMenu[0]<1080 and PositionMenu[1]>433 and PositionMenu[1]<465:
                    importar = True   

                """
                conectar +=1
                if conectar == 1:
                    p1=[PositionMenu[0],PositionMenu[1]]

                if conectar == 2:
                    pygame.draw.line(Menu, (44,44,44), (p1[0],p1[1]), (PositionMenu[0], PositionMenu[1]),3)
                    conectar = 0
                            
                """

        pygame.draw.rect(Menu,(219, 177, 48),seleccionRect,5)

        pygame.draw.rect(Menu,(87, 89, 97),seleccionRect2)


        Menu.blit(Borrar_Image,(948,340))
        Menu.blit(Girar_Image,(1021,340))
        #print(eliminar)
        
        #for indicadorActual in indicadorEstado:
            #if indicadorActual == 0:
        #print(RectsList[28])
        #print(PuntosEnlace)    
        if simulacion:
            eliminar = False
            voltear = False
            activo = False
            activo2 = False
            seleccionFPoder[0] = False
            seleccionResistencia[0] = False
            conectar = 0
            PositionSimulacion = pygame.mouse.get_pos()
            
            #print (NodosE)
            for i in NodosE:
                ListaTensiones += [[random.randint(1,10),random.randint(1,1000)]]
            #print(ListaTensiones)
            MostrarTensiones = True
            simulacion = False

        if eliminar:
            pygame.draw.rect(Menu,(255,255,255),infoEliminar)
            activoEliminar = fuente2.render("Seleccione el componente electronico que desea eliminar", True, (negro))
            Menu.blit(activoEliminar,infoEliminar)
        if not eliminar:
            pygame.draw.rect(Menu,(negro),infoEliminar)

        if voltear:
            pygame.draw.rect(Menu,(255,255,255),infoEliminar)
            activoEliminar = fuente2.render("Seleccione el componente electronico que desea girar", True, (negro))
            Menu.blit(activoEliminar,infoEliminar)

        if exportar:  
            for cadaComponente in ListaGrafo:
                GuardarCircuito(userText3,str(cadaComponente))
            for i in NodosE:
                GuardarCircuito(userText3+"Nodos",str(i))

            userText3 = ""
            exportar = False

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

            try:
                guardado = CargarCircuito(userText3) #test code
                #guardado2 = CargarCircuito(userText3+"Nodos")
                # ListaGrafo.append([userText,userText2,indicadorEstado[Posicion],recs.x,recs.y,a,b])
                for cadaLinea in guardado:

                    nombreCargado = cadaLinea.split(",")[0].split("'")[1]
                    valorCargado = cadaLinea.split(",")[1].split("'")[1]
                    indEstadoCargado = int(cadaLinea.split(",")[2])
                    XCargado = int(cadaLinea.split(",")[3])
                    YCargado = int(cadaLinea.split(",")[4])
                    
                    print(valorCargado)

                    if indEstadoCargado == 1:
                        Cargando_Image = FPoder_Image
                    
                    if indEstadoCargado == 2:
                        Cargando_Image = FPoderH_Image
                    
                    if indEstadoCargado == 3:
                        Cargando_Image = Resistencia_Image

                    if indEstadoCargado == 4:
                        Cargando_Image = ResistenciaH_Image
                    
                    Menu.blit(Cargando_Image,(XCargado,YCargado))

                    InfoN = fuente2.render(nombreCargado, True, (negro))
                    Menu.blit(InfoN,(XCargado-57,YCargado-40))
                    Menu.blit(fuente2.render(valorCargado, True, (negro)),(XCargado-47,YCargado-20))

                    Posicion = -1
                    for recs in RectsList: # For the squares in the list
                        Posicion+=1
                        if recs.x == XCargado and recs.y == YCargado:
                            indicadorEstado[Posicion] = indEstadoCargado

 



            except:
                print("Circuito inexistente")  
            
            importar = False


        if MostrarTensiones:
            PositionSimulacion = pygame.mouse.get_pos()
            Pos = -1
            for cadaNodo in NodosE:
                Pos+=1
                for cadaPunto in cadaNodo:
                    if cadaPunto.collidepoint(event.pos):
                        print(ListaTensiones[Pos])
                        pygame.draw.rect(Menu,(255,255,255),infoEliminar)
                        TensionActual = fuente2.render("      Voltaje: "+str(ListaTensiones[Pos][0])+" V     Corriente: "+str(ListaTensiones[Pos][1])+" mA", True, (negro))
                        Menu.blit(TensionActual,infoEliminar)

        Menu.blit(FPoder_Image,(981,15))
        if seleccionFPoder[0]:
            Menu.blit(FPoderS_Image,(981,15))

        Menu.blit(Resistencia_Image,(981,90))
        if seleccionResistencia[0]:
            Menu.blit(ResistenciaS_Image,(981,90))
        #Menu.blit(ResistenciaH_Image,(973,220))

        Menu.blit(Importar_Image,(943,428))
        Menu.blit(Exportar_Image,(949,470))
        Menu.blit(Simulacion_Image,(943,567))

        pygame.draw.rect(Menu,color,inputRect)
        textSurface = fuente.render(userText,True,(negro))
        Menu.blit(textSurface,inputRect)

        pygame.draw.rect(Menu,color,inputRectValor)
        textSurface2 = fuente.render(userText2,True,(negro))
        Menu.blit(textSurface2,inputRectValor)

        pygame.draw.rect(Menu,color,inputExpImp)
        textSurface3 = fuente.render(userText3,True,(negro))
        Menu.blit(textSurface3,inputExpImp)

        Nombre = fuente2.render("Nombre:", True, (255,255,255))
        Menu.blit(Nombre,(964,229))

        Valor = fuente2.render("Valor:", True, (255,255,255))
        Menu.blit(Valor,(964,283))

        Unidad = fuente2.render(unid, True, (219, 177, 48))
        Menu.blit(Unidad,(1050,300))

        seleccionado = fuente2.render(textSeleccion, True, (255,255,255))
        Menu.blit(seleccionado,(962,181))

        seleccionado2 = fuente2.render(textSeleccion2, True, (219, 177, 48))
        Menu.blit(seleccionado2,(975,201))

        #Menu.blit(Seleccion_Image,(1006,205))

        pygame.display.update()
        pygame.time.wait(50)
menu()


