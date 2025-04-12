import pygame
import sys
from InformedSearch.AStar import AStar
from InformedSearch.BestFirstSearch import bestMoveBFS
from InformedSearch.miniMax import bestMoveMiniMax
from InformedSearch.DeepHillClimbing import DeepHillClimbing
pygame.init()

# Mau sac
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Gray= (128, 128, 128)
Blue = (0, 0, 255)
Green = (0, 255, 0)

buttonColor= (205, 133, 63)
buttonColorHover=(244,164,96)
textColor= (139,69,19)
# Kich thuoc
Width = 800
Height = 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Settings")


loadImage=pygame.image.load("./Temple/images/wallpapersden.com_stardew-valley-hd-gaming-background_2560x1700.jpg")
loadImage=pygame.transform.scale(loadImage,(Width,Height))
# Font chu
fontRegular = pygame.font.Font("./Temple/font/PressStart2P-Regular.ttf", 20)

def drawButton(button, text, isHover):
    color=buttonColorHover if isHover else buttonColor
    pygame.draw.rect(screen,color,button,border_radius=10)
    pygame.draw.rect(screen,(101,67,33),button,4,border_radius=10)

    textSurface=fontRegular.render(text,True,textColor)
    textRect=textSurface.get_rect(center=button.center)
    screen.blit(textSurface,textRect)

def settings(): 
    global selectedAlgorithm
    running = True
    while running:
        screen.blit(loadImage,(0,0))

        mouseX,mouseY=pygame.mouse.get_pos()

        drawButton(buttonAStar,"A*",buttonAStar.collidepoint(mouseX,mouseY))
        drawButton(buttonBFS,"BFS",buttonBFS.collidepoint(mouseX,mouseY))
        drawButton(buttonMiniMax,"MiniMax",buttonMiniMax.collidepoint(mouseX,mouseY))
        drawButton(buttonDHClimbing, "DHClimbing",buttonDHClimbing.collidepoint(mouseX,mouseY))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttonAStar.collidepoint(mouseX,mouseY):
                    selectedAlgorithm = "A*"
                    return "Astar"
                elif buttonBFS.collidepoint(mouseX,mouseY):
                    selectedAlgorithm = "BestFirstSearch"
                    return "BestFirstSearch"
                elif buttonMiniMax.collidepoint(mouseX,mouseY):
                    selectedAlgorithm = "MiniMax"
                    return "MiniMax"
                elif buttonDHClimbing.collidepoint(mouseX,mouseY):
                    selectedAlgorithm = "DHClimbing"
                    return "DHClimbing"
         
        pygame.display.flip()
        pygame.time.Clock().tick(60)


buttonWidth=Width//2-100
buttonHeight=Height//2
space=70

buttonAStar=pygame.Rect(buttonWidth,buttonHeight,250,50)
buttonBFS=pygame.Rect(buttonWidth,buttonHeight+space,250,50)
buttonMiniMax=pygame.Rect(buttonWidth,buttonHeight+space*2,250,50)
buttonDHClimbing=pygame.Rect(buttonWidth,buttonHeight+space*3,250,50)

selectedAlgorithm = "MiniMax"