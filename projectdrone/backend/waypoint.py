"""Waypoints in backend are actually landing zones. Places where the drone will be able to land.
These are NOT the same waypoints used in the drone package. (TODO: waypoints in backend should be renamed)"""

class Waypoints:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0