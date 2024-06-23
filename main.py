from flask import Flask, request, abort, make_response, redirect, send_file, Response
import os
from waitress import serve
from Config import Host, Port, Threads, noVNC_Host, Lan_IP, Lan_Subnet, Debug
from Utils import language, langs
language=language(request)
render_template=language.render_template

app = Flask("VPS Control Panel", static_folder=None)

import Web.API as API
app.register_blueprint(API.app, url_prefix="/api")
from DB import VM_PATHS

@app.before_request
def Lang_auto():
    if "Lang" not in request.cookies and "Accept-Language" in request.headers:
        languages=request.headers["Accept-Language"].split(",")
        for language in languages:
            if language in langs:
                resp=make_response(redirect(request.full_path))
                resp.set_cookie("Lang", language)
                return resp

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
allowed_css_translation=["style.css"]
allowed_js_translation=["main.js", "server.js"]
@app.route("/static/<path:file>")
def Static(file):
    looking=f"./static/{file}"
    if os.path.isfile(looking):
        if file in allowed_css_translation: return Response(language.translate(open(looking, encoding="utf8+").read()), mimetype="text/css")
        elif file in allowed_js_translation: return Response(language.translate(open(looking, encoding="utf8+").read()), mimetype="text/javascript")
        else: return send_file(looking)
    else: return abort(404)

print("\033[0;32mStarting VPS Control Panel\n\033[0;32mMade by Parham and Inventionpro with ❤️\033[0m")
if Debug: app.run(host=Host, port=Port, debug=True)
else: serve(app, host=Host, port=Port, threads=Threads)