from ap import AP
from skills import factory, loader
from plugins import plugin_loader, plugin_factory
import json
from eventhook import Event_hook
from threading import Thread
import time
from difflib import SequenceMatcher
from operator import itemgetter
from skills.skill_manager import get_skills_data

class MainAP():
    def __init__(self, parent):
        self.__state = None
        self.parent = parent
        
        self.ap: AP
        t = Thread(target = self.__init_ap__)
        t.start()

        self.config: dict = {"use_similarity": True, "similarity_min": 0.6, "similarity_wbw": True}

        self.command = ""
        self.state = "Init"

    def __init_ap__(self):
        self.ap = AP(self)

        self.ap.start = Event_hook()
        self.ap.stop = Event_hook()

        skill_data = get_skills_data()

        loader.load_skills(skill_data["lib"])

        self.skills = [factory.create(item) for item in skill_data["skills"]]
        print(f'skills: {self.skills}')

        with open("./plugins/plugins.json") as f:
            plugin_data = json.load(f)
            print(f'plugins: {plugin_data["plugins"]}')
            plugin_loader.load_plugins(plugin_data["plugins"])

        self.plugins = [plugin_factory.create(item) for item in plugin_data["items"]]

        for item in self.plugins:
            item.register(self.ap)
        
        self.state = "Online"

    def restart(self):
        try:
            self.state = "Restarting"

            self.command = ""

            skill_data = get_skills_data()

            loader.load_skills(skill_data["lib"], True)

            self.skills = [factory.create(item) for item in skill_data["skills"]]
            print(f'skills: {self.skills}')

            with open("./plugins/plugins.json") as f:
                plugin_data = json.load(f)
                print(f'plugins: {plugin_data["plugins"]}')
                plugin_loader.load_plugins(plugin_data["plugins"])

            self.plugins = [plugin_factory.create(item) for item in plugin_data["items"]]

            for item in self.plugins:
                item.register(self.ap)

            self.state = "Online"
        except:
            pass
        self.state = "Online"
    
    def __similar(self, ta: str, tb: str) -> float:
        return SequenceMatcher(None, ta, tb).ratio()

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state: str):
        self.__state = state

    def find_command(self, command:str, t: str):
        self.state = "Answering"
        time.sleep(0.1)
        try:
            self.ap.engine.endLoop()
        except:
            pass
        self.command = command
        self.command = self.command.lower()
        print(f'command: {self.command}')
        self.cmde = False
        for skill in self.skills:
            if self.command in skill.commands(self.command):
                self.cmde = True
                t = Thread(target = self.run_skill, kwargs = {"skill": skill, "t": t})
                t.start()
        if self.cmde == False:
            if self.config["use_similarity"] == True:
                self._similarities = []
                for skill in self.skills:
                    self._similarities.append([skill, self._find_similarity(command, skill.commands(self.command))])
                self._similarities = sorted(self._similarities, key = itemgetter(1), reverse = True)
                if self._similarities[0][1] >= self.config["similarity_min"]:
                    self.cmde = True
                    t = Thread(target = self.run_skill, kwargs = {"skill": self._similarities[0][0], "t": t})
                    t.start()
                else:
                    self.state = "Online"
            else:
                self.state = "Online"

    def _find_similarity(self, command: str, commands) -> float:
        _sv = 0
        for c in commands:
            __s = 0
            if self.config["similarity_wbw"] == True:
                __sw = 0
                for w in command.split(" "):
                    __sw += self.__similar(w, c)
                __s = __sw / len(command.split(" "))
            else:
                __s = self.__similar(command, c)
            if __s > _sv:
                _sv = __s
        return _sv

    def txt_command(self, command: str):
        if self.ap.requested:
            self.answer_text(command)
        else:
            self.find_command(command, "text")

    def voice_command(self):
        if self.ap.requested:
            self.answer_voice()
        else:
            self.__state = "Listening"
            self.interrupvccmd = False
            try:
                self.ap.engine.endLoop()
            except:
                pass
            phrase = None
            self.ap.before_listening.trigger()
            while True:
                phrase = self.ap.listen(False)
                if phrase != None:
                    if  type(phrase) == str:
                        t = Thread(target = self.parent.deactivate_microphone)
                        t.start()
                    break
                if self.interrupvccmd:
                    break
            self.ap.after_listening.trigger(phrase if phrase else "")
            if phrase != None and type(phrase) == str:
                self.find_command(phrase, "voice")
            else:
                self.state = "Online"

    def run_skill(self, skill, t):
        ar = False
        try:
            ar = skill.handle_command(self.command, self.ap, t)
        except Exception as e:
            print(f"Error: {e}")
        if ar != True:
            self.state = "Online"

    def request_voice(self):
        self.request_answer()
        self.parent.activate_microphone()
        self.answer_voice()

    def request_answer(self):
        self.state = "Answer_Requested"
    
    def answer_text(self, text:str):
        self.ap.answer_requested = text
        if self.ap.answer_requested != None and self.ap.answer_requested != "":
            t = Thread(target = self.answer_func)
            t.start()
            self.state = "Answering"

    def answer_func(self):
        self.ap.answer_func(self.ap.answer_requested)
        self.ap.requested = False
        self.ap.answer_requested = None
        self.ap.answer_func = None
        self.state = "Online"

    def answer_voice(self):
        self.interrupvccmd = False
        phrase = None
        self.state = "Answer_Requested_Listening"
        self.ap.before_listening.trigger()
        while True:
            phrase = self.ap.listen(False)
            if phrase != None:
                if type(phrase) == str:
                    t = Thread(target = self.parent.deactivate_microphone)
                    t.start()
                break
            if self.interrupvccmd:
                break
        if phrase != None and type(phrase) == str:
            self.ap.after_listening.trigger(phrase)
            self.answer_text(phrase)
        else:
            self.ap.after_listening.trigger("")
            self.state = "Answer_Requested"

    def loop(self):
        self.state = "Loop"
        self.ap.start.trigger()
        self.ap.say("Hola")
        while True and self.command not in ["adiós", 'hasta luego', 'quitar', 'salir','hasta otra', 'la salida', 'salida']:
            self.command = ""
            self.command = self.ap.listen()
            if self.command:
                self.command = self.command.lower()
                print(f'command heard: {self.command}') 
                for skill in self.skills:
                    if self.command in skill.commands(self.command):
                        try:
                            skill.handle_command(self.command, self.ap, "voice")
                        except Exception as e:
                            print(f"Error: {e}")
            if self.ap.engine.isBusy() == False:
                self.ap.engine.endLoop()

        self.ap.say("Adiós!")
        self.state = "Online"

    def destroy(self):
        self.state = "Destroying"
        try:
            self.ap.engine.endLoop()
        except:
            pass
        print('telling triggers to stop')
        self.ap.stop.trigger()
        print('telling ai to stop')
        self.ap.stop_ap()
        print('deleting ai')
        del(self.ap)
        print('done')