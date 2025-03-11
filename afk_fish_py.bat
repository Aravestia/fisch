@echo off

cd /d %~dp0

start /min cmd /k "python reel\reel_py.py"
start /min cmd /k "python shake\shake_py.py"

exit
