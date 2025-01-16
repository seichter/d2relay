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


class DistoD2Device:
    debug_mode = False
    address = "FD:8B:B0:50:BA:A3"


class ConsoleReport:
    def report_measurement(self, _, data: bytearray):
        print(f"measurement: {struct.unpack('f', data)[0]}")

    def report_byte_level(self, data: bytearray, what: str):
        print(f"{what}: {struct.unpack('B', data)[0]}")


async def reader(address, reporter):
    async with BleakClient(address, timeout=5.0) as client:
        for service in client.services:
            if DistoD2Device.debug_mode:
                print(f"{service.uuid} : {service.description} ")
            for characteristic in service.characteristics:
                if DistoD2Device.debug_mode:
                    print(f"\t{characteristic.uuid} : \t{characteristic.properties}")
                match characteristic.uuid:
                    # measurement
                    case "3ab10101-f831-4395-b29d-570977d5bf94":
                        await client.start_notify(
                            characteristic, reporter.report_measurement
                        )
                        await asyncio.sleep(0.5)

                    # power state
                    case "00002a1a-0000-1000-8000-00805f9b34fb":
                        b = await client.read_gatt_char(characteristic)
                        reporter.report_byte_level(b, "power state")
                        await asyncio.sleep(0.5)

                    # battery level
                    case "00002a19-0000-1000-8000-00805f9b34fb":
                        b = await client.read_gatt_char(characteristic)
                        reporter.report_byte_level(b, "battery level")
                        await asyncio.sleep(0.5)

        while client.is_connected:
            await asyncio.sleep(0.05)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="d2relay",
        description="a tool for reading out Leica Disto D2 devices over BLE",
    )

    parser.add_argument(
        "--address",
        type=str,
        help=f"BLE address for Disto D2, default: {DistoD2Device.address}",
        default=DistoD2Device.address,
    )

    args = parser.parse_args()

    asyncio.run(reader(args.address, ConsoleReport()))
