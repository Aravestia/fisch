import numpy as np
import cv2
import pyautogui
import dxcam

import time
from datetime import datetime

camera = dxcam.create()

reel_pivot = cv2.imread(r"C:\Users\65878\Downloads\Programming\Usable\AHK\fisch\reel\reel_pivot.png", cv2.IMREAD_GRAYSCALE)
reel_pivot_width, reel_pivot_height = reel_pivot.shape[::-1]
reel_pivot_threshold = 0.9

reel_pivot_off = cv2.imread(r"C:\Users\65878\Downloads\Programming\Usable\AHK\fisch\reel\reel_pivot_off.png", cv2.IMREAD_GRAYSCALE)
reel_pivot_off_width, reel_pivot_off_height = reel_pivot_off.shape[::-1]
reel_pivot_off_threshold = 0.9

res_x = 1920
res_y = 1080

grab_left = 572
grab_right = 1348
grab_top = 856
grab_bottom = 887

grab_length = grab_right - grab_left

pivot_pos = 0

bar_length_00 = 233
bar_length_05 = 271
bar_length_15 = 349

start_time = datetime.now()
current_time = start_time

at = datetime.now()

def auto_reel(bar_length):
    global pivot_pos
    global at
    
    grab = camera.grab(region=(grab_left, grab_top, grab_right, grab_bottom))
    
    if grab is not None:
        screenshot = cv2.cvtColor(grab, cv2.COLOR_BGR2GRAY)
        
        result_pivot = cv2.matchTemplate(screenshot, reel_pivot, cv2.TM_CCOEFF_NORMED)
        matches_pivot = np.where(result_pivot >= reel_pivot_threshold)
        
        result_pivot_off = cv2.matchTemplate(screenshot, reel_pivot_off, cv2.TM_CCOEFF_NORMED)
        matches_pivot_off = np.where(result_pivot_off >= reel_pivot_off_threshold)
        
        if len(matches_pivot[0]) > 0 or len(matches_pivot_off[0]) > 0:    
            if len(matches_pivot[0]) > 0:
                pivot_pos = matches_pivot[1][0] + (reel_pivot_width // 2)
            else:
                if len(matches_pivot_off[0]) > 0:
                    pivot_pos = matches_pivot_off[1][0] + (reel_pivot_off_width // 2)
            
            if pivot_pos < bar_length:
                pyautogui.mouseUp()
            elif pivot_pos > grab_length - bar_length:
                pyautogui.mouseDown()
            else:
                pyautogui.mouseDown()
                time.sleep(0.01)
                pyautogui.mouseUp()
                
            at = datetime.now()
    
    ct = datetime.now()            
    if (ct - at).seconds >= 15:
        print("cast")
        
        pyautogui.mouseDown(button='right')
        time.sleep(0.05)
        pyautogui.mouseUp(button='right')
        time.sleep(0.05)
        
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.mouseUp()
        
        at = datetime.now()

print("Program start.")

try:
    while True:
        auto_reel(bar_length=bar_length_15)
except KeyboardInterrupt:
    current_time = datetime.now()
    et = (current_time - start_time).seconds
    print(f"Time elapsed: {et// 3600}h {et // 60}m {et % 60}s")

    
