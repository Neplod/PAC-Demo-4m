from ap import AP
from skill_weather import Skill_weather
from skill_jokes import Skill_Jokes
import pyjokes

ap = AP()

# ap.name = "Robbie the Robot"

def joke():
    # ap.say("I'm a Robot not a commedian")
    funny = pyjokes.get_joke()
    print(funny)
    ap.say(funny)

weather = Skill_weather()
jokes = Skill_Jokes()
ap.register_skill(weather)
ap.register_skill(jokes)
ap.list_skills()

command = ""
while True and command != "goodbye":
    command = ap.listen()
    print("command was:",command)

    if command == "tell me a joke":
        joke()
    # do commands

ap.say("Good bye, I'm going to sleep now")