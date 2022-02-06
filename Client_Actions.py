import subprocess #open LeagueClient
import psutil #access list of processes
import time
import win32gui
import pyautogui


class Client_Actions:
    def __init__(self):
        self.client_location = "C:\\Riot Games\\League of Legends\\LeagueClient.exe"
        self.handle = None

    def is_client_open(self):
        for proc in psutil.process_iter():
            try:
                if proc.name() == u"LeagueClient.exe":
                    return True
            except psutil.AccessDenied:
                print("Permission error or access denied on process")
        
        return False
    
    def launch_client(self):
        print("Opening LeagueClient")
        while(not self.is_client_open()):
                subprocess.Popen(self.client_location)
                print("...",end = '')
                time.sleep(30)
        print("\nClient opened.")

    def kill_client(self):
        kill = {"LeagueClient.exe","League of Legends.exe","RiotClientServices.exe"}

        for proc in psutil.process_iter():
            try:
                if proc.name() in kill:
                    subprocess.call(["taskkill","/F","/IM",proc.name()])
            except psutil.AccessDenied:
                print("Permission error or access denied on process")
    
    def get_handles(self, name="League of Legends"):
        def win_enum_callback(handle, param):
            if name == str(win32gui.GetWindowText(handle)):
                param.append(handle)

        handles = []
        win32gui.EnumWindows(win_enum_callback, handles)
        return handles

    def get_handle_window_rect(self, name="League of Legends"):
        handles = self.get_handles(name)
        return [win32gui.GetWindowRect(handle) for handle in handles]

    def register_window(self, name="League of Legends"):
        handles = self.get_handles(name)
        for handle in handles:
            #print(win32gui.GetWindowRect(handle))
            if win32gui.GetWindowRect(handle)[0] > 0:
                self.handle = handle
        #print("######################")

    def is_active(self):
        return self.handle == win32gui.GetForegroundWindow()

    def set_active(self):
        if not self.is_active():
            pyautogui.press('alt')
            win32gui.SetForegroundWindow(self.handle)
            pyautogui.press('alt')
        return self

    def get_window_rect(self):
        rect = win32gui.GetWindowRect(self.handle)
        return [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]