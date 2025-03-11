#!/bin/bash

cd "$(dirname "$0")"

python3 reel/reel_py.py &  
python3 shake/shake_py.py &  

wait