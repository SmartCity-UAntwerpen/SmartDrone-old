class Waypoint:
    def __init__(self, instance, north, east, down, velocity, action=0x00):
        self.object_id = 0xD23852DC
        self.instance = instance
        self.north = north
        self.east = east
        self.down = down
        self.velocity = velocity
        self.action = action
