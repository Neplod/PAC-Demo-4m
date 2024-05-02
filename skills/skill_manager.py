import codecs
import importlib
from pathlib import Path
import os
import json
import shutil

class Skill():

    def __init__(self, name: str, commands: list[str] = [], code: str = """""", register: bool = False, version: str = "", _isnew: bool = False):
        self.__name: str = name.lower().replace(' ','_').replace('.',',')
        self.__commands: list[str] = commands
        self.__code: str = code
        if _isnew:
            _i = -1
            while True:
                if _i < 0:
                    try:
                        shutil.copytree("skills/skill", f"skills/skillset/{self.__name}")
                        break
                    except:
                        _i =+ 1
                else:
                    try:
                        shutil.copytree("skills/skill", f"skills/skillset/{self.__name}{str(_i)}")
                        self.__name = self.__name + str(_i)
                        break
                    except:
                        _i =+ 1

        self.__path = f"skills/skillset/{self.__name}/"
        
        self.__pypath: str = f"skills.skillset.{self.__name}"
        self.__pypathskill: str = self.__pypath + ".skill"
        self.__skillpath: str = self.__path + "skill.py"
        self.__configpath = self.__path + "config.py"
        self.__version: str = version
        self.__registered: bool = register
        self.update_config()
        self.__rewrite(self.__path+"name.delta-str", self.__name)

        self.name = self.__name
        self.commands = self.__commands
        self.code = self.__code
        self.registered = self.__registered
    
    def __new__(cls, name:str, commands: list[str] = [], code: str = """""", register: bool = False, version: str = "", _isnew: bool = False):
        instance = super().__new__(cls)
        return instance
    
    def __str__(self):
        _c = "\n         ".join(self.__code.split("\n"))
        return f"""{self.__name.capitalize()}: \n   Commands: {", ".join(self.__commands)} \n   Code: {_c} \n   Registered:{self.__registered} \n   Path: {self.__path} \n   PyPath: {self.__pypath} \n   Version: {self.__version} """

    # Properties
    
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value.lower().replace(' ','_').replace('.',',')
        __oldpath = self.__path
        self.__path = f"skills/skillset/{self.__name}/"
        os.rename(__oldpath, self.__path)
        self.__pypath: str = f"skills.skillset.{self.__name}"
        self.__pypathskill: str = self.__pypath + ".skill"
        self.__skillpath: str = self.__path + "skill.py"
        self.__configpath = self.__path + "config.py"
        self.update_config()
        self.__rewrite(self.__path+"name.delta-str", self.__name)
        if self.__registered: self.upload_py()
    @property
    def commands(self) -> list[str]:
        return self.__commands

    @commands.setter
    def commands(self, value: list[str]):
        self.__commands = value
        self.__rewrite(self.__path+"commands.delta-list", "\n".join(self.__commands))
    
    @property
    def pypath(self):
        return self.__pypathskill
    
    @property
    def registered(self):
        return self.__registered
    
    @registered.setter
    def registered(self, value:bool):
        self.__registered = value
        self.update_config()
    
    def commands_append(self, value: str):
        self.__commands.append(value)
        self.__rewrite(self.__path+"commands.delta-list", self.__commands)
    def commands_extend(self, value: str):
        self.__commands.extend(value)
        self.__rewrite(self.__path+"commands.delta-list", self.__commands)
    def commands_pop(self, value: int):
        self.__commands.pop(value)
        self.__rewrite(self.__path+"commands.delta-list", self.__commands)
    def commands_remove(self):
        self.__commands.append()
        self.__rewrite(self.__path+"commands.delta-list", self.__commands)

    @property
    def code(self) -> str:
        return self.__code

    @code.setter
    def code(self, value: str):
        self.__code = value
        self.__rewrite(self.__path+"code.delta", self.__code)

    # Funcs

    def upload_py(self):
        try:
            os.remove(self.__skillpath)
        except:
            pass

        file = codecs.open(self.__skillpath, 'x', 'UTF8')

        self.__fixcode()

        skill = f"""#{self.__version}
from ap import AP
from skills import factory

class Skill ():

    def commands(self, command:str):
        return {self.__commands}

    def handle_command(self, command:str, pa:AP, t: str):
        Functions = functions = pa.functions
        {self.__code}

def initialize():
    factory.register("{self.__name}_skill", Skill)
        """
    
        file.write(skill)
        file.close()
        
        self.update_config()

    def delete(self):
        try: shutil.rmtree(self.__path)
        except: pass
    
    def update_config(self):
        self.__rewrite(self.__configpath, f"""from dataclasses import dataclass

@dataclass
class SkillConfig:
    registered: bool = {self.__registered}
    pypath: str = "{self.__pypath}"
    version: str = "{self.__version}\"""")
    
    def __rewrite(self, path, text):
        try: os.remove(path)
        except: pass
        with codecs.open(path, 'x', 'UTF8') as _file:
            _file.write(text)
    
    def __fixcode(self) -> str:
        sc: list[str] = self.__code.split('\n')
        fix: str = ""
        for i,e in enumerate(sc):
            if i != 0:
                sc[i] = f"""\n        {e}"""
            fix = fix + sc[i]
        self.__code = fix

def obtain(path):
    with codecs.open(path, 'r', 'UTF8') as _file:
        return _file.readlines()

def get_all_skills() -> list[Skill]:
    funcs: list[Skill] = []
    funcspath = os.listdir('skills/skillset/')
    for p in funcspath:
        if p != '__pycache__':
            _p = 'skills/skillset/' + p + "/"
            try:
                _sn = obtain(_p + "name.delta-str")
                _scm = [cm.replace("\n", "").replace("\r", "") for cm in obtain(_p + "commands.delta-list")]
                _scd = "".join(obtain(_p + "code.delta"))
                __scn = [cm.replace("\n", "") for cm in obtain(_p + "config.py")]
                _scnr = eval(__scn[4].replace("    registered: bool = ", ""))
                _scnpp = eval(__scn[5].replace("    pypath: str = ", ""))
                _scnv = eval(__scn[6].replace("    version: str = ", ""))
                funcs.append(Skill(_sn[0], _scm, _scd, _scnr, _scnv, False))
            except: pass
    return funcs

def get_skills_data() -> dict[str, list]:
    data: dict[str, list] = {}
    _datalib: list[str] = []
    _dataskills: list[dict[str, str]] = []

    funcspath = os.listdir('skills/skillset/')

    for p in funcspath:
        if p != '__pycache__':
            _p = 'skills/skillset/' + p + "/"
            try:
                _sn = obtain(_p + "name.delta-str") + "_skill"
                __scn = [cm.replace("\n", "") for cm in obtain(_p + "config.py")]
                _scnr = eval(__scn[4].replace("    registered: bool = ", ""))
                _scnpp = eval(__scn[5].replace("    pypath: str = ", ""))
                if _scnr:
                    _datalib.append(_scnpp)
                    _dataskills.append({"name": _sn})
            except: pass
    data = {"lib": _datalib, "skills": _dataskills}
    return data

if __name__ == "__main__":
    pass