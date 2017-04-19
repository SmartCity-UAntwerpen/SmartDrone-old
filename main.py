import serial
import socket
import thread

UDP_IP = "143.169.219.43"
UDP_IP = "127.0.0.1"
UDP_PORT = 9000

sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

#print "blacklist"
for line in open('blacklist.txt','r'):
	print line





def parseFCdata():
	global data_fc
	done=0
	while (done==0):
		datasplit=[]
		datasplit=data_fc[data_fc.find('3C'):].split(" :")
		if len(datasplit)>=13:
			lengte = int(datasplit[2],16)+int(datasplit[3],16)*256
			topic = datasplit[4:8]
			#print "Topic: ", topic
			#print "Lengte ", lengte
			if lengte ==0:
				lengte=300
			
			if lengte >268:
				print "Lengte: ", lengte, " Delete some data", data_fc[0:data_fc.find('3C')+4], "\nData: ",data_fc
				data_fc=data_fc[data_fc.find('3C')+4:]
			elif len(datasplit)<=lengte+1:
				done=1
			else:		
				##TODO: check  crc
				tekst="".join(datasplit[0:lengte+1])
				print "Export to GCS"
				getal= HexToByte(tekst)
				sock.sendto(getal, (addr))
				data_fc=data_fc[data_fc.find('3C')+lengte*4+4:]
		else:
			done=1
	#print "done: " ,data_fc

def HexToByte( hexStr ):
	bytes = []
	hexStr = ''.join( hexStr.split(" ") )
	for i in range(0, len(hexStr), 2):
		bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
	return ''.join( bytes )

def GCStoFC():
	print "start thread GCStoFC"
	#ser = serial.Serial('/dev/ttyACM0',57600)
	#ser = serial.Serial('/dev/ttyUSB0',57600)
	#ser.timeout = 10
	#print (ser.portstr)
	#global addr
	#global sock
	#while True:
	#	data_gcs_raw, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	#	if(len(data_gcs_raw)>0):
	#		data_gcs=':'.join(hex(ord(x))[2:] for x in data_gcs_raw)
	#		print "received GCS:", data_gcs
			##TODO Filter topic
	#		ser.write(data_gcs_raw)

def FCtoGCS():
	print "start thread FCtoGCS"
	#ser = serial.Serial('/dev/ttyACM0',57600)
	#ser = serial.Serial('/dev/ttyUSB0',57600)
	#ser.timeout = 10
	#print (ser.portstr)
	#global sock
	#while True:
	#	data_fc_raw = ser.readline()
	#	if (len(data_fc_raw)>0):
	#		if len(data_fc)>0:
	#			data_fc+= ' :'
	#		data_fc+= ' :'.join( [ "%02X" % ord( x ) for x in data_fc_raw ] )
	#		print "received FC:", data_fc
	#		parseFCdata()
import time
def print_time( threadName):
   count = 0
   while count < 5:
      #time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, "test" )

data_fc=""
try:
	print "start threads"
	thread.start_new_thread(print_time, ("Thread-1",))

	#thread.start_new_thread( GCStoFC, ( ) )
	#thread.start_new_thread( FCtoGCS, ( ) )
	print "started threads"
except:
   print "Error: unable to start thread"

	
	

#ser.close()