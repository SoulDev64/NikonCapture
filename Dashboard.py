import os
import time
from pprint import pprint
import gphoto2 as gp
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from ConfigurationUX import *
from OpenImage import *

'''
Main window for the App aka TheLauncher
'''

class Dashboard:

    def __init__(self,master,camera) -> None:
        self.master = master
        self.camera = camera
        self.initUX()
        pass

    def initUX(self):

        self.frame = tk.Frame(self.master)
        
        self.button1 = tk.Button(self.frame, text = 'Capture', width = 50, command = self.captureImage)
        self.button1.pack()

        self.button2 = tk.Button(self.frame, text = 'Edit option', width = 50, command = self.editOption)
        self.button2.pack()

        # TODO Make a clean exit (ex.: exit camera before)
        self.button3 = tk.Button(self.frame, text = 'Exit', width = 50, command = lambda: self.master.destroy())
        self.button3.pack()
        
        self.frame.pack()

        #self.editOption({})
        pass

    def editOption(self):
        self.editWindow = tk.Toplevel(self.master)
        self.editWindow.title("NikonCapture # CONFIGURATOR")
        self.editWindow.geometry('1200x700')
        self.configApp = ConfigurationUX(self.editWindow,self.camera)

    def captureImage(self):
        
        try:
            file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            target = os.path.join('/tmp', file_path.name)
            
            camera_file = self.camera.file_get(
                file_path.folder, 
                file_path.name, 
                gp.GP_FILE_TYPE_NORMAL
            )
            camera_file.save(target)
            
            self.showCapture(target)
        except:
            showinfo(title='Error', message='Error capturing')
        return 0

    def showCapture(self,imagePath):
        # New window
        self.showWindow = tk.Toplevel(self.master)
        self.showWindow.title("NikonCapture # VIEW")
        self.showWindow.geometry('1200x800')
        # Load image
        showImg = openImage(self.showWindow,imagePath)
        