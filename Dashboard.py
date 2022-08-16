import os
import io
import time

from pprint import pprint

import gphoto2 as gp

from PIL import ImageTk, Image

from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo

from ConfigurationUX import *
from OpenImage import *
from Preview import *

'''
Main window for the App aka TheLauncher
'''

class Dashboard:

    def __init__(self,master,camera) -> None:
        self.master = master
        self.camera = camera
        self.preview = False
        self.initUX()
        pass

    def initUX(self):

        self.frame = tk.Frame(self.master)
        
        self.button0 = tk.Button(self.frame, text = 'Preview', width = 20, command = self.capturePreviewStart)
        self.button0.pack()
        
        self.button1 = tk.Button(self.frame, text = 'Capture', width = 20, command = self.captureImage)
        self.button1.pack()

        self.button2 = tk.Button(self.frame, text = 'Edit option', width = 20, command = self.editOption)
        self.button2.pack()

        # TODO Make a clean exit (ex.: exit camera before)
        self.button3 = tk.Button(self.frame, text = 'Exit', width = 20, command = lambda: self.master.destroy())
        self.button3.pack()
        
        self.frameView = tk.Frame(self.master)
        self.frameView.pack(side="top", fill="x")

        self.canvas= Canvas(self.frameView, width= 600, height= 400)
        self.canvas.pack()

        self.preview = Preview(self.camera,self.canvas)

        self.frame.pack()
        #self.editOption({})
        pass

    def editOption(self):
        self.editWindow = tk.Toplevel(self.master)
        self.editWindow.title("NikonCapture # CONFIGURATOR")
        self.editWindow.geometry('1200x700')
        self.configApp = ConfigurationUX(self.editWindow,self.camera)

    def capturePreviewStart(self):
        self.preview.start()
        pass

    def capturePreviewStop(self):
        self.preview.stop()
        pass

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
            print(target)
            
            openImage(self.frameView,target)

            self.camera.exit()
            time.sleep(1)
            self.camera.init()

        except:
            showinfo(title='Error', message='Error capturing')
        return 0
        