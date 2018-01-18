class DroneParameters:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

        self.busy = 0

        self.percentage = 100
        self.idStart = -1
        self.idEnd = -1
        self.idNext = -1
        self.idJob = 0

        self.timestamp = 0
        self.available = 1
        self.simdrone = 0
        self.speedfactor = 1.0

    def kill(self):
        del self
