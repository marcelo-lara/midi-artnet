# Description: Fixture definitions for the DMX controller
class Channel:
    name:str = ""
    number:int = 0
    default_value:int = 0
    
    def __init__(self, name:str, number:int, default_value:int = 0):
        self.name = name
        self.number = number
        self.default_value = default_value
        
# fixture setup
fixtures = {
    1: Channel("Head X pos", 1),
    2: Channel("Head X-Fine Pos", 2),
    3: Channel("Head Y Pos", 3),
    4: Channel("Head Y-Fine Pos", 4),
    5: Channel("Head XY Speed", 5),
    6: Channel("Head Dimmer", 6),
    7: Channel("Head Shutter", 7, 255),
    8: Channel("Head Color Wheel", 8),
    9: Channel("Head Gobo Wheel", 9),
    10: Channel("Head AutoPlay", 10),
    11: Channel("Head NC_XY_autorun", 11),
    12: Channel("Head Reset", 12),
    
    16: Channel("Parcan Left Light", 16, 255),
    17: Channel("Parcan Left Red", 17),
    18: Channel("Parcan Left Grreen", 18),
    19: Channel("Parcan Left Blue", 19),
    20: Channel("Parcan Left Strobe", 20),
    21: Channel("Parcan Left AutoColor", 21),
    
    22: Channel("Parcan Right Light", 22, 255),
    23: Channel("Parcan Right Red", 23),
    24: Channel("Parcan Right Grreen", 24),
    25: Channel("Parcan Right Blue", 25),
    26: Channel("Parcan Right Strobe", 26),
    27: Channel("Parcan Right AutoColor", 27),
}
