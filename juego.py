import pygame, pathlib,random,math,io
from pygame import mixer


# Inicilizar Pygame
pygame.init()

#Tamaño de la pantalla
pantalla =pygame.display.set_mode((800,600))

#titulo e icono
pygame.display.set_caption("Starwars Game")
icono = pygame.image.load("C:/Users/darin/Documents/juegopy/archivos/ovni.png")
pygame.display.set_icon(icono)

#poner fondo al juego
fondo=pygame.image.load("C:/Users/darin/Documents/juegopy/archivos/fondo.jpg")

#musica de fondo
mixer.music.load("C:/Users/darin/Documents/juegopy/archivos/musica.mp3")
mixer.music.set_volume(0.3)
# para que se ejecute la musica solo cuando este en el loop
mixer.music.play(-1)

#variables de los enemigos
img_enemigo = []
enemigo_X = []
enemigo_Y = []
enemigo_X_cambio = []
enemigo_Y_cambio = []
cantidad_enemigos = 8

for i in range(cantidad_enemigos):
    #abrir la imagen donde esta el enemigo
    imagen_ene=pygame.image.load("C:/Users/darin/Documents/juegopy/archivos/enemigo_2_45px.png")
    img_enemigo.append(imagen_ene)

    #posiciones aleatorias de los enemigos
    posicionX = random.randint(0,735)
    posicionY= random.randint(50,150)
    enemigo_X.append(posicionX)
    enemigo_Y.append(posicionY)

    #cambios
    enemigo_X_cambio.append(0.5)
    enemigo_Y_cambio.append(50)

#FUNCION DEL ENEMIGO
def enemigo(x,y,cantidad_enemigos):
    #dibujar el enemigo en la pantalla
    pantalla.blit(img_enemigo[cantidad_enemigos],(x,y))

#variable bala
img_bala = pygame.image.load("C:/Users/darin/Documents/juegopy/archivos/bala_16px.png")
bala_X = 0
bala_Y = 500
bala_X_cambio = 0
bala_Y_cambio = 2
bala_visible = False


#puntaje
puntaje = 0
fuente = pygame.font.Font("C:/Users/darin/Documents/juegopy/archivos/Arcade.ttf",32)
fuente_game_over = pygame.font.Font("C:/Users/darin/Documents/juegopy/archivos/Arcade.ttf",70)

#Muestra el mensaje cuando pierdes
def texto_final():
    fuente_final = fuente_game_over.render("GAME OVER: LOS ALIENS GANAN", True,(255,0,0))
    pantalla.blit(fuente_final,(20,200))

#Muestra el puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render("Puntaje:{}".format(puntaje),True,(255,255,255))
    pantalla.blit(texto,(x,y))

#Funcion disparar bala

def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x+16,y+10))

#funcion colision
def hay_colision(x1,x2,y1,y2):
    distancia = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    if distancia < 27:
        return True
    else:
        return False

#Variables del jugador
img_jugador = pygame.image.load("C:/Users/darin/Documents/juegopy/archivos/astronave.png")
jugador_X = 368
jugador_Y = 536
jugador_X_cambio = 0

#funcion del jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))

#INICIO DEL BUCLE DEL JUEGO
ejecutar = True

while ejecutar:
    #colocamos el fondo
    pantalla.blit(fondo,(0,0))
    #iterar por cada evento que suceda en el juego
    for i in pygame.event.get():
        #cierre de pantalla
        if i.type == pygame.QUIT:
            ejecutar = False

        #Cuando se presiona una tecla
        if i.type == pygame.KEYDOWN:
            #tecla izquierda
            if i.key == pygame.K_LEFT:
                jugador_X_cambio -= 0.6
            #tecla derecha
            elif i.key == pygame.K_RIGHT:
                jugador_X_cambio += 0.6
            #tecla espacio
            elif i.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound("C:/Users/darin/Documents/juegopy/archivos/disparo.mp3")
                sonido_disparo.play()
                if not bala_visible:
                    bala_X = jugador_X
                disparar_bala(bala_X,bala_Y)
        
        #cuando se suelta la tecla
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT:
                jugador_X_cambio = 0

    #Modificar la ubicacion del enemigo
    for i in range(cantidad_enemigos):

        #fin del juego
        if enemigo_Y[i]>500:
            for k in range(cantidad_enemigos):
                enemigo_Y[k] = 1000
            texto_final()
            break
        enemigo_X[i] += enemigo_X_cambio[i]
        
        #bordes de los enemigos
        if enemigo_X[i] >= 768:
            enemigo_X_cambio[i] = -0.5
            enemigo_Y[i] += enemigo_Y_cambio[i]
        elif enemigo_X[i] <= 0:
            enemigo_X_cambio[i] = 0.5
            enemigo_Y[i] += enemigo_Y_cambio[i]

        #colision
        colision = hay_colision(enemigo_X[i],bala_X,enemigo_Y[i],bala_Y)
        if colision:
            sonido_colision = mixer.Sound("C:/Users/darin/Documents/juegopy/archivos/Golpe.mp3")
            sonido_colision.play()
            bala_Y = 500
            bala_visible = False
            puntaje += 1
            #una vez muerto el enemigo le debemos cambiar la posicion
            enemigo_X[i] = random.randint(0,735)
            enemigo_Y[i] = random.randint(50,150)
        enemigo(enemigo_X[i],enemigo_Y[i],i)

    #modificamos la posicion del jugador
    jugador_X += jugador_X_cambio

    #bordes del jugador
    if jugador_X <= 0:
        jugador_X = 0
    elif jugador_X >= 736:
        jugador_X = 736

    #modificar la posicion de la bala
    if bala_Y <= -16:
        bala_Y = 500
        bala_visible = False
    
    if bala_visible == True:
        disparar_bala(bala_X,bala_Y)
        bala_Y -= bala_Y_cambio
    
    #Mostramos puntaje
    mostrar_puntaje(10,10)
    jugador(jugador_X,jugador_Y) # dibujamos el jugador
    pygame.display.update() #actualizamos el color de fondo

