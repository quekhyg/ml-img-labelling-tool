from lib.image_dir import *
from lib.file_format import *
from lib.loader import Loader
from lib.main_frame import *
from lib.bottom_frame import *

class MainPage(PageGUI):
    def __init__(self, env):
        super().__init__(env)
                
        self.env.img_dir = ImageDirectory(self.env)
        self.env.ffs = FileFormats(self.env)
        self.env.loader = Loader(self.env)
        self.env.main_frame = MainFrame(self.env)
        self.env.bottom_frame = BottomFrame(self.env)
        
        self.env.main_frame.create_objs(self.env.root)
        
        self.widgets = [self.env.img_dir, self.env.ffs, self.env.loader, self.env.main_frame, self.env.bottom_frame]