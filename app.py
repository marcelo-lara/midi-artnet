#!/usr/bin/env python
import sys
import time
import mido
from app_artnet import Artnet

# open midi port
port = "loopMIDI Port 0"
midi_multiplier = 255/126

# setup artnet
target_ip = '255.255.255.255' # typically in 2.x or 10.x range
universe = 0 				  # see docs
packet_size = 64			  # it is not necessary to send whole universe

artnet = Artnet()

def handle_msg(msg):
    if msg.type in ["note_off", "songpos", "clock", "control_change"]: return
        
    match msg.type:
        case "note_on":
            if msg.note > 80: 
                print("note_on: " + str(msg.note) + " " + str(msg.velocity))
                return
            dmx_val = int((msg.velocity-1)*midi_multiplier)
            dmx_ch = msg.note+1
            
            if msg.note > 35:
                dmx_ch = dmx_ch - 36
                artnet.fadeout(dmx_ch, (12.7*2)-(msg.velocity/5))
                return
            
            #direct send artnet            
            artnet.send(dmx_ch, dmx_val)

        case "stop":
            print("stop")
            artnet.blackout()

        case "start":
            print("start")
            artnet.reset()

        case _:     
            print(msg)

#wait for user break
try:
    with mido.open_input(port, callback=handle_msg) as midi_in:
        print("listening on " + port  + ". Press Control-C to exit.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print('')
    
print("closing..")
    
#close artnet output
del artnet
