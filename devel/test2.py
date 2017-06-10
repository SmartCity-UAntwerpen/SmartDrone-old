import time
import projectdrone.UAV.PathActions as pa
import projectdrone.drone.dronecomms as dc
from projectdrone.UAV.Pathaction import Pathaction
from projectdrone.drone.dronecomms import *

# load pathactions & waypoints to drone
# load pathactions & waypoints to drone
pathactions = [Pathaction(0x00, pa.PATHACTION_MODE_FOLLOWVECTOR, pa.PATHACTION_ENDCONDITION_ABOVEALTITUDE,
                          pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT,
                          condition_parameters=[env.fly_height, 0.0, 0.0, 0.0]),
               Pathaction(0x01, pa.PATHACTION_MODE_FOLLOWVECTOR, pa.PATHACTION_ENDCONDITION_LEGREMAINING,
                          pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT),
               Pathaction(0x02, pa.PATHACTION_MODE_GOTOENDPOINT, pa.PATHACTION_ENDCONDITION_TIMEOUT,
                          pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT,
                          condition_parameters=[env.settletime, 0.0, 0.0, 0.0]),
               Pathaction(0x03, pa.PATHACTION_MODE_LAND, pa.PATHACTION_ENDCONDITION_NONE,
                          pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT)]
waypoints = [Waypoint(0x00, 0.0, 0.0, env.fly_height, env.speed_takeoff, 0x00),
             Waypoint(0x01, 15.20, 8.20, env.fly_height, env.speed_horizontal, 0x01),
             Waypoint(0x02, 15.20, 8.20, env.fly_height, env.speed_landing, 0x02),
             Waypoint(0x03, 15.20, 8.20, 0.0, env.speed_landing, 0x03)]
for pathaction in pathactions:
    dc.set_pathaction(pathaction)
for waypoint in waypoints:
    dc.set_waypoint(waypoint)
dc.set_pathplan(len(waypoints), len(pathactions))
while 1:
    print dc.get_pathaction_active()
    print dc.get_position()
    time.sleep(1)
