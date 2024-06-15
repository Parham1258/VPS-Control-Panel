# Config file for VPS Control Panel
Company="Company" # Company name, will show before the VPS Control Panel text

Host="0.0.0.0" # Host (127.0.0.1 for local access only, 0.0.0.0 for remote access)
Port=50009 # Port
Threads=6

noVNC_Host="hosting.parham200.ir"

# For NAT Loopback:
Lan_IP="192.168.0.213"
Lan_Subnet="192.168."

Multiple_API_Actions=False # Whether you want to allow multiple API actions for a server at once or not

# Cooldown System:
Cooldown_Toggle=True
Cooldown=1 # How many seconds before another API action is allowed
Cooldown_If_In_Cooldown=2 # How many seconds are added to the current Cooldown because you're already on cooldown

If_No_Permission_404=True # If you don't have permission to view a server, the API (Panel already does that) will return 404 (Not Found) instead of 401 (Unauthorized)

VMRUN_PATH = r'"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"'

# Developer Options:
Debug=False