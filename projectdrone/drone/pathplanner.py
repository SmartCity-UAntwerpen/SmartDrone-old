"""The plathplanner takes the job from the backend en translates it to a path (=a list of waypoints) that the drone should fly to
in order to reach the destination."""
import waypoint


def plan_path(droneparameters, destinationWP):
    above_takeoffWP = waypoint.Waypoint(droneparameters.X, droneparameters.Y, 200) # height of 20cm, change desired flight height here
    above_destinationWP = waypoint.Waypoint(destinationWP.X, destinationWP.Y, 200) # height of 20cm, change desired flight height here
    destinationWP = waypoint.Waypoint(destinationWP.X, destinationWP.Y, destinationWP.Z)
    droneparameters.path = [above_takeoffWP, above_destinationWP, destinationWP] # creates the whole path of waypoints
    droneparameters.targetWP = droneparameters.path[0] # sets the target waypoint to the first waypoint of the path
    print("targetWP: " + str(droneparameters.targetWP.X) + " - " + str(droneparameters.targetWP.Y) + " - " + str(droneparameters.targetWP.Z))
    droneparameters.onJob = True
