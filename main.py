import datetime
import pyautogui
from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from Screen_Recorder import Ui_Screen_Recorder
import sys
import win32gui, win32con
import time
import os

Minimize = win32gui.GetForegroundWindow()

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)


time_stamp = datetime.datetime.now().strftime('%A_%d-%b-%Y %I-%M %p')    
                                                        # %A for fullname weekday
                                                        # %d for date with prefix zero
                                                        # %b for small month name
                                                        # %Y for year
                                                        # %I for hour
                                                        # %M for minute
                                                        # %p for am/pm

directory = 'Screen Record'
parent = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Videos')

path = os.path.join(parent, directory)

try:
    os.mkdir(path)
except Exception as e:
    pass

def minimizeWindow():
    window = win32gui.FindWindow(None, "Screen Recorder")
    win32gui.ShowWindow(window,win32con.SW_MINIMIZE)


file_name = f'{path}\{time_stamp}.mp4'

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
captured_video = cv2.VideoWriter(file_name, fourcc, 30.0, (width, height))


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()


    def run(self):
        self.task_execution()


    def task_execution(self):

        self.minimized = False
        while True:
            img = ImageGrab.grab(bbox =(0, 0, width, height))
            img_np = np.array(img)
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            captured_video.write(img_final)
            cv2.imshow('Screen Recorder', img_final)

            if self.minimized:
                pass
            else:
                self.minimized = not self.minimized
                minimizeWindow()

            if cv2.waitKey(1) == ord('q'):
                break
        # When everything done, release the video capture object
        captured_video.release()
        
        # Closes all the frames
        cv2.destroyAllWindows()

startexecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Toggle = True
        self.tog = True
        self.ui = Ui_Screen_Recorder()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.endTask)
        self.ui.pushButton_3.clicked.connect(self.close)

    def startTask(self):
        if self.Toggle:
            self.ui.movie = QtGui.QMovie("recording-gif.gif")
            self.ui.label.setMovie(self.ui.movie)
            self.ui.movie.start()

            startexecution.start()
            self.Toggle = not self.Toggle

    def endTask(self):
        if not self.Toggle:
            
            window = win32gui.FindWindow(None, "Screen Recorder")
            win32gui.ShowWindow(window,win32con.SW_MAXIMIZE)
            pyautogui.keyDown('q')
            pyautogui.keyUp('q')
            self.Toggle = not self.Toggle
            time.sleep(1.5)
            sys.exit()
        
#-------------------------------------------------------------------------------------------------#

app = QApplication(sys.argv)
Screen_Recorder = Main()
Screen_Recorder.show()
time.sleep(1.5)
win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
sys.exit(app.exec_())