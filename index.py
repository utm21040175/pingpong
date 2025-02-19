import pygame

gris = (125,125,125)
lila = (251,243,207)
rojo = (255,0,0)
negro = (0,0,0)
blanco = (255,255,255)


pygame.mixer.init()
pygame.mixer.music.load("sonido.mp3")#Es para poder poner la musica en el juego
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)#Para que el volumen este bajo

golpe_sonido = pygame.mixer.Sound("Golpe.mp3")

pygame.init()
ventana = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Ping pong")
font = pygame.font.Font(None, 36)
game_over = False
pausa = False



def show_text(text, x=50, y=200, color = gris):#Esto es para mostrar textos 
    texto = font.render(text, True,  color)
    ventana.blit(texto,(x,y))
    
def generate_bricks():
    rows = 1
    columns = 12
    bricks = []
    for j in range(rows):
        for i in range(columns):
            brick = pygame.Rect(310, 5 + i * 45, 20, 40) 
            bricks.append(brick)
    return bricks

def main():
    global game_over, pausa
    #Crear la pelota
    ball = pygame.image.load("ball.png")
    speed = [4, 4]
    ballrect = ball.get_rect()
    ballrect.move_ip(320, 150)

    ##Crear el bate
    bate = pygame.image.load("bat2.png")
    baterect = bate.get_rect()
    baterect.move_ip(10, 240)
     
    #crear el segundo bate
    bateD= pygame.image.load("bat2.png")
    bateDrect = bateD.get_rect()
    bateDrect.move_ip(610, 240)

    bricks = generate_bricks()
    izq = 0
    dere = 0 

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:#Esto es para que cuando le demos espacio al teclado se repita de nuevo el uego
                if event.key == pygame.K_SPACE and game_over:
                    ballrect.topleft = (320,150)
                    speed = [2,2]
                    baterect.topleft = (10,240)#Esto es para que vuelva a salir por la parte de arriba 
                    bateDrect.topleft = (610, 240)
                    game_over = False
                    bricks = generate_bricks()
                    izq = 0 #inicializamos en 0
                    dere = 0 #inicializamos en 0
                    pygame.mixer.music.unpause()
                    
                elif event.key == pygame.K_p:
                    pausa = not pausa

        if not game_over and not pausa:
            ballrect = ballrect.move(speed)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]and baterect.top > 5:
                baterect =  baterect.move(0, -5)
            if keys [pygame.K_DOWN]and baterect.bottom  < ventana.get_height():
                baterect = baterect.move(0, 5)  
            if keys[pygame.K_w]and bateDrect.top > 0: #le cambie la letra para que se mueva con la "a"
                bateDrect =  bateDrect.move(0, -5)
            if keys [pygame.K_s]and bateDrect.bottom  < ventana.get_height(): #le cambie la letra para que se mueva con la "d"
                bateDrect = bateDrect.move(0, 5)  
            if (ballrect.left < 0 ):
                dere += 1  #se suma cuando topa 
                speed[0] = -speed[0]
                ballrect.topleft = (320,150)
            if (ballrect.right > ventana.get_width()):
                izq += 1 #se suma cuando topa 
                speed[0] = -speed[0]
                ballrect.topleft = (320,150)
            if(ballrect.top < 0 or ballrect.bottom > ventana.get_height()):
                speed[1] = -speed[1]
            if (baterect.colliderect(ballrect)):##Esto es para que cuando la pelota colicione con el bat cambie de direccion 
                golpe_sonido.play()
                speed[1] = -speed[1] - 0.2
            if(bateDrect.colliderect(ballrect)):
                golpe_sonido.play()
                speed[0] = -speed[0] - 0.2
                
            if izq == 5:
                game_over = True
                show_text("Jugador Izquierdo Gana!", y=240, color = rojo)
            elif dere == 5:
                game_over = True
                show_text("Jugador Derecho Gana!", y=230, color = rojo)
            if not game_over:
                ventana.fill(lila)
                ventana.blit(ball,ballrect)
                ventana.blit(bate,baterect)
                ventana.blit(bateD, bateDrect)
            
            for brick in bricks:
                pygame.draw.rect(ventana, blanco, brick)
                
            show_text(f"Jugador Izquierdo: {izq}", x=30, y=25, color = rojo)
            show_text(f"Jugador Derecho: {dere}", x=400, y=25 , color = rojo)
        elif pausa:
                texto = font.render("El juego esta en pausa", True, rojo)
                ventana.blit(texto,(50,200))
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()