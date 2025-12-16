'''
import pygame
import sys 
pygame.init()

#defining size of game window
windowsSize = pygame.display.set_mode((680,680)) 
pygame.display.set_caption("Printer")

#defining font attributes
myFont = pygame.font.SysFont("times new roman", 70)
helloWorld = myFont.render("Hello World", 1, (188, 143, 143), (0, 0, 0))

while 1:
    for event in pygame.event.get():
     if event.type==pygame.QUIT: sys.exit()
    windowsSize.blit(helloWorld, (0, 0))
    pygame.display.update()
'''