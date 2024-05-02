# Skill Loader
import importlib

class PluginInterface:
    """ A pluging has a single function called initialize"""

    @staticmethod
    def initialize() -> None:
        """ Initialize the plugin """
        
def import_module(name:str) -> PluginInterface:
    return importlib.import_module(name) # type: ignore

def reload_module(name: str) -> PluginInterface:
    return importlib.reload(name)

def load_skills(plugins: list[str], reload: bool = False)->None:
    """ Load the plugins """
    for plugin_name in plugins:
       plugin = None
       if reload: plugin = import_module(plugin_name) 
       else: plugin = reload_module(plugin_name)
       plugin.initialize()
