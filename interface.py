import pygame
import math
import tkinter as tk
from tkinter import filedialog as fd
import shutil
import os


# Copies the selected image file and saves it to the 'img' directory for the detector
def fileCheck():
    dstPath = "img/"
    path = fd.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpeg"),
                                                                              ("png files", "*.png"),
                                                                              ("jpg files", "*.jpg")))
    try:
        shutil.copy(path, dstPath)
    except Exception as e:
        print(f'Something went wrong: {e}')


def createBttn(mainSurface, text, textX, textY, c=(0, 0, 0)):
    paddingW = text.get_width() * 0.3
    paddingH = text.get_height() * 0.1
    dimension = [textX - paddingW / 2, textY - paddingH / 2, text.get_width() + paddingW, text.get_height() + paddingH]
    pygame.draw.rect(mainSurface, c, dimension, border_radius=10)
    mainSurface.blit(text, (textX, textY))


# Calculates what coordinate of the item's horizontal centre is
def horizontalC(item, mainSurface):
    return int((mainSurface.get_width() - item.get_width()) // 2)


# Resizes Images
def resizeImg(file, factor):
    resizedImg = pygame.image.load(f'resource/{file}').convert_alpha()
    resizedImg = pygame.transform.smoothscale\
        (resizedImg, (resizedImg.get_width() / factor, resizedImg.get_height() / factor))
    return resizedImg


# Creates a Rendered Text with Given String
def createText(t, f="tommy.otf", s=40, c=(58, 101, 139)):
    text = pygame.font.Font(f'resource/{f}', s)
    renderedText = text.render(t, True, c)
    return renderedText


# Collision Detection for Rectangles (shapes, images, texts)
def hoverObject(mouse, objects, objectX, objectY):
    paddingW = objects.get_width() * 0.3
    paddingH = objects.get_height() * 0.1
    dimension = [objectX - paddingW / 2, objectY - paddingH / 2,
                 objects.get_width() + paddingW, objects.get_height() + paddingH]
    area = pygame.Rect(dimension)
    if area.collidepoint(mouse[0], mouse[1]):
        return True
    else:
        return False


def main():
    # -----------------------------Setup------------------------------------------------- #
    global fileList, programState, YELLOW, NAVY

    # https://stackoverflow.com/questions/1406145 (how to get rid of tk window)
    root = tk.Tk()
    root.withdraw()
    if root.wm_state() == 'withdrawn':
        root.iconify()

    pygame.init()

    pygame.display.set_caption("INFRAA")

    # -----------------------------Program Variable Initialization----------------------- #
    surfaceSizeX = 1200
    surfaceSizeY = 800

    clock = pygame.time.Clock()

    mainSurface = pygame.display.set_mode((surfaceSizeX, surfaceSizeY))

    # Colour Constants
    YELLOW = (253, 186, 33)  # FDBA21
    BLUE = (58, 101, 139)
    NAVY = (20, 61, 89)  # 143D59
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (230, 232, 237)
    DARKGRAY = (213, 215, 219)

    # Program State (MAIN, LOG, ATTENDANCE, CLASS)
    programState = "MAIN"

    # Create a variable to save the button state
    pageNum = 0
    yVal = 100
    nextPage = 0

    # IMAGES INIT #
    # Logo Images
    logoImg = resizeImg('logo.jpg', 4)
    logoHoverImg = resizeImg('logoHover.jpg', 4)
    logoInit = logoImg

    # TEXTS INIT #
    # Menu Header Texts
    menuLogText = createText('Log')
    menuAttendanceText = createText('Attendance')
    menuClassText = createText('Class')

    # BUTTONS INIT #
    # Add Student Button
    addBttn = createText('Add', s=30, c=WHITE)
    addBttnC = GRAY

    # -----------------------------Main Game Loop---------------------------------------- #

    while True:
        # -----------------------------Event Handling------------------------------------ #
        ev = pygame.event.poll()

        if ev.type == pygame.QUIT:
            break
        if ev.type == pygame.MOUSEBUTTONUP:
            mouseUp = True
        else:
            mouseUp = False

        mousePos = pygame.mouse.get_pos()

        # ----------------------------- Game Logic / Drawing -------------------------------- #

        # —ESSENTIAL GRAPHICS— #
        # Background
        mainSurface.fill((242, 244, 249))
        # Header
        pygame.draw.rect(mainSurface, (233, 235, 240), (0, 0, surfaceSizeX, 70))
        # Logo
        mainSurface.blit(logoInit, (5, 5))
        # Menu Text
        mainSurface.blit(menuLogText, (350, 10))
        mainSurface.blit(menuAttendanceText, (550, 10))
        mainSurface.blit(menuClassText, (900, 10))

        # Logo Hover
        if hoverObject(mousePos, logoInit, 5, 5):
            logoInit = logoHoverImg
            if mouseUp:
                programState = 'MAIN'
        else:
            logoInit = logoImg

        # Menu Text Hover
        if hoverObject(mousePos, menuLogText, 350, 10):
            menuLogText = createText('Log', c=NAVY)
            if mouseUp:
                programState = 'LOG'
        else:
            menuLogText = createText('Log', c=BLUE)

        if hoverObject(mousePos, menuAttendanceText, 550, 10):
            menuAttendanceText = createText('Attendance', c=NAVY)
            if mouseUp:
                programState = 'ATTENDANCE'
        else:
            menuAttendanceText = createText('Attendance', c=BLUE)

        if hoverObject(mousePos, menuClassText, 900, 10):
            menuClassText = createText('Class', c=NAVY)
            if mouseUp:
                programState = 'CLASS'
        else:
            menuClassText = createText('Class', c=BLUE)

        # ——————— MAIN MENU ——————— #
        if programState == 'MAIN':
            pass

        # ——————— LOG MENU ——————— #
        if programState == 'LOG':
            menuLogText = createText('Log', c=NAVY)

        # ——————— ATTENDANCE MENU ——————— #
        if programState == 'ATTENDANCE':
            menuAttendanceText = createText('Attendance', c=NAVY)

        # ——————— CLASS MENU ——————— #
        if programState == 'CLASS':
            menuClassText = createText('Class', c=NAVY)
            createBttn(mainSurface, addBttn, 100, 100, addBttnC)
            addBttnHover = hoverObject(mousePos, addBttn, 100, 100)
            if addBttnHover:
                addBttnC = DARKGRAY
                if mouseUp:
                    fileCheck()
            else:
                addBttnC = GRAY


        '''
        pygame.draw.circle(mainSurface, YELLOW, (100, 100), 50)
        pygame.draw.circle(mainSurface, NAVY, (200, 100), 50)
        pygame.draw.circle(mainSurface, (227, 227, 227), (300, 100), 50)
        pygame.draw.circle(mainSurface, (255, 255, 255), (400, 100), 50)
        '''

        '''
        if os.path.exists('data/time.txt'):
            f = open("data/time.txt", "r")  # Open the file
            fileList = f.readlines()  # Read the file into a list
            f.close()  # Close the file

            # removes \n from the text, rends the text, blit the text: 100 each
            for i in range(0, len(fileList)):
                fileList[i] = fileList[i].strip()
                nameTime = createText(fileList[i], s=80, c=(0, 0, 0))
                mainSurface.blit(nameTime, (100, 100 + 100 * i))
        else:
            pass

        if mouseUp:
            nextPage += 1

        pygame.draw.circle(mainSurface, circleColor, circlePos, circleSize)
        '''

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()
