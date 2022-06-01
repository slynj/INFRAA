import pygame
import math
import tkinter as tk
from tkinter import filedialog as fd
import shutil
import os
import time as t


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
    # paddingW = text.get_width() * 0.3
    # paddingH = text.get_height() * 0.1
    paddingW = 15
    paddingH = 5
    dimension = [textX, textY, text.get_width() + paddingW, text.get_height() + paddingH]
    pygame.draw.rect(mainSurface, c, dimension, border_radius=10)
    mainSurface.blit(text, (textX + paddingW/2, textY + paddingH/2))


# Calculates what coordinate of the item's horizontal centre is
def horizontalC(item, mainSurface):
    return int((mainSurface.get_width() - item.get_width()) // 2)


# Resizes Images
def resizeImg(file, factor):
    resizedImg = pygame.image.load(file).convert_alpha()
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
    # paddingW = objects.get_width() * 0.3
    # paddingH = objects.get_height() * 0.1
    paddingW = 15
    paddingH = 5
    dimension = [objectX, objectY, objects.get_width() + paddingW, objects.get_height() + paddingH]
    area = pygame.Rect(dimension)
    if area.collidepoint(mouse[0], mouse[1]):
        return True
    else:
        return False


def main():
    # -----------------------------Setup------------------------------------------------- #
    #global fileList, programState, YELLOW, NAVY

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
    GREEN = (88, 168, 112)
    RED = (194, 62, 62)

    # Program State (MAIN, LOG, ATTENDANCE, CLASS)
    programState = "MAIN"

    # IMAGES INIT #
    # Logo Images
    logoImg = resizeImg('resource/logo.jpg', 4)
    logoHoverImg = resizeImg('resource/logoHover.jpg', 4)
    logoInit = logoImg
    # Main Page Images
    mainImg1 = resizeImg('resource/mainPage1.png', 1)
    mainImg2 = resizeImg('resource/mainPage2.png', 1)
    mainImg3 = resizeImg('resource/mainPage3.png', 1)
    mainImg = mainImg1
    mainImgTime1 = t.time()

    # TEXTS INIT #
    # Menu Header Texts
    menuLogText = createText('Log')
    menuAttendanceText = createText('Attendance')
    menuClassText = createText('Class')

    # BUTTONS INIT #
    # Add Student Button
    addBttn = createText('Add', s=30, c=WHITE)
    addBttnC = GRAY
    # Next Page Button
    rightBttn = createText(' > ', s=30, c=WHITE)
    leftBttn = createText(' < ', s=30, c=WHITE)
    rightBttnC = DARKGRAY
    leftBttnC = DARKGRAY

    leftArrow = False
    rightArrow = False

    logPageNum = 0
    attPageNum = 0
    classPageNum = 0

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

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                leftArrow = True
            if ev.key == pygame.K_RIGHT:
                rightArrow = True

        mousePos = pygame.mouse.get_pos()

        # ----------------------------- Game Logic / Drawing -------------------------------- #

        # ——————— MENU BAR GRAPHICS ——————— #
        # Background
        mainSurface.fill((242, 244, 249))
        # Header
        pygame.draw.rect(mainSurface, (233, 235, 240), (0, 0, surfaceSizeX, 70))
        # Logo
        mainSurface.blit(logoInit, (0, 0))
        # Menu Text
        mainSurface.blit(menuLogText, (350, 10))
        mainSurface.blit(menuAttendanceText, (550, 10))
        mainSurface.blit(menuClassText, (900, 10))

        # Logo Hover
        if hoverObject(mousePos, logoInit, 0, 0):
            logoInit = logoHoverImg
            if mouseUp:
                programState = 'MAIN'
                mainImg = mainImg1
                mainImgTime1 = t.time()
        else:
            logoInit = logoImg

        # Menu Text Hover
        if hoverObject(mousePos, menuLogText, 350, 10):
            menuLogText = createText('Log', c=NAVY)
            if mouseUp:
                programState = 'LOG'
                logPageNum = 0
        else:
            menuLogText = createText('Log', c=BLUE)

        if hoverObject(mousePos, menuAttendanceText, 550, 10):
            menuAttendanceText = createText('Attendance', c=NAVY)
            if mouseUp:
                programState = 'ATTENDANCE'
                attPageNum = 0
        else:
            menuAttendanceText = createText('Attendance', c=BLUE)

        if hoverObject(mousePos, menuClassText, 900, 10):
            menuClassText = createText('Class', c=NAVY)
            if mouseUp:
                programState = 'CLASS'
                classPageNum = 0
        else:
            menuClassText = createText('Class', c=BLUE)

        # ——————— MAIN MENU ——————— #
        if programState == 'MAIN':
            # Display Diffrent Images Every 3 seconds
            mainImgTime2 = t.time()
            if (mainImgTime2 - mainImgTime1) > 3:
                mainImgTime1 = mainImgTime2
                if mainImg == mainImg1:
                    mainImg = mainImg2
                elif mainImg == mainImg2:
                    mainImg = mainImg3
                else:
                    mainImg = mainImg1
            mainSurface.blit(mainImg, (0, 70))


        # ——————— LOG MENU ——————— #
        if programState == 'LOG':
            menuLogText = createText('Log', c=NAVY)

            if os.path.exists('data/time.txt'):
                f = open("data/time.txt", "r")  # Open the file
                fileLists = f.readlines()  # Read the file into a list
                fileList = []
                studentNum = 0
                for i in range(len(fileLists)-2):
                    if i % 3 == 0:
                        fileList.append([fileLists[i].strip()])
                        fileList[studentNum].append(fileLists[i+1].strip())
                        fileList[studentNum].append(fileLists[i+2].strip())
                        studentNum += 1
                f.close()  # Close the file

                # Page control by up/down keys
                if leftArrow:
                    logPageNum -= 1
                    leftArrow = False
                elif rightArrow:
                    logPageNum += 1
                    rightArrow = False

                createBttn(mainSurface, leftBttn, 550, 720, leftBttnC)
                createBttn(mainSurface, rightBttn, 600, 720, rightBttnC)
                leftBttnHover = hoverObject(mousePos, leftBttn, 550, 720)
                rightBttnHover = hoverObject(mousePos, rightBttn, 600, 720)

                if leftBttnHover:
                    leftBttnC = GRAY
                    rightBttnC = DARKGRAY
                    if mouseUp:
                        logPageNum -= 1
                elif rightBttnHover:
                    rightBttnC = GRAY
                    leftBttnC = DARKGRAY
                    if mouseUp:
                        logPageNum += 1
                else:
                    leftBttnC = DARKGRAY
                    rightBttnC = DARKGRAY

                # Calculate What the Maximum Page Number is Depending on the Length of the File
                if len(fileList) < 8:
                    maxPage = 0
                else:
                    if len(fileList) % 8 == 0:
                        maxPage = len(fileList) / 8 - 1
                    else:
                        maxPage = math.floor(len(fileList) / 8)

                # Set Min/Max Page Number and Calculate the index number of the Last Element (for the for loop)
                if logPageNum >= maxPage:
                    logPageNum = maxPage
                    lastElement = 8 * maxPage + (len(fileList) - (8 * maxPage))
                else:
                    if logPageNum <= 0:
                        logPageNum = 0
                    if len(fileList) < 8:
                        lastElement = len(fileList)
                    else:
                        lastElement = 8 * logPageNum + 8

                logPageNum = int(logPageNum)
                lastElement = int(lastElement)

                # Draw the Names
                for j in range(8 * logPageNum, lastElement):
                    elementNum = j - 8 * logPageNum

                    name = fileList[j][0]
                    presence = fileList[j][1]
                    time = fileList[j][2]

                    studentNameBttn = createText(name, s=30, c=BLACK)
                    studentPresenceBttn = createText(presence, s=30, c=BLACK)
                    studentTimeBttn = createText(time, s=30, c=BLACK)

                    # If the name is too long to fit in, just show the first name
                    if studentNameBttn.get_width() >= 200:
                        nameSplit = name.split(" ", 1)
                        nameShort = nameSplit[0]
                        studentNameBttn = createText(nameShort, s=30, c=BLACK)

                    studentBttnsY = 150 + 70 * elementNum
                    studentNameBttnX = 80
                    studentPresenceBttnX = 450
                    studentTimeBttnX = 800

                    studentNameBttnHover = hoverObject(mousePos, studentNameBttn, studentNameBttnX, studentBttnsY)
                    studentPresenceBttnHover = hoverObject(mousePos, studentPresenceBttn, studentPresenceBttnX,
                                                           studentBttnsY)
                    studentTimeBttnHover = hoverObject(mousePos, studentTimeBttn, studentTimeBttnX, studentBttnsY)

                    # If any of the buttons are hovered, show the full name
                    # (since long names' last name is not shown)
                    if studentNameBttnHover or studentPresenceBttnHover or studentTimeBttnHover:
                        studentBttnC = DARKGRAY
                        studentNameBttn = createText(name, s=30, c=BLACK)
                        studentNameBttnX = 100

                        createBttn(mainSurface, studentPresenceBttn, studentPresenceBttnX, studentBttnsY, studentBttnC)
                        createBttn(mainSurface, studentNameBttn, studentNameBttnX, studentBttnsY, studentBttnC)
                        createBttn(mainSurface, studentTimeBttn, studentTimeBttnX, studentBttnsY, studentBttnC)
                    else:
                        studentBttnC = GRAY
                        createBttn(mainSurface, studentNameBttn, studentNameBttnX, studentBttnsY, studentBttnC)
                        createBttn(mainSurface, studentPresenceBttn, studentPresenceBttnX, studentBttnsY, studentBttnC)
                        createBttn(mainSurface, studentTimeBttn, studentTimeBttnX, studentBttnsY, studentBttnC)

            else:
                pass

        # ——————— ATTENDANCE MENU ——————— #
        if programState == 'ATTENDANCE':
            menuAttendanceText = createText('Attendance', c=NAVY)

            if os.path.exists("img/.DS_Store"):
                os.remove("img/.DS_Store")

            imgList = os.listdir('img/')
            imgListLen = len(imgList)

            if imgListLen == 0 or not os.path.exists("data/time.txt"):
                pass
            else:
                # Page control by up/down keys
                if leftArrow:
                    attPageNum -= 1
                    leftArrow = False
                elif rightArrow:
                    attPageNum += 1
                    rightArrow = False

                leftBttnHover = hoverObject(mousePos, leftBttn, 550, 720)
                rightBttnHover = hoverObject(mousePos, rightBttn, 600, 720)

                if leftBttnHover:
                    leftBttnC = GRAY
                    rightBttnC = DARKGRAY
                    if mouseUp:
                        attPageNum -= 1
                elif rightBttnHover:
                    rightBttnC = GRAY
                    leftBttnC = DARKGRAY
                    if mouseUp:
                        attPageNum += 1
                else:
                    leftBttnC = DARKGRAY
                    rightBttnC = DARKGRAY

                createBttn(mainSurface, leftBttn, 550, 720, leftBttnC)
                createBttn(mainSurface, rightBttn, 600, 720, rightBttnC)

                # Calculate What the Maximum Page Number is Depending on the Length of the File
                if imgListLen < 10:
                    attMaxPage = 0
                else:
                    if imgListLen % 10 == 0:
                        attMaxPage = imgListLen / 10 - 1
                    else:
                        attMaxPage = math.floor(imgListLen / 10)

                # Set Min/Max Page Number and Calculate the index number of the Last Element (for the for loop)
                if attPageNum >= attMaxPage:
                    attPageNum = attMaxPage
                    attLastElement = 10 * attMaxPage + (imgListLen - (10 * attMaxPage))
                else:
                    if attPageNum <= 0:
                        attPageNum = 0
                    if imgListLen < 10:
                        attLastElement = imgListLen
                    else:
                        attLastElement = 10 * attPageNum + 10

                # file content checking
                f = open("data/time.txt", "r")  # Open the file
                while True:
                    if len(f.readlines()) >= attLastElement:
                        break

                # Depending on the Page Number, change the index number (which changes the images to display)
                for i in range(10 * attPageNum, attLastElement):
                    attElementNum = i - 10 * attPageNum

                    # Change X and Y of the Img Depending on their index Number
                    if attElementNum > 4:
                        attElementNum -= 5
                        studentImgY = 470
                    else:
                        studentImgY = 150

                    if attElementNum == 0:
                        studentImgX = 100

                    # Student Images Display
                    studentImg = pygame.image.load('img/'+imgList[i]).convert_alpha()
                    studentImg = pygame.transform.smoothscale(studentImg, (160, 200))

                    studentImgModifiedX = studentImgX + attElementNum * 200
                    mainSurface.blit(studentImg, (studentImgModifiedX, studentImgY))

                    # Save Student Presence in List
                    f = open("data/time.txt", "r")  # Open the file
                    fileLists = f.readlines()  # Read the file into a list
                    fileList = []
                    for j in range(len(fileLists) - 1):
                        if j % 3 == 0:
                            fileList.append(fileLists[j + 1].strip())
                    f.close()  # Close the file

                    # Display Student Presence
                    studentPresenceImg = createText(fileList[i], s=30, c=WHITE)
                    if fileList[i] == 'Absent':
                        studentPresenceImgC = RED
                    elif fileList[i] == 'Present':
                        studentPresenceImgC = GREEN
                    else:
                        studentPresenceImgC = DARKGRAY

                    studentImgCentre = horizontalC(studentImg, mainSurface)
                    studentPresenceImgCentre = horizontalC(studentPresenceImg, mainSurface) - 7

                    studentPresenceImgX = studentImgModifiedX - (studentImgCentre - studentPresenceImgCentre)
                    studentPresenceImgY = studentImgY + 210
                    createBttn(mainSurface, studentPresenceImg, studentPresenceImgX, studentPresenceImgY, studentPresenceImgC)

                    # Get Student Name
                    base = os.path.basename(f'img/{imgList[i]}')
                    imgName = os.path.splitext(base)[0]

                    # Img Hover
                    studentImgHover = hoverObject(mousePos, studentImg, studentImgModifiedX, studentImgY)

                    # Name Display When Hovered
                    if studentImgHover:
                        studentNameImg = createText(imgName, s=30, c=WHITE)
                        studentNameImgC = BLUE

                        studentNameImgCentre = horizontalC(studentNameImg, mainSurface) - 7

                        studentImgModifiedX = studentImgModifiedX - (studentImgCentre - studentNameImgCentre)
                        studentImgModifiedY = studentImgY - studentNameImg.get_height() - 10
                        createBttn(mainSurface, studentNameImg, studentImgModifiedX, studentImgModifiedY, studentNameImgC)

        # ——————— CLASS MENU ——————— #
        if programState == 'CLASS':
            menuClassText = createText('Class', c=NAVY)

            if os.path.exists("img/.DS_Store"):
                os.remove("img/.DS_Store")

            # Add Button Draw & Collision Detection
            dimensionAddBttn = [100, 150, addBttn.get_width() + 100, addBttn.get_height() + 165]
            pygame.draw.rect(mainSurface, addBttnC, dimensionAddBttn, border_radius=10)
            addSymbText = createText('+', s=100, c=WHITE)
            mainSurface.blit(addBttn, (150, 150 + 165 / 1.5))
            mainSurface.blit(addSymbText, (158, 160))

            addBttnArea = pygame.Rect(dimensionAddBttn)
            if addBttnArea.collidepoint(mousePos[0], mousePos[1]):
                addBttnHover = True
            else:
                addBttnHover = False

            if addBttnHover:
                addBttnC = DARKGRAY
                if mouseUp:
                    fileCheck()
            else:
                addBttnC = GRAY

            imgList = os.listdir('img/')
            imgListLen = len(imgList)

            if imgListLen == 0 or not os.path.exists("data/time.txt"):
                pass
            else:
                # Page control by up/down keys
                if leftArrow:
                    classPageNum -= 1
                    leftArrow = False
                elif rightArrow:
                    classPageNum += 1
                    rightArrow = False

                # Arrow Button Hover Detection
                leftBttnHover = hoverObject(mousePos, leftBttn, 550, 720)
                rightBttnHover = hoverObject(mousePos, rightBttn, 600, 720)

                if leftBttnHover:
                    leftBttnC = GRAY
                    rightBttnC = DARKGRAY
                    if mouseUp:
                        classPageNum -= 1
                elif rightBttnHover:
                    rightBttnC = GRAY
                    leftBttnC = DARKGRAY
                    if mouseUp:
                        classPageNum += 1
                else:
                    leftBttnC = DARKGRAY
                    rightBttnC = DARKGRAY

                # Page Control on Screen
                createBttn(mainSurface, leftBttn, 550, 720, leftBttnC)
                createBttn(mainSurface, rightBttn, 600, 720, rightBttnC)

                # Calculate What the Maximum Page Number is Depending on the Length of the File
                if imgListLen < 10:
                    classMaxPage = 0
                elif imgListLen % 9 == 0:
                    classMaxPage = imgListLen / 9 - 1
                else:
                    classMaxPage = math.floor(imgListLen / 9)

                # Set Min/Max Page Number and Calculate the index number of the Last Element (for the for loop)
                if classPageNum >= classMaxPage:
                    classPageNum = classMaxPage
                    classLastElement = imgListLen
                else:
                    if classPageNum <= 0:
                        classPageNum = 0
                    if imgListLen < 10:
                        classLastElement = imgListLen
                    else:
                        classLastElement = 9 * classPageNum + 9

                # file content checking
                f = open("data/time.txt", "r")  # Open the file
                while True:
                    if len(f.readlines()) >= classLastElement:
                        break

                # Display the Student Images
                for i in range(9 * classPageNum, classLastElement):
                    # Index Num of the Image in Terms of the Row of the Page
                    classElementNum = i - 9 * classPageNum

                    # Change X and Y of the Img Depending on their index Number
                    if classElementNum < 4:
                        studentImgY = 150
                        studentImgX = 300
                    else:
                        classElementNum -= 4
                        studentImgY = 470
                        if classElementNum == 0:
                            studentImgX = 100

                    # Student Images Display
                    studentImg = pygame.image.load('img/' + imgList[i]).convert_alpha()
                    studentImg = pygame.transform.smoothscale(studentImg, (160, 200))

                    studentImgModifiedX = studentImgX + classElementNum * 200
                    mainSurface.blit(studentImg, (studentImgModifiedX, studentImgY))

                    # Get the Student Name from the Img File Name
                    base = os.path.basename(f'img/{imgList[i]}')
                    imgName = os.path.splitext(base)[0]

                    studentNameImg = createText(imgName, s=30, c=WHITE)
                    studentNameImgC = BLUE

                    # If the Name is Longer than the Image Display Size, Only Show First Name
                    if studentNameImg.get_width() >= 160:
                        nameSplit = imgName.split(" ", 1)
                        nameShort = nameSplit[0]
                        studentNameImg = createText(nameShort, s=30, c=WHITE)

                    # Calculate the Centre X / Y Values for the Names
                    studentNameImgCentre = horizontalC(studentNameImg, mainSurface) - 7
                    studentImgCentre = horizontalC(studentImg, mainSurface)
                    studentImgModifiedNameX = studentImgModifiedX - (studentImgCentre - studentNameImgCentre)
                    studentImgModifiedY = studentImgY - studentNameImg.get_height() - 10

                    # If the Name or the Image is Hovered, Show the Full Name, Change the Colour, Calculate the new  XY Values
                    if hoverObject(mousePos, studentImg, studentImgModifiedX, studentImgY) or \
                       hoverObject(mousePos, studentNameImg, studentImgModifiedNameX, studentImgModifiedY):
                        studentNameImg = createText(imgName, s=30, c=WHITE)
                        studentNameImgC = YELLOW

                        studentNameImgCentre = horizontalC(studentNameImg, mainSurface) - 7
                        studentImgCentre = horizontalC(studentImg, mainSurface)

                        studentImgModifiedNameX = studentImgModifiedX - (studentImgCentre - studentNameImgCentre)
                        studentImgModifiedY = studentImgY - studentNameImg.get_height() - 10

                    # Draw the name
                    createBttn(mainSurface, studentNameImg, studentImgModifiedNameX, studentImgModifiedY, studentNameImgC)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()
