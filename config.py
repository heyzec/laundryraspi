import json
from pathlib import Path
from typing import Dict, List

# Open up settings.json file in the same directory as config.py
p = Path(__file__).with_name("settings.json")
with p.open('r') as f:
    settings: dict = json.load(f)

### EXPORTED VARIABKES ###

ENDPOINT: str = settings['endpoint']
FLOOR: int = settings['floor']
PING_FREQUENCY: int = settings['ping_server_frequency']
REQUEST_TIMEOUT: int = settings['timeout']
TOKEN: str = settings['token']

MACHINES: List[Dict[str, int]] = settings['machines']
