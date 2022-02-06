import pyautogui

class Vision:
    def screenshot(self, name, region=False):
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

        pyautogui.screenshot(name, region=region)

    def pixel_matches_color(self, coords, rgb, relative=True, threshold=10):
        """ Matches the color of a pixel relative to the window's position """
        wx, wy = (0,0)
        if relative:
            wx, wy = self.get_window_rect()[:2]
        x, y = coords

        """ for i in range(50):
            print((x),(y-i+25) ,pyautogui.pixel((x+wx), (y+wy-i+25)))
        """
        return pyautogui.pixelMatchesColor(x + wx, y + wy, rgb, tolerance=threshold)