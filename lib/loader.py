import tkinter as tk
from tkinter import messagebox, filedialog
import pickle

from lib.image_label import *

def compare(original_iter, new_iter):
    return set(new_iter)-set(original_iter)

class Loader:
    def __init__(self, env):
        self.env = env
        self.create_objs(env.root)
    
    #####
    
    def create_objs(self, parent):
        self.frame = tk.Frame(parent)
        self.title = tk.Label(self.frame, text='Load Labels from File:', font=self.env.fonts['large'])
        self.button = tk.Button(self.frame, command=self.load_file, text='Browse', font=self.env.fonts['medium'])
    
    #####
    
    def load_file(self):
        if not self.env.saved:
            response = tk.messagebox.askyesno('Load Labelled Data from File',
                                              ('Are you sure you want to load labelled data from file? '
                                               'All current unsaved labels will be lost or overwritten.'))
        if self.env.saved or response:
            filename = filedialog.askopenfilename(initialdir=self.env.img_dir.var.get(), title='Select a File')
            if filename:
                with open(filename, 'rb') as f:
                    ffs = pickle.load(f)
                    img_d = pickle.load(f)

                new_labels = compare((cl.var.get() for cl in self.env.class_labels_list), img_d.values())
                new_filenames = compare((il.name for il in self.env.img_list), img_d.keys())
                n = len(new_filenames)
                new_ffs = compare(self.env.ffs.current, ffs)

                if new_ffs:
                    tk.messagebox.showerror('Load Error',
                                            (f'Error: Load file contains unaccepted file types: {list(new_ffs)}. '
                                             'Please accept these file types and reload file.'))
                else:
                    if new_filenames:
                        response_filenames = tk.messagebox.askyesno('Files not Found',
                                                                    ('Warning: Load file contains labelled data for {n} files '
                                                                     'not found in current directory. '
                                                                     f'E.g. {list(new_filenames)[:min(n,3)]}.\nProceed?'))
                    if not new_filenames or response_filenames:
                        if new_labels:
                            response_labels = tk.messagebox.askyesno('Load Warning',
                                                                     (f'Warning: Load file contains new class labels: {new_labels}. '
                                                                      'Proceed to load file and add new class labels?'))
                            if response_labels:
                                for label in new_labels:
                                    self.env.main_frame.add_show_class_label(label)
                        if not new_labels or response_labels:
                            for image_name, class_label_name in img_d.items():
                                existing_cl = [cl for cl in self.env.class_labels_list if cl.name == class_label_name]
                                assert len(existing_cl) == 1, ('Error: There are multiple class labels with the same name. '
                                                               'Please change before proceeding.')
                                for il in self.env.img_list:
                                    if il.name == image_name:
                                        il.cl = existing_cl[0]
                                        il.entry['textvariable'] = il.cl.var
                                        break
                            self.env.main_frame.refresh_img_list()

    #####
    
    def show(self):
        self.frame.pack(pady=10, side=tk.TOP, anchor=tk.W)
        self.title.pack(padx=10, side=tk.LEFT)
        self.button.pack(padx=10, side=tk.LEFT)
        
    def hide(self):
        self.frame.pack_forget()