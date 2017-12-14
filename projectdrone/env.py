import navpy


class env:
    fly_height = -4.0
    speed_takeoff = 2
    speed_landing = 2
    speed_horizontal = 1.5
    settletime = 2

    addrwaypoints = "http://smartcity.ddns.net:10000/map/stringmapjson/drone"

    addrnewid = "http://smartcity.ddns.net:10000/bot/newBot/drone"
    addrkillid = "http://smartcity.ddns.net:10000/bot/delete"
    addradvertise = "http://smartcity.ddns.net:8082/advertise"
    addrjobdone = "http://smartcity.ddns.net:8090/completeJob"

    mqttbroker = "smartcity.ddns.net"
    mqttusername = "root"
    mqttpassword = "smartcity"
    mqttport = 1883

    mqttTopicJob = "drone/job"
    mqttTopicJobdone = "drone/jobdone"
    mqttTopicPos = "drone/pos"

    tcpip="smartcity.ddns.net"
    tcpport=8888
    restport=8082

    haertbeattime = 10
    haertbeattimedead = 60*60*0.5

    homelat = 51.1785531
    homelon = 4.4183511
    homealt = 0

    receive_timeout = 1.0 # 1 sec receive timeout

    printNewPos = False

    port = 'COM4'
    #port = '/dev/ttyS0'
    rate = 57600

    standardspeedSimulation = 70

    def generatedNEDwaypoints(self):
        print (navpy.lla2ned(51.1785531, 4.4183511, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1784002, 4.4180879, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1783561, 4.4182861, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1787070, 4.4185652, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1787534, 4.4184587, 0, env.homelat, env.homelon, env.homealt))
