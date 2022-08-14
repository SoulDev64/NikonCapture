# Import required libraries
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pprint import pprint

class openImage:
    def __init__(self,master,imagePath):
        self.master = master
        isFile = os.path.isfile(imagePath)
        if isFile:
            frame = ttk.Frame(self.master, width=1200, height=795)
            frame.pack()

            frame.place(anchor='center', relx=0.5, rely=0.5)

            img = Image.open(imagePath)
            #img.thumbnail((1200,795))
            img = img.resize(size=(1200,795),resample=ImageTk.Image.Resampling.BICUBIC)
            
            # Create an object of tkinter ImageTk
            imgTk = ImageTk.PhotoImage(img)

            # Create a Label Widget to display the text or Image
            label = ttk.Label(frame, image = imgTk)
            label.image = imgTk

            label.pack()
        else:
            # TODO Imaage file are not in the files system
            print('Error: Imaage file are not in the files system')
            pass
