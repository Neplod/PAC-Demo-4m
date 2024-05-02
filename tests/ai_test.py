from ap import AP
from time import sleep

ap = AP()
print ("say something")
message = ""
while True and message != 'good bye':
    message = ap.listen()
    if message:
        print(message)
    # sleep(0.5)