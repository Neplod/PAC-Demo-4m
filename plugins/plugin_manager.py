import codecs
import importlib
from pathlib import Path
import os
import json

class Plugin():

    def __init__(self, name: str, code: str = """""", register: str = """""", _ispy: bool| None = None):
        self.__name: str = name.lower().replace(' ','_').replace('.',',')
        self.__code: str = code
        self.__register: str = register
        self.__old:str = self.__name
        if _ispy != None:
            self.__py: bool = _ispy
        else:
            self.__py: bool = False
    
    def __new__(cls, name:str, code: str = """""", register: str = """""",_ispy: bool|None = None):
        instance = super().__new__(cls)
        return instance
    
    def __str__(self):
        return f"""{self.__name.capitalize()}: \n   Code:{self.__code} \n   Register:{self.__register}"""

    # Properties
    
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        oldpy = self.__py
        self.delete()
        self.__old = self.__name
        self.__name = value.lower().replace(' ','_').replace('.',',').replace('1','o').replace('1','o').replace('2','t').replace('3','t').replace('4','f').replace('5','f').replace('6','s').replace('7','s').replace('8','e').replace('9','n').replace('0','z')
        self.toPy(False if oldpy else True)

    @property
    def code(self) -> str:
        return self.__code

    @code.setter
    def code(self, value: str):
        self.__code = value
    
    @property
    def register(self) -> str:
        return self.__register

    @register.setter
    def register(self, value: str):
        self.__register = value

    # Funcs

    def toPy(self, only_txt: bool = False):
        try:
            os.remove(f"plugins/pluginset/{self.__name}.py")
        except:
            pass
        try:
            os.remove(f"plugins/pluginset/{self.__name}.txt")
        except:
            pass

        file = codecs.open(f'plugins/pluginset/{self.__name}.txt', 'x', 'UTF8')

        self.__fixcode()

        plugin = f"""#0.0.1
from dataclasses import dataclass
from ap import AP
import plugins.plugin_factory

@dataclass
class {self.__name.capitalize()}_plugin:
    name = '{self.__name}'

    {self.__code}

    def register(self, pa:AP):
        self.pa: AP = pa
		self.functions = self.Functions = self.pa.functions
        {self.register}
        return self

def initialize():
    plugins.plugin_factory.register("{self.__name}_plugin", {self.__name.capitalize()}_plugin)

        """
    
        file.write(plugin)
        file.close()

        if not only_txt:
            path = Path(f"plugins/pluginset/{self.__name}.txt")

            newpath = path.with_suffix('.py')

            self._editinjson(self.__old)

            path.rename(newpath)
            self.__py = True
        else:
            self.__py = False

    def deletePy(self):
        try:
            os.remove(f"plugins/pluginset/{self.__name}.py")
            self._unregisterinjson()
            self.__py = False
        except:
            pass
    
    def delete(self):
        self.deletePy()
        try:
            os.remove(f"plugins/pluginset/{self.__name}.txt")
        except:
            pass
    
    def _registerinjson(self):
        with codecs.open('./plugins/plugins.json', 'r', 'UTF8') as file:
            data = json.load(file)
            data["plugins"].append(f'plugins.pluginset.{self.__name}')
            data["items"].append({"name":f"{self.__name}_plugin"})
        self.__rewrite(data, './plugins/plugins.json')
    
    def _editinjson(self, old: str):
        with codecs.open('./plugins/plugins.json', 'r', 'UTF8') as file:
            data = json.load(file)
            if f'plugins.pluginset.{old}' in data['plugins']:
                data["plugins"][data["plugins"].index(f'plugins.pluginset.{old}')] = f'plugins.pluginset.{self.__name}'
                data["items"][data["items"].index({"name":f"{old}_plugin"})] = {"name":f"{self.__name}_plugin"}
                file.close()
                self.__rewrite(data, './plugins/plugins.json')
            else:
                file.close()
                self._registerinjson()
    
    def _unregisterinjson(self):
        with codecs.open('./plugins/plugins.json', 'r', 'UTF8') as file:
            data = json.load(file)
            data["plugins"].pop(data['plugins'].index(f'plugins.pluginset.{self.__name}'))
            data["items"].pop(data['items'].index({"name":f"{self.__name}_plugin"}))
        self.__rewrite(data, './plugins/plugins.json')
            
    def __rewrite(self, data: any, path:str):
        os.remove(path)
        newfile = open(path, 'x')
        newfile.write(str(data).replace("'",'"'))
        newfile.close()
    
    def __fixcode(self) -> str:
        sc: list[str] = self.__code.split('\n')
        fix: str = ""
        for i,e in enumerate(sc):
            if i != 0:
                sc[i] = f"""\n    {e}"""
            fix = fix + sc[i]
        self.__code = fix
        sc: list[str] = self.__register.split('\n')
        fix: str = ""
        for i,e in enumerate(sc):
            if i != 0:
                sc[i] = f"""\n        {e}"""
            fix = fix + sc[i]
        self.__register= fix

def get_all_plugins() -> list[Plugin]:
    funcs: list[Plugin] = []
    funcspath = os.listdir('plugins/pluginset/')
    for p in funcspath:
        if p != '__pycache__':
            with codecs.open(f'./plugins/pluginset/{p}', encoding='UTF8') as _file:
                _lines = _file.readlines()
            _regist = _lines.index('    def register(self, pa:AP):\n')
            try:
                _name = _lines[-2].split('"')[1][:-7]
            except:
                try:
                    _name = _lines[-1].split('"')[1][:-7]
                except:
                    _name = _lines[-3].split('"')[1][:-7]
            _code = _lines[_lines.index(f"    name = '{_name}'\n")+2:_regist-1]
            _register = _lines[_regist+3:-4]

            for i,l in enumerate(_code):
                _code[i] = l[4:]
                _code[i] = _code[i].replace('\n', '')
            _code = '\n'.join(_code)

            for i,l in enumerate(_register):
                _register[i] = l[8:]
                _register[i] = _register[i].replace('\n', '')
            _register = '\n'.join(_register)

            funcs.append(Plugin(_name, f"""{_code}""", f"""{_register}""", _ispy = True if p.endswith('.py') else False))
    return funcs