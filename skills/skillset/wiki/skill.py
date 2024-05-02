#0.0.1
from ap import AP
from skills import factory

class Skill ():

    def commands(self, command:str):
        return ['háblame sobre algo', 'búscame una cosa', 'búscame algo', 'háblame sobre una cosa', 'me puedes hablar sobre una cosa', 'me puedes hablar sobre algo', 'búscame en wikipedia una cosa', 'búscame una cosa en la wikipedia', 'búscame una cosa en la wiki']

    def handle_command(self, command:str, pa:AP, t: str):
        Functions = functions = pa.functions
        def requested(answer):
            try:
                wiki = functions.import_lib("wikipedia")
                wiki.set_lang("es")
                search = wiki.search(answer)
                if len(search) == 0:
                    pa.say(f"No se han encontrado resultados para {answer}")
                elif len(search) == 1:
                    pa.say(f"He encontrado este resultado para {answer}. {search[0]}.")
                    msg = str(wiki.summary(search[0], sentences = 6)).replace('\n', '')
                    pa.send_msg(msg)
                elif len(search) == 2:
                    pa.say(f"He encontrado estos resultado para {answer}. Sobre {search[0]}, y también sobre {search[1]}.")
                    msg = [str(wiki.summary(search[0], sentences = 3)).replace('\n', ''), str(wiki.summary(search[1], sentences = 3)).replace('\n', '')]
                    msg = msg[0] + "\n" + msg[1]
                    pa.send_msg(msg)
                else:
                    pa.say(f"He encontrado estos resultado para {answer}. Sobre {search[0]}, sobre {search[1]}, y también sobre {search[2]}.")
                    msg = [str(wiki.summary(search[0], sentences = 2)).replace('\n', ''), str(wiki.summary(search[1], sentences = 2)).replace('\n', ''), str(wiki.summary(search[2], sentences = 2)).replace('\n', '')]
                    msg = msg[0] + "\n" + msg[1] + "\n" + msg[2]
                    pa.send_msg(msg)
                if len(search) > 3:
                    pa.say("También hay más resultados, si quieres puedes investigar por ti mismo.")
            except:
                pa.say("Ha habido un error")
        pa.say("¿Qué quieres que busque en Wikipedia?")
        return pa.request_answer(t, requested)

def initialize():
    factory.register("wiki_skill", Skill)
        