#include "serlib.h"
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <sys/ioctl.h>
#include <termios.h>

#include <linux/serial.h>
#include <linux/types.h>
#include <linux/ioctl.h>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

//Patch: missing IOCTL's
#define TIOCGRS485	0x542E
#define TIOCSRS485	0x542F

//Because of incompatibility between glibc headers and kernel headers, termios2 has to be manually declared
//Attention!!! c_cc length should match the c_cc length in the kernel. If problems occur setting arbitrary baud rate, check this!!!

struct termios2 {
	tcflag_t c_iflag;		/* input mode flags */
	tcflag_t c_oflag;		/* output mode flags */
	tcflag_t c_cflag;		/* control mode flags */
	tcflag_t c_lflag;		/* local mode flags */
	cc_t c_line;			/* line discipline */
	cc_t c_cc[19];		    /* control characters */
	speed_t c_ispeed;		/* input speed */
	speed_t c_ospeed;		/* output speed */
};

struct serial_rs485_2 {
	__u32	flags;			/* RS485 feature flags */
#define SER_RS485_ENABLED		(1 << 0)
#define SER_RS485_RTS_ON_SEND		(1 << 1)
#define SER_RS485_RTS_AFTER_SEND	(1 << 2)
#define SER_RS485_RTS_BEFORE_SEND	(1 << 3)
	__u32	delay_rts_before_send;	/* Milliseconds */
	__u32	delay_rts_after_send;	/* Milliseconds */
	__u32	padding[5];		/* Memory is cheap, new structs
					   are a royal PITA .. */
};


int SerlibInitPort(int *fd,char *PortName, uint32 Baudrate)
{
    struct termios2 options;
	struct serial_rs485_2 rs485conf;
    int res;

    if (fd==NULL) return 1; //Invalid fd pointer

    //Open serial port
    *fd=open (PortName,O_RDWR);

    if (*fd==-1)
        {
        #ifdef SERLIB_DEBUG
            printf ("Can't open serial port %s\n\r",PortName);
        #endif
        return 1;
        }

    //Configure serial port
    //tcgetattr(*fd,&options);


    options.c_cflag = CBAUDEX | /*CRTSCTS |*/ CS8 | CLOCAL | CREAD; //CBAUDEX=BOTHER: select arbitrary baud rate
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;

    /* set input mode (non-canonical, no echo,...) */
    options.c_lflag = 0;

    options.c_cc[VTIME]    = 0;   /* inter-character timer unused */
    options.c_cc[VMIN]     = 1;   /* blocking read until 1 char received */

    options.c_ospeed=Baudrate;
    options.c_ispeed=Baudrate;

    tcflush(*fd, TCIFLUSH );

    //res=ioctl(*fd, 1076646955, &options);
    //Set options and baud rate
    res=ioctl(*fd, TCSETS2, &options);
    if (res<0)
    {
        #ifdef SERLIB_DEBUG
            printf ("IOCTL err: TIOCSSERIAL: %d (%s)",errno, strerror(errno));
        #endif
        return 1;
    }


    return 0;
}

void SerlibClosePort(int *fd)
{
    struct serial_rs485 rs485conf;
    if (fd==NULL) return;

    close (*fd);
}

void SerlibWriteBlock(int *fd, uint8 *Data, uint32 Length)
{
    if (fd==NULL) return;
    write(*fd,Data,Length);
    tcdrain(*fd); //Wait until everything has been written
}

uint8 SerlibReadByte(int *fd)
{
    uint8 Data;
    if (fd==NULL) return 0;
    read(*fd,&Data,1);
    return Data;
}
void SerlibReadBlock(int *fd, uint8 *Data, uint32 Length)
{
    if (fd==NULL) return;
    read(*fd,Data,Length);
}
