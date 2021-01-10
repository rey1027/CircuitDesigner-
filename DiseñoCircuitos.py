import pygame  
import sys    
import random  
import time    
import threading # hilos
import eztext
pygame.init()


def menu():
    Menu = pygame.display.set_mode([1098,646]) # Play window with its dimensions     

    fuente = pygame.font.Font(None,25)
    userText = ""
    userText2 = ""

    fuente2 = pygame.font.Font(None,25)

    textSeleccion = "Componente:"
    textSeleccion2 = " ------ "

    unid = "---"

    Seleccion_Image = pygame.image.load("resistencia.png").convert()
    Seleccion_Image = pygame.transform.scale(Seleccion_Image, (55, 100))

    MainMenu_Image = pygame.image.load("fondo1.png").convert()
    Resistencia_Image = pygame.image.load("resistencia.png").convert()
    ResistenciaH_Image = pygame.image.load("resistenciah.png").convert()
    ResistenciaS_Image = pygame.image.load("resistenciaS.png").convert()
    FPoder_Image = pygame.image.load("fuentepoder.jpg").convert()
    FPoderS_Image = pygame.image.load("fuentepoderS2.jpg").convert()
    
    Menu.fill((13, 31, 74))

    global conectar
    conectar = 0

    global seleccionFPoder
    seleccionFPoder = [False]

    global seleccionResistencia
    seleccionResistencia = [False]

    Menu.blit(MainMenu_Image,(10,5))

    inputRect = pygame.Rect(977,249,112,22)

    inputRectValor = pygame.Rect(977,299,82,22)

    seleccionRect =  pygame.Rect(972,170,120,220)

    seleccionRect2 = pygame.Rect(975,173,115,214)

    color = (255, 255, 255)
    colorPassive = pygame.Color("gray15")
    colo = colorPassive

    activo = False
    activo2 = False

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
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                PositionMenu = pygame.mouse.get_pos()
                print(PositionMenu)

                if inputRect.collidepoint(event.pos):
                    #activo = True
                    inputRect.x = 1100

                if not inputRect.collidepoint(event.pos):
                    activo = False

                if inputRectValor.collidepoint(event.pos):
                    activo2 = True

                if not inputRectValor.collidepoint(event.pos):
                    activo2 = False              

                if seleccionFPoder[0] and PositionMenu[0]<900 and PositionMenu[1]<570:
                    Menu.blit(FPoder_Image,(PositionMenu[0]-30,PositionMenu[1]-35))
                    seleccionFPoder[0]=False
                    InfoN = fuente2.render(userText, True, (0,0,0))
                    InfoV = fuente2.render(userText2, True, (0,0,0))
                    Menu.blit(InfoN,(PositionMenu[0],PositionMenu[1]))
                    Menu.blit(InfoV,(PositionMenu[0],PositionMenu[1]+20))
                    textSeleccion2 = " ------ "
                    unid="---"

                if seleccionResistencia[0] and PositionMenu[0]<900 and PositionMenu[1]<570:
                    Menu.blit(Resistencia_Image,(PositionMenu[0]-20,PositionMenu[1]-30))
                    seleccionResistencia[0]=False
                    InfoN = fuente2.render(userText, True, (0,0,0))
                    InfoV = fuente2.render(userText2, True, (0,0,0))
                    Menu.blit(InfoN,(PositionMenu[0],PositionMenu[1]))
                    Menu.blit(InfoV,(PositionMenu[0],PositionMenu[1]+20))
                    textSeleccion2 = " ------ "
                    unid="---"    


                if PositionMenu[0]>1000 and PositionMenu[0]<1060 and PositionMenu[1]>5 and PositionMenu[1]<75:
                    seleccionFPoder[0] = True
                    seleccionResistencia[0] = False
                    textSeleccion2 = "Fuente"
                    unid = "V"

                if PositionMenu[0]>1013 and PositionMenu[0]<1043 and PositionMenu[1]>90 and PositionMenu[1]<160:
                    seleccionResistencia[0] = True
                    seleccionFPoder[0] = False
                    textSeleccion2 = "Resistencia"
                    unid = "Ω"    

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

        Menu.blit(FPoder_Image,(1000,5))
        if seleccionFPoder[0]:
            Menu.blit(FPoderS_Image,(1000,5))

        Menu.blit(Resistencia_Image,(1014,90))
        if seleccionResistencia[0]:
            Menu.blit(ResistenciaS_Image,(1014,90))
        #Menu.blit(ResistenciaH_Image,(973,220))


        pygame.draw.rect(Menu,color,inputRect)
        textSurface = fuente.render(userText,True,(0,0,0))
        Menu.blit(textSurface,inputRect)

        pygame.draw.rect(Menu,color,inputRectValor)
        textSurface2 = fuente.render(userText2,True,(0,0,0))
        Menu.blit(textSurface2,inputRectValor)

        Nombre = fuente2.render("Nombre:", True, (255,255,255))
        Menu.blit(Nombre,(979,229))

        Valor = fuente2.render("Valor:", True, (255,255,255))
        Menu.blit(Valor,(979,283))

        Unidad = fuente2.render(unid, True, (219, 177, 48))
        Menu.blit(Unidad,(1065,300))

        seleccionado = fuente2.render(textSeleccion, True, (255,255,255))
        Menu.blit(seleccionado,(977,181))

        seleccionado2 = fuente2.render(textSeleccion2, True, (219, 177, 48))
        Menu.blit(seleccionado2,(990,201))

        #Menu.blit(Seleccion_Image,(1006,205))

        pygame.display.update()
        pygame.time.wait(50)
menu()


