#!/usr/bin/env python

"""
D2 is a minimal relay tool to output Leica DISTO D2 data to the console

Copyrights (c) 2021-2025 Hartmut Seichter

Distributed under the terms of the MIT License

"""

import argparse
import struct
import asyncio
from bleak import BleakClient

# ['0000180f-0000-1000-8000-00805f9b34fb', '0000180a-0000-1000-8000-00805f9b34fb', '3ab10100-f831-4395-b29d-570977d5bf94']


class DistoD2Device:
    debug_mode = True
    address = "FD:8B:B0:50:BA:A3"
    uuid = {
        "3ab10101-f831-4395-b29d-570977d5bf94": "report_measurement",
        "00002a29-0000-1000-8000-00805f9b34fb": "nordic_soc",
        "00002a1a-0000-1000-8000-00805f9b34fb": "battery_level",
    }


def report_measurement(caller, data: bytearray):
    print(f"measurement: {struct.unpack('f', data)}")


def report_battery_level(data: bytearray):
    print(data)


async def main():
    async with BleakClient(DistoD2Device.address, timeout=5.0) as client:
        if DistoD2Device.debug_mode:
            for service in client.services:
                print(f"{service.uuid} : {service.description} ")
                for characteristic in service.characteristics:
                    print(f"\t{characteristic.uuid} : \t{characteristic.properties}")
                    match characteristic.uuid:
                        # measurement
                        case "3ab10101-f831-4395-b29d-570977d5bf94":
                            await client.start_notify(
                                characteristic, report_measurement
                            )
                        case "00002a1a-0000-1000-8000-00805f9b34fb":
                            b = await client.read_gatt_char(characteristic)
                            report_battery_level(b)

        await asyncio.sleep(5.0)

        # print(f"{s.description} {s.uuid}")

        # print(client.services)

        # battery_level = await client.read_gatt_char(DistoD2Device.uuid["battery_level"])

        # print(f"battery level: {int.from_bytes(battery_level)}")
        #
        # 0000180f-0000-1000-8000-00805f9b34fb : Battery Service
        # 0000180a-0000-1000-8000-00805f9b34fb : Device Information
        # 3ab10100-f831-4395-b29d-570977d5bf94 : Unknown
        # 00001801-0000-1000-8000-00805f9b34fb : Generic Attribute Profile

        # value = await client.read_gatt_char("2A24")
        # # print(f"measurement  : {struct.unpack('f', value)[0]} {value}")
        # print("Model Number: {0}".format("".join(map(chr, value))))

        # value = await client.read_gatt_char("00002a1a-0000-1000-8000-00805f9b34fb")
        # print(f"measurement  : {struct.unpack('i', value)[0]} {value}")

    # device = DistoD2Device()
    # try:
    #     await device.connect()
    #     battery_level = await device.read_battery_level()
    #     print(f"battery level: {battery_level}")
    #     await device.disconnect()
    # except Exception as e:
    #     print(e)


asyncio.run(main())


# class DISTO(gatt.Device):
#     debug_mode = False
#     keepalive_hack = True

#     def connect_succeeded(self):
#         super().connect_succeeded()
#         print("[%s] Connected" % (self.mac_address))

#     def connect_failed(self, error):
#         super().connect_failed(error)
#         print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

#     def disconnect_succeeded(self):
#         super().disconnect_succeeded()
#         print("[%s] Disconnected" % (self.mac_address))
#         # aweful hack to keep the DISTO from disconnecting
#         # this will drain your distos battery!
#         if DISTO.keepalive_hack:
#             self.connect()

#     def services_resolved(self):
#         super().services_resolved()

#         if DISTO.debug_mode:
#             print("[%s] Resolved services" % (self.mac_address))
#         for service in self.services:
#             if DISTO.debug_mode:
#                 print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
#             for characteristic in service.characteristics:
#                 if DISTO.debug_mode:
#                     print(
#                         "[%s]    Characteristic [%s]"
#                         % (self.mac_address, characteristic.uuid)
#                     )

#                 characteristic.read_value()
#                 characteristic.enable_notifications()

#     def characteristic_value_updated(self, characteristic, value):
#         if DISTO.debug_mode:
#             # this is here for debugging ... there many more things to implement
#             # if characteristic.uuid == '3ab10102-f831-4395-b29d-570977d5bf94':
#             print(
#                 characteristic.uuid, ":", type(value), len(value)
#             )  # ,int.from_bytes(value,byteorder='big', signed=False))
#             # else:
#             #     print( characteristic.uuid, ":", value.decode("utf-8"))
#             print("\traw   :", value)
#             if len(value) == 2:
#                 print("\tuint16  :", struct.unpack(">H", value)[0])
#             if len(value) == 4:
#                 print("\tfloat :", struct.unpack("f", value)[0])
#             elif len(value) == 8:
#                 print("\tdouble:", struct.unpack("d", value)[0])

#         elif characteristic.uuid == "3ab10101-f831-4395-b29d-570977d5bf94":
#             self.report_measurement(value)
#         # Vendor ID
#         elif characteristic.uuid == "00002a29-0000-1000-8000-00805f9b34fb":
#             # for whatever reasons the D2 reports itself as the BLE SoC
#             # thats driving it - a Nordic Semi nRF51822 - a 16MhZ Cortex-M0
#             is_leica = value.decode("utf-8") == "nRF51822"
#         elif characteristic.uuid == "00002a1a-0000-1000-8000-00805f9b34fb":
#             print("Battery level", value)

#     def report_measurement(self, value):
#         float_val = struct.unpack("f", value)[0]
#         print(round(float_val, 3), "m")


# if __name__ == "__main__":
#     # generic manager
#     manager = gatt.DeviceManager()

#     # well this is only for the D2 but other BLE devices by Leica should
#     # work similar - usually they just have more functions
#     device = DISTO(mac_address=DISTO_D2.mac_address, manager=manager)
#     device.connect()
#     manager.run()
