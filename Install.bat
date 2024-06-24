@echo off
title VPS Control Panel Installer
cls
color f
echo [0;33mThis script requiers Python to run, Please install the latest version of Python from https://www.python.org/ and make sure to check the `Add to PATH`[0m
echo [0;33mThis script will install git with winget automatically[0m
echo [0;32mThis script will install VPS Control Panel in ./VPS-Control-Panel directory[0m
echo [0;33mPress any key to continue with the installation[0m
pause >nul
echo [0;32mStarted the installation[0m
echo [0;33mInstalling Git[0m
winget install --id Git.Git -e --source winget
echo [0;33mCloning the repository from GitHub[0m
git clone https://github.com/Parham1258/VPS-Control-Panel
cd VPS-Control-Panel
echo [0;33mInstalling requirements[0m
pip install -r requirements.txt
echo [0;32mInstallation completed in ./VPS-Control-Panel directory[0m
echo [0;33mPress any key to open the configuration file, Learn more at https://github.com/Parham1258/VPS-Control-Panel/wiki/Config#config-file[0m
pause >nul
notepad Config.py
echo [0;33mPress any key to open the VM Paths file, Learn more at https://github.com/Parham1258/VPS-Control-Panel/wiki/Config#vm-paths-file[0m
pause >nul
notepad VM Paths.json
echo [0;32mTo start the panel, you can run it with ./VPS-Control-Panel/start.bat later[0m
echo [0;33mPress any key to start the panel[0m
pause >nul
start.bat