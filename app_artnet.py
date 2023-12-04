import time
from stupidArtnet import StupidArtnet
from singleton import SingletonMeta
from concurrent.futures import ThreadPoolExecutor

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


class Artnet(metaclass=SingletonMeta):
    _artnet = None
    _pool = ThreadPoolExecutor(10)


    def __init__(self) -> None:
        target_ip = '255.255.255.255' # typically in 2.x or 10.x range
        universe = 0 				  # see docs
        packet_size = 64			  # it is not necessary to send whole universe
        self._artnet = StupidArtnet(target_ip, universe, packet_size, 60, True, True)
        print(self._artnet)
        self.reset()
    
    def __del__(self):
        self._artnet.blackout()
        self._artnet.stop()
        print("Artnet stopped")
        del self._artnet        

    def reset(self):
        self._artnet.blackout()
        for dmx_ch in fixture_setup:
            self._artnet.set_single_value(dmx_ch[0], dmx_ch[1])
        self._artnet.show()
        
    def blackout(self):
        self._artnet.blackout()
        self._artnet.show()
        
    def send(self, channel, value):
        self._artnet.set_single_value(channel, value)
        self._artnet.show()

    def _hadle_fadeout(self, channel, interval_ms):
        curr_value = self._artnet.buffer[channel-1]
        for i in range(curr_value, 0, -1):
            self._artnet.set_single_value(channel, i)
            self._artnet.show()
            time.sleep(interval_ms/1000)

    def fadeout(self, channel, interval_ms):
        self._pool.submit(self._hadle_fadeout, channel, interval_ms)

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




