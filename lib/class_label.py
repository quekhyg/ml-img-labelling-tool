import tkinter as tk
from tkinter import messagebox
from functools import partial

class ClassLabel:
    count = 0
    def __init__(self, env, name = None):
        ClassLabel.count += 1
        self.env = env
        self.name = name if name else f'ClassLabel{ClassLabel.count}'
        self.serial, self.label, self.delbtn = None, None, None
    
    def __str__(self):
        if self.serial:
            s = self.serial['text']
            return f'Class Label {s}: {self.name}'
        else:
            return f'Class Label: {self.name}'
    
    ######
    
    def create_objs(self, i, parent):
        self.i = i
        self.serial = tk.Label(parent, text=str(i+1), font=self.env.fonts['small'])
        self.var = tk.StringVar(parent, value=self.name)
        self.var.trace_add('write', self.rename)
        self.label = tk.Entry(parent, textvariable=self.var,
                              font=self.env.fonts['small'], justify=tk.CENTER)
        self.delbtn = tk.Button(parent, command=partial(self.env.main_frame.delete_show_class_labels, self),
                                text='Delete', font=self.env.fonts['small'])
    
    #####
    
    def rename(self, var, index, mode): #Checks that user changes to the class label name does not cause errors
        if self.env.sep in self.var.get():
            tk.messagebox.showerror('Class Label Error',
                                    f'Error: Class label cannot contain \'{self.env.sep}\'!')
            self.var.set(self.name)
        else:
            if self.var.get() in [cl.var.get() for cl in self.env.class_labels_list if cl is not self]:
                tk.messagebox.showwarning('Class Label Warning',
                                          ('Class label already exists. '
                                           'Please choose a unique class name, '
                                           'otherwise loading and saving data may be corrupted.'))
            self.name = self.var.get()
            self.env.saved = False
    
    #####
    
    def validate(self):
        assert self.serial, f'Error: Serial number label widget not created for this class label ({self.name}) yet'
        assert self.label, f'Error: Entry widget not created for this class label ({self.name}) yet'
        assert self.delbtn, f'Error: Delete button widget not created for this class label ({self.name}) yet'
    
    #####
    
    def show(self, offset=1, sticky=tk.W+tk.E):
        self.validate()
        self.serial.grid(row=self.i+offset, column=0, sticky=sticky)
        self.label.grid(row=self.i+offset, column=1, sticky=sticky)
        self.delbtn.grid(row=self.i+offset, column=2, sticky=sticky)
    
    def hide(self):
        self.validate()
        self.serial.grid_remove()
        self.label.grid_remove()
        self.delbtn.grid_remove()