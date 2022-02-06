import pyautogui
import ctypes
import time

class Mouse:
    def mouse_move(self, x, y, relative=True, speed=0.5):
        wx, wy = (0,0)
        if relative:
            wx, wy = self.get_window_rect()[:2]
        pyautogui.moveTo(wx + x, wy + y, speed) 

    def click(self, x,y, relative=True, delay=0.1, speed=0.5, button="left"):
        self.mouse_move(x, y, relative, speed)
        time.sleep(delay)
        
        if button == 'left':
            code1 = 0x0002
            code2 = 0x0004
        elif button == 'right':
            code1 = 0x0008
            code2 = 0x0010
        
        ctypes.windll.user32.mouse_event(code1, 0, 0, 0,0) # left down
        time.sleep(0.2)
        ctypes.windll.user32.mouse_event(code2, 0, 0, 0,0) # left up
        time.sleep(0.2)
