from projectdrone.drone.dronecomms import *
import unittest


# note - this test requires a flightcontroller attached to succeed
# note - if wrong com port in env this will cause test failure aswell
class testdroneComms(unittest.Testcase):

    def waypointTest(self):
        instance = 0x00
        north = 5.50
        east = 3.30
        down = 4.40
        velocity = 2.20
        waypoint = Waypoint(instance, north, east, down, velocity)
        set_waypoint(waypoint)
        waypoint_received = Waypoint.get_instance(instance)
        # dangerous to compare object instances - compare field equality
        self.assertEquals(waypoint_received.instance, instance)
        self.assertEquals(waypoint_received.north, north)
        self.assertEquals(waypoint_received.east, east)
        self.assertEquals(waypoint_received.down, down)
        self.assertEquals(waypoint_received.velocity == velocity)
        return
