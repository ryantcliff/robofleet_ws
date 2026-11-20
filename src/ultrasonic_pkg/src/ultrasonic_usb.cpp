#include <iostream>
#include <string>
#include <atomic>
#include <chrono>
#include <cstring>
#include <stdlib.h>
#include <errno.h>
#include <termios.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <poll.h>
#include <unistd.h>
#include "ultrasonic_pkg/ultrasonic_usb.hpp"

int arduino_fd;

int init_arduino(void)
{
	/* Open USB "file" as Read-Write (O_RDWR)
	 * and do not become process's controlling terminal
	*/
	arduino_fd = open (ARDUINO_PORT, O_RDWR | O_NOCTTY);
	if (arduino_fd < 0)
	{
		return errno;
	}
	
	struct termios tty;
	memset(&tty, 0, sizeof(tty));
	
	if (tcgetattr(arduino_fd, &tty) != 0)
	{
		close(arduino_fd);
		return errno;
	}
	
	cfsetispeed(&tty, B9600);
	cfsetospeed(&tty, B9600);
	
	/* Control modes 
	 *   Character size mask = 8
	 *   Enable receiver
	 *   Ignore modem control lines
	 */
	tty.c_cflag = CS8 | CREAD | CLOCAL;
	
	/* Clearing all of below puts us in "non-canonical" mode,
	 *   or "raw" mode (characters immediately available instead
	 *   of having to wait for a line-ending character)
	 */
	 
	/* Input modes */
	tty.c_iflag = 0;
	
	/* Output modes */
	tty.c_oflag = 0;
	
	/* Local modes */
	tty.c_lflag = 0;
	
	/* Special characters
	 *   Non-blocking reads; read_packet() waits with its own deadline.
	 *   (VMIN > 0 blocks forever until the first byte arrives, which hung
	 *   the node when the Nano missed a request, e.g. while it resets on open.)
	 */
	tty.c_cc[VMIN] = 0;
	tty.c_cc[VTIME] = 0;
	
	/* Apply new configuration immediately */
	if (tcsetattr(arduino_fd, TCSANOW, &tty) != 0)
	{
		close(arduino_fd);
		return errno;
	}
	
	/* Discards data written but not transmitted,
	 *   or data received but not read
	 */
	tcflush(arduino_fd, TCIOFLUSH);
	
	return 0;
}

/* Read up to len bytes, giving up after timeout_ms. Returns bytes read. */
static int read_packet(char *buf, int len, int timeout_ms)
{
	auto deadline = std::chrono::steady_clock::now() + std::chrono::milliseconds(timeout_ms);
	int got = 0;
	while (got < len)
	{
		auto left = std::chrono::duration_cast<std::chrono::milliseconds>(
			deadline - std::chrono::steady_clock::now()).count();
		if (left <= 0)
		{
			break;
		}
		struct pollfd pfd = { arduino_fd, POLLIN, 0 };
		if (poll(&pfd, 1, (int)left) <= 0)
		{
			break;
		}
		int n = read(arduino_fd, buf + got, len - got);
		if (n <= 0)
		{
			break;
		}
		got += n;
	}
	return got;
}

void get_arduino_data (uint8_t *l, uint8_t *c, uint8_t *r)
{
	char read_buf[PACKETLEN];
	tcflush(arduino_fd, TCIFLUSH);
	
	/* Write 1 byte request */
	int bytes_written = write(arduino_fd, REQUEST, sizeof(REQUEST));
	if (bytes_written < 0)
	{
		*l = 0xFF;
		*c = 0xFF;
		*r = 0xFF;
		return;
	}
	/* Read 8 bytes from Arduino (replies take 15-35 ms; a few never come) */
	memset(read_buf, 0, sizeof(read_buf));
	int num_bytes = read_packet(read_buf, sizeof(read_buf), REPLY_TIMEOUT_MS);
	
	/* If error, set data to "invalid" */
	if (num_bytes < 0)
	{
		*l = 0xFF;
		*c = 0xFF;
		*r = 0xFF;
		return;
	}
	/* If nothing received, set data to "invalid" */
	else if (num_bytes == 0)
	{
		*l = 0xFF;
		*c = 0xFF;
		*r = 0xFF;
		return;
	}
	/* If less than 8 bytes received, set data to "invalid" */
	else if (num_bytes != PACKETLEN)
	{
		*l = 0xFF;
		*c = 0xFF;
		*r = 0xFF;
		return;
	}
	
	/* If START and STOP bytes are incorrect, packet is most 
	 *   likely also incorrect, set data to "invalid"
	 */
	if ((unsigned char)read_buf[idx_start] != START || (unsigned char)read_buf[idx_stop] != STOP)
	{
		*l = 0xFF;
		*c = 0xFF;
		*r = 0xFF;
		return;
	}
	
	/* If any sensor ID byte is incorrect, packet is most
	 *   likely also incorrect, set data to "invalid"
	 */
	if ((unsigned char)read_buf[idx_leftid] != LEFT ||
		(unsigned char)read_buf[idx_centerid] != CENTER ||
		(unsigned char)read_buf[idx_rightid] != RIGHT)
	{
		*l = 0xFF;
		*c = 0xFF;
		*r = 0xFF;
		return;
	}
	
	/* If packet is correct length and well-formatted,
	 *   set data to their corresponding values
	 */
	*l = (uint8_t)(unsigned char)read_buf[idx_leftdata];
	*c = (uint8_t)(unsigned char)read_buf[idx_centerdata];
	*r = (uint8_t)(unsigned char)read_buf[idx_rightdata];
}






