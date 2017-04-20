from mqtt import mqtt
import time

mqttclient=mqtt("iot.eclipse.org",1883,"Drone", "test")

def publish():
    mqttclient.publish("test", "I like "+str(1));


#Connecteer met Mqtt Host
def start_mqtt_listener():
    mqttclient.connect()
    mqttclient.add_listener_func(mqtt_recieve)

#Wordt opgeroepen wanneer er een Mqtt bericht binnenkomt
def mqtt_recieve(msg):
    print(msg)
    if (msg == "I like 1"):
        print("1")

start_mqtt_listener()


publish()
time.sleep(0.1)