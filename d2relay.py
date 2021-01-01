#!/usr/bin/env python

"""
D2 is a minimal relay tool to output Leica DISTO D2 data to the console

Copyrights (c) 2021 Hartmut Seichter

Distributed under the terms of the MIT License

"""

import gatt
import struct

debug_mode = False
keepalive_hack = True


class DISTOManager(gatt.DeviceManager):
    def __init__(self, adapter_name):
        super().__init__(adapter_name)


    def run(self):
        super().run()

    def on_idle(self):
        pass

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
        # aweful hack to keep the DISTO from disconnecting
        # this will drain your distos battery!
        if keepalive_hack:
            self.connect() 

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

        if debug_mode:
            # this is here for debugging ... there many more things to implement
            # if characteristic.uuid == '3ab10102-f831-4395-b29d-570977d5bf94':
            print(characteristic.uuid,':',type(value),len(value)) # ,int.from_bytes(value,byteorder='big', signed=False))
            # else:
            #     print( characteristic.uuid, ":", value.decode("utf-8"))
            print('\traw   :',value)
            if len(value) == 2:
                print("\tuint16  :",struct.unpack('>H',value)[0])
            if len(value) == 4:
                print("\tfloat :",struct.unpack('f',value)[0])
            elif len(value) == 8:
                print('\tdouble:',struct.unpack('d',value)[0])
                
        elif characteristic.uuid == '3ab10101-f831-4395-b29d-570977d5bf94':
            self.report_measurement(value)
        # Vendor ID
        elif characteristic.uuid == '00002a29-0000-1000-8000-00805f9b34fb':
            # for whatever reasons the D2 reports itself as the BLE SoC 
            # thats driving it - a Nordic Semi nRF51822 - a 16MhZ Cortex-M0
            is_leica = value.decode('utf-8') == 'nRF51822'
        elif characteristic.uuid == '00002a1a-0000-1000-8000-00805f9b34fb':
                print('Battery level',value)

        
    
    def report_measurement(self,value):
        float_val = struct.unpack('f',value)[0]
        print(round(float_val,3),'m')


# note: Make it configurable
manager = DISTOManager(adapter_name='hci0')

# well this is only for the D2 but other BLE devices by Leica should
# work similar - usually they just have more functions
device = DISTO(mac_address= 'FD:8B:B0:50:BA:A3', manager=manager)
device.connect()
manager.run()