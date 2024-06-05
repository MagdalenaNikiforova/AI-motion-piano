import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
pygame.display.set_caption('AI_Motion piano')

bckg = pygame.image.load("photos\Backgrnd.jfif")
screen.blit(pygame.transform.scale(bckg, (1000, 800)), (0, 0))

font = pygame.font.SysFont('Corbel', 35) #font of the text in teh button
text = font.render('START', True, (0, 0, 0))

lightpurp = (203, 195, 227)
darkpurp = (153, 50, 204)

bw = 200 #button width
bh = 50 #button height

pygame.display.flip()


while True:
    pygame.event.pump()
    event = pygame.event.wait()

    if event.type == QUIT:
        pygame.display.quit()
    elif event.type == VIDEORESIZE:
        screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
        screen.blit(pygame.transform.scale(bckg, event.dict['size']), (0, 0))
        pygame.display.flip()

    w = screen.get_width() #width of the screen
    h = screen.get_height() #height of the screen

    if event.type == pygame.MOUSEBUTTONDOWN: #mouse is clicked ont he button
        if (w/2 - bw/2) <= mouse[0] <= (w/2 + bw/2) and (h/2 - bh/2) <= mouse[1] <= (h/2 + bh/2):
            pygame.display.quit()
            pygame.quit()
            exec(open("openCamWindow.py").read())


    mouse = pygame.mouse.get_pos() #coordinates of the mouse

    if (w/2 - bw/2) <= mouse[0] <= (w/2 + bw/2) and (h/2 - bh/2) <= mouse[1] <= (h/2 + bh/2):
        pygame.draw.rect(screen, lightpurp, [w/2 - bw/2, h/2 - bh/2, bw, bh])
    else:
        pygame.draw.rect(screen, darkpurp, [w/2 - bw/2, h/2 - bh/2, bw, bh])

    screen.blit(text, (w/2 - bw/2 + 50, h/2 - bh/2 + 10))#adding text on the button

    pygame.display.update()





