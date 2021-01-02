# D2Relay

D2 Relay is a small tool to relay measurements of a [Leica DISTO&trade; D2](https://shop.leica-geosystems.com/buy/disto/d2) device to the console. This tool is developed and tested only on Linux.

&copy; Copyrights 2021 Hartmut Seichter 

## Prerequisites

You need to install `gatt` integration for python. To do so only for your user account it is sufficient to execute:

```
$ pip install --user gatt
```


## Screenshot

![d2relay capturing data from the device](doc/screenshot.jpg)


## Todo

Plenty of hints can be found in my [notes](./notes.md) while reverse engineering my device.

* [ ] Infer correct units
* [ ] Detect error states such as 255 (too close)
* [ ] Make things configurable by using command line parameters 
* [ ] Interactive Mode: trigger measurements over BT
* [ ] Demonstrator with FreeCAD or the like
