import threading
import time
import serial
import socket

class GCStoFC (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print "Starting GCStoFC"
        global addr
        global sock
        global ser
        global whitelist
        whitelist= set()
        while True:
        	data_gcs_raw, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        	if(len(data_gcs_raw)>0):
        		data_gcs= ' :'.join( [ "%02X" % ord( x ) for x in data_gcs_raw ] )
        		#print "received GCS:", data_gcs
                datasplit=[]
                datasplit = data_gcs[data_gcs.find('3C'):].split(" :")
                topic =''.join(str(e) for e in datasplit[4:8])
                if (topic == 'DC5238D2' or topic == 'F4D44860' or topic == '00D5F582' or topic=='468F7E38'):
                    print (data_gcs)
                ##TODO Filter topic
                lenbefore= len(list(whitelist))
                whitelist.add(topic)
                if lenbefore<len(list(whitelist)):
                    print "topiclist lengte: ",len(list(whitelist)),"\ttopic", topic
                ser.write(data_gcs_raw)

class FCtoGCS(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Starting FCtoGCS"

        global sock
        global ser
        global data_fc
        data_fc=''
        while True:
            data_fc_raw = ser.readline()
            if (len(data_fc_raw)>0):
                if len(data_fc)>0:
           		    data_fc+= ' :'
               	data_fc+= ' :'.join( [ "%02X" % ord( x ) for x in data_fc_raw ] )
           	#print "received FC: ", data_fc
        	parseFCdata()

class whitelistwriter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global whitelist
        lenbefore=0
        while True:

            time.sleep(10)
            lenafter = len(list(whitelist))
            if lenbefore<lenafter:
                lenbefore=lenafter
                f = open('whitelist.txt', 'w')
                for line in list(whitelist):
                    f.write(line + '\n')
                f.close()
                print "Whitelist saved"

def parseFCdata():
    global data_fc
    global addr
    done = 0
    while (done == 0):
        datasplit = []
        if data_fc.find('3C')>0:
            print "Delete some data", data_fc[0:data_fc.find('3C')]
        datasplit = data_fc[data_fc.find('3C'):].split(" :")
        if len(datasplit) >= 13:
            lengte = int(datasplit[2], 16) + int(datasplit[3], 16) * 256
            topic = datasplit[4:8]
            # print "Topic: ", topic
            # print "Lengte ", lengte
            if lengte == 0:
                lengte = 300

            if lengte > 268:
                print "Lengte: ", lengte, " Delete some data", data_fc[0:data_fc.find('3C') + 4], "\nData: ", data_fc
                data_fc = data_fc[data_fc.find('3C') + 4:]
            elif len(datasplit) <= lengte + 1:
                done = 1
            else:
                ##TODO: check  crc
                tekst = "".join(datasplit[0:lengte + 1])
                getal = HexToByte(tekst)
                sock.sendto(getal, (addr))
                data_fc = data_fc[data_fc.find('3C') + lengte * 4 + 4:]
        else:
            done = 1
        #if done==1:
            #print "done: ",data_fc

def HexToByte( hexStr ):
	bytes = []
	hexStr = ''.join( hexStr.split(" ") )
	for i in range(0, len(hexStr), 2):
		bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
	return ''.join( bytes )

def initSerial():
    global ser
    ser = serial.Serial('/dev/ttyUSB0',57600)
    ser.timeout = 10
    print (ser.portstr)
def initSock():
    global sock
    #UDP_IP = "143.169.220.181"
    UDP_IP = "127.0.0.1"
    UDP_PORT = 9000
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))


initSerial()
initSock()
# Create new threads
gcstofc = GCStoFC()
fctogcs = FCtoGCS()
whitelistwriter = whitelistwriter()

# Start new Threads
data_gcs_raw, addr = sock.recvfrom(1024)
gcstofc.start()
fctogcs.start()
createWhitelist=1
if createWhitelist==1:
    whitelistwriter.start()