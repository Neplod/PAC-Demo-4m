#0.0.1
from ap import AP
from skills import factory

class Skill ():

    def commands(self, command:str):
        return ['bread']

    def handle_command(self, command:str, pa:AP, t: str):
        Functions = functions = pa.functions
        pa.say("Bread")

def initialize():
    factory.register("bread_skill", Skill)
        