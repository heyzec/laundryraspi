sudo cp sensor.service /etc/systemd/system/
sudo systemctl enable sensor.service

sudo mkdir -p /etc/cron.d
sudo cp wifi-check-cron /etc/cron.d/
mkdir -p /home/pi/.log
touch /home/pi/.log/network.log
