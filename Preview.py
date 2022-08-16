import os
import io
import time
import threading
from pprint import pprint
import gphoto2 as gp
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from ConfigurationUX import *
from OpenImage import *

class Preview:

    def __init__(self,camera,previewCanvas):
        self.__camera = camera
        self.__canvas = previewCanvas
        self.__preview = False
        #self.__threadTimer = th.Timer(1.0, self.capture) #0.04

    def setInterval(interval, times = -1):
        # This will be the actual decorator,
        # with fixed interval and times parameter
        def outer_wrap(function):
            # This will be the function to be
            # called
            def wrap(*args, **kwargs):
                stop = threading.Event()

                # This is another function to be executed
                # in a different thread to simulate setInterval
                def inner_wrap():
                    i = 0
                    while i != times and not stop.isSet():
                        stop.wait(interval)
                        function(*args, **kwargs)
                        i += 1

                t = threading.Timer(0, inner_wrap)
                t.daemon = True
                t.start()
                return stop
            return wrap
        return outer_wrap

    @setInterval(0.04)
    def capture(self):
        if self.__preview == True:
            # Start camera preview
            camera_file = self.__camera.capture_preview()
            
            file_data = camera_file.get_data_and_size()

            # display image
            data = memoryview(file_data)
            imgTk = ImageTk.PhotoImage(data=data)
            self.__canvas.create_image(10,10,anchor=NW,image=imgTk)
            self.__canvas.image = imgTk

    def start(self):
        if self.__preview == False:
            self.__preview = True
            self.stop = self.capture()

        else:
            self.__preview = False
            self.stop.set()
            # TODO Stop capture preview

    def stop(self):

        pass