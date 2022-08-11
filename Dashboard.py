from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import gphoto2 as gp
from pprint import pprint
from ConfigurationUX import *
import os
#from Capture import *


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
        
        self.button1 = tk.Button(self.frame, text = 'Capture', width = 50, command = self.capture_image)
        self.button1.pack()

        self.button2 = tk.Button(self.frame, text = 'Edit option', width = 50, command = self.editOption)
        self.button2.pack()
        
        self.frame.pack()

        #self.editOption({})
        pass

    def editOption(self):
        self.editWindow = tk.Toplevel(self.master)
        self.editWindow.title("AStrophoto # NikonCapture # CONFIGURATOR")
        self.editWindow.geometry('1200x700')
        self.configApp = ConfigurationUX(self.editWindow,self.camera)

    def capture_image(self):
        print('Capturing image')
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join('/tmp', file_path.name)
        print('Copying image to', target)
        camera_file = self.camera.file_get(
            file_path.folder, 
            file_path.name, 
            gp.GP_FILE_TYPE_NORMAL
        )
        camera_file.save(target)
        return 0