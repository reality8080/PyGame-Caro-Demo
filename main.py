import pygame
import sys
from PlayGame import index,settings
from game_logger import GameLogger
pygame.init()
game_logger = GameLogger()
def drawButton(button, text, isHover):
    color = buttonColorHover if isHover else buttonColor
    pygame.draw.rect(screen, color, button, border_radius=10)
    pygame.draw.rect(screen, (101, 67, 33), button, 4, border_radius=10)

    textSurface = fontRegular.render(text, True, textColor)
    textRect = textSurface.get_rect(center=button.center)
    screen.blit(textSurface, textRect)

def drawLabel(labelTitle, text):
    pygame.draw.rect(screen, (222, 184, 135), labelTitle, border_radius=10)
    pygame.draw.rect(screen, (101, 67, 33), labelTitle, 4, border_radius=10)

    textSurfaceTitle = fontLabel.render(text, True, textColor)
    textTitle = textSurfaceTitle.get_rect(center=labelTitle.center)
    screen.blit(textSurfaceTitle, textTitle)

Width, Height = 800, 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Menu")

loadImage = pygame.image.load("./Temple/images/wallpapersden.com_stardew-valley-hd-gaming-background_2560x1700.jpg")
loadImage = pygame.transform.scale(loadImage, (Width, Height))

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)

buttonColor = (205, 133, 63)
buttonColorHover = (244, 164, 96)
textColor = (139, 69, 19)

fontRegular = pygame.font.Font("./Temple/font/PressStart2P-Regular.ttf", 20)
fontLabel = pygame.font.Font("./Temple/font/PressStart2P-Regular.ttf", 78)

buttonWidth = Width // 2 - 100
buttonHeight = Height // 2
space = 70

buttonStart = pygame.Rect(buttonWidth, buttonHeight, 200, 50)
buttonSetting = pygame.Rect(buttonWidth, buttonHeight + space, 200, 50)
buttonQuit = pygame.Rect(buttonWidth, buttonHeight + space * 2, 200, 50)

labelTitle = pygame.Rect(Width // 2 - 205, 50, 400, 200)

running = True

while running:
    screen.blit(loadImage, (0, 0))
    mouseX, mouseY = pygame.mouse.get_pos()

    drawButton(buttonStart, "Start", buttonStart.collidepoint(mouseX, mouseY))
    drawButton(buttonSetting, "Setting", buttonSetting.collidepoint(mouseX, mouseY))
    drawButton(buttonQuit, "Quit", buttonQuit.collidepoint(mouseX, mouseY))

    drawLabel(labelTitle, "Menu")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttonStart.collidepoint(mouseX, mouseY):
                print("Start")
                index.start("MiniMax")
            elif buttonSetting.collidepoint(mouseX, mouseY):
                print("Setting")
                algo = settings.settings()
                if algo:
                    index.start(algo)
            elif buttonQuit.collidepoint(mouseX, mouseY):
                print("Quit")
                running = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
