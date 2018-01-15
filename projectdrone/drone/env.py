import math

fly_height = -4.0
speed_takeoff = 2
speed_landing = 2
speed_horizontal = 1.5
settletime = 2

addrwaypoints = "http://smartcity.ddns.net:10000/map/stringmapjson/drone"

addrnewid = "http://smartcity.ddns.net:10000/bot/newBot/drone"
addrkillid = "http://smartcity.ddns.net:10000/bot/delete"
addradvertise = "http://172.16.0.12:8082/advertise"
addrjobdone = "http://smartcity.ddns.net:8090/completeJob"

mqttbroker = "smartcity.ddns.net"
mqttusername = "root"
mqttpassword = "smartcity"
mqttport = 1883

mqttTopicJob = "drone/job"
mqttTopicJobdone = "drone/jobdone"
mqttTopicPos = "drone/pos"

# for simulation
tcpip="smartcity.ddns.net"
tcpport=8888

restport=8082

haertbeattime = 10
haertbeattimedead = 60*60*0.5

homelat = 51.1785531
homelon = 4.4183511
homealt = 0


# calculations for pitch and roll of camera when enough space is available to measure the entire camera view
# x_DIS1 = 2200 # distance between under camera (on ground) and edge of view on x-axis where pixel coordinate = 0
# x_DIS2 = 2650 # distance between under camera (on ground) and edge of view on x-axis where pixel coordinate = 640
# x_DIS = x_DIS1 + x_DIS2 # total distance of view of camera in mm on x-axis
# y_DIS1 = 1440 # distance between under camera (on ground) and edge of view on y-axis where pixel coordinate = 0
# y_DIS2 = 1630 # distance between under camera (on ground) and edge of view on y-axis where pixel coordinate = 480
# y_DIS = y_DIS1 + y_DIS2 # total distance of view of camera in mm
# dx = 640 # x pixel distance = camera resolution
# dy = 480 # y pixel distance
# CAM_height = 2060 #height of camera in mm
# x_alpha = math.atan2(x_DIS1, CAM_height) # angle over x_DIS1
# x_beta = math.radians(100) - x_alpha # total angle over x-axis is 100 degrees: proven by experiment
# y_alpha = math.atan2(y_DIS1, CAM_height) # angle over y_DIS1
# y_beta = math.radians(75) - y_alpha # total angle over y-axis is 75 degrees: proven by experiment

# calculations for pitch and roll of camera when not enough space is available to measure the entire camera view
# explanation of calculation can be found in documentation
# V.313 corridor setup (battery facing the door) - 15/01/2018
CAM_height = 2450
dx = 640  # x pixel distance = camera resolution
dy = 480  # y pixel distance
x_SDW = 800  # short distance from point under camera to wall
x_H = 1720  # height on wall from ground to end of camera view on the side where X_SDW was measured
x_beta1 = math.atan2(x_SDW, CAM_height)  # tangent definition
x_alpha1 = x_beta1
x_S = math.sqrt( math.pow(CAM_height,2) + math.pow(x_SDW,2 ) )  # pythagoras
x_L = math.sqrt( math.pow(x_S,2) + math.pow(x_H,2) - 2 * x_S * x_H * math.cos(x_beta1) )  # law of cosines
x_beta2 = math.acos( (math.pow(x_H,2) - math.pow(x_L, 2) - math.pow(x_S,2)) / (-2 * x_L * x_S) )
x_alpha2 = math.radians(100) - x_alpha1 - x_beta1 - x_beta2

y_SDW = 1830  # short distance from point under camera to wall
y_H = 0  # height on wall from ground to end of camera view on the side where Y_SDW was measured
y_beta1 = math.atan2(y_SDW, CAM_height)
y_alpha1 = y_beta1
y_S = math.sqrt( math.pow(CAM_height,2) + math.pow(y_SDW,2 ) )
y_L = math.sqrt( math.pow(y_S,2) + math.pow(y_H,2) - 2 * y_S * y_H * math.cos(y_beta1) )
y_beta2 = math.acos( (math.pow(y_H,2) - math.pow(y_L, 2) - math.pow(y_S,2)) / (-2 * y_L * y_S) )
y_alpha2 = math.radians(75) - y_alpha1 - y_beta1 - y_beta2

x_alpha = x_alpha1 + x_alpha2
x_beta = x_beta1 + x_beta2
y_alpha = y_alpha1 + y_alpha2
y_beta = y_beta1 + y_beta2

print("xalpha, xbeta, yalpha, ybeta: " + str(math.degrees(x_alpha)) + ", " + str(math.degrees(x_beta)) + ", " + str(math.degrees(y_alpha)) + ", " + str(math.degrees(y_beta)))


receive_timeout = 1.0 # 1 sec receive timeout

printNewPos = False

port = 'COM4'
#port = '/dev/ttyS0'
rate = 57600

standardspeedSimulation = 70

