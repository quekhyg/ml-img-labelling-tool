class PageGUI:
    def __init__(self, env):
        self.env = env
        self.widgets = []
 
    def show(self):
        for widget in self.widgets:
            widget.show()
        
    def hide(self):
        for widget in self.widgets:
            widget.hide()