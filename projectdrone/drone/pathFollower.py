""" The pathfollower module checks continously if the drone is at the desired position.
When this is the case the next waypoint can be changed."""
import time


class Pathfollower:
    def __init__(self, droneparameters):
        self.droneparameters = droneparameters

    def check_position(self):
        isArrived = False
        while not isArrived:
            # checks if drone is within threshold of target waypoint
            if self.check_drone_proximity(self.droneparameters.targetWP):  # checks of drone is at the target waypoint
                if self.check_drone_proximity(self.droneparameters.path[len(
                        self.droneparameters.path) - 1]):  # checks if drone is at destination waypoint (= last waypoint in path list)
                    isArrived = True
                    print("JOB COMPLETED: AT DESTINATION")
                    self.droneparameters.onJob = False
                    self.droneparameters.path = []
                    self.droneparameters.targetWP.X = None
                    self.droneparameters.targetWP.Y = None
                    self.droneparameters.targetWP.Z = None
                    self.droneparameters.currentwaypointID = 0
                    self.droneparameters.state = 0
                else:
                    print("ARRIVED AT WAYPOINT, USING NEXT ONE")
                    self.droneparameters.currentwaypointID += 1
                    self.droneparameters.targetWP = self.droneparameters.path[self.droneparameters.currentwaypointID]
            time.sleep(2)

    # TODO insert right threshold values.
    def check_drone_proximity(self, waypoint):
        print("Waypoint XYZ: " + str(waypoint.X) + " - " + str(waypoint.Y) + " - " + str(waypoint.Z))
        if waypoint.X - 50 <= self.droneparameters.X <= waypoint.X + 50 \
                and waypoint.Y - 50 <= self.droneparameters.Y <= waypoint.Y + 50 \
                and waypoint.Z - 50 <= self.droneparameters.Z <= waypoint.Z + 50:
            return True
        else:
            return False
