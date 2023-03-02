import tkinter as tk
from functools import partial

class FileFormats:
    def __init__(self, env, options=['png','jpg','gif']):
        self.env = env
        self.current = []
        self.options = options
        self.create_objs(env.root)
    
    #####
    
    def create_objs(self, parent, s='Accepted File Types:'):
        self.ff_frame = tk.Frame(parent)
        self.title = tk.Label(self.ff_frame, text='Accepted File Types:', font=self.env.fonts['large'])
        self.create_chkbtns(self.ff_frame)
    
    def create_chkbtns(self, parent):
        self.frame = tk.Frame(parent)
        self.chkbtns = {}
        self.vars = {}
        for option in self.options:
            var = tk.BooleanVar(parent)
            self.vars[option] = var
            self.chkbtns[option] = tk.Checkbutton(self.frame, variable=var,
                                                  command=partial(self.update_file_format, var),
                                                  text=option, font=self.env.fonts['medium'])

    #####
    
    def get_options(self): #Gets list of allowed fileformats
        self.current = [k for k, v in self.vars.items() if v.get()]
    
    def update_file_format(self, var): #Updates list of ImageLabel objects whenever the allowable fileformats are updated
        if var.get():
            self.get_options()
            self.env.main_frame.populate_img_list()
        else:
            response = tk.messagebox.askyesno('Uncheck File Format',
                                              ('Are you sure you want to uncheck this file format? '
                                               'All current unsaved changes associated with files with this format will be lost.'))
            if response:
                self.get_options()
                self.env.main_frame.populate_img_list()
            else:
                var.set(True)
    
    #####
    
    def show(self):
        self.ff_frame.pack(pady=10, side=tk.TOP, anchor=tk.W)
        self.title.pack(padx=10, side=tk.LEFT)
        self.frame.pack(padx=10, side=tk.LEFT)
        for i, chkbtn in enumerate(self.chkbtns.values()): #To display the checkbuttons within the frame
            chkbtn.grid(row=0, column=i)
    
    def hide(self):
        self.ff_frame.pack_forget()