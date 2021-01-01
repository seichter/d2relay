# Notes 

This is just a log-book of my afternoon session to get data out of my DISTO&trade; into another system that isn't my iPhone. There are some resources on the internet but none of them deals with the D2 as a typical BT device. The D2 can be very easily parsed using GATT.


## Goal

Goal of this tool should be a console output that can be easily being parsed. Measurement and unit should be available. Additional states such as front or back-measurements or special functions (trigonometric etc.) of the DISTO&trade; are not a goal.

 
## GATT on the Leica DISTO&trade; D2

The following items can be found:


```
[FD:8B:B0:50:BA:A3] Connected
[FD:8B:B0:50:BA:A3] Resolved services
[FD:8B:B0:50:BA:A3]  Service [0000180a-0000-1000-8000-00805f9b34fb]
[FD:8B:B0:50:BA:A3]    Characteristic [00002a29-0000-1000-8000-00805f9b34fb]
[FD:8B:B0:50:BA:A3]  Service [0000180f-0000-1000-8000-00805f9b34fb]
[FD:8B:B0:50:BA:A3]    Characteristic [00002a1a-0000-1000-8000-00805f9b34fb]
[FD:8B:B0:50:BA:A3]    Characteristic [00002a19-0000-1000-8000-00805f9b34fb]
[FD:8B:B0:50:BA:A3]  Service [3ab10100-f831-4395-b29d-570977d5bf94]
[FD:8B:B0:50:BA:A3]    Characteristic [3ab1010c-f831-4395-b29d-570977d5bf94]
[FD:8B:B0:50:BA:A3]    Characteristic [3ab1010a-f831-4395-b29d-570977d5bf94]
[FD:8B:B0:50:BA:A3]    Characteristic [3ab10109-f831-4395-b29d-570977d5bf94]
[FD:8B:B0:50:BA:A3]    Characteristic [3ab10102-f831-4395-b29d-570977d5bf94]
[FD:8B:B0:50:BA:A3]    Characteristic [3ab10101-f831-4395-b29d-570977d5bf94]
[FD:8B:B0:50:BA:A3]  Service [00001801-0000-1000-8000-00805f9b34fb]
[FD:8B:B0:50:BA:A3]    Characteristic [00002a05-0000-1000-8000-00805f9b34fb]
[FD:8B:B0:50:BA:A3] Disconnected
```

If a new measurement appears on the display, characteristic `3ab10102-f831-4395-b29d-570977d5bf94` is changed


The characteristics on the D2 are in raw byte format:

```
00002a29-0000-1000-8000-00805f9b34fb : <class 'bytes'> 8
00002a1a-0000-1000-8000-00805f9b34fb : <class 'bytes'> 1
00002a19-0000-1000-8000-00805f9b34fb : <class 'bytes'> 1
3ab1010c-f831-4395-b29d-570977d5bf94 : <class 'bytes'> 8
3ab1010a-f831-4395-b29d-570977d5bf94 : <class 'bytes'> 4
3ab10102-f831-4395-b29d-570977d5bf94 : <class 'bytes'> 2
3ab10101-f831-4395-b29d-570977d5bf94 : <class 'bytes'> 4
```

When converting to UTF-8 Strings:

```
00002a29-0000-1000-8000-00805f9b34fb : nRF51822
00002a1a-0000-1000-8000-00805f9b34fb : 
00002a19-0000-1000-8000-00805f9b34fb : 
3ab1010c-f831-4395-b29d-570977d5bf94 : D2     
3ab1010a-f831-4395-b29d-570977d5bf94 : 
3ab10102-f831-4395-b29d-570977d5bf94 : 
3ab10101-f831-4395-b29d-570977d5bf94 : 
```

It turns out `3ab10101-f831-4395-b29d-570977d5bf94` is the actual measurement in
the preset units (m in my case). The four byte value is a simple IEEE754 `float`. 

The value in `3ab10102-f831-4395-b29d-570977d5bf94` is presumably the units associated with the measurement. The coding needs to be figured out later. Once I have read the manual to change to other settings.


## Post Mortem

The Bluetooth stack on Linux (bluez 5.55) keeps constantly crashing. Reverse engineering this protocoll is a reboot fest. The connection is really flakey but I think this is mainly a Linux BLE issue.


