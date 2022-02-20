from Client_Actions import Client_Actions
from Vision import Vision
from Mouse import Mouse
import json
import time
import pyautogui

class TFT_Bot(Client_Actions, Vision, Mouse):
    def __init__(self):
        file = open("settings.json")
        self.settings = json.load(file)
        for k,v in self.settings.items():
            setattr(self, k, v)
        file.close()

        self.handle = None
        self.stages = ["Find match", "Accept match", "Ingame", "Exit", "Play again"]
        self.cStage = 0
        self.nStage = 1
        self.last_action = time.time()
        self.length = 600

    def start(self):
        if not self.is_client_open():
            self.launch_client()

        self.register_window()
        self.set_active()
        self.get_in_lobby()

    def stage_increase(self):
        self.cStage = self.nStage
        self.nStage = (self.nStage +1) % 5
        self.last_action = time.time()
    
    def inactive(self):
        return self.last_action + self.length < time.time()

    def reset(self):
        self.cStage = 0
        self.nStage = 1
        self.last_action = time.time()
        self.kill_client()
        while self.is_client_open():
            time.sleep(1)
        self.start()


    def stage_print(self):
        print("Current stage: ", self.stages[self.cStage], "Next stage: ", self.stages[self.nStage])

    def get_in_lobby(self):
        #Check play button
        if self.pixel_matches_color((120,26),(7,177,178),10):
            print("Opening TFT NORMAL lobby.")
            self.click(120,35)
            time.sleep(0.5)
            #Click TFT, Normal, Confirm
            self.click(625,210)
            self.click(580,515)
            self.click(540,690)
            self.mouse_move(650,690)

    def find_match(self):
        #Check if "Find match" button is clickable
        if self.pixel_matches_color((540,663),(5,150,170)):
                self.click(600,675)
                print('In queue.')
                self.mouse_move(750,675)
                return True

    def accept_match(self):
        #Check if client closed and we entered loading screen
        handles_windows_rect = self.get_handle_window_rect()
        if len([rect for rect in handles_windows_rect if rect[0] > 0]) == 0:
            self.stage_increase()
            print("Enterin game.")
            return True

        #Check for accept button
        if self.pixel_matches_color((700,535),(9, 194, 181)): #700,535 | 9 194 181
            print("Accepting match.")
            self.click(650,550)
            self.mouse_move(800,550)
            return True

    def exit_game(self):
        #Check if client has reopened
        handles_windows_rect = self.get_handle_window_rect()
        if len([rect for rect in handles_windows_rect if rect[0] > 0]) > 0:
            self.register_window()
            self.stage_increase()
            return True
        #Check if exit button is on screen
        if self.pixel_matches_color((740,540),(8,65,83),False) and self.pixel_matches_color((920,540),(8,65,83),False):
            print("Exiting game.")
            self.click(780,550,False)
            time.sleep(0.3)
            self.click(780,550,False)

    def play_again(self):
        if self.pixel_matches_color((540,670),(5,150,170)):
                self.click(600,675)
                print('Play again.')
                self.mouse_move(750,675)
                return True

    def game_loop(self):
        if self.stages[self.nStage] == "Find match":
            if self.find_match():
                self.stage_increase()
        elif self.stages[self.nStage] == "Accept match":
            if self.accept_match():
                self.stage_increase()
        elif self.stages[self.nStage] == "Exit":
            if self.exit_game():
                self.stage_increase()
        elif self.stages[self.nStage] == "Play again":
            if self.play_again():
                self.stage_increase()

        if self.stages[self.cStage] == "Find match":
            self.find_match()
        elif self.stages[self.cStage] == "Accept match":
            self.accept_match()
        elif self.stages[self.cStage] == "Ingame":
            pass
        elif self.stages[self.cStage] == "Exit":
            self.exit_game()
        elif self.stages[self.cStage] == "Play again":
            self.play_again()

if __name__ == "__main__":
    x = TFT_Bot()
    x.start()
    start = time.time()
    while True:
        x.game_loop()
        if time.time()- start > 60:
            start = time.time()
            x.stage_print()
        if x.inactive():
            print("Time from last action:", time.time()-x.last_action)
            x.reset()
    
    


