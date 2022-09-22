import logging
import os
import sys
import time

WLAN = 'wlan0'
PINGIP = '8.8.8.8'
PING_INTERVAL = 5
MAX_PING_FAILURES = 3
MAX_RESTART_FAILURES = 3


rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
if os.environ.get('JOURNAL_STREAM') is not None:
    from systemd import journal
    handler = journal.JournalHandler()
else:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s: [%(levelname)s] %(message)s'))
rootLogger.addHandler(handler)


ping_failures = 0     # Number of consecutive failures to ping
restart_failures = 0  # Number of attempts to restart wifi driver
while True:
    exit_code = os.system(f"ping -c 1 -W 5 -I {WLAN} {PINGIP} 2>&1 >/dev/null")

    if exit_code == 0:
        logging.debug(f"Successful ping to {PINGIP}")
        ping_failures = 0
        restart_failures = 0
    else:
        logging.info(f"Failed ping to {PINGIP}")
        ping_failures += 1

    if restart_failures >= MAX_RESTART_FAILURES:
        logging.error("Restarting wifi module failed 3 times, rebooting...")
        os.system(f"sudo reboot")
        restart_failures = 0

    if ping_failures >= MAX_PING_FAILURES:
        logging.warning("Failed to ping 3 times, restarting module...")
        os.system(f"sudo modprobe -r brcmfmac && sudo modprobe brcmfmac")
        ping_failures = 0
        restart_failures += 1

    time.sleep(PING_INTERVAL)

