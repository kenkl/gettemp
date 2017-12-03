# gettemp
A simple RPi0W-based temperature display, polling remote DS18B sensors.

The display itself is the [PiSupply PaPiRus](https://www.pi-supply.com/product/papirus-zero-epaper-screen-phat-pi-zero/) eInk display (also available from [ThePiHut](https://thepihut.com/products/papirus-zero-epaper-eink-screen-phat-for-pi-zero?variant=28041609745)). This project relies on Python libraries, installed if you follow the directions in [their README.md](https://github.com/PiSupply/PaPiRus/blob/master/README.md)

The RPi0W for this project came from [Adafruit](https://www.adafruit.com/product/3400).

The remote sensors are (currently) the [Dallas DS18B](https://www.adafruit.com/product/374) connected to a network-connected Arduino or ESP8266 (or similar) device. In the code, Ardu1 references an Arduino Uno with the Ethernet Shield, and ESP1 references an [Adafruit Huzzah ESP8266 breakout](https://www.adafruit.com/product/2471).

Both are running code based on the simple web server, exposing the sensor reading via JSON (for ease of parsing) to http calls. ToDo: publish the ESP1 code in a repo here.

Currently, I don't attempt to do anything fancy with the data - simply displaying it as text on the display. In landscape-orientation, you get (roughly) five lines of screen real-estate. I use that to display the polling of a sensor in the living-room (ESP1), my home-office (Datacentre), and outside.

The script (gettemp.py) is wired up to launch at system startup via /etc/rc.local. Depending how it behaves long-term, I might construct a simple watchdog to ensure the script runs continuously, uninterrupted.

I don't (currently) have it in a case or anything fancy. It's simply stuck to the door-jam with a bit of [BluTack](https://www.amazon.com/Blu-Tack-060968-Reusable-Adhesive-75g/dp/B001FGLX72/ref=sr_1_3?ie=UTF8&qid=1512329012&sr=8-3&keywords=blue+tack):

![alt text](https://raw.githubusercontent.com/kenkl/gettemp/master/action_shot.jpg "gettemp action shot")
