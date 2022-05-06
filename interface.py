import pygame
import math
import tkinter as tk
from tkinter import filedialog as fd
import shutil


# Copies the selected image file and saves it to the 'img' directory for the detector
def fileCheck():
    dstPath = "img/"
    path = fd.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpeg"),
                                                                              ("png files", "*.png"),
                                                                              ("jpg files", "*.jpg")))
    print(path)
    shutil.copy(path, dstPath)


# Calculates the distance between two points
def distFromPoints(point1, point2):
    distance = math.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))
    return distance


def main():
    """ Set up the game and run the main game loop """
    root = tk.Tk()
    root.withdraw()

    pygame.init()  # Prepare the pygame module for use
    surfaceSize = 480  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    # Create the the size, position and color for a circle
    circlePos = [200, 200]
    circleSize = 30
    circleColor = (255, 0, 0)

    # Create a variable to save the button state
    buttonOn = False  # Default to off

    while True:
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
            if hover:
                circleColor = (255, 0, 0)
                buttonOn = True

        if buttonOn:
            buttonOn = False
            fileCheck()

        mainSurface.fill((255, 255, 255))

        pygame.draw.circle(mainSurface, circleColor, circlePos, circleSize)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()