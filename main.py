# -----------------------------------------------------------------------------
# Name:        INFRAA — Intelligent Face Recognition based Attendance Application
#
# Purpose:     This project is an application of face detecting technology, where
#              a program detects students’ faces and records their presence. The
#              recorded data is presented to the teachers through a graphic user
#              interface in order to efficiently deliver the information.
#
# Author:      Lyn Jeong
# Created:     05-May-2022
# Updated:     02-Jun-2022
# -----------------------------------------------------------------------------
# I think this project deserves a level 4+ because it demonstrates all of the level
# 4 criteria along with many extra features and implementations to improve the program.
# INFRAA also implements a real world problem / situation and applies the knowledge learned
# in the course to connect it back to my own interests and ideas.
#
# Features Added:
#   - facial detection
#       -> face detection based program
#       -> detects the face, records the time and presence in a file
#       -> on the detecting screen, a box is drawn with names to specify who was detected
#   - threading
#       -> runs two scripts in parallel to have easier / better user experience
#       -> efficiently divides jobs for each scripts
#   - file manipulations
#       -> dynamically read/write/store data to display the information
#       -> also use it to communicate between two scripts
#   - adding new student
#       -> new students can be added to the attendance program with just one picture
#   - dynamic buttons / collision detection
#       -> all the buttons react when they are hovered and are interactive
#   - detailed help menus
#       -> very detailed and user friendly help menus and instructions
#   - animations
#       -> moving main screen (changing images)
#       -> moving loading screen
#   - page controls
#       -> page controlled by buttons and keyboards
#       -> page number also shown
#   - user friendly interface
#       -> colour themed and layouted to be simple and eye catching
#       -> appealing looks
#   - clear program states
#       -> various states dividing out different screens
#   - effective use of loops
#       -> effectively used for loops especially for displaying the images
#   - created custom functions
#       -> created many custom functions that are used throughout the program
#   - finds default webcam
#       -> finds a default webcam that would be used for the detector
#       -> from camera 0, finds the camera number that suits the program
# -----------------------------------------------------------------------------
# Copy Rights & Credits:
#   - IMG
#       -> https://www.freepik.com/free-photo/be-focus-patient-while-teaching-new-things_13133035.htm
#           Freepik License | @gpointstudio
#       -> https://www.freepik.com/free-photo/red-shirt-group-people-business-conference-modern-classroom-daytime_9694506.htm
#           Freepik License | @standret
#       -> https://www.freepik.com/free-photo/group-young-people-sitting-conference-together_9341662.htm
#           Freepik License | @mego-studio
#   - FONT
#       -> https://www.dafont.com/made-tommy.font
#           Dafont License | @MadeType
# -----------------------------------------------------------------------------
from threading import Thread
import subprocess

# Threading to run two files in parallel
# https://stackoverflow.com/questions/60001867
t1 = Thread(target=subprocess.call, args=(["python3", "detector.py"],))
t2 = Thread(target=subprocess.call, args=(["python3", "interface.py"],))

t1.start()
t2.start()

t1.join()
t2.join()
