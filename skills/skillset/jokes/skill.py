#0.0.1
from ap import AP
from skills import factory

class Skill ():

    def commands(self, command:str):
        return ['cuéntame un chiste', 'dime un chiste', 'me aburro', 'dime algo gracioso', 'cuéntame algo gracioso']

    def handle_command(self, command:str, pa:AP, t: str):
        Functions = functions = pa.functions
        pyjokes = functions.import_lib("pyjokes")
                        pa.say(pyjokes.get_joke(language='es'))

def initialize():
    factory.register("jokes_skill", Skill)
        