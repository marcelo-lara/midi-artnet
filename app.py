#!/usr/bin/env python
import time
import mido
from stupidArtnet import StupidArtnet
from threading import Timer
from fixtures import fixtures
from app_settings import getLoopbackInterface

## setup
artnet = None
_timers = {}
_, port = getLoopbackInterface()

# open midi port
midi_multiplier = 255/126

# setup artnet
target_ip = '255.255.255.255' # typically in 2.x or 10.x range
universe = 0 				  # see docs
packet_size = 64			  # it is not necessary to send whole universe
artnet = StupidArtnet(target_ip, universe, packet_size, 60, True, True)
artnet.start()

## ArtNet functions -----------------------------------------------------------------
def clear_timers():
    global _timers
    for _, timer in _timers.items():
        timer.cancel()
    _timers = {}

def artnet_blackout():
    clear_timers()
            
    global artnet
    artnet.blackout()
    artnet.start()

def artnet_reset():
    print("reset")
    artnet_blackout()
    global artnet
    for channel, fixture in fixtures.items():
        artnet.set_single_value(channel, fixture.default_value)

def _fade_handler(ch:int, value:int, interval_ms:int):
    global _timers
    if value < 0: 
        _timers[ch].cancel()
        del _timers[ch]
        return

    #send value
    global artnet
    artnet.set_single_value(ch, value)

    # define speed
    step = 1
    if interval_ms < 2: step = 3

    # set next timer    
    _timers[ch] = Timer((interval_ms/1000), _fade_handler, args=[ch, value-step, interval_ms])
    _timers[ch].daemon = True
    _timers[ch].start()

def artnet_fadeout(channel:int, interval_ms:int):
    
    #cancel previous fader
    global _timers
    if channel in _timers:
        _timers[channel].cancel()
        del _timers[channel]

    #trigger fadeout        
    curr_value = artnet.buffer[channel-1]
    _fade_handler(channel, curr_value, interval_ms)



artnet_reset()

## Midi functions -----------------------------------------------------------------
def handle_msg(msg):
    if msg.type in ["note_off", "control_change"]: return
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
            print("stop", flush=True)
            artnet_reset()

        case "start":
            print("start", flush=True)
            artnet_reset()

        case "clock":
            print("clock:" + str(msg.pos), flush=True)

        case _:     
            print(msg, flush=True)

## Main -----------------------------------------------------------------
try:
    with mido.open_input(port, callback=handle_msg) as midi_in:
        print("listening on " + port  + ". Press Control-C to exit.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print('')
    
#close artnet output
print("closing..")
artnet_blackout()
artnet.stop()
