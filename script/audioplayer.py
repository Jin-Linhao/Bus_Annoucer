import pygame
import pygame.mixer
from pygame.locals import *
import sys
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((640,600))

sounda = pygame.mixer.Sound("02.wav")
channela = sounda.play()
while channela.get_busy():
   pygame.time.delay(10000)

circle = pygame.draw.circle(window, (50,30,90),(90,30),16,5)
window.blit(window,circle)

window.blit(window,circle)

while True:
	for event in pygame.event.get():
		pygame.quit()
		sys.exit()
	pygame.display.update()
