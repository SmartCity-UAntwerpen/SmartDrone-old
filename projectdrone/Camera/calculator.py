#!usr/bin/python3.5

# Calculates X Y and yaw angle of quadcopter based on given [X,Y]coordinates of 3 known calibration points located on the drone (=infrared leds)
# Calculates the coordinate of the middle between the 2 outer coordinates
# Calculates the degree of the angle (yaw) according to a vertical line drawn through the middle ranges from [0 360]
import math

def get_middle(x1,y1,x2,y2):
    x_m = (x1 + x2) / 2                         # X coordinate of drone middle
    y_m = (y2 + y2) / 2                         # Y coordinate of drone middle
    
    return x_m, y_m;
    

def get_yaw(x1,y1,x2,y2):
    x_diff = x1 - x2
    y_diff = y1 - y2
    yaw = math.degrees(math.atan2(y_diff, x_diff))

    if yaw < 0:                                 # Check for negatives, we want range [0 360] degrees
        yaw += 360

    yaw += 90                                   # turn 90 degrees so that the angle is viewed from a vertical line

    if yaw >= 360:                              # normalize to [0 360] degrees
        yaw -= 360
        
    return yaw


def calculate(coordinates):
    if len(coordinates) == 6:
        if coordinates[0] == -1 or coordinates[1] == -1: # 0 points given
            x_m = -1
            y_m = -1
            yaw = -1
        elif coordinates[2] == -1 or coordinates[3] == -1: # only 1 point given
            x_m = coordinates[0]
            y_m = coordinates[1]
            yaw = -1
        elif coordinates[4] == -1 or coordinates[5] == -1: # only 2 points given
           x_m, y_m = get_middle(coordinates[0],coordinates[1],coordinates[2],coordinates[3])
           yaw = get_yaw(coordinates[0],coordinates[1],coordinates[2],coordinates[3])
        else: # 3 points given
           x_m, y_m = get_middle(coordinates[0],coordinates[1],coordinates[4],coordinates[5])
           yaw = get_yaw(coordinates[0],coordinates[1],coordinates[4],coordinates[5])
        
        return str(int(x_m)) + ';' + str(int(y_m)) + ';' + str(int(yaw))
    
    print('Array not 6 long!')
    return str(-1) + ';' + str(-1) + ';' + str(-1)
