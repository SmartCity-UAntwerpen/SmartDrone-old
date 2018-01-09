
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

D_x = 4900 # distance of view of camera in mm
D_y = 3170 # distance of view of camera in mm
PS_x = 0 #Pixel Start x
PS_y = 0 # Pixel start y
PE_x = 640 # Pixel End on x-as (highest x pixel)
PE_y = 480 # Pixel End
dx = PE_x - PS_x # x pixel distance
dy = PE_y - PS_y # y pixel distance
Rx = D_x / dx # x Ratio: mm/pixel
Ry = D_y / dy # y Ratio: mm/pixel

pixel_view_width = 225
camera_height = 2450 #height of camera in mm




receive_timeout = 1.0 # 1 sec receive timeout

printNewPos = False

port = 'COM4'
#port = '/dev/ttyS0'
rate = 57600

standardspeedSimulation = 70

