# Elo touchscreen raspberry pi emulator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The emulator is made according to this [manual](https://wiki.tizen.org/USB/Linux_USB_Layers/Configfs_Composite_Gadget).

# Installation 

I use the latest Raspberry Pi OS version within Raspberry Pi Zero W. For the moment it's `Linux raspberrypi 4.19.118+ #1311 Mon Apr 27 14:16:15 BST 2020 armv6l GNU/Linux`.

1. Copy the content of the `configfs` folder to any place you like around the system. 
Also put `touch-control/touch-server.sh` to anywhere you wish. I use `/usr/local/lib/gk` directory.  
2. Then edit `/etc/rc.local` (the easiest way to execute something on system start with root privileges by default).
Add these lines before the `exit 0` statement.
```bash
/usr/local/lib/gk/setup-elo.sh
/usr/local/lib/gk/touch-server.sh &
```

# Control the touchscreen

In the `touch-control` folder there is an example GUI for controlling touchscreen. 
To start it's necessary to install tkinter for python3.
 
```
sudo apt install python3-tk
pip3 install -r requirements.txt
```

Then run it by passing ip address of your raspberry e.g. `./app.py 192.168.1.77`.

API to the touchscreen are in the `elo.py`.

```python
import socket
from elo import send_touch, send_move, send_release, send_tap

sock = socket.socket()
sock.connect((host, port))

# makes touchscreen to produce tap 
send_tap(sock, x, y)

...

# for detailed control use these
send_touch(sock, x, y)
send_move(sock, x + 100, x + 100)   
send_release(sock, x + 200, y + 200)
```

---
**Note**

Moving also works without touch/release, but original elo device sends them at the begin/end of sequence. 
Not aware about any side effects of skipping them.

---

# Tests

Run `pytest` in `touch-control` folder or in the repo's root.
