import customtkinter as ctk

class APP(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color = '#dedede')
        self.label = ctk.CTkLabel(self, text = 'Hi, everyone', text_color = '#000000')
        self.label.grid(column = 1, row = 1)
    
def initialize() -> list[ctk.CTkFrame, dict]:
    return [APP, {'a':''}]