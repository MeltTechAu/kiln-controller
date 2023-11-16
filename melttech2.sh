#!/bin/bash
sudo apt install onboard -y
sudo apt-get install python3-dev python3-virtualenv libevent-dev virtualenv -y
git clone https://github.com/MeltTechAu/kiln-controller &
sudo systemctl enable vncserver-x11-serviced --now &
sleep 10
cd kiln-controller
virtualenv -p python3 venv
source venv/bin/activate
export CFLAGS=-fcommon
pip3 install greenlet bottle gevent gevent-websocket paho.mqtt
sleep 20
#source venv/bin/activate; ./kiln-controller.py &
sleep 10
xdg-open http://127.0.0.1:8081 &
#cp /home/pi/kiln-controller/MeltTech2.Desktop ~/Desktop &
cp /home/pi/kiln-controller/MeltTech-Tuner.desktop ~/Desktop &
sudo cp /home/pi/kiln-controller/lib/init/kiln-controller.service /etc/systemd/system/ &
#sudo systemctl enable kiln-controller &
/home/pi/kiln-controller/start-on-boot &
sudo systemctl enable kiln-controller &
#sudo vnclicensewiz



#reboot


