from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


import time
from stupidArtnet import StupidArtnet
from threading import Timer
from fixtures import fixtures

## setup
artnet = None

# setup artnet
target_ip = '255.255.255.255' # typically in 2.x or 10.x range
universe = 0 				  # see docs
packet_size = 64			  # it is not necessary to send whole universe
artnet = StupidArtnet(target_ip, universe, packet_size, 60, True, True)
artnet.start()


## ArtNet functions -----------------------------------------------------------------
@app.get("/scene/{scene_id}")
def scene_play(scene_id):
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
    artnet_reset()

    # set scene
    for channel, value in scene_levels.items():
        artnet.set_single_value(channel, value)

    # wait for keyboard interrupt
    print("scene: " + scene_name, flush=True)


def artnet_reset():
    print("reset")
    global artnet
    for channel, fixture in fixtures.items():
        artnet.set_single_value(channel, fixture.default_value)
artnet_reset()

