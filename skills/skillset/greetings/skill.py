#0.0.1
from ap import AP
from skills import factory

class Skill ():

    def commands(self, command:str):
        return ['gracias', 'muchas gracias', 'muchas gracias!', 'ok gracias', 'ok', 'gracias', 'gracias!', 'oki', 'gracias!', 'oki gracias!', 'oki gracias', 'oki', 'gracias', 'ok gracias!', 'ok', 'gracias']

    def handle_command(self, command:str, pa:AP, t: str):
        Functions = functions = pa.functions
        pa.say("De nada, si tienes alguna cosa más no dudes en decírmelo.")

def initialize():
    factory.register("greetings_skill", Skill)
        