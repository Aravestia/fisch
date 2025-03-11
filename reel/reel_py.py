import numpy as np
import cv2
import pyautogui
import dxcam

import time
from datetime import datetime
import os

class Reel():
    def __init__(self):

        self.variables = []
        with open("variables.txt", "r") as file:
            self.variables = [line.strip() for line in file]
            
        self.camera = dxcam.create(device_idx=int(self.variables[1]), output_idx=0)

        self.reel_pivot = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reel_pivot.png"), cv2.IMREAD_GRAYSCALE)
        self.reel_pivot_width, self.reel_pivot_height = self.reel_pivot.shape[::-1]
        self.reel_pivot_threshold = 0.9

        self.reel_pivot_off = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reel_pivot_off.png"), cv2.IMREAD_GRAYSCALE)
        self.reel_pivot_off_width, self.reel_pivot_off_height = self.reel_pivot_off.shape[::-1]

        self.res_x = 1920
        self.res_y = 1080

        self.grab_left = 572
        self.grab_right = 1348
        self.grab_top = 856
        self.grab_bottom = 887

        self.grab_length = self.grab_right - self.grab_left

        self.pivot_pos = 0
        self.pivot_pos_prev = 0

        self.bar_lengths = {
            "0" : 233,
            "0.05" : 271,
            "0.1" : 309,
            "0.15" : 349,
            "0.2" : 387,
        }
        self.bar_length = self.bar_lengths[self.variables[3]]

        self.start_time = datetime.now()
        self.current_time = self.start_time

        self.action = False
        self.at = datetime.now()

    def follow_pivot(self, pivot_pos, pivot_pos_prev):
        if pivot_pos < self.bar_length:
            pyautogui.mouseUp()
            print("<<")
        elif pivot_pos > self.grab_length - self.bar_length:
            pyautogui.mouseDown()
            time.sleep(0.25)
            print(">>")
        else:
            if pivot_pos_prev > pivot_pos:
                pyautogui.click()
                time.sleep(0.02)
                print("<=")
            elif pivot_pos_prev < pivot_pos:
                pyautogui.mouseDown()
                print("=>")
            else:
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                print("==")

    def cast_rod(self):
        print("cast")

        pyautogui.mouseDown(button='right')
        time.sleep(0.05)
        pyautogui.mouseUp(button='right')
        time.sleep(0.05)
        
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.mouseUp()
        
        self.action = False
        self.at = datetime.now()

    def auto_reel(self):  
        grab = self.camera.grab(region=(self.grab_left, self.grab_top, self.grab_right, self.grab_bottom))
        
        if grab is not None:
            screenshot = cv2.cvtColor(grab, cv2.COLOR_BGR2GRAY)
            
            result_pivot = cv2.matchTemplate(screenshot, self.reel_pivot, cv2.TM_CCOEFF_NORMED)
            if np.max(result_pivot) < self.reel_pivot_threshold:
                result_pivot = cv2.matchTemplate(screenshot, self.reel_pivot_off, cv2.TM_CCOEFF_NORMED)
            
            matches_pivot = np.where(result_pivot >= self.reel_pivot_threshold)
            
            if len(matches_pivot[0]) > 0:    
                self.pivot_pos = matches_pivot[1][0] + (self.reel_pivot_width // 2)
                
                self.follow_pivot(self.pivot_pos, self.pivot_pos_prev)
                    
                self.pivot_pos_prev = self.pivot_pos
                self.action = True
                self.at = datetime.now()
                
        ct = datetime.now()
        seconds_before_cast = float(self.variables[5]) if self.action else float(self.variables[7])
        
        if (ct - self.at).seconds >= seconds_before_cast:
            self.cast_rod()

if __name__ == '__main__':
    reel = Reel()
    
    try:
        while True:
            reel.auto_reel()
    except KeyboardInterrupt:
        current_time = datetime.now()
        et = (current_time - reel.start_time).seconds
        print(f"Time elapsed: {et // 3600}h {(et // 60) % 60}m {et % 60}s")

    
