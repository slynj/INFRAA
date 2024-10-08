import pygame
import math
import tkinter as tk
from tkinter import filedialog as fd
import shutil
import os
import time as t
from datetime import date, time, datetime, timedelta


def dataFileExist(fileName):
    """
    Check if the File / Path Exists. If Not, Create it

    :param fileName: str
        name of the file to check
    :return:
        None
    """
    if not os.path.exists(f'{fileName}'):
        open(f'{fileName}', 'x')


def fileCheck():
    """
    Copies the selected image file and saves it to the 'img' directory for the detector

    :return:
        None
    """
    dstPath = "img/"
    path = fd.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpeg"),
                                                                              ("png files", "*.png"),
                                                                              ("jpg files", "*.jpg")))
    try:
        shutil.copy(path, dstPath)
    except Exception as error:
        return


def removeFiles(fileName):
    """
    Remove Files if they Exist

    :return:
        None
    """
    if os.path.exists(fileName):
        os.remove(fileName)


def currentTime():
    """
    Return the current time in YYYY-MM-DD HH:MM:SS format

    :return: datetime
        the current time in YYYY-MM-DD HH:MM:SS format
    """
    today = date.today()
    now = datetime.now()
    currentTimes = time(now.hour, now.minute, now.second)
    return datetime.combine(today, currentTimes)


def createBttn(mainSurface, text, textX, textY, c=(0, 0, 0)):
    """
    Creates a button with the rendered text given

    :param mainSurface: pygame.Surface
        the surface to draw the elements
    :param text: pygame.Surface
        the rendered text of the button
    :param textX: float
        the X coordinate of the button
    :param textY: float
        the Y coordinate of the button
    :param c: tuple[int, int, int] = (0, 0, 0)
        colour of the button
    :return:
        None
    """
    paddingW = 15
    paddingH = 5
    dimension = [textX, textY, text.get_width() + paddingW, text.get_height() + paddingH]
    pygame.draw.rect(mainSurface, c, dimension, border_radius=10)
    mainSurface.blit(text, (textX + paddingW/2, textY + paddingH/2))


def horizontalC(item, mainSurface):
    """
    Calculates what coordinate of the item's horizontal centre is

    :param item: pygame.Surface
        element to be horizontally centered
    :param mainSurface:  pygame.Surface
        the surface to draw the elements
    :return: int
        the x coordinate where the element would be centered
    """
    return int((mainSurface.get_width() - item.get_width()) // 2)


def resizeImg(file, factor):
    """
    Resizes Images

    :param file:  str
        the name of the file to load
    :param factor: int
        the multiplier to reduce/increase the image size by
    :return: pygame.Surface
        the resized version of the image
    """
    resizedImg = pygame.image.load(file).convert_alpha()
    resizedImg = pygame.transform.smoothscale\
        (resizedImg, (resizedImg.get_width() / factor, resizedImg.get_height() / factor))
    return resizedImg


def createText(t, f="tommy.otf", s=40, c=(58, 101, 139)):
    """
    Creates a Rendered Text with Given String

    :param t: str
        the text string to render
    :param f: str
        the name of the font being used to render the text
    :param s: float
        the size of the text
    :param c: tuple[int, int, int] = (58, 101, 139)
        colour of the text
    :return: pygame.Surface
        rendered text
    """
    text = pygame.font.Font(f'resource/{f}', s)
    renderedText = text.render(t, True, c)
    return renderedText


def hoverObject(mouse, objects, objectX, objectY):
    """
    Collision Detection for Rectangles (shapes, images, texts)

    :param mouse: tuple
        XY coordinates of the mouse pointer
    :param objects: pygame.Surface
        the object to detect the collision
    :param objectX: float
        the X coordinate of the object
    :param objectY: float
        the Y coordinate of the object
    :return: bool
        if the mouse and the object collide or not
    """
    paddingW = 15
    paddingH = 5
    dimension = [objectX, objectY, objects.get_width() + paddingW, objects.get_height() + paddingH]
    area = pygame.Rect(dimension)
    if area.collidepoint(mouse[0], mouse[1]):
        return True
    else:
        return False


def pageControl(mainSurface, mousePos, pageNums):
    """
    Page Control by Buttons / Keys

    :param mainSurface: pygame.Surface
        the surface to draw the elements
    :param mousePos: tuple
        XY coordinates of the mouse pointer
    :param pageNums: int
        current page number
    :return: int
        return the changed page number
    """
    global leftArrow, rightArrow, leftBttn, rightBttn, leftBttnC, rightBttnC, mouseUp, GRAY, DARKGRAY
    # Left / Right Keyboard Detection
    if leftArrow:
        pageNums -= 1
        leftArrow = False
    elif rightArrow:
        pageNums += 1
        rightArrow = False

    # Arrow Buttons Hover Detection
    leftBttnHover = hoverObject(mousePos, leftBttn, 550, 720)
    rightBttnHover = hoverObject(mousePos, rightBttn, 600, 720)

    if leftBttnHover:
        leftBttnC = GRAY
        rightBttnC = DARKGRAY
        if mouseUp:
            pageNums -= 1
    elif rightBttnHover:
        rightBttnC = GRAY
        leftBttnC = DARKGRAY
        if mouseUp:
            pageNums += 1
    else:
        leftBttnC = DARKGRAY
        rightBttnC = DARKGRAY

    createBttn(mainSurface, leftBttn, 550, 720, leftBttnC)
    createBttn(mainSurface, rightBttn, 600, 720, rightBttnC)

    return pageNums


def pageNumDisplay(mainSurface, curretNum, maxNum):
    """
    Displays the Current Page Number and the Max Page Number

    :param mainSurface: mainSurface: pygame.Surface
        the surface to draw the elements
    :param curretNum: int
        current page number
    :param maxNum: int
        maximum page number
    :return:
        None
    """
    global BLUE
    currentPageNum = createText(str(curretNum + 1), s=15, c=BLUE)
    MaxPageNum = createText(str(maxNum + 1), s=15, c=BLUE)
    slash = createText('/', s=15, c=BLUE)
    mainSurface.blit(currentPageNum, (570, 768))
    mainSurface.blit(slash, (595, 768))
    mainSurface.blit(MaxPageNum, (620, 768))



def nonFace():
    """
    If the Face was not Detected and the imgStatus.txt was created by the detector, display an Error Window

    :return:
        None
    """
    global mainSurface, errorImg, xBttn, mousePos, xBttn, RED, BLACK
    # Read the file from the Detector
    if os.path.exists("data/imgStatus.txt"):
        f = open('data/imgStatus.txt', 'r')
        imgStatus = f.read()
        f.close()
        # If the image is unrecognizable
        if imgStatus == 'ImageNR':
            # Error Window
            mainSurface.blit(errorImg, (horizontalC(errorImg, mainSurface), 200))
            mainSurface.blit(xBttn, (950, 205))
            # Closing Button
            if hoverObject(mousePos, xBttn, 950, 205):
                xBttn = createText('x', s=50, c=RED)
                if mouseUp:
                    f = open('data/imgStatus.txt', 'w')
                    f.write('')
                    f.close()
            else:
                xBttn = createText('x', s=50, c=BLACK)


def main():
    # -----------------------------Setup------------------------------------------------- #
    global leftArrow, rightArrow, leftBttn, rightBttn, leftBttnC, rightBttnC, mouseUp, GRAY, DARKGRAY, BLUE, \
        mainSurface, errorImg, xBttn, mousePos, xBttn, RED, BLACK

    # initial setting for tk window (browsing)
    # https://stackoverflow.com/questions/1406145 (how to get rid of tk window)
    root = tk.Tk()
    root.withdraw()
    if root.wm_state() == 'withdrawn':
        root.iconify()

    pygame.init()

    pygame.display.set_caption("INFRAA")

    # -----------------------------Program Variable Initialization----------------------- #
    # Surface Size
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
    LIGHTGRAY = (242, 244, 249)
    GREEN = (88, 168, 112)
    RED = (194, 62, 62)

    # Program State (LOAD, MAIN, LOG, ATTENDANCE, CLASS, HELP)
    programState = "LOAD"

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
    # Help Page Images
    helpFAQImg = resizeImg('resource/helpFAQ.png', 1)
    helpMFImg1 = resizeImg('resource/helpMF1.png', 1)
    helpMFImg2 = resizeImg('resource/helpMF2.png', 1)
    helpMFImg3 = resizeImg('resource/helpMF3.png', 1)
    helpHWImg = resizeImg('resource/helpHW.png', 1)
    helpMFImg = helpMFImg1
    # Error Message Images
    errorImg = resizeImg('resource/error.png', 1)
    cameraErrorImg = resizeImg('resource/noCameraError.png', 1)
    # Loading Screen Images
    loadImg1 = resizeImg('resource/loading1.png', 1)
    loadImg2 = resizeImg('resource/loading2.png', 1)
    loadImg3 = resizeImg('resource/loading3.png', 1)
    loadImg4 = resizeImg('resource/loading4.png', 1)
    loadImg5 = resizeImg('resource/loading5.png', 1)
    loadNC1 = resizeImg('resource/loadingNC1.png', 1)
    loadNC2 = resizeImg('resource/loadingNC2.png', 1)
    loadNC3 = resizeImg('resource/loadingNC3.png', 1)
    loadNC4 = resizeImg('resource/loadingNC4.png', 1)
    loadNC5 = resizeImg('resource/loadingNC5.png', 1)
    imgNum = 0
    loadImgList = [loadImg1, loadImg2, loadImg3, loadImg4, loadImg5]

    # TEXTS INIT #
    # Menu Header Texts
    menuLogText = createText('Log')
    menuAttendanceText = createText('Attendance')
    menuClassText = createText('Class')
    # Error Window Texts
    xBttn = createText('x', s=50, c=BLACK)

    # BUTTONS INIT #
    # Add Student Button
    addBttn = createText('Add', s=30, c=WHITE)
    addBttnC = GRAY
    # Next Page Button
    rightBttn = createText(' > ', s=30, c=WHITE)
    leftBttn = createText(' < ', s=30, c=WHITE)
    rightBttnC = DARKGRAY
    leftBttnC = DARKGRAY
    # Help Button
    helpBttn = createText(' ? ', s=30, c=WHITE)
    helpBttnC = GRAY
    helpFAQBttn = createText('FAQ', s=30, c=BLACK)
    helpMFBttn = createText('Menus / Features', s=30, c=BLACK)
    helpHW = createText('How it Works', s=30, c=BLACK)

    # MENU PAGES VARIABLES #
    # Front / Back Page Control
    leftArrow = False
    rightArrow = False
    # Page Num
    logPageNum = 0
    attPageNum = 0
    classPageNum = 0

    # INITIALIZE FILES #
    # Delete and Create a new time.txt
    removeFiles('data/time.txt')
    file = open('data/time.txt', 'x')
    file.close()

    # Empty the imgStatus.txt file
    removeFiles('data/imgStatus.txt')
    file = open('data/imgStatus.txt', 'x')
    file.write('')
    file.close()

    removeFiles('data/detectorError.txt')
    removeFiles('data/noDetector.txt')

    # ----------------------------- Main Game Loop ---------------------------------------- #

    while True:
        # ----------------------------- Event Handling ------------------------------------ #
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

        # Remove .DS_Store Files That are Automatically Created
        removeFiles("img/.DS_Store")

        # ----------------------------- Game Logic / Drawing -------------------------------- #

        # ——————— LOAD MENU ——————— #
        if programState == 'LOAD':
            # Background
            mainSurface.fill(LIGHTGRAY)
            # Update Time
            mainImgTime2 = t.time()
            # Change Img Every Second
            if (mainImgTime2 - mainImgTime1) > 1:
                imgNum += 1
                mainImgTime1 = mainImgTime2
            if imgNum > 4:
                imgNum = 0

            mainSurface.blit(loadImgList[imgNum], (0, 0))

            imgList = os.listdir('img/')
            imgListLen = len(imgList)

            if os.path.exists('data/detectorError.txt'):
                loadImgList = [loadNC1, loadNC2, loadNC3, loadNC4, loadNC5]
                mainSurface.blit(cameraErrorImg, (horizontalC(cameraErrorImg, mainSurface), 200))
                mainSurface.blit(xBttn, (950, 205))
                # Closing Button
                if hoverObject(mousePos, xBttn, 950, 205):
                    xBttn = createText('x', s=50, c=RED)
                    if mouseUp:
                        removeFiles('data/detectorError.txt')
                else:
                    xBttn = createText('x', s=50, c=BLACK)

            # Wait until the detector finishes writing on the file
            if os.path.exists('data/time.txt'):
                f = open('data/time.txt', 'r')
                lines = len(f.readlines())

                if lines >= 3 * imgListLen:
                    removeFiles('data/detectorError.txt')
                    dataFileExist('data/noDetector.txt')
                    programState = 'MAIN'
                    mainImg = mainImg1
                    mainImgTime1 = t.time()

        else:
            # ——————— MENU BAR GRAPHICS ——————— #
            # Background
            mainSurface.fill(LIGHTGRAY)
            # Header
            pygame.draw.rect(mainSurface, (233, 235, 240), (0, 0, surfaceSizeX, 70))
            # Logo
            mainSurface.blit(logoInit, (0, 0))
            # Menu Text
            mainSurface.blit(menuLogText, (350, 10))
            mainSurface.blit(menuAttendanceText, (550, 10))
            mainSurface.blit(menuClassText, (900, 10))
            # Help Button
            createBttn(mainSurface, helpBttn, 1140, 16, helpBttnC)

            # Logo Hover
            # MAIN hover / click
            if hoverObject(mousePos, logoInit, 0, 0):
                logoInit = logoHoverImg
                if mouseUp:
                    programState = 'MAIN'
                    mainImg = mainImg1
                    mainImgTime1 = t.time()
            else:
                logoInit = logoImg

            # Menu Text Hover
            # LOG hover/ click
            if hoverObject(mousePos, menuLogText, 350, 10):
                menuLogText = createText('Log', c=NAVY)
                if mouseUp:
                    programState = 'LOG'
                    logPageNum = 0
            else:
                menuLogText = createText('Log', c=BLUE)

            # ATTENDANCE hover / click
            if hoverObject(mousePos, menuAttendanceText, 550, 10):
                menuAttendanceText = createText('Attendance', c=NAVY)
                if mouseUp:
                    programState = 'ATTENDANCE'
                    attPageNum = 0
            else:
                menuAttendanceText = createText('Attendance', c=BLUE)

            # CLASS hover / click
            if hoverObject(mousePos, menuClassText, 900, 10):
                menuClassText = createText('Class', c=NAVY)
                if mouseUp:
                    programState = 'CLASS'
                    classPageNum = 0
            else:
                menuClassText = createText('Class', c=BLUE)

            # HELP hover / click
            if hoverObject(mousePos, helpBttn, 1140, 16):
                helpBttnC = GRAY
                createBttn(mainSurface, helpBttn, 1140, 16, helpBttnC)
                if mouseUp:
                    programState = 'HELP'
                    helpState = 'FAQ'
            else:
                helpBttnC = DARKGRAY
                createBttn(mainSurface, helpBttn, 1140, 16, helpBttnC)

        # ——————— MAIN MENU ——————— #
        if programState == 'MAIN':
            # Display Different Images Every 3 seconds
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

                # Arrow Button Drawing / Arrow Keys Controlling Page Number
                logPageNum = pageControl(mainSurface, mousePos, logPageNum)

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

                # Current Page / Max Page Display
                pageNumDisplay(mainSurface, int(logPageNum), int(maxPage))

                # file content checking
                f = open("data/time.txt", "r")  # Open the file
                while True:
                    if len(f.readlines()) >= lastElement:
                        f.close()
                        break

                # Draw the Names
                for j in range(8 * int(logPageNum), int(lastElement)):
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

            imgList = os.listdir('img/')
            imgListLen = len(imgList)

            if imgListLen == 0 or not os.path.exists("data/time.txt"):
                pass
            else:
                # Arrow Button Drawing / Arrow Keys Controlling Page Number
                attPageNum = pageControl(mainSurface, mousePos, attPageNum)

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

                # Current Page / Max Page Display
                pageNumDisplay(mainSurface, int(attPageNum), int(attMaxPage))

                # file content checking
                f = open("data/time.txt", "r")  # Open the file
                while True:
                    if len(f.readlines()) >= attLastElement:
                        f.close()
                        break

                # Depending on the Page Number, change the index number (which changes the images to display)
                for i in range(10 * int(attPageNum), int(attLastElement)):
                    attElementNum = i - 10 * attPageNum

                    # Change X and Y of the Img Depending on their index Number
                    if attElementNum > 4:
                        attElementNum -= 5
                        studentImgY = 460
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
                    mouseUp = False
                    fileCheck()
            else:
                addBttnC = GRAY

            imgList = os.listdir('img/')
            imgListLen = int(len(imgList))

            if imgListLen == 0 or not os.path.exists("data/time.txt"):
                pass
            else:
                # Check the Number of Student Written on the time.txt File
                file = open('data/time.txt', 'r')
                timeFileLength = int(len(file.readlines()) / 3)
                file.close()

                # Compare it with the Number of Student Images to Check if the Data Needs to be Appended
                if os.path.exists('data/noDetector.txt') and timeFileLength != imgListLen:
                    timeFileNameList = []

                    # Append the Students' Name that is on the txt File
                    for j in range(timeFileLength*3):
                        file = open('data/time.txt', 'r')
                        timeFileName = file.readlines()
                        file.close()
                        if j % 3 == 0:
                            timeFileNameList.append(timeFileName[j].strip('\n'))

                    # Get the Student Name from the Img File Name
                    for i in range(imgListLen):
                        base = os.path.basename(f'img/{imgList[i]}')
                        imgName = os.path.splitext(base)[0]

                        # If it is the New Student, Add to the txt File
                        if imgName not in timeFileNameList:
                            record = imgName + '\n' + 'Absent' + '\n' + str(currentTime()) + '\n'
                            file = open('data/time.txt', 'a')
                            file.write(record)
                            file.close()

                # Arrow Button Drawing / Arrow Keys Controlling Page Number
                classPageNum = pageControl(mainSurface, mousePos, classPageNum)

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

                # Current Page / Max Page Display
                pageNumDisplay(mainSurface, int(classPageNum), int(classMaxPage))

                # file content checking
                f = open("data/time.txt", "r")  # Open the file
                while True:
                    if len(f.readlines()) >= classLastElement:
                        f.close()
                        break

                # Display the Student Images
                for i in range(9 * int(classPageNum), int(classLastElement)):
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

                    nonFace()

                    f = open('data/imgStatus.txt', 'r')
                    imgStatus = f.read()
                    f.close()

                    if imgStatus != 'ImageNR':
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

        # ——————— HELP MENU ——————— #
        if programState == 'HELP':
            # Menu Indication (—)
            underLine = createText('—', s=40, c=YELLOW)

            # ——————— FAQ ——————— #
            if helpState == 'FAQ':
                # Draw the Menu Button / Images
                helpFAQBttn = createText('FAQ', s=30, c=YELLOW)
                mainSurface.blit(helpFAQImg, (0, 70))
                mainSurface.blit(underLine, (184, 120))

            # ——————— Menus / Features ——————— #
            if helpState == 'MF':
                # Lists of Page Images
                helpMFPageList = [helpMFImg1, helpMFImg2, helpMFImg3]

                # Draw Menu Button / Images
                helpFAQBttn = createText('Menus / Features', s=30, c=YELLOW)
                mainSurface.blit(helpMFImg, (0, 70))
                mainSurface.blit(underLine, (550, 120))

                # Page Control by Buttons / Keyboard
                helpMFPageNum = pageControl(mainSurface, mousePos, helpMFPageNum)

                # Page Number Max / Min Limits
                if helpMFPageNum > 2:
                    helpMFPageNum = 2
                elif helpMFPageNum < 0:
                    helpMFPageNum = 0

                # Current Page / Max Page Display
                pageNumDisplay(mainSurface, int(helpMFPageNum), 2)

                # Set the Image to Display According to the Page Number
                helpMFImg = helpMFPageList[helpMFPageNum]

            # ——————— How it Works ——————— #
            if helpState == 'HW':
                helpMFBttn = createText('How it Works', s=30, c=YELLOW)
                mainSurface.blit(helpHWImg, (0, 70))
                mainSurface.blit(underLine, (930, 120))

            # ——————— Menu Buttons Hover / Click Detection ——————— #
            # FAQ Menu
            if hoverObject(mousePos, helpFAQBttn, 170, 100):
                helpFAQBttn = createText('FAQ', s=30, c=YELLOW)
                if mouseUp:
                    helpState = 'FAQ'
            else:
                if helpState != 'FAQ':
                    helpFAQBttn = createText('FAQ', s=30, c=BLACK)

            # Menus / Feautres Menu
            if hoverObject(mousePos, helpMFBttn, 450, 100):
                helpMFBttn = createText('Menus / Features', s=30, c=YELLOW)
                if mouseUp:
                    helpState = 'MF'
                    helpMFImg = helpMFImg1
                    helpMFPageNum = 0
            else:
                if helpState != 'MF':
                    helpMFBttn = createText('Menus / Features', s=30, c=BLACK)

            # How it Works Menu
            if hoverObject(mousePos, helpHW, 850, 100):
                helpHW = createText('How it Works', s=30, c=YELLOW)
                if mouseUp:
                    helpState = 'HW'
            else:
                if helpState != 'HW':
                    helpHW = createText('How it Works', s=30, c=BLACK)

            # Display the Menu Buttons
            mainSurface.blit(helpFAQBttn, (170, 100))
            mainSurface.blit(helpMFBttn, (450, 100))
            mainSurface.blit(helpHW, (850, 100))

        nonFace()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


main()
