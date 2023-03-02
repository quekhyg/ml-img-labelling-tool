import os
import tkinter as tk
from tkinter import messagebox, filedialog

class ImageDirectory:
    def __init__(self, env):
        self.env = env
        self.create_objs(env.root)
        
    #####
    
    def create_objs(self, parent): #Creates widgets pertaining to the directory of images to be labelled
        self.frame = tk.Frame(parent)
        self.var = tk.StringVar(parent, value=os.getcwd().replace('\\','/'))
        self.title = tk.Label(self.frame, text='Current Directory: ', font=self.env.fonts['large'])
        self.label = tk.Label(self.frame, textvariable=self.var, font=self.env.fonts['medium'])
        self.button = tk.Button(self.frame, command=self.select_dir,
                                text='Change Directory', font=self.env.fonts['medium'])
    
    def get_files(self): #Gets a list of filenames with the correct file format in current directory, and stores it in self.files
        filenames = []
        for ff in self.env.ffs.current:
            filenames += [file for file in os.listdir() if file.endswith(ff)]
        self.files = filenames
    
    #####
    
    def select_dir(self): #Changes current directory to user-selected directory
        if not self.env.saved:
            response = tk.messagebox.askyesno('Change Directory',
                                              ('Are you sure you want to change directory? '
                                               'All current unsaved changes will be lost.'))
        if self.env.saved or response:
            new_dir = filedialog.askdirectory(initialdir=self.var.get(), title='Select a Folder')
            if new_dir:
                self.var.set(new_dir)
                os.chdir(new_dir)
                self.env.main_frame.populate_img_list()

    #####

    def show(self):
        self.frame.pack(pady=10, side=tk.TOP, anchor=tk.W)
        self.title.pack(padx=10, side=tk.LEFT)
        self.label.pack(padx=10, side=tk.LEFT)
        self.button.pack(padx=10, side=tk.RIGHT)
    
    def hide(self):
        self.frame.pack_forget()