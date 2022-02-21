import pyautogui
from PIL import ImageGrab
import cv2
import numpy as np

class Vision:
    """ def screenshot(self, name, region=False):
        window = self.get_window_rect()
        if not region:
            # Set the default region to the area of the window
            region = window
        else:
            # Adjust the region so that it is relative to the window
            wx, wy = window[:2]
            region = list(region)
            region[0] += wx
            region[1] += wy

        pyautogui.screenshot(name, region=region) """

    def pixel_matches_color(self, coords, rgb, relative=True, threshold=10):
        """ Matches the color of a pixel relative to the window's position """
        wx, wy = (0,0)
        if relative:
            wx, wy = self.get_window_rect()[:2]
        x, y = coords
        return pyautogui.pixelMatchesColor(x + wx, y + wy, rgb, tolerance=threshold)

    def screen_shot(self):
        img = ImageGrab.grab()
        img = np.array(img)
        return cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    def locateOnScreen(self,needle,haystack):
        needle_img = cv2.imread(needle)
        result = cv2.matchTemplate(haystack,needle_img,cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.9:
            return max_loc
        else: return (None,None)
    
    def locateAllOnScreen(self,needle,haystack):
        needle_img = cv2.imread(needle)
        result = cv2.matchTemplate(haystack,needle_img,cv2.TM_CCOEFF_NORMED)

        threshold = 0.9
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        locations = [(x,y) for x,y in locations]

        #getting rid of similar points
        d=30
        locations = {((x - (x % d)), (y - (y % d))) : (x,y) for x, y in locations}
        locations = list(locations)
        return locations