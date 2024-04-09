from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

## app 
from stupidArtnet import StupidArtnet
from fixtures import fixtures

# setup artnet
artnet = None
target_ip = '255.255.255.255' # typically in 2.x or 10.x range
universe = 0 				  # see docs
packet_size = 64			  # it is not necessary to send whole universe
artnet = StupidArtnet(target_ip, universe, packet_size, 60, True, True)

# web server
app = FastAPI()

@app.get("/dmx/reset")
def read_item():
    print("reset")
    global artnet
    artnet.start()

    for channel, fixture in fixtures.items():
        artnet.set_single_value(channel, fixture.default_value)
    return {"status": "ok"}

@app.get("/dmx/play")
def play_scene():
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
    global artnet
    for channel, value in scene_levels.items():
        artnet.set_single_value(channel, value)
    return {"status": "ok"}

@app.get("/dmx/close")
def artnet_close():
    global artnet
    print("blackout ..")
    artnet.blackout()
    artnet.stop()
    return {"status": "ok"}


# static web server
app.mount("/", StaticFiles(directory="./www",html = True))
