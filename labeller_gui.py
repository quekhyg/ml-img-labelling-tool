import tkinter as tk

from lib.main_page import *

class LabelGUI:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry('1200x700',)
        self.root.title('Labeller GUI')
        
        self.fonts = {'large':('Arial', 18),'medium':('Arial', 12),'small':('Arial', 10)}
        self.sep = ','
        self.saved = True
        
        self.class_labels_list = [] #List of ClassLabel objects
        self.img_list = [] #List of ImageLabel objects
        
        self.main_page = MainPage(self) #MainPage object
        
        self.label_page_list = [] #List of LabellingPage objects
        self.selected_lps = [] #List of LabellingPage objects that are checkbutton-checked
        
        self.main_page.show()
        
        #####
        
        self.root.mainloop()

if __name__ == '__main__':
    LabelGUI()