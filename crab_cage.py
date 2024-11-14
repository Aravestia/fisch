import cv2
import pyautogui
import numpy as np
import time
import keyboard

# Load the template image of the button
template_path = r"C:\Users\65878\Downloads\Programming\Usable\AHK\fisch\e.png"
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
template_width, template_height = template.shape[::-1]

# Threshold for template matching
threshold = 0.7  # Adjust based on how closely the template should match

center_x = 0
center_y = 0
center_x_prev = 0
center_y_prev = 0

def click_shake():
    global center_x
    global center_y
    global center_x_prev
    global center_y_prev
    
    #time.sleep(0.2)
    
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)  # Convert screenshot to numpy array
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Find locations where the matching score is above the threshold
    locations = np.where(result >= threshold)

    # If any match is found
    if len(locations[0]) > 0:
        y, x = locations[0][0], locations[1][0]
        center_x, center_y = x + template_width // 2, y + template_height // 2
        
        if center_x != center_x_prev or center_y != center_y_prev:
            pyautogui.moveTo(center_x, center_y)
            
            pyautogui.mouseDown(button='right')
            time.sleep(0.01)
            pyautogui.mouseUp(button='right')
            
            pyautogui.mouseDown()
            time.sleep(0.45)
            pyautogui.mouseUp()
            
            print(f"Clicked at: ({center_x}, {center_y})")
            
        center_x_prev = center_x
        center_y_prev = center_y

while True:
    click_shake()
