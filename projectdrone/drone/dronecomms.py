from projectdrone.UAV.Pathplan import Pathplan
from projectdrone.UAV.AcuatorDesired import ActuatorDesired
from projectdrone.UAV.GPSPostitionSensor import GPSPositionSensor
from projectdrone.UAV.LibrePilotSerial import *
from projectdrone.UAV.WaypointActive import WaypointActive
from projectdrone.UAV.Waypoint import Waypoint
from projectdrone.UAV import object_ids


# create a new waypoint
def set_waypoint(waypoint):
    data = waypoint.package()
    send(waypoint.object_id, waypoint.instance, data, len(data))


# add a pathaction - note PathActions.py for more info on options
def set_pathaction(pathaction):
    data = pathaction.package()
    send(pathaction.object_id, pathaction.instance, data, len(data))


# update the pathplan
def set_pathplan(waypointcount, pathactioncount):
    object_id = object_ids.pathplan
    data = Pathplan(waypointcount, pathactioncount).package()
    send(object_id, 0x00, data, len(data))


# get the current thrust value
def get_thrust():
    actuator_desired = ActuatorDesired.get_instance()
    thrust = actuator_desired.thrust
    return thrust


# get the position
def get_position():
    sensordata = GPSPositionSensor.get_instance()
    return [sensordata.latitude, sensordata.longitude,  sensordata.altitude]


# get the current amount of waypoints
def get_waypoint_count():
    pathplan = Pathplan.get_instance()
    waypoint_count = pathplan.waypoint
    return waypoint_count


# get the active waypoint
def get_waypoint_active():
    waypoint_active = WaypointActive.get_instance().waypointActive
    return waypoint_active


# get the current pathaction
def get_pathaction_active():
    waypoint_active = WaypointActive.get_instance().waypointActive
    waypoint = Waypoint.get_instance(waypoint_active)  # get the currently active waypoint
    return waypoint.action

