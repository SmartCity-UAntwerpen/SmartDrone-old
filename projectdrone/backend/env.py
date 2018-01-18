# Parameters for calculation
fly_height = 500
speed_takeoff = 2000
speed_landing = 2000
speed_horizontal = 1500
settletime = 2

# REST
restport = 8082
addrwaypoints = "http://smartcity.ddns.net:10000/map/stringmapjson/drone"
addrnewid = "http://smartcity.ddns.net:10000/bot/newBot/drone"
addrkillid = "http://smartcity.ddns.net:10000/bot/delete"
addradvertise = "http://smartcity.ddns.net:8082/advertise"
addrjobdone = "http://smartcity.ddns.net:8090/completeJob"

# MQTT
mqttbroker = "smartcity.ddns.net"
mqttusername = "root"
mqttpassword = "smartcity"
mqttport = 1883
mqttTopicJob = "drone/job"
mqttTopicJobdone = "drone/jobdone"
mqttTopicPos = "drone/pos"

# Heartbeat
haertbeattime = 10
haertbeattimedead = 30  # 30 seconds
