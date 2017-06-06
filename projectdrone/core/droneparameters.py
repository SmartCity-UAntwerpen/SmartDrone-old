
class DroneParameters:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0
        self.job=0
        self.buzy=0
        self.percentage=100
        self.idStart=0
        self.idEnd=0
        self.idJob=0
        self.timestamp=0
        self.available=1
        self.simdrone=0
        self.speedfactor=1.0
    def kill(self):
        del self
