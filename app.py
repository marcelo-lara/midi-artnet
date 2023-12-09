#!/usr/bin/env python
import sys
import time
import mido
from stupidArtnet import StupidArtnet
from threading import Timer

# fixture setup
fixture_setup = [
    #Head EL150
    [1,  0,  "X pos"],
    [2,  0,  "X-Fine Pos"],
    [3,  0,  "Y Pos"],
    [4,  0,  "Y-Fine Pos"],
    [5,  0,  "XY Speed"],
    [6,  0,  "Dimmer"],
    [7,  255,  "Shutter"],
    [8,  0,  "Color Wheel"],
    [9,  0,  "Gobo Wheel"],
    [10, 0,  "AutoPlay"],
    [11, 0,  "NC_XY_autorun"],
    #[12, 0,  "Reset"],
    
    # Parcan Left
    [16, 255, "Light"],
    [17, 0, "Red"],
    [18, 0, "Grreen"],
    [19, 0, "Blue"],
    [20, 0, "Strobe"],
    [21, 0, "AutoColor"],

    # Parcan Left
    [22, 255, "Light"],
    [23, 0, "Red"],
    [24, 0, "Grreen"],
    [25, 0, "Blue"],
    [26, 0, "Strobe"],
    [27, 0, "AutoColor"],
]

def artnet_blackout():
    global _timer
    if _timer != None:
        _timer.cancel()
        _timer = None
        
    global artnet
    artnet.blackout()
    artnet.start()

def artnet_reset():
    artnet_blackout()
    global artnet
    for dmx_ch in fixture_setup:
        artnet.set_single_value(dmx_ch[0], dmx_ch[1])

def _fade_handler(ch:int, value:int, interval_ms:int):
    global _timer
    if value < 0:
        _timer.cancel()
        _timer = None
        return

    #send value
    global artnet
    artnet.set_single_value(ch, value)

    # set next timer    
    _timer = Timer((interval_ms/1000), _fade_handler, args=[ch, value-1, interval_ms])
    _timer.daemon = True
    _timer.start()

def artnet_fadeout(channel:int, interval_ms:int):
    
    #cancel previous fader
    global _timer
    if _timer != None:
        _timer.cancel()
        _timer = None

    #trigger fadeout        
    curr_value = artnet.buffer[channel-1]
    _fade_handler(channel, curr_value, interval_ms)


## setup
artnet = None
_timer = None

# open midi port
port = "loopMIDI Port 0"
midi_multiplier = 255/126

# setup artnet
target_ip = '255.255.255.255' # typically in 2.x or 10.x range
universe = 0 				  # see docs
packet_size = 64			  # it is not necessary to send whole universe
artnet = StupidArtnet(target_ip, universe, packet_size, 60, True, True)
artnet.start()
artnet_reset()

def handle_msg(msg):
    if msg.type in ["note_off", "songpos", "clock", "control_change"]: return
    global artnet

    match msg.type:
        case "note_on":
            if msg.note > 80: 
                print("note_on: " + str(msg.note) + " " + str(msg.velocity))
                return
            dmx_val = int((msg.velocity-1)*midi_multiplier)
            dmx_ch = msg.note+1
            
            if msg.note > 35:
                dmx_ch = dmx_ch - 36
                interval = (12.7*2)-(msg.velocity/5)
                # print("fadeout: " + str(dmx_ch) + " " + str(interval))
                artnet_fadeout(dmx_ch, interval)
                return
            
            #direct send artnet
            artnet.set_single_value(dmx_ch, dmx_val)

        case "stop":
            print("stop")
            artnet_blackout()

        case "start":
            print("start")
            artnet_reset()

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
artnet_blackout()
artnet.stop()
