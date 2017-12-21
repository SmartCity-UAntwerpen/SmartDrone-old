"""The plathplanner takes the job from the backend en translates it to a path (=a list of waypoints) that the drone should fly to
in order to reach the destination."""
from projectdrone.drone import waypoint


def plan_path(droneparameters, destinationWP):
    above_takeoffWP = waypoint.Waypoint(droneparameters.X, droneparameters.Y, 1000) #height of 1000mm, change desired flight height here
    above_destinationWP = waypoint.Waypoint(destinationWP.X, destinationWP.Y, 1000)
    destinationWP = waypoint.Waypoint(destinationWP.X, destinationWP.Y, destinationWP.Z)
    droneparameters.path = {above_takeoffWP, above_destinationWP, destinationWP} # creates the whole path of waypoints
    droneparameters.targetWP = droneparameters.path[0] #sets the target waypoint to the first waypoint of the path
    droneparameters.onJob = True
