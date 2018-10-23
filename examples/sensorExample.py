#!/usr/bin/env python
# ----------------------------------------------------------------------------
# MIT License
# shows how to get sensor data from the create 2

from __future__ import print_function

import time

from pycreate2 import Create2

PORT = 'COM4'
BAUD = 115200

bot = Create2(port=PORT, baud=BAUD)
try:
    with bot:
        bot.start()
        bot.safe()
        print('Starting ...')
        while True:
            # Packet 100 contains all sensor data.
            sensor_state = bot.get_sensors()

            print('==============Updated Sensors==============')
            print(sensor_state)
            time.sleep(2)
except KeyboardInterrupt:
    print("Bye")
finally:
    if bot.is_open:
        bot.close()
