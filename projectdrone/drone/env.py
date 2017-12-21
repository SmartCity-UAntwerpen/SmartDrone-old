
fly_height = -4.0
speed_takeoff = 2
speed_landing = 2
speed_horizontal = 1.5
settletime = 2

addrwaypoints = "http://143.129.39.151:10000/map/stringmapjson/drone"

addrnewid = "http://143.129.39.151:10000/bot/newBot/drone"
addrkillid = "http://143.129.39.151:10000/bot/delete"
addradvertise = "http://143.129.39.151:8082/advertise"
addrjobdone = "http://143.129.39.151:8090/completeJob"

mqttbroker = "143.129.39.151"
mqttusername = "root"
mqttpassword = "smartcity"
mqttport = 1883

mqttTopicJob = "drone/job"
mqttTopicJobdone = "drone/jobdone"
mqttTopicPos = "drone/pos"

tcpip="143.129.39.151"
tcpport=8888
restport=8082

haertbeattime = 10
haertbeattimedead = 60*60*0.5

homelat = 51.1785531
homelon = 4.4183511
homealt = 0

view_length = 3250 # view of camera in mm
view_width = 1700 # view of camera in mm
pixel_view_length = 640
pixel_view_width = 480
camera_height = 2400 #height of camera in mm




receive_timeout = 1.0 # 1 sec receive timeout

printNewPos = False

port = 'COM4'
#port = '/dev/ttyS0'
rate = 57600

standardspeedSimulation = 70

