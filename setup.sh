#!/bin/bash

echo Please change the default password of the RPi.
echo Default password is 'raspberry'.
passwd

echo Installing wifi...
sudo chmod +x ./wifi-setupv2.sh
sudo ./wifi-setupv2.sh

echo Ensuring sensor script runs permanently
sudo cp ./sensor.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable sensor.service
