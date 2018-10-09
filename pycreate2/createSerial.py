# The MIT License
#
# Copyright (c) 2017 Kevin Walchko
#
# This is basically the interface between the Create2 and pyserial

from __future__ import division, print_function

import struct

import serial


class SerialCommandInterface(object):
    """
    This class handles sending commands to the Create2. Writes will take in tuples
    and format the data to transfer to the Create.
    """

    def __init__(self, port, baud=115200, timeout=1):
        """
        Constructor.

        Creates the serial port, but doesn't open it yet. Call open(port) to open
        it.
        """
        self.ser = serial.serial_for_url(port, baud=baud, timeout=timeout, do_not_open=True)

    def __del__(self):
        """
        Destructor.

        Closes the serial port
        """
        self.close()

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def is_open(self):
        return self.ser.is_open

    def open(self):
        """
        Opens a serial port to the create.

        port: the serial port to open, ie, '/dev/ttyUSB0'
        buad: default is 115200, but can be changed to a lower rate via the create api
        """
        if self.ser.is_open:
            print("Serial port {} already open".format(self.ser.name))
        # self.ser.close()
        self.ser.open()
        if self.ser.is_open:
            # print("Create opened serial: {}".format(self.ser))
            print('-' * 40)
            print(' Create opened serial connection')
            print('   port: {}'.format(self.ser.port))
            print('   datarate: {} bps'.format(self.ser.baudrate))
            print('-' * 40)
        else:
            raise Exception('Failed to open serial port {}'.format(self.ser.name))

    def write(self, opcode, data=None):
        """
        Writes a command to the create. There needs to be an opcode and optionally
        data. Not all commands have data associated with it.

        opcode: see creaet api
        data: a tuple with data associated with a given opcode (see api)
        """
        if not self.ser.is_open:
            raise Exception('You must open the serial port first')

        msg = (opcode,)

        # Sometimes opcodes don't need data. Since we can't add
        # a None type to a tuple, we have to make this check.
        if data:
            msg += data

        self.ser.write(struct.pack('B' * len(msg), *msg))

    def read(self, num_bytes):
        """
        Read a string of 'num_bytes' bytes from the robot.

        Arguments:
            num_bytes: The number of bytes we expect to read.
        """
        if not self.ser.is_open:
            raise Exception('You must open the serial port first')

        data = self.ser.read(num_bytes)
        return data

    def close(self):
        """
        Closes the serial connection.
        """
        if self.ser and self.ser.is_open:
            print('Closing port {} @ {}'.format(self.ser.name, self.ser.port))
            self.ser.close()
