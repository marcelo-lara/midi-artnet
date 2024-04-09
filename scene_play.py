#!/usr/bin/env python
import time
from stupidArtnet import StupidArtnet
from threading import Timer
from app.fixtures import fixtures

## setup
artnet = None

# setup artnet
target_ip = '255.255.255.255' # typically in 2.x or 10.x range
universe = 0 				  # see docs
packet_size = 64			  # it is not necessary to send whole universe
artnet = StupidArtnet(target_ip, universe, packet_size, 60, True, True)
artnet.start()


## ArtNet functions -----------------------------------------------------------------

def artnet_reset():
    print("reset")
    global artnet
    for channel, fixture in fixtures.items():
        artnet.set_single_value(channel, fixture.default_value)
artnet_reset()

scene_name = 'piano'
scene_levels = {
    
    ## left parcan
    16: 255,
    17: 64,
    19: 255,
    
    ## right parcan
    22: 255,
    23: 64,
    25: 255,
    
}





## Main -----------------------------------------------------------------
try:
    
    # set scene
    for channel, value in scene_levels.items():
        artnet.set_single_value(channel, value)

    # wait for keyboard interrupt
    print("scene: " + scene_name, flush=True)
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print('')
    
#close artnet output
print("blackout ..")
artnet.blackout()
artnet.stop()
