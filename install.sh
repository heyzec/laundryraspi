#! /usr/bin/env bash

# This script just copies a bunch of files around to set things up. Run it and
# (maybe restart and) everything should work. Make sure wifi has been set up
# before running this.

sudo cp sensor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sensor.service

# Wifi things. Register our cron job, and make a directory for its logs.
cp ./wifi-check.sh /home/pi/wifi-check.sh
mkdir -p /home/pi/.log
touch /home/pi/.log/network.log
crontab ./wifi-check.cron

