#0.0.1
from ap import AP
from skills import factory

class Skill ():

    def commands(self, command:str):
        return ['hola', 'buenos días', 'buenas tardes', 'buenas', 'hi']

    def handle_command(self, command:str, pa:AP, t: str):
        Functions = functions = pa.functions
        pa.say("Hola")

def initialize():
    factory.register("hi_skill", Skill)
        