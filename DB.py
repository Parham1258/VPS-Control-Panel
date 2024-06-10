import os
import sys
import json
from threading import Thread
import time
if not os.path.isfile("VM Paths.json"):
    print("\033[0;31mCouldn't find `VM Paths.json`\033[0")
    sys.exit(1)
VM_PATHS = json.load(open("VM Paths.json", encoding="utf8+"))
def Loader():
    global VM_PATHS
    while True:
        new=json.load(open("VM Paths.json", encoding="utf8+"))
        if VM_PATHS.items()!=new.items():
            VM_PATHS.clear()
            VM_PATHS.update(new)
            print("\033[0;32mDetected changes on VM Paths, Updated!")
        time.sleep(1)
Thread(target=Loader, args=(), daemon=True).start()