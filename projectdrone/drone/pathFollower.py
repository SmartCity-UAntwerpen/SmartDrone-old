""" The pathfollower module checks continously if the drone is at the desired position.
When this is the case the next waypoint can be changed."""


class Pathfollower:

    def __init__(self, droneparameters):
        self.droneparameters = droneparameters

    def check_position(self): #TODO insert right threshold values
        # checks if drone is within threshold of target waypoint
        if self.check_drone_proximity(self.droneparameters.targetWP):   # checks of drone is at the target waypoint
            if self.check_drone_proximity(self.droneparameters.path[len(self.droneparameters.path)]):    # checks if drone is at destination waypoint
                # TODO job done
                print("JOB COMPLETED: AT DESTINATION")
                self.droneparameters.onJob = False
                self.droneparameters.path = []
                self.droneparameters.targetWP.X = self.droneparameters.X
                self.droneparameters.targetWP.Y = self.droneparameters.Y
                self.droneparameters.targetWP.Z = self.droneparameters.Z
                self.droneparameters.currentwaypointID = 0
            else:
                self.droneparameters.currentwaypointID += 1
                self.droneparameters.targetWP = self.droneparameters.path[self.droneparameters.currentwaypointID]

    def check_drone_proximity(self, waypoint):
        if waypoint.X - 50 <= self.droneparameters.X <= waypoint.X + 50 \
                and waypoint.Y - 50 <= self.droneparameters.Y <= waypoint.Y \
                and waypoint.Z - 20 <= self.droneparameters.Z <= waypoint.Z:
            return True
        else:
            return False
