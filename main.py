from datetime import datetime
import logging
from time import sleep
from os import mkdir
from os.path import join, isdir
import socket

from sensor import Machine
import requests

from config import ENDPOINT, FLOOR, REQUEST_TIMEOUT, PING_FREQUENCY, MACHINES, TOKEN

def main() -> None:
    logging.info("Initializing script, hello world!")

    machines = [Machine(x['pin'], x['pos']) for x in MACHINES]

    while True:
        update_rpi_ip()
        for m in machines:
            m.update()
        sleep(PING_FREQUENCY)

def update_rpi_ip() -> None:
    ip: str = get_ip()
    try:
        requests.put(ENDPOINT+"/raspi", timeout=REQUEST_TIMEOUT, json={"floor": FLOOR, "ip_addr": ip}, headers={"x-api-key": TOKEN})
    except (requests.ConnectionError, Exception) as e:
        logging.error(f"Error while trying to update RPi IP to backend: {e}")

# Following code is taken from https://stackoverflow.com/a/28950776
def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
 
if __name__ == "__main__":
    # Set up basic logging
    if not isdir("logs"):
        mkdir("logs")
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] [%(levelname)s] %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        handlers=[
                            # Send to both stderr and file at the same time
                            logging.FileHandler(join('logs',f'{datetime.today().date()}.log')),
                            logging.StreamHandler()
                        ])
    main()
