import numpy as np
import cv2
import pyautogui
import dxcam

import time
from datetime import datetime

camera = dxcam.create()

template_path = r"C:\Users\65878\Downloads\Programming\Usable\AHK\fisch\shake.png"
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
template_width, template_height = template.shape[::-1]
template_threshold = 0.5

center_x_prev = 0
center_y_prev = 0

start_time = datetime.now()
current_time = start_time

def click_shake(center_x, center_y):
    pyautogui.moveTo(center_x, center_y)
    time.sleep(0.01)
            
    pyautogui.mouseDown(button='right')
    time.sleep(0.01)
    pyautogui.mouseUp(button='right')
    time.sleep(0.01)
    
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()
    
    print("click")

def auto_shake():
    global center_x_prev
    global center_y_prev
    
    grab = camera.grab()
    
    if grab is not None:  
        screenshot = cv2.cvtColor(grab, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(result >= template_threshold)
        
        if len(matches[0]) > 0:
            center_x = matches[1][0] + (template_width // 2)
            center_y = matches[0][0] + (template_height // 2)
            print(f"x: {center_x}, y: {center_y}")
            
            if center_x != center_x_prev or center_y != center_y_prev:
                click_shake(center_x, center_y)
                
                center_x_prev = center_x
                center_y_prev = center_y
            else:
                print("wait")
                time.sleep(0.01)
            
    time.sleep(0.1)   

run_count = 0
print("Program start.")

try:
    while True:
        auto_shake()
   
except KeyboardInterrupt:
    current_time = datetime.now()
    et = (current_time - start_time).seconds
    print(f"Time elapsed: {et// 3600}h {et // 60}m {et % 60}s")

    
