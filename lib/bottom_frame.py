import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
from lib.labelling_page import *

class BottomFrame:
    def __init__(self, env):
        self.env = env
        self.create_objs(env.root)
    
    #####
    
    def create_objs(self, parent):
        self.bottom_frame = tk.Frame(parent)
        self.save_button = tk.Button(self.bottom_frame, command=self.save,
                                     text='Save Changes to File', font=self.env.fonts['large'])
        self.label_button = tk.Button(self.bottom_frame, command=self.start_labelling,
                                      text='Start Labelling!', font=self.env.fonts['large'])
        self.var = tk.BooleanVar(self.bottom_frame)
        self.auto_chkbtn = tk.Checkbutton(self.bottom_frame, variable=self.var,
                                          text='Fast Mode', font=self.env.fonts['medium'])

    #####
    
    def save(self):
        if self.env.saved:
            tk.messagebox.showinfo('Save Data',
                                   'There are no changes to be saved')
        else:
            img_d = {il.name: il.cl.var.get() for il in self.env.img_list if il.cl}
            if not img_d:
                response = tk.messagebox.askyesno('Save Data',
                                                  'Warning: There are no images labelled, proceed?')
            if img_d or response:
                filename = tk.filedialog.asksaveasfilename()
                if filename:                
                    with open(filename, 'wb') as f:
                        pickle.dump(self.env.ffs.current, f)
                        pickle.dump(img_d, f)
                    self.env.saved = True
    
    def start_labelling(self): #Reinitialises all LabellingPage objects with latest information from main menu
        for lp in self.env.label_page_list:
            del lp
        self.env.label_page_list = [LabellingPage(self.env, il) for il in self.env.img_list]
        self.env.selected_lps = [lp for lp in self.env.label_page_list if lp.il.var.get()]
        
        for i, lp in enumerate(self.env.selected_lps): #To provide page numbers
            lp.i = i
            lp.create_counter_label(self.env.root)
        
        for cl in self.env.class_labels_list: #Disabling modifications to entries
            cl.label['state'] = tk.DISABLED
        for il in self.env.img_list:
            il.entry['state'] = tk.DISABLED
        
        if self.env.selected_lps:
            self.env.main_page.hide()
            self.env.selected_lps[0].show() #Starting the user labelling process with the first selected image
            self.env.selected_lps[0].create_binding()
    
    #####

    def show(self):
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=20)
        for i, wt in enumerate([3,3,1]):
            self.bottom_frame.columnconfigure(i, weight=wt)
        
        self.save_button.grid(row=0, column=0)
        self.label_button.grid(row=0, column=1, sticky=tk.E)
        self.auto_chkbtn.grid(row=0, column=2, sticky=tk.W, padx=5)
    
    def hide(self):
        self.bottom_frame.pack_forget()