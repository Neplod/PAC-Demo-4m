import customtkinter
from skills.skill_manager import Skill, get_all_skills
from plugins.plugin_manager import Plugin, get_all_plugins
from functions import PrivateFunctions
import os
from PIL import Image
from main_ap import MainAP
from clients.manager import get_library_data as lib_clients
from threading import Thread
import sys
import time

class SideBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        self.__app = None
        self.grid(row=0, column=0, sticky="nsew")

        self.home_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "home_ico.png")), size=(30, 30))

        self.label = customtkinter.CTkLabel(self, text="PAC",
                                            compound="left", font=customtkinter.CTkFont(family = 'Ubuntu', size=30, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self, corner_radius=5, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_homemenu)
        self.home_button.grid(row=1, column=0, padx=20, pady=10)
        self.skill_button = customtkinter.CTkButton(self, corner_radius=5, height=40, border_spacing=10, text="Skill",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_skillmenu)
        self.skill_button.grid(row=2, column=0, padx=20, pady=10)
        self.plugin_button = customtkinter.CTkButton(self, corner_radius=5, height=40, border_spacing=10, text="Plugin",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_pluginmenu)
        self.plugin_button.grid(row=3, column=0, padx=20, pady=10)
        self.ap_button = customtkinter.CTkButton(self, corner_radius=5, height=40, border_spacing=10, text="Personal Assistant",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_apmenu)
        self.ap_button.grid(row=4, column=0, padx=20, pady=10)
        self.clients_button = customtkinter.CTkButton(self, corner_radius=5, height=40, border_spacing=10, text="Clients",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_clientsmenu)
        self.clients_button.grid(row=5, column=0, padx=20, pady=10)
        self.restartpa_button = customtkinter.CTkButton(self, corner_radius = 5, height = 40, border_spacing = 10 , text = "Restart PA", fg_color = "transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command = master.restart_pa)
        self.restartpa_button.grid(row = 6, column = 0, padx = 20, pady = 10)

class HomeMenu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.title = customtkinter.CTkLabel(self, text = "Personal Assistant Creator", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky = "W")
        self.insf = customtkinter.CTkFrame(self)
        self.insf.grid_columnconfigure(0, weight = 1)
        f = open('./instructions.txt', 'r')
        i = f.readlines()
        f.close()
        self.ins = customtkinter.CTkTextbox(self.insf, fg_color = "transparent", height = 2000, font = customtkinter.CTkFont('arial', size = 15))
        self.ins.insert("0.0", ''.join(i))
        self.ins.configure(state= "disabled")
        self.ins.grid(row=0, column=0, padx=5, pady=5, sticky = "NESW")
        self.insf.grid(row = 1, column = 0, padx = 30, pady = (10,10), sticky = "NESW")

class SkillMenu(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.save_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "save_ico.png")), size=(30, 30))
        self.export_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "export_ico.png")), size=(30, 30))
        self.delete_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "delete_ico.png")), size=(30, 30))
        self.grid_columnconfigure(0, weight = 1)
        self.label = customtkinter.CTkLabel(self, text="Personal Assistant Skills", compound="left", anchor = "w", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky = "W")
        _skills: list[Skill] = get_all_skills()
        self.skills: list[SkillFrame] = []
        for i, skill in enumerate(_skills):
            self.skills.append(SkillFrame(self, skill.name, '\n'.join(skill.commands), skill.code, True, skill, i))
            self.skills[-1].grid(column = 0, row = i+1, padx = 30, pady = 10, sticky = "EW")
        
        self.more = customtkinter.CTkFrame(self)
        self.more.grid_columnconfigure(2, weight = 1)

        self.more_addbtn = customtkinter.CTkButton(self.more, text = "Add Skill", command = self.newskill)
        self.more_addbtn.grid(column = 0, row = 0, columnspan = 2, padx=10, pady=(10, 10), sticky = "WE")

        self.more_lib = customtkinter.StringVar(self.more, "", "libi")
        self.more_libe = customtkinter.CTkEntry(self.more, textvariable = self.more_lib)
        self.more_libb = customtkinter.CTkButton(self.more, text = "Install Lib", fg_color = "#2f2f2f", hover_color = "#222222", command = self.installlib)

        self.more_libe.grid(column = 0, row = 1, padx=10, pady=(10, 10), sticky = "W")
        self.more_libb.grid(column = 1, row = 1, padx=10, pady=(10, 10), sticky = "W")

        self.more.grid(column = 0, row = len(self.skills) + 1, padx = 30, pady = 10, sticky = "EW")

    def delete(self, idx: int):
        self.skills.pop(idx)
        self.reprint()
    
    def reprint(self):
        for i, skill in enumerate(self.skills):
            skill.grid_forget()
            skill.grid(column = 0, row = i+1, padx = 30, pady = 10, sticky = "EW")
    
    def newskill(self):
        __newskill = Skill("name", "my skill", "#Your Code", False, "0.0.1", True)
        self.skills.append(SkillFrame(self, __newskill.name, "my skill", "#Your Code", False, __newskill, len(self.skills)))
        self.more.grid_forget()
        self.skills[-1].grid(column = 0, row = len(self.skills), padx = 30, pady = 10, sticky = "EW")
        self.more.grid(column = 0, row = len(self.skills) + 1, padx = 30, pady = 10, sticky = "EW")
    
    def installlib(self):
        installed = PrivateFunctions.install_lib(self.more_lib.get())
        print(f"Installed {self.more_lib.get()}" if installed else f"Not founded {self.more_lib.get()}")
        self.more_lib.set("")

class SkillFrame(customtkinter.CTkFrame):
    def __init__(self, master, name: str = "", commands: str = "", code: str = "#Your Code", saved:bool = True, skill: Skill = Skill, idx: int = 0):
        super().__init__(master)
        self.grid_columnconfigure((0), weight = 1)
        self.__name = customtkinter.StringVar(self, name)
        self.__commands = commands
        self.__code = code
        self.__skill: Skill = skill
        self.__saved = saved
        self.__idx = idx
        self.name_entry = customtkinter.CTkEntry(self, width=500, placeholder_text="Skill Name", textvariable = self.__name)
        self.name_entry.grid(row=0, column=0, padx=10, pady=(10, 10), sticky = "W", columnspan = 4)
        self.commands_entry = customtkinter.CTkTextbox(self, height = 100)
        self.commands_entry.insert("0.0", self.__commands)
        self.commands_entry.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky = "EW", columnspan = 4)
        self.code_entry = customtkinter.CTkTextbox(self, height=300, )
        self.code_entry.insert("0.0", self.__code)
        font = self.code_entry.cget("font")
        tab_size = font.measure('    ')
        self.code_entry.configure(tabs = tab_size)
        self.code_entry.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky = "SEW", columnspan = 4)
        self.save_button = customtkinter.CTkButton(self, text = "", image = master.save_ico, height = 30, width = 30, fg_color = "transparent", command = lambda: self.save(True))
        self.export_button = customtkinter.CTkButton(self, text = "", image = master.export_ico, height = 30, width = 30, fg_color = "transparent", command = lambda: self.save())
        self.delete_button = customtkinter.CTkButton(self, text = "", image = master.delete_ico, height = 30, width = 30, fg_color = "transparent", hover_color = '#880000', command = lambda: self.delete())
        self.save_button.grid(row=0, column=1, padx=10, pady=(10, 10))
        self.export_button.grid(row=0, column=2, padx=10, pady=(10, 10))
        self.delete_button.grid(row=0, column=3, padx=10, pady=(10, 10))

        self.name_entry.bind('<FocusOut>', lambda event: self.focusoutname())
        self.commands_entry.bind('<FocusOut>', lambda event: self.focusoutcommands())
        self.code_entry.bind('<FocusOut>', lambda event: self.focusoutcode())
        self.bind('<Button-1>', lambda event: self.focus_set())
    
    @property
    def name(self):
        return self.__name.get()
    @property
    def commands(self):
        self.__commands = self.commands_entry.get('0.0', 'end')
        return self.__commands
    @property
    def code(self):
        self.__code = self.code_entry.get('0.0', 'end')
        return self.__code
    
    def focusoutname(self):
        self.__skill.name = self.name
        self.__saved = False
    
    def focusoutcommands(self):
        self.__skill.commands = self.commands.split('\n')
        self.__saved = False

    def focusoutcode(self):
        self.__skill.code = self.code
        self.__skill.registered = False
        self.__saved = False
    
    def delete(self):
        self.__skill.delete()
        del self.__skill
        self.grid_forget()
        self.master.delete(self.__idx)
    
    def save(self, ot: bool = False):
        self.__skill.name = self.name
        self.__skill.commands = self.commands.split('\n')
        self.__skill.code = self.code
        self.__skill.registered = True if not ot else False
        self.__skill.upload_py()

class PluginMenu(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.save_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "save_ico.png")), size=(30, 30))
        self.export_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "export_ico.png")), size=(30, 30))
        self.delete_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "delete_ico.png")), size=(30, 30))
        self.grid_columnconfigure(0, weight = 1)
        self.label = customtkinter.CTkLabel(self, text="Personal Assistant Plugins", compound="left", anchor = "w", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky = "W")
        _plugins: list[Plugin] = get_all_plugins()
        self.plugins: list[PluginFrame] = []
        for i, plugin in enumerate(_plugins):
            self.plugins.append(PluginFrame(self, plugin.name, plugin.code, plugin.register, True, plugin, i))
            self.plugins[-1].grid(column = 0, row = i+1, padx = 30, pady = 10, sticky = "EW")
        
        self.more = customtkinter.CTkFrame(self)
        self.more.grid_columnconfigure(2, weight = 1)

        self.more_addbtn = customtkinter.CTkButton(self.more, text = "Add Plugin", command = self.newplugin)
        self.more_addbtn.grid(column = 0, row = 0, columnspan = 2, padx=10, pady=(10, 10), sticky = "WE")

        self.more_lib = customtkinter.StringVar(self.more, "", "libi")
        self.more_libe = customtkinter.CTkEntry(self.more, textvariable = self.more_lib)
        self.more_libb = customtkinter.CTkButton(self.more, text = "Install Lib", fg_color = "#2f2f2f", hover_color = "#222222", command = self.installlib)

        self.more_libe.grid(column = 0, row = 1, padx=10, pady=(10, 10), sticky = "W")
        self.more_libb.grid(column = 1, row = 1, padx=10, pady=(10, 10), sticky = "W")

        self.more.grid(column = 0, row = len(self.plugins) + 1, padx = 30, pady = 10, sticky = "EW")

    def delete(self, idx: int):
        self.plugins.pop(idx)
        self.reprint()
    
    def reprint(self):
        for i, plugin in enumerate(self.plugins):
            plugin.grid_forget()
            plugin.grid(column = 0, row = i+1, padx = 30, pady = 10, sticky = "EW")
    
    def newplugin(self):
        __newplugin = Plugin("name", "#Your Code", "#Your Events")
        self.plugins.append(PluginFrame(self, "name", "#Your Code", "#Your Events", False, __newplugin, len(self.plugins)))
        self.more.grid_forget()
        self.plugins[-1].grid(column = 0, row = len(self.plugins), padx = 30, pady = 10, sticky = "EW")
        self.more.grid(column = 0, row = len(self.plugins) + 1, padx = 30, pady = 10, sticky = "EW")
    
    def installlib(self):
        installed = PrivateFunctions.install_lib(self.more_lib.get())
        print(f"Installed {self.more_lib.get()}" if installed else f"Not founded {self.more_lib.get()}")
        self.more_lib.set("")

class PluginFrame(customtkinter.CTkFrame):
    def __init__(self, master, name: str = "", code: str = "#Your Code", register: str = "#Your Events", saved:bool = True, plugin: Plugin = Plugin, idx: int = 0):
        super().__init__(master)
        self.grid_columnconfigure((0), weight = 1)
        self.__name = customtkinter.StringVar(self, name)
        self.__code = code
        self.__register =  register
        self.__plugin: Plugin = plugin
        self.__saved = saved
        self.__idx = idx
        self.name_entry = customtkinter.CTkEntry(self, width=500, placeholder_text="Skill Name", textvariable = self.__name)
        self.name_entry.grid(row=0, column=0, padx=10, pady=(10, 10), sticky = "W", columnspan = 4)
        self.code_entry = customtkinter.CTkTextbox(self, height=300, )
        self.code_entry.insert("0.0", self.__code)
        font = self.code_entry.cget("font")
        tab_size = font.measure('    ')
        self.code_entry.configure(tabs = tab_size)
        self.code_entry.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky = "SEW", columnspan = 4)
        self.register_entry = customtkinter.CTkTextbox(self, height = 100)
        self.register_entry.insert("0.0", self.__register)
        font = self.register_entry.cget("font")
        tab_size = font.measure('    ')
        self.register_entry.configure(tabs = tab_size)
        self.register_entry.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky = "EW", columnspan = 4)
        self.save_button = customtkinter.CTkButton(self, text = "", image = master.save_ico, height = 30, width = 30, fg_color = "transparent", command = lambda: self.save(True))
        self.export_button = customtkinter.CTkButton(self, text = "", image = master.export_ico, height = 30, width = 30, fg_color = "transparent", command = lambda: self.save())
        self.delete_button = customtkinter.CTkButton(self, text = "", image = master.delete_ico, height = 30, width = 30, fg_color = "transparent", hover_color = '#880000', command = lambda: self.delete())
        self.save_button.grid(row=0, column=1, padx=10, pady=(10, 10))
        self.export_button.grid(row=0, column=2, padx=10, pady=(10, 10))
        self.delete_button.grid(row=0, column=3, padx=10, pady=(10, 10))

        self.name_entry.bind('<FocusOut>', lambda event: self.focusoutname())
        self.code_entry.bind('<FocusOut>', lambda event: self.focusoutcode())
        self.register_entry.bind('<FocusOut>', lambda event: self.focusoutregister())
        self.bind('<Button-1>', lambda event: self.focus_set())
    
    @property
    def name(self):
        return self.__name.get()
    @property
    def code(self):
        self.__code = self.code_entry.get('0.0', 'end').replace('	','    ')
        return self.__code
    @property
    def register(self):
        self.__register = self.register_entry.get('0.0', 'end').replace('	','    ')
        return self.__register
    
    def focusoutname(self):
        self.__plugin.name = self.name
        self.__saved = False

    def focusoutcode(self):
        self.__plugin.code = self.code
        self.__saved = False
    
    def focusoutregister(self):
        self.__plugin.register = self.register
        self.__saved = False
    
    def delete(self):
        self.__plugin.delete()
        del self.__plugin
        self.grid_forget()
        self.master.delete(self.__idx)
    
    def save(self, ot: bool = False):
        self.__plugin.name = self.name
        self.__plugin.code = self.code
        self.__plugin.register = self.register
        self.__plugin.toPy(ot)

class APMenu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pa: MainAP
        self.parent = master
        t = Thread(target = self.__mainpa__)
        t.start()
        self.bind('<Button-1>', lambda event: self.focus_set())
        self.send_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "send_ico.png")), size=(30, 30))
        self.microphone_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "microphone_ico.png")), size=(20, 30))
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.bottom = customtkinter.CTkFrame(self, corner_radius = 20, height = 40, fg_color = "#222222", border_width = 0)
        self.bottom.grid(row = 1, column = 0, sticky = "SEW", pady = 20, padx = 20)
        self.bottom_mic = customtkinter.CTkFrame(self, corner_radius = 20, height = 40, width = 40, fg_color = "#77aaff", border_width = 0)
        self.bottom.columnconfigure(0, weight = 1)
        self.bottom_textinp = customtkinter.CTkEntry(self.bottom, height = 40, border_width = 0, fg_color = "transparent", corner_radius = 2, text_color = "#ffffff", placeholder_text = "Write Down Here", placeholder_text_color = "#aaaaaa")
        self.bottom_textinp.grid(column = 0, row = 0, sticky = "NSEW", padx = 15)
        self.send_button = customtkinter.CTkButton(self.bottom, text = "", image = self.send_ico, height = 30, width = 30, fg_color = "transparent", hover_color = '#333333', command = lambda: self.send_msg())
        self.microphone_button = customtkinter.CTkButton(self.bottom, text = "", image = self.microphone_ico, height = 30, width = 20, fg_color = "transparent", hover_color = '#333333', command = lambda: self.activate_microphone())
        self.microphone_button.grid(row = 0, column = 1)
        self.microphone_button_a = customtkinter.CTkButton(self.bottom_mic, text = "", image = self.microphone_ico, height = 30, width = 20, fg_color = "transparent", hover_color = "#77aaff", command = lambda: self.deactivate_microphone())
        self.send_button.grid(row = 0, column = 2, padx = 15)
        self.bottom_textinp.bind("<Return>", self.__sendmsge__)

        self.chat_frame = customtkinter.CTkScrollableFrame(self, fg_color = "transparent", border_width = 0)
        self.chat_frame.grid(row = 0, column = 0, padx = 10, sticky = "NSEW")
        self.chat_frame.columnconfigure((0,1), weight = 1)
        self.chat_frame.bind('<Button-1>', lambda event: self.focus_set())

        self.__messages: list[MsgBubble] = []
        self.msg_dire = ["W","E"]

    def __mainpa__(self):
        self.pa = MainAP(self)
    
    def __addmsg__(self, t: int, txt: str):
        self.__messages.append(MsgBubble(self.chat_frame, t, txt))
        self.__messages[-1].grid(column = t, row = len(self.__messages)-1, sticky = f"S{self.msg_dire[t]}", pady = 2)
        self.chat_frame.after(10, self.chat_frame._parent_canvas.yview_moveto, 1.0)
    
    def __sendmsge__(self, event):
        self.send_msg()

    def send_msg(self):
        try:
            txt = self.bottom_textinp.get()
            if txt != "" and self.pa.state == "Online":
                self.__addmsg__(1, txt)
                t = Thread(target = self.pa.txt_command, kwargs = {"command": txt})
                t.start()
                self.bottom_textinp.delete(0, "end")
                time.sleep(0.1)
            elif self.pa.state == "Answer_Requested":
                t = Thread(target = self.__addmsg__, args = (1, txt))
                t2 = Thread(target = self.pa.answer_text, kwargs = {"text": txt})
                t.start()
                t2.start()
                self.bottom_textinp.delete(0, "end")
                time.sleep(0.1)
        except:
            pass
    
    def voice_msg(self, txt:str):
        if txt != "" or txt != None:
            t = Thread(target = self.__addmsg__, args = (1, txt))
            t.start()

    def send_msg_ap(self, txt: str|None):
        if txt != "" or txt != None:
            t = Thread(target = self.__addmsg__, args = (0, txt))
            t.start()
    
    def activate_microphone(self):
        try:
            if self.pa.state == "Online":
                t = Thread(target = self.pa.voice_command)
                t.start()
                self.bottom_textinp.grid_forget()
                self.microphone_button.grid_forget()
                self.send_button.grid_forget()
                self.bottom.grid_forget()
                self.bottom_mic.grid(row = 1, column = 0, sticky = "S", pady = 20, padx = 20)
                self.microphone_button_a.grid(row = 0, column = 0, padx = 15)
            elif self.pa.state == "Answer_Requested":
                t = Thread(target = self.pa.answer_voice)
                t.start()
                self.bottom_textinp.grid_forget()
                self.microphone_button.grid_forget()
                self.send_button.grid_forget()
                self.bottom.grid_forget()
                self.bottom_mic.grid(row = 1, column = 0, sticky = "S", pady = 20, padx = 20)
                self.microphone_button_a.grid(row = 0, column = 0, padx = 15)
        except:
            pass
    
    def deactivate_microphone(self):
        try:
            self.pa.interrupvccmd = True
            self.microphone_button_a.grid_forget()
            self.bottom_mic.grid_forget()
            self.bottom.grid(row = 1, column = 0, sticky = "SEW", pady = 20, padx = 20)
            self.bottom_textinp.grid(column = 0, row = 0, sticky = "NSEW", padx = 15)
            self.microphone_button.grid(row = 0, column = 1)
            self.send_button.grid(row = 0, column = 2, padx = 15)
        except:
            pass
    
    def restart_pa(self):
        try:
            if self.pa.state == "Online":
                t = Thread(target = self.pa.restart)
                t.start()
        except:
            pass

    @property
    def messages(self):
        return self.__messages
    @property
    def nmsg(self):
        return len(self.__messages)

class MsgBubble(customtkinter.CTkLabel):
    def __init__(self, master, t = 0, txt = ""):
        self.__type = t
        self.__color = ["#aaaaaa", "#77aaff"][t]
        self.__txt = txt
        super().__init__(master, height = 40, corner_radius = 20, fg_color =  self.__color, text_color = "#ffffff", text = self.__txt, wraplength = 480, justify = "left", anchor = "w")
    
    @property
    def bubbletype(self):
        return self.__type
    @property
    def txt(self):
        return self.__txt
    @txt.setter
    def txt(self, txt:str):
        self.__txt = txt

class ClientsMenu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.inner_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

        self.inner_frame.grid_columnconfigure(0, weight = 1)

        self.inner_frame.clientl = []
        lc = lib_clients()
        for i, c in enumerate(lc[0]):
            self.inner_frame.clientl.append(ClientFrame(self.inner_frame, self, c, lc[1][i]))
            self.inner_frame.clientl[-1].grid(column = 0, row = i+1, padx = 30, pady = 10, sticky = "EW")

        self.inner_frame.grid(row=1, column=0, sticky="nsew")
    
    def launch(self, app, config):
        self.inner_frame.grid_forget()
        self.current_client = app(self)
        self.current_client.grid(row=1, column=0, sticky="nsew")
        self.quit_client_button = customtkinter.CTkButton(self, text = 'Exit Client', command = self.quit_cc)
        self.quit_client_button.grid(column = 0, row = 0, sticky = 'EW')
    
    def quit_cc(self):
        self.quit_client_button.grid_forget()
        self.current_client.grid_forget()
        self.inner_frame.grid(row=1, column=0, sticky="nsew")

class ClientFrame(customtkinter.CTkFrame):
    def __init__(self, master, mm = None, cn:str = None , ci:list = None):
        super().__init__(master)
        self.label = customtkinter.CTkLabel(self, text = cn)
        self.label.grid(column = 0, row = 0)
        self.button = customtkinter.CTkButton(self, text = "Launch", command = lambda: mm.launch(ci[0], ci[1]))
        self.button.grid(column = 0, row = 1)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.__app = None

        self.title("PAC")
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "app/images")
        self.protocol("WM_DELETE_WINDOW", self.stop)

        #SideBar 
        self.sidebar = SideBar(self)
        self.sidebar.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        #Menus
        self.home_frame = HomeMenu(self)
        self.skill_frame = SkillMenu(self)
        self.plugin_frame = PluginMenu(self)
        self.ap_frame = APMenu(self)
        self.clients_frame = ClientsMenu(self)

        self.select_homemenu()

    def stop(self):
        try:
            if self.ap_frame.pa.state:
                self.ap_frame.pa.destroy()
                self.destroy()
                sys.exit()
        except:
            pass

    def restart_pa(self):
        self.ap_frame.restart_pa()

    def select_menu(self, name):
        self.sidebar.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.sidebar.skill_button.configure(fg_color=("gray75", "gray25") if name == "skill" else "transparent")
        self.sidebar.plugin_button.configure(fg_color=("gray75", "gray25") if name == "plugin" else "transparent")
        self.sidebar.ap_button.configure(fg_color=("gray75", "gray25") if name == "ap" else "transparent")
        self.sidebar.clients_button.configure(fg_color=("gray75", "gray25") if name == "clients" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "skill":
            self.skill_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.skill_frame.grid_forget()
        if name == "plugin":
            self.plugin_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.plugin_frame.grid_forget()
        if name == "ap":
            self.ap_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.ap_frame.grid_forget()
        if name == "clients":
            self.clients_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.clients_frame.grid_forget()
    
    def select_homemenu(self):
        self.select_menu('home')
    def select_skillmenu(self):
        self.select_menu('skill')
    def select_pluginmenu(self):
        self.select_menu('plugin')
    def select_apmenu(self):
        self.select_menu('ap')
    def select_clientsmenu(self):
        self.select_menu('clients')

app = App()
app.mainloop()

#Bread 👍