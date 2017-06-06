class env:
    fly_height = -4.0
    speed_takeoff = 0.5
    speed_landing=0.5
    speed_horizontal=1
    settletime=2

    #addrwaypoints="http://143.129.39.151:10000/map/stringmapjson/drone"
    addrwaypoints="http://127.0.0.1:8082/fakewaypoints"

    addrnewid= "http://143.129.39.151:10000/bot/newBot/drone"
    addrkillid="http://143.129.39.151:10000/delete"

    addradvertise="http://127.0.0.1:8082/advertise"
    bedugaddrnewid = True

    addrjobdone=""

    mqttbroker="143.129.39.151"
    #mqttbroker="iot.eclipse.org"#"smartcity-ua.ddns.net"    mqttport=1883
    mqttusername="root"
    mqttpassword="smartcity"
    mqttport=1883

    mqttTopicJob="drone/job"
    mqttTopicJobdone="drone/jobdone"
    mqttTopicPos="drone/pos"

    tcpport=8888
    restport=8082

    haertbeattime = 10
    haertbeattimedead = 60*60*24

    homelat = 51.1785531
    homelon = 4.4183511
    homealt = 0

    printNewPos = False

    port = 'COM4'
    rate = 57600

    standardspeedSimulation=70

    printNewPos = False
