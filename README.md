# VPS Control Panel
VPS Control Panel is a free control panel service for your VMware Workstation VMs  
VPS Control Panel provides features such as
- Server power actions
- noVNC support
- Easy to use GUI
- and more...
# Compatibility
To install VPS Control Panel you need to have VMware Workstation installed  
Bellow you can see a list of the supported VMware Workstation versions
| Vmware Workstation version | Supported | Description                                                   |
|----------------------------|------------------|---------------------------------------------------------------|
| VMware Workstation 17      | ✅ | Latest version, This panel is also created with this version  |
| VMware Workstation 16 and bellow | ⚠️ | **You shouldn't use old versions as they may have issues and vulnerabilities** *but if you still have to*, should work as long as there is a `vmrun` |
| VMware Workstation 5 and bellow | ❌ | There is no vmrun on these versions |

Compatible Operating Systems
| OS | Supported | Description |
|----|-----------|-------------|
| Windows 🪟 | ✅ | This panel is also created with Windows |
| Linux 🐧 | ✅ | Extra steps required |
# Installation
Use the command bellow to clone the repo
```sh
git clone https://github.com/Parham1258/VPS-Control-Panel
```
> [!NOTE]
> If you're on linux, you should install pip and python 3.12  
> If you're on windows, you should install the latest python version from https://www.python.org/  
> Make sure to do `Add to PATH` when installing python on windows

Now do
```sh
cd VPS-Control-Panel
pip install -r requirements.txt
```
to install packages
> [!IMPORTANT]
> Make sure to configure the VPS Control Panel in `Config.py` and the VM Paths in `VM Paths.json` before using it.

> [!WARNING]
> Don't put the noVNC credentials for your servers unless you have noVNC in `/static/noVNC`; otherwise, it will fail.

Now run the main.py with python
```sh
python main.py
```
> [!NOTE]
> If you're on linux, you can use systemd to run it, for the instructions, please google `How to run a python file with systemd`

Done! you can use the panel now

> [!NOTE]
> To add/remove servers from the VPS Control Panel, edit the `VM Paths.json` and it will be automatically reloaded