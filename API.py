from flask import Blueprint, request, Response, abort
import subprocess
import time
from Config import Multiple_API_Actions, Cooldown_Toggle, Cooldown, Cooldown_If_In_Cooldown, If_No_Permission_404, VMRUN_PATH

app = Blueprint("API", "VPS Control Panel API")

from DB import VM_PATHS

if not Multiple_API_Actions: server_action_running=[]
def run_vmrun_command(command, server, resp=True):
    if not Multiple_API_Actions and server!=None:
        if server in server_action_running:
            if resp: return {"error": "A action for this server is already running"}
            else: return None
        server_action_running.append(server)
    result = subprocess.run(f"{VMRUN_PATH} {command}", capture_output=True, text=True, shell=True)
    if not Multiple_API_Actions and server!=None: server_action_running.remove(server)
    if not resp: return result.stdout.strip()
    if result.returncode == 0: return {"status": "success"}, 200
    else:
        print(f"\033[0;31mVMRUN Error:\n{result.stdout.strip()}\033[0")
        return {"status": "error", "error": "An unknown error occured; If you're a admin, Please check the console"}, 500

ip_cooldowns={}
@app.before_request
def ip_cooldown():
    if Cooldown_Toggle:
        current_time = round(time.time())
        if request.path.startswith("/api/") and request.remote_addr in ip_cooldowns and ip_cooldowns[request.remote_addr]>current_time:
            ip_cooldowns[request.remote_addr]+=Cooldown_If_In_Cooldown
            return {"status": "error", "error": f"You're on cooldown, please try again in {ip_cooldowns[request.remote_addr]-current_time} seconds."}, 429
        ip_cooldowns[request.remote_addr]=current_time+Cooldown

def get_server_status(server):
    server_status=run_vmrun_command("list", server, False)
    if server_status==None: return None
    return server_status.strip().split("\n")[1:]

@app.route("/servers")
def servers():
    if "Key" not in request.cookies: return {"status": "error", "error": "Unauthorized"}, 401
    server_status=run_vmrun_command("list", None, False)
    if server_status==None: return {"error": "A action for this server is already running"}
    server_status=server_status.strip().split("\n")[1:]
    servers=[]
    for id in VM_PATHS:
        if request.cookies["Key"]==VM_PATHS[id][1]: servers.append({"ID": id, "Status": "Online" if VM_PATHS[id][0] in server_status else "Offline", "Name": VM_PATHS[id][2]})
    return {"status": "success", "servers": servers}
@app.route("/server_status")
def server_status():
    if "id" not in request.args or request.args["id"] not in VM_PATHS: return {"error": "VPS not found"}, 404
    if "Key" not in request.cookies or request.cookies["Key"]!=VM_PATHS[request.args["id"]][1]:
        if If_No_Permission_404: return abort(404)
        else: return {"error": "Unauthorized"}, 401
    server_status=get_server_status(request.args["id"])
    if server_status==None: return {"error": "A action for this server is already running"}
    if VM_PATHS[request.args["id"]][0] in server_status: return {"Status": "Online"}, 200
    else: return {"Status": "Offline"}, 200
@app.route("/power_on", methods=["POST"])
def power_on():
    if "ID" not in request.form or request.form["ID"] not in VM_PATHS: return {"error": "VPS not found"}, 404
    if "Key" not in request.cookies or request.cookies["Key"]!=VM_PATHS[request.form["ID"]][1]:
        if If_No_Permission_404: return abort(404)
        else: return {"error": "Unauthorized"}, 401
    server_status=get_server_status(request.form["ID"])
    if server_status==None: return {"error": "A action for this server is already running"}
    if VM_PATHS[request.form["ID"]][0] in server_status: return {"error": "Already started"}, 409
    return run_vmrun_command(f'start "{VM_PATHS[request.form["ID"]][0]}" nogui', request.form["ID"])
@app.route("/shutdown", methods=["POST"])
def shutdown():
    if "ID" not in request.form or request.form["ID"] not in VM_PATHS: return {"error": "VPS not found"}, 404
    if "Key" not in request.cookies or request.cookies["Key"]!=VM_PATHS[request.form["ID"]][1]:
        if If_No_Permission_404: return abort(404)
        else: return {"error": "Unauthorized"}, 401
    server_status=get_server_status(request.form["ID"])
    if server_status==None: return {"error": "A action for this server is already running"}
    if VM_PATHS[request.form["ID"]][0] not in server_status: return {"error": "Not started"}, 409
    return run_vmrun_command(f'stop "{VM_PATHS[request.form["ID"]][0]}" soft nogui', request.form["ID"])
@app.route("/restart", methods=["POST"])
def restart():
    if "ID" not in request.form or request.form["ID"] not in VM_PATHS: return {"error": "VPS not found"}, 404
    if "Key" not in request.cookies or request.cookies["Key"]!=VM_PATHS[request.form["ID"]][1]:
        if If_No_Permission_404: return abort(404)
        else: return {"error": "Unauthorized"}, 401
    server_status=get_server_status(request.form["ID"])
    if server_status==None: return {"error": "A action for this server is already running"}
    if VM_PATHS[request.form["ID"]][0] not in server_status: return {"error": "Not started"}, 409
    return run_vmrun_command(f'reset "{VM_PATHS[request.form["ID"]][0]}" soft nogui', request.form["ID"])
@app.route("/reset", methods=["POST"])
def reset():
    if "ID" not in request.form or request.form["ID"] not in VM_PATHS: return {"error": "VPS not found"}, 404
    if "Key" not in request.cookies or request.cookies["Key"]!=VM_PATHS[request.form["ID"]][1]:
        if If_No_Permission_404: return abort(404)
        else: return {"error": "Unauthorized"}, 401
    server_status=get_server_status(request.form["ID"])
    if server_status==None: return {"error": "A action for this server is already running"}
    if VM_PATHS[request.form["ID"]][0] not in server_status: return {"error": "Not started"}, 409
    return run_vmrun_command(f'reset "{VM_PATHS[request.form["ID"]][0]}" hard nogui', request.form["ID"])
@app.route("/power_off", methods=["POST"])
def power_off():
    if "ID" not in request.form or request.form["ID"] not in VM_PATHS: return {"error": "VPS not found"}, 404
    if "Key" not in request.cookies or request.cookies["Key"]!=VM_PATHS[request.form["ID"]][1]:
        if If_No_Permission_404: return abort(404)
        else: return {"error": "Unauthorized"}, 401
    server_status=get_server_status(request.form["ID"])
    if server_status==None: return {"error": "A action for this server is already running"}
    if VM_PATHS[request.form["ID"]][0] not in server_status: return {"error": "Not started"}, 409
    return run_vmrun_command(f'stop "{VM_PATHS[request.form["ID"]][0]}" hard nogui', request.form["ID"])

@app.after_request
def dark_mode(response: Response):
  response.headers["color-scheme"]="light-dark"
  return response