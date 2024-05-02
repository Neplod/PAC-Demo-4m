import customtkinter as ctk

class APP(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color = '#dedede')
        self.grid_columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.ins = ctk.CTkTextbox(self, text_color = "black", fg_color = "transparent", height = 2000, font = ctk.CTkFont('arial', size = 15))
        self.ins.insert("0.0", 'Consequat consectetur est ea commodo quis in id consectetur exercitation ipsum minim dolor. Qui aliqua magna pariatur velit occaecat proident elit incididunt. Nulla qui tempor sit incididunt labore elit ullamco enim adipisicing ea reprehenderit magna est in. Veniam laboris sint adipisicing eu labore. Qui do velit consectetur dolore. Tempor et qui adipisicing do irure. Excepteur ipsum culpa enim aute. Incididunt anim eu enim pariatur cillum nisi et sunt culpa minim. Esse sint cupidatat incididunt cillum occaecat commodo qui laborum minim proident eu. Commodo irure aute nulla ea ad in id elit eiusmod mollit ipsum. Aute esse do Lorem ex Lorem laboris est aliqua velit esse enim ad anim. Eu aliquip sit sunt consectetur cillum consectetur sint officia in exercitation dolor cillum. Id esse aute voluptate anim nisi minim aliquip voluptate commodo consectetur cupidatat. Sunt cillum voluptate elit irure id officia commodo aliqua est sint officia elit laborum qui. Incididunt enim reprehenderit Lorem ex exercitation adipisicing incididunt do cillum incididunt. Magna pariatur cillum laborum pariatur ex fugiat. Culpa sit nostrud laboris in irure officia eu pariatur consequat eu consectetur. Lorem ex ea irure voluptate. Et enim sit nostrud qui et. Amet sint ad enim excepteur nulla sint sint. Labore non nulla enim irure nisi qui.')
        self.ins.configure(state= "disabled")
        self.ins.grid(row=0, column=0, padx=5, pady=5, sticky = "NESW")

def initialize() -> list[ctk.CTkFrame, dict]:
    return [APP, {'a':''}]