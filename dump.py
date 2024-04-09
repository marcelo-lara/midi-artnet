#!/usr/bin/env python
import time
import mido
from app_settings import getLoopbackInterface

# open midi port
_, port = getLoopbackInterface()

def handle_msg(msg):
    print(msg)

try:
    with mido.open_input(port, callback=handle_msg) as midi_in:
        print("listening on " + port  + ". Press Control-C to exit.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print('')
    
#close artnet output
print("closing..")
