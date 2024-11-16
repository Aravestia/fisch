import cv2
import pyautogui
import numpy as np
import time
import keyboard

template_path = r"C:\Users\65878\Downloads\Programming\Usable\AHK\fisch\shake.png"
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
template_width, template_height = template.shape[::-1]
template_threshold = 0.5

center_x = 0
center_y = 0
center_x_prev = 0
center_y_prev = 0

def click_shake(center_x, center_y):
    pyautogui.moveTo(center_x, center_y)
            
    pyautogui.mouseDown(button='right')
    time.sleep(0.01)
    pyautogui.mouseUp(button='right')
    
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()
    
    #print(f"Clicked at: ({center_x}, {center_y})")

def auto_shake():
    global center_x
    global center_y
    global center_x_prev
    global center_y_prev
    
    screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    matches = np.where(result >= template_threshold)

    if len(matches[0]) > 0:
        x = matches[1][0]
        y = matches[0][0]
        center_x = x + (template_width // 2)
        center_y = y + (template_height // 2)
        
        if center_x != center_x_prev or center_y != center_y_prev:
            click_shake(center_x, center_y)
            
        center_x_prev = center_x
        center_y_prev = center_y

toggle = True

while True:
    if keyboard.is_pressed('f5'):
        toggle = not toggle
        print(f"Auto shake: {toggle}")
        time.sleep(0.5) 
    
    if toggle:
        auto_shake()
        time.sleep(0.05)
    
