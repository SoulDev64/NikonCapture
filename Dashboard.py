import os
import io
import time

from datetime import datetime

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
        self.captureBaseFileName = "capture_"

        self.initUX()
        self.fixGrid()

        self.getSummary()
        self.capturePreviewStart()

    def initUX(self):

        self.frame = tk.Frame(self.master)
        #self.frame.configure(bg='black')
        
        self.button0 = tk.Button(self.frame, text = 'Preview', width = 20, command = self.capturePreviewStart)
        self.button1 = tk.Button(self.frame, text = 'Capture', width = 20, command = self.captureImage, bg='red')
        self.button2 = tk.Button(self.frame, text = 'Edit option', width = 20, command = self.editOption)
        self.button3 = tk.Button(self.frame, text = 'Exit', width = 20, command = lambda: self.master.destroy())# TODO Make a clean exit (ex.: exit camera before)
        
        # Summary infos
        self.frameSummary = tk.Frame(self.frame)
        self.summary = tk.Text(self.frameSummary)
        scroll = tk.Scrollbar(self.frameSummary)
        self.summary.configure(yscrollcommand=scroll.set)
        self.summary.pack(side=tk.LEFT)
        
        scroll.config(command=self.summary.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # For view the last capture image
        self.frameView = Canvas(self.frame, width= 1200, height= 795) # TODO Set relative size
        # self.frameView.configure(bg='black')
        # For view the capture preview image (liveview)
        self.canvas= Canvas(self.frame, width= 600, height= 400)
        # self.canvas.configure(bg='black')

        self.preview = Preview(self.camera,self.canvas)

    '''
    Set position of each widget in the content grid
    '''
    def fixGrid(self):

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Global frame
        self.frame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=2)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.rowconfigure(4, weight=0)
        self.frame.rowconfigure(5, weight=0)

        # Canvas Capture View
        self.frameView.grid(column=1, row=0, rowspan=5, sticky=(N, S, E, W))
        # Canvas Preview
        self.canvas.grid(column=0, row=0, sticky=(N, E, W))
        # BT Preview
        self.button0.grid(column=0, row=1, sticky=(N, E, W))
        # BT Capture
        self.button1.grid(column=0, row=2, sticky=(N, E, W))
        # Summary
        self.frameSummary.grid(column=0, row=3, sticky=(N, E, W))
        # BT Options
        self.button2.grid(column=0, row=4, sticky=(N, E, W))
        # BT Exit
        self.button3.grid(column=0, row=5, sticky=(S, E, W))
    
    def getSummary(self):
        try:
            text = self.camera.get_summary()
            print('Summary')
            print('=======')
            self.summary.insert(tk.END, str(text))
            pprint(text)
        except Exception as ex:
            print(str(ex))

    def editOption(self):
        self.editWindow = tk.Toplevel(self.master)
        self.editWindow.title("NikonCapture # CONFIGURATOR")
        self.editWindow.geometry('1200x700')
        self.configApp = ConfigurationUX(self,self.editWindow,self.camera)

    def capturePreviewStart(self):
        self.preview.start()
        pass

    def capturePreviewStop(self):
        self.preview.stop()
        pass

    def captureImage(self):
        
        try:
            file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)

            target = os.path.join('captures', self.getCaptureFileName())
            
            camera_file = self.camera.file_get(
                file_path.folder, 
                file_path.name, 
                gp.GP_FILE_TYPE_NORMAL
            )
            
            camera_file.save(target)
            print(target)
            
            openImage(self.frameView,target)

            '''self.camera.exit()
            time.sleep(1)
            self.camera.init()'''

        except:
            showinfo(title='Error', message='Error capturing')
        return 0
        
    def getCaptureFileName(self):
        now = datetime.now()
        strName = now.strftime('%Y%m%d_%H-%M-%S.jpg')
        return self.captureBaseFileName + strName