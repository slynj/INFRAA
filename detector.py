import face_recognition
import cv2
import numpy as np
import os
from datetime import date, time, datetime, timedelta

global fileNum2, encodedImg, faceEncoding, faceNames, initial, currentFaces

# Initialize Variables
fileNum2 = 0
encodedImg = []
processThisFrame = True
knownFaceEncodings = []
knownFaceNames = []
faceLocations = []
faceEncodings = []
faceNames = []
initial = True
currentFaces = []


def newFace(imgFile, faceName):
    """
    Adds a new face and name

    :param imgFile: str
        name of the student image file to be loaded
    :param faceName: str
        name of the student face
    :return: bool, str
        True if the face is not recongized, face name if the face is recognized
    """
    global faceEncoding
    # Status Shared with the Interface
    image = face_recognition.load_image_file(f"img/{imgFile}")
    try:
        faceEncoding = face_recognition.face_encodings(image)[0]
    # Face Not Recognized From the Image
    except IndexError as error:
        os.remove(f"img/{imgFile}")
        f = open('data/imgStatus.txt', 'w')
        f.write('ImageNR')
        f.close()
        return True

    knownFaceEncodings.append(faceEncoding)
    knownFaceNames.append(faceName)


def addFace():
    """
    Counts the number of files in the img directory to see if there are any new students added

    :return:
        None
    """
    global fileNum2, encodedImg, currentFaces

    # Remove DS_Store Files
    if os.path.exists("img/.DS_Store"):
        os.remove("img/.DS_Store")

    fileNum1 = len(os.listdir('img/'))

    # New Images are added
    if fileNum1 != fileNum2:
        imgList = os.listdir('img/')
        # Append to lists and time.txt
        for i in range(fileNum1):
            if imgList[i] not in encodedImg:
                base = os.path.basename(f'img/{imgList[i]}')
                imgName = os.path.splitext(base)[0]

                encodedImg.append(imgList[i])
                newFaceRecog = newFace(imgList[i].replace("'", ""), imgName)

                if not newFaceRecog:
                    currentFaces.append([imgName])
                    currentFaces[-1].append('Absent')
                    currentFaces[-1].append(currentTime())

                    record = currentFaces[-1][0] + '\n' + currentFaces[-1][1] + '\n' + str(currentFaces[-1][2]) + '\n'

                    if fileNum1 != len(open("data/time.txt", "r").readlines())/3:
                        file = open('data/time.txt', 'a')
                        file.write(record)
                        file.close()

        fileNum2 = fileNum1


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


def programInit():
    """
    Program Files and Lists Initialize

    :return:
        None
    """
    global initial, currentFaces

    if initial:
        initial = False

        # Collect Data and append it to a list
        for i in range(len(knownFaceNames)):
            currentFaces.append([knownFaceNames[i]])
            currentFaces[i].append('Absent')
            currentFaces[i].append(currentTime())

        # Write Data on the FIle
        for j in range(len(currentFaces)):
            nameStored = currentFaces[j][0]
            presenceStored = currentFaces[j][1]
            timeStored = currentFaces[j][2]

            record = nameStored + '\n' + presenceStored + '\n' + str(timeStored) + '\n'

            file = open('data/time.txt', 'a')
            file.write(record)
            file.close()


def dataFileExist(fileName):
    """
    Check if the File / Path Exists. If Not, Create it

    :param fileName: str
        name of the file to check
    :return:
        None
    """
    if not os.path.exists(f'data/{fileName}.txt'):
        open(f'data/{fileName}.txt', 'x')


def webcamCheck(videoCaptures):
    """
    Check if the Webcam is Functioning and Data is Being Read

    :param videoCaptures
        the data read through the webcam by the open cv library
    :return: Bool
        if the data is being read from the webcam
    """
    ret, frame = videoCaptures.read()

    if frame is None:
        return True
    else:
        return False


# Set default webcam,
videoCapture = cv2.VideoCapture(0)
if webcamCheck(videoCapture):
    videoCapture = cv2.VideoCapture(4)
    if webcamCheck(videoCapture):
        videoCapture = cv2.VideoCapture(5)
        if webcamCheck(videoCapture):
            dataFileExist('detectorError')

# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
while True:

    programInit()
    addFace()

    # Grab a single frame of video
    ret, frame = videoCapture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgbSmallFrame = smallFrame[:, :, ::-1]

    # Only process every other frame of video to save time
    if processThisFrame:
        # Find all the faces and face encodings in the current frame of video
        faceLocations = face_recognition.face_locations(rgbSmallFrame)
        faceEncodings = face_recognition.face_encodings(rgbSmallFrame, faceLocations)

        faceNames = []
        for faceEncoding in faceEncodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(knownFaceEncodings, faceEncoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            faceDistances = face_recognition.face_distance(knownFaceEncodings, faceEncoding)
            bestMatchIndex = np.argmin(faceDistances)
            if matches[bestMatchIndex]:
                name = knownFaceNames[bestMatchIndex]

            faceNames.append(name)

            dataFileExist('time')

            for i in range(len(currentFaces)):

                if currentFaces[i][0] == name:
                    nameStored = currentFaces[i][1]
                    presenceStored = currentFaces[i][1]
                    timeStored = currentFaces[i][2]

                    duration = currentTime() - timeStored
                    duration_in_s = duration.total_seconds()

                    if duration_in_s > 5:
                        recurringName = False

                        currentFaces[i][2] = currentTime()
                        if presenceStored == 'Present':
                            currentFaces[i][1] = 'Absent'
                        elif presenceStored == 'Absent':
                            currentFaces[i][1] = 'Present'

                        # Update variable values
                        nameStored = currentFaces[i][0]
                        presenceStored = currentFaces[i][1]
                        timeStored = currentFaces[i][2]

                        record = nameStored + '\n' + presenceStored + '\n' + str(timeStored) + '\n'

                        lineNum = 0
                        file = open("data/time.txt", "r")

                        for line in file.readlines():
                            lineNum += 1
                            if line.find(name) >= 0:
                                recurringName = True
                                break

                        # Update the previous information if it is a recurring name
                        if recurringName:
                            file = open('data/time.txt', 'r')
                            data = file.readlines()
                            data[lineNum] = presenceStored + '\n'
                            data[lineNum+1] = str(timeStored) + '\n'
                            file.close()

                            file = open('data/time.txt', 'w')
                            file.writelines(data)
                            file.close()

    processThisFrame = not processThisFrame

    # Display the results
    for (top, right, bottom, left), name in zip(faceLocations, faceNames):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # try:
        # Display the resulting image
    cv2.imshow('INFRAA Detector', frame)
    # except Exception as e:
    #     print("JLDKJFLSKDJFLKSD")
    #     dataFileExist('data/detectorError.txt')

    # Hit 'q' on the keyboard to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
videoCapture.release()
cv2.destroyAllWindows()