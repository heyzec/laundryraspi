script=`pwd`/main.py
sed -i "s|script_loc|$script|g" sensor.service
cp sensor.service /etc/systemd/system
systemctl enable sensor.service
