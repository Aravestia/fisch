@echo off

cd /d %~dp0

start /min cmd /k "python shake\shake_py.py"

exit
