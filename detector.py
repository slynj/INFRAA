import face_recognition
import cv2
import numpy as np
import os
from datetime import date, time, datetime

global fileNum2, encodedImg

# Set default webcam
video_capture = cv2.VideoCapture(1)

# Initialize some variables
fileNum2 = 0
encodedImg = []

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


# Adds a new face and name
def newFace(imgFile, faceName):
    image = face_recognition.load_image_file(f"img/{imgFile}")
    faceEncoding = face_recognition.face_encodings(image)[0]

    known_face_encodings.append(faceEncoding)
    known_face_names.append(faceName)


# Counts the number of files in the img directory to see if there are any new students added
def addFace():
    global fileNum2, encodedImg

    # ignore
    if os.path.exists("img/.DS_Store"):
        os.remove("img/.DS_Store")

    fileNum1 = len(os.listdir('img/'))

    if fileNum1 != fileNum2:
        imgList = os.listdir('img/')
        for i in range(fileNum1):
            if imgList[i] not in encodedImg:
                base = os.path.basename(f'img/{imgList[i]}')
                imgName = os.path.splitext(base)[0]

                encodedImg.append(imgList[i])
                newFace(imgList[i].replace("'", ""), imgName)

        fileNum2 = fileNum1


def currentTime():
    """ Return the current time in YYYY-MM-DD HH:MM:SS format """
    today = date.today()
    now = datetime.now()
    current_time = time(now.hour, now.minute, now.second)
    return datetime.combine(today, current_time)


currentFaces = []
global initial
initial = True

def currentFace():
    global initial

    if initial:
        initial = False
        for i in range(len(known_face_names)):
            currentFaces.append([known_face_names[i]])

    # for i in range(len(known_face_names)):
    #     if known_face_names[i] != currentFaces[i][0]:
    #         print("jjsdkjf;alksdj;flaksj")
    #         currentFaces[i][0].append(known_face_names[i])
    print(len(known_face_names))
    print(len(currentFaces))
    print(currentFaces[1][0])
    if len(known_face_names) != len(currentFaces):
        index = len(currentFaces)
        for i in range(index):
            if known_face_names[i] != currentFaces[i][0]:
                print("j")
                currentFaces[i][0].append(known_face_names[i])
                if index != len(known_face_names):
                    index += 1
    print(currentFaces)
    # if fileNum1 != fileNum2:
    #     imgList = os.listdir('img/')
    #     for i in range(fileNum1):
    #         if imgList[i] not in encodedImg:


# https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
while True:
    addFace()
    currentFace()

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # # Or instead, use the known face with the smallest distance to the new face
            # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            # best_match_index = np.argmin(face_distances)
            # if matches[best_match_index]:
            #     name = known_face_names[best_match_index]

            face_names.append(name)

            timeRecord = name + ' ' + str(currentTime()) + '\n'

            if not os.path.exists('data/time.txt'):
                open('data/time.txt', 'x')

            file = open('data/time.txt', 'a')
            file.write(timeRecord)
            file.close()

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
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

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()