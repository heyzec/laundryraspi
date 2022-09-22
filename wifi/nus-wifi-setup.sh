#!/usr/bin/env bash
# 1. Run [`wifi-setup.sh`](https://github.com/OrcaTech-RC4/laundrybot-raspi/blob/master/wifi-setup.sh)
#    script, move created `wpa_supplicant.conf` file to `/etc/wpa_supplicant/wpa_supplicant.conf`
#
# 2. Edit `/etc/dhcpcd.conf` by appending these lines:
#    interface wlan0
#    env ifwireless=1
#    env wpa_supplicant_driver=wext,nl80211
#
# 3. Reboot and profit.

# Safety feature in case this script is accidentally run wrongly
#grep -q 'Raspbian' /etc/os-release || echo This is not a raspberry pi!; exit


if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi


COUNTRY_CODE="SG"

getpass() {
    read -srp 'Password: ' userpass
    echo
    read -srp 'Confirm password: ' userpassconf

    if [[ "$userpass" == "$userpassconf" ]]; then
        passmatch=true
    else
        passmatch=false
    fi
}

echo Enter NUSNET ID to setup
read -rp 'NUSNET (e0123456): ' nusnetid
userid="nusstu\\$nusnetid"


passmatch=false
getpass
while [[ "$passmatch" == false ]];
do
    echo
    echo Wrong password entered\!
    echo Please re-enter your password.
    getpass
done

# https://eparon.me/2016/09/09/rpi3-enterprise-wifi.html
passhashraw=$(echo -n "${userpass}" | iconv -t utf16le | openssl md4)

# https://stackoverflow.com/questions/21906330/remove-stdin-label-in-bash
passhash=${passhashraw#*= }

echo passhash is "$passhash"

# https://eparon.me/2016/09/09/rpi3-enterprise-wifi.html
wpasuppconftext="ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=$COUNTRY_CODE
network={
    priority=1
    ssid=\"NUS_STU\"
    key_mgmt=WPA-EAP
    eap=PEAP
    identity=\"$userid\"
    password=hash:$passhash
    phase2=\"auth=MSCHAPV2\"
}"

echo "$wpasuppconftext" > /etc/wpa_supplicant/wpa_supplicant.conf


cat >> /etc/dhcpcd.conf <<EOF
interface wlan0
env ifwireless=1
env wpa_supplicant_driver=wext,nl80211
EOF

echo "It's nice to meet you $userid"
echo "Wifi setup complete"
