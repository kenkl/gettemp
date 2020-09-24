# gettemp
A simple RPi0W-based temperature display, polling remote DS18B sensors.

The display itself is the [PiSupply PaPiRus](https://www.pi-supply.com/product/papirus-zero-epaper-screen-phat-pi-zero/) eInk display (also available from [ThePiHut](https://thepihut.com/products/papirus-zero-epaper-eink-screen-phat-for-pi-zero?variant=28041609745)). This project relies on Python libraries, installed if you follow the directions in [their README.md](https://github.com/PiSupply/PaPiRus/blob/master/README.md)

The RPi0W for this project came from [Adafruit](https://www.adafruit.com/product/3400).

The remote sensors are (currently) the [Dallas DS18B](https://www.adafruit.com/product/374) connected to a network-connected Arduino or ESP8266 (or similar) device. In the code, Ardu1 references an Arduino Uno with the Ethernet Shield, and ESP1 references an [Adafruit Huzzah ESP8266 breakout](https://www.adafruit.com/product/2471).

Both are running code based on the simple web server, exposing the sensor reading via JSON (for ease of parsing) to http calls. ToDo: publish the ESP1 code in a repo here.

Currently, I don't attempt to do anything fancy with the data - simply displaying it as text on the display. In landscape-orientation, you get (roughly) five lines of screen real-estate. I use that to display the polling of a sensor in the living-room (ESP1), my home-office (Datacentre), and outside.

For continuous updates, I have a line in the crontab of the user context running this. Because ambient temperatures don't change *that* quickly, I run this every five minutes (could do 10, 20 or even 30, really):

```
*/5 * * * * /home/pi/gettemp/gettemp.py
```

I don't (currently) have it in a case or anything fancy. It's simply stuck to the door-jam with a bit of [BluTack](https://www.amazon.com/Blu-Tack-060968-Reusable-Adhesive-75g/dp/B001FGLX72/ref=sr_1_3?ie=UTF8&qid=1512329012&sr=8-3&keywords=blue+tack):

![alt text](https://raw.githubusercontent.com/kenkl/gettemp/master/action_shot.jpg "gettemp action shot")

2020-09-24: 

After almost 3 years, this thing is still in service, although I've made a couple changes. First, it no longer lives on the door-jam, but on my desk; I had to change the orientation of the display. Also, the outside sensor is on the south end of the house, and is not terribly accurate as it picks up ambient heat from the house. When the sun shines on it, it's _wildly_ wrong. So, I added a bit of code to grab the temperature from [openweathermap.org](https://openweathermap.org/) (account required). It tends to be a lot more accurate, especially during the day.

The OpenWeather key and city are stored in secrets.py, which only needs these two lines:

```
owmkey = "APPID=0123456789abcdef"
city = "New%20York,us"
```

Of _course_, you'll want to provide your own APPID here; the pictured one will not work. Also, note that spaces in the city name need to be pre-encoded (I don't do anything clever with that in my code) with '%20' to assemble a proper URL string.

After all this time, I _still_ don't have a case for it, but here's an updated snapshot of it sitting on my desk, propped up against a speaker, showing the new line populated with openweathermap.org data:

![alt text](https://raw.githubusercontent.com/kenkl/gettemp/master/action_shot2.jpg "gettemp action shot 2")


