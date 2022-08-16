# Import required libraries
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pprint import pprint

class openImage:
    def __init__(self,frame,imagePath):
        self.frame = frame
        isFile = os.path.isfile(imagePath)
        if isFile:

            # Reset frameView
            for widget in self.frame.winfo_children():
                widget.destroy()
            #self.frame.place(anchor='center', relx=0.5, rely=0.5)

            img = Image.open(imagePath)
            #img.thumbnail((1200,795))
            img = img.resize(size=(1200,795),resample=ImageTk.Image.Resampling.BICUBIC)
            
            # Create an object of tkinter ImageTk
            imgTk = ImageTk.PhotoImage(img)

            # Create a Label Widget to display the text or Image
            label = ttk.Label(self.frame, image = imgTk)
            label.image = imgTk

            label.pack()
        else:
            # TODO Imaage file are not in the files system
            print('Error: Imaage file are not in the files system')
            pass
