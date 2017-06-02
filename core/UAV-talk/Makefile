CC=gcc
APP_BINARY=uavtalk-test

ML=/home/lubuntu/minimod/Libs/

CFLAGS += -g -DLINUX -Wall -I$(ML) -I../lib/ -I.
LFLAGS += -lpthread -L$(ML) -lrt

OBJECTS=main.o serlib.o LibrePilotSerial.o

all: uavtalk-test
Debug: uavtalk-test
uavtalk-test: $(OBJECTS)
	$(CC) $(CFLAGS) $(LFLAGS) $(OBJECTS) -o $(APP_BINARY)

-include $(OBJECTS:.o=.d)

%.o: %.c
	$(CC) -c $(CFLAGS) $*.c -o $*.o
	$(CC) -MM $(CFLAGS) $*.c > $*.d

cleanDebug: clean
clean:
	rm -f $(OBJECTS)
	rm -f $(OBJECTS:.o=.d)
	rm -f $(APP_BINARY)





