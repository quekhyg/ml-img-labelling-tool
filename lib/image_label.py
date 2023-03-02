import tkinter as tk
from PIL import Image, ImageTk
from functools import partial

class ImageLabel:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.image = Image.open(name)
        self.i, self.cl = None, None #cl should be an object of the ClassLabel class
    
    def __str__(self):
        if self.i:
            return f'Image Label {self.i}: {self.name}'
        else:
            return f'Image Label: {self.name}'
        
    #####
    
    def create_objs(self, parent):
        self.name_label = tk.Label(parent, text=self.name, font=self.env.fonts['small'])
        self.thumbnail = self.create_image(parent, size=(40,40))
        self.create_entry(parent)
        self.var = tk.BooleanVar(parent)
        self.chkbtn = tk.Checkbutton(parent, variable=self.var, command=partial(self.env.main_frame.update_counter, self.var))
    
    def create_entry(self, parent):
        if self.cl:
            assert self.cl.var, (f'Error in creating entry widget for {self.name}: '
                                         f'String variable not created for associated class label ({self.cl.name}) yet')
            self.entry = tk.Entry(parent, textvariable=self.cl.var,
                                  font=self.env.fonts['small'], justify=tk.CENTER)
        else:
            self.entry = tk.Entry(parent, font=self.env.fonts['small'], justify=tk.CENTER)

    #####
    
    def create_full_image(self, parent, size=(600,400)):
        self.full_image = self.create_image(parent, size)
    
    #####
    
    def create_image(self, parent, size):
        resize_factor = max(self.image.width/size[0], self.image.height/size[1])
        wd = int(self.image.width/resize_factor)
        ht = int(self.image.height/resize_factor)
        photo_image = ImageTk.PhotoImage(self.image.resize((wd, ht))) #returns a resized photo image
        
        img = tk.Label(parent)
        img.image = photo_image
        img.configure(image=photo_image)

        return img

    #####
    
    def validate(self):
        assert self.name_label, f'Error: Filename label widget not created for this file ({self.name}) yet'
        assert self.thumbnail, f'Error: Thumbnail label widget not created for this file ({self.name}) yet'
        assert self.entry, f'Error: Entry widget for class label not created for this file ({self.name}) yet'
        assert self.chkbtn, f'Error: Checkbutton widget not created for this file ({self.name}) yet'
        #assert self.i, f'Error: Serial number not assigned to this file ({self.name}) yet'

    #####
    
    def show(self, offset=1, sticky=tk.W+tk.E):
        self.validate()
        self.name_label.grid(row=self.i+offset, column=0, sticky=tk.W)
        self.thumbnail.grid(row=self.i+offset, column=1, sticky=sticky)
        self.entry.grid(row=self.i+offset, column=2, sticky=sticky)
        self.chkbtn.grid(row=self.i+offset, column=3, sticky=sticky)
    
    def hide(self):
        self.validate()
        self.name_label.grid_remove()
        self.thumbnail.grid_remove()
        self.entry.grid_remove()
        self.chkbtn.grid_remove()