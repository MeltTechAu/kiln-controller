Kiln Controller
==========

Turns a Raspberry Pi into an Awesome, web-enabled kiln controller.

## Features

  * easy to create new kiln schedules and edit / modify existing schedules
  * no limit to runtime - fire for days if you want
  * view status from multiple devices at once - computer, tablet etc
  * real-time firing cost estimate
  * NIST-linearized conversion for accurate K type thermocouple readings
  * supports PID parameters you tune to your kiln
  * monitors temperature in kiln after schedule has ended
  * api for starting and stopping at any point in a schedule
  * supports MAX31856 and MAX31855 thermocouple boards
  * support for K, J, N, R, S, T, E, or B type thermocouples
  * accurate simulation
  * support for shifting schedule when kiln cannot heat quickly enough
  * prevents integral wind-up when temperatures not near the set point
  * automatic restarts if there is a power outage or other event
  
  2023 updates
  * added Touch Fuction Edit/Stage Points MT
  * added Talking kiln controller No connection for replacement of damaged part Audio notification with real voice MT
  
  future
  Working on Cone Mode implementation
**Run Kiln Schedule**

![Image](https://github.com/jbruce12000/kiln-controller/blob/master/public/assets/images/kiln-running.png)

## Software 

### Raspberry PI OS

Download [Raspberry PI OS](https://www.raspberrypi.org/software/). Use Rasberry PI Imaging tool to install the OS on an SD card. Boot the OS, open a terminal and...

    $ sudo apt-get update
    $ sudo apt-get dist-upgrade
    $ sudo apt-get install python3-dev python3-virtualenv libevent-dev virtualenv
    $ git clone https://github.com/jbruce12000/kiln-controller
    $ cd kiln-controller
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ export CFLAGS=-fcommon
    $ pip3 install --upgrade setuptools
    $ pip3 install greenlet bottle gevent gevent-websocket


### Raspberry PI deployment

If you're done playing around with simulations and want to deploy the code on a Raspberry PI to control a kiln, you'll need to do this in addition to the stuff listed above:

    $ cd kiln-controller
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ export CFLAGS=-fcommon
    $ pip3 install -r requirements.txt

## Configuration

All parameters are defined in config.py, review/change to your mind's content. found in home/kiln-controller directory

You should change, test, and verify PID parameters in config.py.  Here is a [PID Tuning Guide](https://github.com/jbruce12000/kiln-controller/blob/master/docs/pid_tuning.md). There is also an [autotuner](https://github.com/jbruce12000/kiln-controller/blob/master/docs/ziegler_tuning.md). Be patient with tuning. No tuning is perfect across a wide temperature range.

Tune from cold kiln for best results. use MT icon or copy past method see above links fot tuning
While tuning do not start kiln controller only run one thing at a time either tuning ot controller software in web browser.

You may want to change the configuration parameter **sensor_time_wait**. It's the duty cycle for the entire system.  It's set to 14 seconds by default which means that a decision is made every 14s about whether to turn on relay[s] and for how long. If you use mechanical relays, you may want to increase this. At 2s, my SSR switches 11,000 times in 13 hours.

## Usage

### Server Startup

    $ source venv/bin/activate; ./kiln-controller.py

### Autostart Server onBoot
If you want the server to autostart on boot, run the following command:

    $ /home/pi/kiln-controller/start-on-boot

### Client Access

Click http://127.0.0.1:8081 for local development or the IP
of your PI and the port defined in config.py (default 8081).

### Simulation

In config.py, set **simulate=True**. Start the server and select a profile and click Start. Simulations run at near real time.

### Watcher

If you're busy and do not want to sit around watching the web interface for problems, there is a watcher.py script which you can run on any machine in your local network or even on the raspberry pi which will watch the kiln-controller process to make sure it is running a schedule, and staying within a pre-defined temperature range. When things go bad, it sends messages to a slack channel you define. I have alerts set on my android phone for that specific slack channel. Here are detailed [instructions](https://github.com/jbruce12000/kiln-controller/blob/master/docs/watcher.md).

**Edit Kiln Schedule**

![Image](https://github.com/jbruce12000/kiln-controller/blob/master/public/assets/images/kiln-schedule.png)

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Origin
This project was originally forked from https://github.com/apollo-ng/picoReflow and jbruce12000 but has diverged a large amount. and it will keep evolving
