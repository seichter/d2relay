#!/usr/bin/env python

"""
D2 is a minimal relay tool to output Leica DISTO D2 data to the console

Copyrights (c) 2021 Hartmut Seichter

Distributed under the terms of the MIT License

"""


MODEL_NUMBER_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
MANUFACTURER_UUID = "00002a29-0000-1000-8000-00805f9b34fb"
MEASUREMENT_UUID  = "3ab10101-f831-4395-b29d-570977d5bf94"

d2_mac_address = "FD:8B:B0:50:BA:A3"

import logging
import asyncio
import platform

import struct

import asyncio

from bleak import BleakScanner
from bleak import BleakClient
from bleak import _logger as logger


CHARACTERISTIC_UUID = MEASUREMENT_UUID


def report_measurement(value):
    float_val = struct.unpack('f',value)[0]
    print(round(float_val,3),'m')

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    # print("{0}: {1}".format(sender, data))
    report_measurement(data)


async def run(address, debug=False):
    if debug:
        import sys

        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))

        # await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        # await asyncio.sleep(30.0)
        # await client.stop_notify(CHARACTERISTIC_UUID)

        x = input("Press")

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        for val_f in range(256):
            for val_b in range(256):
        
                print(val_f,val_b,'start')

                data = bytearray([val_f, val_b])
                await asyncio.wait_for(client.write_gatt_char("3ab10109-f831-4395-b29d-570977d5bf94", data),timeout=5)

                print(val_f,val_b,'end')

        await asyncio.sleep(5.0)

        await client.stop_notify(CHARACTERISTIC_UUID)



if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        d2_mac_address  # <--- Change to your device's address here if you are using Windows or Linux
        if platform.system() != "Darwin"
        else "B9EA5233-37EF-4DD6-87A8-2A875E821C46"  # <--- Change to your device's address here if you are using macOS
    )
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(address, True))


