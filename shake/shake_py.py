import numpy as np
import cv2
import pyautogui
import dxcam

import time
from datetime import datetime
import os

class Shake():
    def __init__(self):

        self.variables = []
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "variables.txt"), "r") as file:
            self.variables = [line.strip() for line in file]
        
        self.camera = dxcam.create(device_idx=int(self.variables[1]), output_idx=0)

        self.template = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shake.png"), cv2.IMREAD_GRAYSCALE)
        self.template_width, self.template_height = self.template.shape[::-1]
        self.template_threshold = 0.8

        self.res_x = 1920
        self.res_y = 1080

        self.grab_left = 400
        self.grab_right = self.res_x - self.grab_left
        self.grab_top = 150
        self.grab_bottom = self.res_y - self.grab_top

        self.center_x_prev = 0
        self.center_y_prev = 0

        self.start_time = datetime.now()

    def click_shake(self, center_x, center_y):
        pyautogui.moveTo(center_x, center_y)
                
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right')
        time.sleep(0.1)
        
        pyautogui.click()

        print("click")

    def auto_shake(self):     
        grab = self.camera.grab(region=(self.grab_left, self.grab_top, self.grab_right, self.grab_bottom))
        
        if grab is not None:
            screenshot = cv2.cvtColor(grab, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(screenshot, self.template, cv2.TM_CCOEFF_NORMED)
            matches = np.where(result >= self.template_threshold)
            
            if len(matches[0]) > 0:
                center_x = matches[1][0] + (self.template_width // 2) + self.grab_left
                center_y = matches[0][0] + (self.template_height // 2) + self.grab_top
                
                if abs(center_x - self.center_x_prev) > 1 or abs(center_y - self.center_y_prev) > 1:
                    print(f"x: {center_x}, y: {center_y}")
                    self.click_shake(center_x, center_y)
                    
                    self.center_x_prev = center_x
                    self.center_y_prev = center_y
            else:
                time.sleep(0.2)

if __name__ == '__main__':
    shake = Shake()
    print("start.")

    try:
        while True:
            shake.auto_shake()
    except KeyboardInterrupt:
        current_time = datetime.now()
        et = (current_time - shake.start_time).seconds
        print(f"Time elapsed: {et // 3600}h {(et // 60) % 60}m {et % 60}s")

    
