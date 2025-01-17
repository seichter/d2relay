# D2Relay

D2 Relay is a small tool to relay measurements of a [Leica DISTO&trade; D2](https://shop.leica-geosystems.com/buy/disto/d2) device to the console.

&copy; Copyrights 2021-2025 Hartmut Seichter

## Installation

Create a `venv`

```console
[me@machine d2relay]$ python -m venv .venv
```

Activate the venv:

```console
[me@machine d2relay]$ source .venv/bin/activate
```

Activate the venv:

```console
(.venv) [me@machine d2relay]$ pip install -r requirements.txt
```

Check usage ...

```console
(.venv) [me@machine d2relay]$ python -m app --help
usage: d2relay [-h] [--address ADDRESS]

a tool for reading out Leica Disto D2 devices over BLE

options:
 -h, --help         show this help message and exit
 --address ADDRESS  BLE address for Disto D2, default: FD:8B:B0:50:BA:A3
```


## Collaboration

There are many ways to collaborate, please open an issue or a pull request. Some ideas:

* create a proper d2relay module to encapsulate the functionality
* support other Leica BLE devices (or some relabeled Bosch devices)

## Screenshot

![d2relay capturing data from the device](doc/screenshot.jpg)

## Todo

Plenty of hints can be found in my [notes](./doc/notes.md) while reverse engineering my device.

* [ ] Infer correct units
* [ ] Detect error states such as 255 (too close)
* [x] Make things configurable by using command line parameters
* [ ] Interactive Mode: trigger measurements over BT
* [ ] Demonstrator with FreeCAD or the like

## Copyright & License

d2relay is &copy; 2021-2025 Hartmut Seichter - licenses under the terms MIT licence
