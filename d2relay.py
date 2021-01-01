#!/usr/bin/env python

"""
D2 is a minimal relay tool to output Leica DISTO D2 data to the console

Copyrights (c) 2021 Hartmut Seichter

Distributed under the terms of the MIT License

"""

import gatt
import struct

debug_mode = False

class DISTO(gatt.Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))
        self.connect() # aweful hack to keep the DISTO from disconnecting
        # this will drain your distos battery!

    def services_resolved(self):
        super().services_resolved()

        if debug_mode:
            print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            if debug_mode:
                print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                if debug_mode:
                    print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))

                characteristic.read_value()
                characteristic.enable_notifications()


    def characteristic_value_updated(self, characteristic, value):
        if characteristic.uuid == '3ab10101-f831-4395-b29d-570977d5bf94':
            self.report(value)
        elif debug_mode:
            # this is here for debugging ... there many more things to implement
            # if characteristic.uuid == '3ab10102-f831-4395-b29d-570977d5bf94':
            print(characteristic.uuid,':',type(value),len(value)) # ,int.from_bytes(value,byteorder='big', signed=False))
            # else:
            #     print( characteristic.uuid, ":", value.decode("utf-8"))
            if len(value) == 2:
                print("uint16  :",int.from_bytes(value,byteorder='big',signed=False))
            if len(value) == 4:
                print("\tfloat :",struct.unpack('f',value))
            elif len(value) == 8:
                print('\tdouble:',struct.unpack('ff',value))
    
    def report(self,value):
        float_val = struct.unpack('f',value)[0]
        print(round(float_val,3),'m')


# note: Make it configurable
manager = gatt.DeviceManager(adapter_name='hci0')

# well this is only for the D2 but other BLE devices by Leica should
# work similar - usually they just have more functions
device = DISTO(mac_address= 'FD:8B:B0:50:BA:A3', manager=manager)
device.connect()
manager.run()