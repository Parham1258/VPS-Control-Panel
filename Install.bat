@echo off
title VPS Control Panel Installer
cls
color f
echo [0;33mThis script requiers Python to run, Please install the latest version of python from https://www.python.org/ and make sure to check the `Add to PATH`
echo [0;32mThis script will install VPS Control Panel in ./VPS-Control-Panel directory
echo [0mPress any key to continue with the installation
pause >nul
echo Started the installation
echo Installing Git
winget install --id Git.Git -e --source winget
echo Cloning the repository from GitHub
git clone https://github.com/Parham1258/VPS-Control-Panel
cd VPS-Control-Panel
echo Installing requirements
pip install -r requirements.txt
echo Installation completed in ./VPS-Control-Panel directory
echo Press any key to open the configuration file, Learn more at https://github.com/Parham1258/VPS-Control-Panel/wiki/Config#config-file
pause >nul
notepad Config.py
echo Press any key to open the VM Paths file, Learn more at https://github.com/Parham1258/VPS-Control-Panel/wiki/Config#vm-paths-file
pause >nul
notepad VM Paths.json
echo To start the panel, you can run it with ./VPS-Control-Panel/start.bat later
echo Press any key to start the panel
pause >nul
start.bat