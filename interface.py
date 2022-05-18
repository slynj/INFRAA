import pygame
import math
import tkinter as tk
from tkinter import filedialog as fd
import shutil
import os


def fileCheck():
    """Copies the selected image file and saves it to the 'img' directory for the detector"""
    dstPath = "img/"
    path = fd.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpeg"),
                                                                              ("png files", "*.png"),
                                                                              ("jpg files", "*.jpg")))
    try:
        shutil.copy(path, dstPath)
    except Exception as e:
        print(f'Something went wrong: {e}')


def distFromPoints(point1, point2):
    """Calculates the distance between two points"""
    distance = math.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))
    return distance


def createText(t, f="Arial", s=200, c=(255, 255, 0), b=False, i=False):
    '''
    Receives a string and other characters of a text and returns a rendered text
    Parameters
    ----------
    t: str
        the string of the text to be rendered
    f: str = "Arial"
        the string indicating the font style of the text
    s: int = 200,
        size of the text
    c: tuple[int, int, int] = (255, 255, 0)
        colour of the text
    b: bool = False
        indication if the text would be bold
    i: bool = False
        indication if the text would be italicized
    Returns
    -------
    pygame.Surface
        rendered text
    '''

    font = pygame.font.SysFont(f, s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text


def createBttn(mainSurface, text, textX, textY, c=(0, 0, 0)):
    '''
    Receives a text of the button with XY coordinates and draws a rectangle button with that text
    Parameters
    ----------
    mainSurface: pygame.Surface
        the surface to draw the elements
    text: pygame.Surface
        the rendered text of the button
    textX: float
        the X coordinate of the button
    textY: float
        the Y coordinate of the button
    c: tuple[int, int, int] = (0, 0, 0)
        colour of the button
    Returns
    -------
    None
    '''
    paddingW = text.get_width() * 0.3
    paddingH = text.get_height() * 0.1
    dimension = [textX - paddingW / 2, textY - paddingH / 2, text.get_width() + paddingW, text.get_height() + paddingH]
    pygame.draw.rect(mainSurface, c, dimension, border_radius=10)
    mainSurface.blit(text, (textX, textY))



def horizontalC(item, mainSurface):
    '''
    Calculates what coordinate of the item's horizontal centre is
    Parameters
    ----------
    mainSurface: pygame.Surface
        the surface to draw the elements
    item: pygame.Surface
        element to be horizontally centered
    Returns
    -------
    int
        the x coordinate where the element would be centered
    '''
    return int((mainSurface.get_width() - item.get_width()) // 2)


# Resizes Images
def resizeImg(file, factor):
    resizedImg = pygame.image.load(f'resource/{file}').convert_alpha()
    resizedImg = pygame.transform.smoothscale\
        (resizedImg, (resizedImg.get_width() / factor, resizedImg.get_height() / factor))
    return resizedImg


def font(t, f="tommy.otf", s=40, c=(58, 101, 139)):
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


def clickObject(objects, mouseUp):
    if hoverObject(objects) and mouseUp:
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

    programState = "MAIN"

    # Create the the size, position and color for a circle
    circlePos = [200, 200]
    circleSize = 30
    circleColor = (255, 0, 0)

    # Create a variable to save the button state
    buttonOn = False  # Default to off
    pageNum = 0
    yVal = 100
    nextPage = 0

    # Images Init
    logoImg = resizeImg('logo.jpg', 4)
    logoHoverImg = resizeImg('logoHover.jpg', 4)
    logoInit = logoImg

    # Texts Init
    # Menu Header Texts
    menuLogText = font('Log')
    menuAttendanceText = font('Attendance')
    menuClassText = font('Class')

    # -----------------------------Main Game Loop---------------------------------------- #

    while True:
        # -----------------------------Event Handling------------------------------------ #
        # change order, make hover function
        mousePos = pygame.mouse.get_pos()

        if distFromPoints(circlePos, mousePos) < circleSize:
            hover = True
            circleColor = (100, 0, 0)
        else:
            hover = False
            circleColor = (255, 0, 0)

        ev = pygame.event.poll()

        if ev.type == pygame.QUIT:
            break
        if ev.type == pygame.MOUSEBUTTONUP:
            mouseUp = True
            if hover:
                circleColor = (255, 0, 0)
                buttonOn = True
        else:
            mouseUp = False

        if buttonOn:
            buttonOn = False
            fileCheck()

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
            menuLogText = font('Log', c=NAVY)
            if mouseUp:
                programState = 'LOG'
        else:
            menuLogText = font('Log', c=BLUE)

        if hoverObject(mousePos, menuAttendanceText, 550, 10):
            menuAttendanceText = font('Attendance', c=NAVY)
            if mouseUp:
                programState = 'ATTENDANCE'
        else:
            menuAttendanceText = font('Attendance', c=BLUE)

        if hoverObject(mousePos, menuClassText, 900, 10):
            menuClassText = font('Class', c=NAVY)
            if mouseUp:
                programState = 'CLASS'
        else:
            menuClassText = font('Class', c=BLUE)


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
