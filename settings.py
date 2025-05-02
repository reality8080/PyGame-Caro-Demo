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
Gray = (128, 128, 128)
Blue = (0, 0, 255)
Green = (0, 255, 0)

buttonColor = (205, 133, 63)
buttonColorHover = (244, 164, 96)
textColor = (139, 69, 19)
# Kich thuoc
Width = 800
Height = 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Settings")


loadImage = pygame.image.load(
    "./Temple/images/wallpapersden.com_stardew-valley-hd-gaming-background_2560x1700.jpg")
loadImage = pygame.transform.scale(loadImage, (Width, Height))
# Font chu
fontRegular = pygame.font.Font("./Temple/font/PressStart2P-Regular.ttf", 20)


def drawButton(button, text, isHover):
    color = buttonColorHover if isHover else buttonColor
    pygame.draw.rect(screen, color, button, border_radius=10)
    pygame.draw.rect(screen, (101, 67, 33), button, 4, border_radius=10)

    textSurface = fontRegular.render(text, True, textColor)
    textRect = textSurface.get_rect(center=button.center)
    screen.blit(textSurface, textRect)


def settings():
    global selectedAlgorithm
    running = True
    while running:
        screen.blit(loadImage, (0, 0))

        mouseX, mouseY = pygame.mouse.get_pos()

        drawButton(buttonAStar, "A*", buttonAStar.collidepoint(mouseX, mouseY))
        drawButton(buttonBFS, "BFS", buttonBFS.collidepoint(mouseX, mouseY))
        drawButton(buttonMiniMax, "MiniMax",
                   buttonMiniMax.collidepoint(mouseX, mouseY))
        drawButton(buttonDHClimbing, "DHClimbing",
                   buttonDHClimbing.collidepoint(mouseX, mouseY))
        drawButton(buttonBackTracking, "Backtracking",
                   buttonBackTracking.collidepoint(mouseX, mouseY))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttonAStar.collidepoint(mouseX, mouseY):
                    selectedAlgorithm = "A*"
                    return "Astar"
                elif buttonBFS.collidepoint(mouseX, mouseY):
                    selectedAlgorithm = "BestFirstSearch"
                    return "BestFirstSearch"
                elif buttonMiniMax.collidepoint(mouseX, mouseY):
                    selectedAlgorithm = "MiniMax"
                    return "MiniMax"
                elif buttonDHClimbing.collidepoint(mouseX, mouseY):
                    selectedAlgorithm = "DHClimbing"
                    return "DHClimbing"
                elif buttonBackTracking.collidepoint(mouseX, mouseY):
                    selectedAlgorithm = "Backtracking"
                    return "Backtracking"
        pygame.display.flip()
        pygame.time.Clock().tick(60)


buttonWidth = 250
buttonHeight = 50
space = 70
center_X = (Width - buttonWidth) // 2
Start_y = Height//2-(buttonHeight+space)

buttonAStar = pygame.Rect(center_X, Start_y, buttonWidth, buttonHeight)
buttonBFS = pygame.Rect(center_X, Start_y+space, buttonWidth, buttonHeight)
buttonMiniMax = pygame.Rect(
    center_X, Start_y+space*2, buttonWidth, buttonHeight)
buttonDHClimbing = pygame.Rect(
    center_X, Start_y+space*3, buttonWidth, buttonHeight)
buttonBackTracking = pygame.Rect(
    center_X, Start_y+space*4, buttonWidth, buttonHeight)

selectedAlgorithm = "MiniMax"
