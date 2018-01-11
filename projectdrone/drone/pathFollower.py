""" The pathfollower module checks continously if the drone is at the desired position.
When this is the case the next waypoint can be changed."""


class Pathfollower:

    def __init__(self, droneparameters):
        self.droneparameters = droneparameters

    def check_position(self):
        # checks if drone is within threshold of target waypoint
        if self.check_drone_proximity(self.droneparameters.targetWP):   # checks of drone is at the target waypoint
            if self.check_drone_proximity(self.droneparameters.path[len(self.droneparameters.path)-1]):    # checks if drone is at destination waypoint (= last waypoint in path list)
                # TODO job done: MQTT
                print("JOB COMPLETED: AT DESTINATION")
                self.droneparameters.onJob = False
                self.droneparameters.path = []
                self.droneparameters.targetWP.X = None
                self.droneparameters.targetWP.Y = None
                self.droneparameters.targetWP.Z = None
                self.droneparameters.currentwaypointID = None
                self.droneparameters.state = 0
            else:
                self.droneparameters.currentwaypointID += 1
                self.droneparameters.targetWP = self.droneparameters.path[self.droneparameters.currentwaypointID]

    #TODO insert right threshhold values.
    def check_drone_proximity(self, waypoint):
        if waypoint.X - 200 <= self.droneparameters.X <= waypoint.X + 200 \
                and waypoint.Y - 200 <= self.droneparameters.Y <= waypoint.Y + 200 \
                and waypoint.Z - 30 <= self.droneparameters.Z <= waypoint.Z + 100:
            return True
        else:
            return False
