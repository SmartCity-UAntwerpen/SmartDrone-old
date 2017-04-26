from drone import Drone

list = []

def create_drone():
    list.append(Drone())

def remove_drone(id):
    for drone in list:
        if (drone.id==id):
            print ("Drone "+ str(drone.id)+" removed")
            list.remove(drone)

create_drone()
create_drone()
remove_drone(2)
for drone in list:
    print(drone)