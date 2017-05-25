class env:
    fly_height = 4
    speed_takeoff = 0.5
    speed_landing=0.5
    speed_horizontal=1
    settletime=2

    addrwaypoints="http://146.175.140.44:1994/map/stringmapjson/drone"
    addrnewid= "http://146.175.140.44:1994/bot/newBot/drone"

    mqttbroker="iot.eclipse.org"#"smartcity-ua.ddns.net"
    mqttport=1883
    mqttusername="root"
    mqttpassword="smartcity"

    tcpport=8888