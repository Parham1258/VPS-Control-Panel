from flask import Flask, render_template, request, abort
from waitress import serve
from Config import Host, Port, Threads, noVNC_Host, Lan_IP, Lan_Subnet, Debug

app = Flask("VPS Control Panel")

import API
app.register_blueprint(API.app, url_prefix="/api")
from DB import VM_PATHS

@app.errorhandler(404)
def not_found_error(error): return render_template("404.html"), 404
@app.errorhandler(405)
def not_found_error(error): return render_template("405.html"), 405
@app.route("/")
def index(): return render_template("index.html"), 200
@app.route("/server")
def server():
    if "id" not in request.args or request.args["id"] not in VM_PATHS or "Key" not in request.cookies or request.cookies["Key"]!=VM_PATHS[request.args["id"]][1]: return abort(404), 404
    if len(VM_PATHS[request.args["id"]])>3: vnc={"VNC": True, "Host": Lan_IP if request.remote_addr.startswith(Lan_Subnet) else noVNC_Host, "Port": VM_PATHS[request.args["id"]][3], "Password": VM_PATHS[request.args["id"]][4]}
    else: vnc={"VNC": False}
    server_status=API.run_vmrun_command("list", None, False).strip().split("\n")[1:]
    return render_template("server.html", ID=request.args["id"], Name=VM_PATHS[request.args["id"]][2], Status="Online" if VM_PATHS[request.args["id"]][0] in server_status else "Offline", **vnc), 200

print("\033[0;32mStarting VPS Control Panel\n\033[0;32mMade by Parham and Inventionpro with ❤️\033[0m")
if Debug: app.run(host=Host, port=Port, debug=True)
else: serve(app, host=Host, port=Port, threads=Threads)