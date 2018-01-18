CC=/home/lubuntu/rpi/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-g++ -std=c++1y
APP_BINARY=rpi-irpos-template
REMOTE_SERVER=pi@172.16.0.200
REMOTE_PATH=/home/pi
REMOTE_PASS='raspberry'
ML=/home/lubuntu/minimod/Libs/
ML_ROB=/home/lubuntu/robotica/lib/
ML_RPI=/home/lubuntu/rpi-cp/
LOGFILE='log.csv'

CFLAGS += -g -DLINUX -Wall -I$(ML) -I. -I$(ML_RPI)usr/local/include -std=c++11
LFLAGS += -lpthread  -Wl,-unresolved-symbols=ignore-in-shared-libs,-rpath,/usr/local/lib -L$(ML) -L$(ML_RPI)usr/local/lib -lopencv_core -lopencv_features2d -lopencv_highgui -lrt -lopencv_imgproc -lopencv_photo -lopencv_ml -lopencv_imgcodecs -lopencv_video -lopencv_videoio


OBJECTS=main.o $(ML)ansi.o udp.o

all: rpi-irpos-template
Debug: rpi-irpos-template
rpi-irpos-template: $(OBJECTS)
	$(CC) $(CFLAGS) $(LFLAGS) $(OBJECTS) -o $(APP_BINARY)

-include $(OBJECTS:.o=.d)

%.o: %.cpp
	$(CC) -c $(CFLAGS) $*.cpp -o $*.o
	$(CC) -MM $(CFLAGS) $*.cpp > $*.d

cleanDebug: clean
clean:
	rm -f $(OBJECTS)
	rm -f $(OBJECTS:.o=.d)
	rm -f $(APP_BINARY)
install:
	chmod +x $(APP_BINARY)
	sshpass -p $(REMOTE_PASS) scp -o StrictHostKeyChecking=no  $(APP_BINARY) $(REMOTE_SERVER):$(REMOTE_PATH)
	sshpass -p $(REMOTE_PASS) scp -o StrictHostKeyChecking=no  sim.jpg $(REMOTE_SERVER):$(REMOTE_PATH)
rundebug:
	sshpass -p $(REMOTE_PASS) ssh -t $(REMOTE_SERVER)  "sudo gdbserver localhost:5000 $(REMOTE_PATH)/$(APP_BINARY)"
runnodebug:
	sshpass -p $(REMOTE_PASS) ssh -t $(REMOTE_SERVER) sudo $(REMOTE_PATH)/$(APP_BINARY)
plotlog:
	rm -f $(LOGFILE)
	sshpass -p $(REMOTE_PASS) scp -o StrictHostKeyChecking=no  $(REMOTE_SERVER):$(REMOTE_PATH)/$(LOGFILE) .
	octave --persist logplot.m
plotdelete:
	sshpass -p $(REMOTE_PASS) ssh -t $(REMOTE_SERVER) rm -f $(REMOTE_PATH)/$(LOGFILE)


