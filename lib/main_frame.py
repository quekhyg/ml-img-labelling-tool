import tkinter as tk
from tkinter import messagebox

from lib.class_label import *
from lib.image_label import *

class MainFrame:
    def __init__(self, env):
        self.env = env
    
    #####
    
    def create_objs(self, parent, n=4):
        self.main_frame = tk.Frame(parent)
        self.create_classes_objs(self.main_frame, n)
        self.create_img_objs(self.main_frame)
        self.create_fun_buttons(self.main_frame)
    
    def create_classes_objs(self, parent, n): #Creating table of class labels
        self.classes_frame = tk.Frame(parent)
        self.classes_label = tk.Label(self.classes_frame, text='Class Labels', font=self.env.fonts['large'])
        self.classes_add_button = tk.Button(self.classes_frame, command=self.add_show_class_label,
                                            text='Add Class Label', font=self.env.fonts['medium'])
        self.classes_table = tk.Frame(self.classes_frame, relief=tk.SUNKEN, bd=5)
        self.classes_col_labels = [tk.Label(self.classes_table, text='S/N', font=self.env.fonts['medium']),
                                  tk.Label(self.classes_table, text='Class Label', font=self.env.fonts['medium'])]
        
        for i in range(n):
            self.add_class_label()
    
    def create_img_objs(self, parent): #Creating table of images to be labelled
        self.img_list_frame = tk.Frame(parent)
        self.img_list_label = tk.Label(self.img_list_frame, text='List of Images in Directory', font=self.env.fonts['large'])
        self.img_list_table = tk.Frame(self.img_list_frame, relief=tk.SUNKEN, bd=5)
        self.img_list_col_labels = [tk.Label(self.img_list_table, text='Name', font=self.env.fonts['medium'], anchor=tk.W),
                                    tk.Label(self.img_list_table, text='Thumbnail', font=self.env.fonts['medium']),
                                    tk.Label(self.img_list_table, text='Class Label', font=self.env.fonts['medium'])]
        
        self.env.img_dir.get_files()
        for filename in self.env.img_dir.files:
            self.add_img(filename)

    def create_fun_buttons(self, parent): #Creating buttons for useful functions and counter of number of images selected
        self.funs_frame = tk.Frame(parent)
        self.funs_select_all_btn = tk.Button(self.funs_frame, command=self.select_all,
                                             text='Select All', font=self.env.fonts['medium'])
        self.funs_select_remaining_btn = tk.Button(self.funs_frame, command=self.select_remaining,
                                                   text='Select Remaining', font=self.env.fonts['medium'])
        self.funs_clear_selection_btn = tk.Button(self.funs_frame, command=self.clear_selection,
                                                  text='Clear Selection', font=self.env.fonts['medium'])
        
        self.int_var = tk.IntVar(parent)
        self.counter_label = tk.Label(self.funs_frame, text=f'{self.int_var.get()} Images Selected', font=self.env.fonts['medium'])
    
    #####
    
    def add_class_label(self, name = None): #Adding a new class label to the list
        i = len(self.env.class_labels_list)
        cl = ClassLabel(self.env, name)
        cl.create_objs(i, self.classes_table)
        self.env.class_labels_list.append(cl)
        self.env.saved = False
    
    def add_show_class_label(self, name = None): #Adding a new class label to the list and displaying it
        self.add_class_label(name)
        self.env.class_labels_list[-1].show()
    
    def delete_show_class_labels(self, cl): #Deleting class label from the list and removing it from display
        response = tk.messagebox.askyesno('Delete Class Label',
                                          ('Are you sure you want to delete this class label? '
                                           'All current labels associated with this class will be lost.'))
        if response:
            cl.hide()
            del self.env.class_labels_list[cl.i]
            for cl_later in self.env.class_labels_list[cl.i:]:
                cl_later.hide()
                cl_later.i -= 1
                cl_later.serial['text'] = str(cl_later.i+1)
                cl_later.show()
            
            refresh = False
            for il in self.env.img_list: #Updating images in image list, which were labelled with the class label that was just deleted
                if il.cl == cl:
                    il.hide()
                    il.cl = None
                    il.entry = tk.Entry(il.name_label.master, font=self.env.fonts['small'], justify=tk.CENTER)
                    refresh = True
            if refresh:
                self.refresh_img_list()        
            self.env.saved = False
    
    #####
    
    def add_img(self, name): #Adding a new ImageLabel object to the list
        il = ImageLabel(self.env, name)
        il.create_objs(self.img_list_table)
        self.env.img_list.append(il)
        self.env.saved = False
    
    def add_show_img(self, name): #Adding a new ImageLabel object to the list and updating display
        self.add_img(name)
        self.env.img_list[-1].show()
    
    def delete_img(self, il): #Deleting an ImageLabel object from the list
        il.hide()
        del self.env.img_list[il.i]
        for il_later in self.env.img_list[il.i:]:
            il_later.i -= 1
        self.env.saved = False
    
    def populate_img_list(self): #Updates list of ImageLabel objects with the list of relevant images in current directory
        self.env.img_dir.get_files() #Gets the latest list of relevant image files in the current directory
        existing_files = [il.name for il in self.env.img_list][::-1] #List is reversed to avoid mess when deleting its own elements
        
        for filename, il in zip(existing_files, self.env.img_list[::-1]): #List is reversed to avoid mess...
            if filename not in self.env.img_dir.files: #Deletes an ImageLabel object if its filename is not found in current directory
                self.delete_img(il)

        for filename in self.env.img_dir.files:
            if filename not in existing_files: #Adds an ImageLabel object if filename in current directory but not in current list
                self.add_img(filename)
        
        self.refresh_img_list()
        self.reset_counter()
    
    #####
    
    def select_all(self): #Selects all ImageLabels' checkbuttons
        for il in self.env.img_list:
            il.chkbtn.select()
        self.reset_counter()
    
    def select_remaining(self): #Selects the ImageLabel's checkbuttons if not yet labelled by user, and deselects otherwise
        for il in self.env.img_list:
            if il.cl:
                il.chkbtn.deselect()
            else:
                il.chkbtn.select()
        self.reset_counter()
    
    def clear_selection(self): #Deselects all ImageLabels' checkbuttons
        for il in self.env.img_list:
            il.chkbtn.deselect()
        self.reset_counter()
    
    def reset_counter(self): #Reinitialises counter to the current number of checkbuttons checked
        n = 0
        for il in self.env.img_list:
            if il.var.get():
                n += 1
        self.int_var.set(n)
        self.update_counter_text()
    
    def update_counter(self, var): #Quick update of counter via increment/decrement
        if var.get():
            self.int_var.set(self.int_var.get()+1)
        else:
            self.int_var.set(self.int_var.get()-1)
        self.update_counter_text()
    
    def update_counter_text(self): #Updating text in the counter label
        self.counter_label['text'] = f'{self.int_var.get()} Images Selected'

    #####
    
    def config_main(self, wts=[4,10,1]): #Config settings for main frame
        for i, wt in enumerate(wts):
            self.main_frame.columnconfigure(i, weight=wt)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.grid_propagate(False)
    
    def config_classes(self, wts=[1,4,2]): #Config settings for table of class labels
        for i, wt in enumerate(wts):
            self.classes_table.columnconfigure(i, weight=wt)
        self.classes_table.grid_propagate(False)
    
    def config_img_list(self, wts=[10,2,5,1]): #Config settings for table of images to be labelled
        for i, wt in enumerate(wts):
            self.img_list_table.columnconfigure(i, weight=wt)
        self.img_list_table.grid_propagate(False)
    
    def refresh_img_list(self): #Redisplaying each ImageLabel object in the list
        for i, il in enumerate(self.env.img_list):
            il.i = i
            il.hide()
            il.show()
    
    def show(self):
        ##Main Frame
        self.main_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.config_main()
        
        # Class Label Frame
        self.classes_frame.grid(row=0, column=0, padx=10, sticky='nsew')
        self.classes_label.pack(anchor=tk.W) #Populating classes_frame
        self.classes_add_button.pack(side=tk.BOTTOM)
        self.config_classes()
        
        for i, col_label in enumerate(self.classes_col_labels): #Populating column headers
            col_label.grid(row=0, column=i, sticky=tk.W+tk.E)
        self.classes_table.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        for cl in self.env.class_labels_list: #Populating classes_table
            cl.show()
        
        # Image Label Frame
        self.img_list_frame.grid(row=0, column=1, padx=10, sticky='nsew')
        self.img_list_label.pack(anchor=tk.W)
        self.config_img_list()
        self.img_list_table.pack(expand=True, fill=tk.BOTH, padx=5, ipadx=5)
        
        for i, col_label in enumerate(self.img_list_col_labels):
            col_label.grid(row=0, column=i, sticky=tk.W+tk.E, padx=5 if i==0 else 0)
        self.refresh_img_list()
        
        # Functional Buttons Frame
        self.funs_frame.grid(row=0, column=2, padx=10)
        self.funs_select_all_btn.pack(pady=10)
        self.funs_select_remaining_btn.pack(pady=10)
        self.funs_clear_selection_btn.pack(pady=10)
        self.counter_label.pack(pady=10)
    
    def hide(self):
        self.main_frame.pack_forget()