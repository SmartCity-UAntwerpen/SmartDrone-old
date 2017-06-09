class env:
    fly_height = -4.0
    speed_takeoff = 2
    speed_landing = 2
    speed_horizontal = 1.5
    settletime = 2

    addrwaypoints = "http://143.129.39.151:10000/map/stringmapjson/drone"
    #addrwaypoints="http://127.0.0.1:8082/fakewaypoints"

    addrnewid = "http://143.129.39.151:10000/bot/newBot/drone"
    bedugaddrnewid = False
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

    tcpport=8888
    restport=8082

    haertbeattime = 10
    haertbeattimedead = 60*60*0.5

    homelat = 51.1785531
    homelon = 4.4183511
    homealt = 0

    printNewPos = False

    #port = 'COM3'
    port = '/dev/ttyS0'
    rate = 57600

    standardspeedSimulation = 70
