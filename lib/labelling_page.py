import tkinter as tk
from functools import partial
import pickle

from lib.page import *

class LabellingPage(PageGUI):
    def __init__(self, env, il):
        super().__init__(env)
        self.il = il
        self.class_buttons = []
        self.i = None
        self.ncol = 5
        self.create_objs(self.env.root)
    
    #####
    
    def create_objs(self, parent):
        self.il.create_full_image(parent) #Create label to place full sized photo image
        self.create_fun_buttons(parent) #Creating buttons for previous image, next image, and each possible class label
        self.remove_button = tk.Button(parent, command=partial(self.set_class_label, None),
                                       text='Remove Class Label', font=self.env.fonts['medium']) #Creating button to remove class label
        self.note = tk.Label(parent, text=('Tip: For quicker labelling, '
                                           'you may type the S/N of the class label instead of clicking the button. '
                                           'Left and right arrow keys also move you to the previous and next image respectively.'),
                             font=self.env.fonts['small']) #Text to display on screen to help user
        self.main_menu_button = tk.Button(parent, command=self.back_to_main_menu,
                                          text='Back to Main Menu', font=self.env.fonts['large']) #Creating button to return to main menu
    
    def create_fun_buttons(self, parent):
        self.fun_frame = tk.Frame(parent)
        
        self.back_button = tk.Button(self.fun_frame, command=self.previous_img, text='<<', font=self.env.fonts['large'])
        self.next_button = tk.Button(self.fun_frame, command=self.next_img, text='>>', font=self.env.fonts['large'])
        
        self.btn_frame = tk.Frame(self.fun_frame)
        for i, cl in enumerate(self.env.class_labels_list):
            button = tk.Button(self.btn_frame, command=partial(self.set_class_label, cl),
                               text=cl.var.get(), font=self.env.fonts['medium'])
            if self.il.cl == cl:
                button['bg'] = 'green'
            self.class_buttons.append(button)

    def create_counter_label(self, parent): #Text to display page number
        self.counter_label = tk.Label(parent, text=f'{self.i+1}/{len(self.env.selected_lps)}', font=self.env.fonts['large'])

    def create_binding(self): #Function to enable labelling the images via keypressing in addition to clicking buttons
        self.env.root.bind('<Key>', lambda event: self.key_bind(event))
        self.env.root.bind('<Left>', lambda event: self.previous_img())
        self.env.root.bind('<Right>', lambda event: self.next_img())
    
    #####
    
    def previous_img(self): #Displays previous LabellingPage object
        self.hide()
        if self.i == 0:
            self.env.selected_lps[-1].show()
            self.env.selected_lps[-1].create_binding()
        else:
            self.env.selected_lps[self.i-1].show()
            self.env.selected_lps[self.i-1].create_binding()

    def next_img(self): #Displays next LabellingPage object
        self.hide()
        if self.i == len(self.env.selected_lps)-1:
            self.env.selected_lps[0].show()
            self.env.selected_lps[0].create_binding()
        else:
            self.env.selected_lps[self.i+1].show()
            self.env.selected_lps[self.i+1].create_binding()
    
    def back_to_main_menu(self): #Displays MainPage object
        self.hide()
        self.env.root.unbind('<Key>')
        self.env.root.unbind('<Left>')
        self.env.root.unbind('<Right>')
        for cl in self.env.class_labels_list: #Re-enabling modifications to entries
            cl.label['state'] = tk.NORMAL
        for il in self.env.img_list:
            il.entry['state'] = tk.NORMAL
        self.env.main_page.show()
    
    def set_class_label(self, cl): #Assigns the user-selected class label to the ImageLabel object of this LabellingPage object
        self.il.cl = cl
        self.recolour_buttons()
        if cl is None:
            self.il.entry = tk.Entry(self.il.name_label.master, font=self.env.fonts['small'], justify=tk.CENTER)
        else:
            self.il.entry['textvariable'] = self.il.cl.var
        if self.env.bottom_frame.var.get():
            self.next_img()
    
    def key_bind(self, event): #Enables keypress to perform labelling of the ImageLabel object
        for i, cl in enumerate(self.env.class_labels_list):
            if str(i+1) == event.char:
                self.set_class_label(cl)
                break

    def recolour_buttons(self): #Highlights user-selected class label button
        for button in self.class_buttons:
            if self.il.cl and self.il.cl.name == button['text']:
                button['bg'] = 'green'
            else:
                button['bg'] = self.env.root.cget('bg')

    #####
    
    #In contrast to the main page, since the components of a labelling page do not each have a show method defined, the show and hide methods are redefined for the labelling page here. As such, the widgets attribute is not needed for the labelling page class.
    
    def show(self): #To display all the widgets on this page
        self.counter_label.pack(side=tk.LEFT, anchor=tk.N)
        self.il.full_image.pack(fill=tk.Y, pady=10)
        
        #Filling the frame which contains the buttons for previous image, next image, and labelling the image with a class
        self.fun_frame.pack(fill=tk.X, expand=True, pady=10)
        for i, wt in enumerate([1,5,1]):
            self.fun_frame.columnconfigure(i, weight=wt)
        self.back_button.grid(row=0, column=0, padx=10)
        self.btn_frame.grid(row=0, column=1, padx=10)
        for i in range(self.ncol):
            self.btn_frame.columnconfigure(i, weight=1)
        for i, button in enumerate(self.class_buttons):
            button.grid(row=i//self.ncol, column=i%self.ncol, padx=5, pady=5)
        self.next_button.grid(row=0, column=2, padx=10)
        
        self.remove_button.pack(pady=5)
        self.note.pack(side=tk.BOTTOM, pady=5)
        self.main_menu_button.pack(side=tk.BOTTOM, pady=10)
    
    def hide(self): #To hide all the widgets on this page
        self.counter_label.pack_forget()
        self.il.full_image.pack_forget()
        self.fun_frame.pack_forget()
        self.remove_button.pack_forget()
        self.note.pack_forget()
        self.main_menu_button.pack_forget()