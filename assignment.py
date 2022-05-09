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
# Updated:
# -----------------------------------------------------------------------------
# I think this project deserves a level XXXXXX because ...
#
# Features Added:
#   ...
#   ...
#   ...
# -----------------------------------------------------------------------------
from threading import Thread
import subprocess

# Threading to run two files in parallel
# https://stackoverflow.com/questions/60001867
t1 = Thread(target=subprocess.run, args=(["python", "detector.py"],))
t2 = Thread(target=subprocess.run, args=(["python", "interface.py"],))

t1.start()
t2.start()

t1.join()
t2.join()
