#0.0.1
from dataclasses import dataclass
from ap import AP
import plugins.plugin_factory

@dataclass
class Parrot_plugin:
    name = 'parrot'

    def parrot(self, sentence):
        print(f"Parrot says: {sentence}")

    def register(self, pa:AP):
        self.pa: AP = pa
        self.functions = self.Functions = self.pa.functions
        self.pa.after_listening.register(self.parrot)
        self.pa.after_speaking.register(self.parrot)
        return self

def initialize():
    plugins.plugin_factory.register("parrot_plugin", Parrot_plugin)