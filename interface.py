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


def bttnDimension(mouse, text, textX, textY):
    '''
    Collision detection for the button, returns TRUE or FALSE
    Parameters
    ----------
    mouse: tuple
        XY coordinates of the mouse pointer
    text: pygame.Surface
        the rendered text of the button
    textX: float
        the X coordinate of the button
    textY: float
        the Y coordinate of the button
    Returns
    -------
    bool
        if the mouse is touching the button or not
    '''
    paddingW = text.get_width() * 0.3
    paddingH = text.get_height() * 0.1
    dimension = [textX - paddingW / 2, textY - paddingH / 2, text.get_width() + paddingW, text.get_height() + paddingH]
    bttn = pygame.Rect(dimension)
    if bttn.collidepoint(mouse[0], mouse[1]):
        return True
    else:
        return False


def displayImg(mainSurface, imgFile, x, y):
    '''
    Draws the image on the given coordinates
    Parameters
    ----------
    mainSurface: pygame.Surface
        the surface to draw the elements
    imgFile: pygame.Surface
        the loaded image to be drawn
    x: float
        x coordinate of the image to be drawn
    y: float
        y coordinate of the image to be drawn
    Returns
    -------
    None
    '''
    mainSurface.blit(imgFile, (x, y))


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


def main():
    """ Set up the game and run the main game loop """
    root = tk.Tk()
    root.withdraw()

    pygame.init()  # Prepare the pygame module for use
    surfaceSizeX = 1200  # Desired physical surface size, in pixels.
    surfaceSizeY = 800  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSizeX, surfaceSizeY))

    # Create the the size, position and color for a circle
    circlePos = [200, 200]
    circleSize = 30
    circleColor = (255, 0, 0)

    # Create a variable to save the button state
    buttonOn = False  # Default to off
    pageNum = 0
    yVal = 100
    nextPage = 0

    while True:
        global fileList
        mainSurface.fill((255, 255, 255))

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

        if os.path.exists('data/time.txt'):
            f = open("data/time.txt", "r")  # Open the file
            fileList = f.readlines()  # Read the file into a list
            f.close()  # Close the file

            for i in range(0, len(fileList)):
                fileList[i] = fileList[i].strip()
                nameTime = createText(fileList[i], s=80, c=(0, 0, 0))
                mainSurface.blit(nameTime, (100, 100 + 100 * i))

            # for i in range(0, len(fileList)):
            #     fileList[i] = fileList[i].strip()

            #print(fileList)
        else:
            pass

        if mouseUp:
            nextPage += 1



        pygame.draw.circle(mainSurface, circleColor, circlePos, circleSize)

        # removes \n from the text, rends the text, blit the text: 100 each

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()