from Client_Actions import Client_Actions
from Vision import Vision
from Mouse import Mouse
import json
import time
import pyautogui
import random

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
        self.champions = "Yordle"

    def start(self):
        if not self.is_client_open():
            self.launch_client()

        self.register_window()
        self.set_active()
        self.get_in_lobby()

    def stage_increase(self):
        self.cStage = self.nStage
        self.nStage = (self.nStage +1) % len(self.stages)
        self.last_action = time.time()
    
    def inactive(self):
        return self.last_action + self.length < time.time() and not self.stages[self.cStage] == "Ingame"

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
            self.area_click((75,30,170,55))
            time.sleep(0.5)
            #Click TFT, Normal, Confirm
            self.area_click((580,180,670,270))
            self.area_click((540,514,620,520))
            self.area_click((470,680,610,697))
            self.area_mouse_move((800,600,1000,700)) #(800,600,1000,700)

    def find_match(self):
        #Check if "Find match" button is clickable
        if self.pixel_matches_color((540,663),(5,150,170)):
                self.area_click((470,667,610,690))
                print('In queue.')
                self.area_mouse_move((800,600,1000,700))
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
            self.area_click((560,540,720,565))
            self.area_mouse_move((800,600,1000,700))
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
            self.area_click((740,540,920,560), False)
            time.sleep(0.3)
            self.area_click((740,540,920,560), False)

    def play_again(self):
        if self.pixel_matches_color((540,670),(5,150,170)):
                self.area_click((470,667,610,690))
                print('Play again.')
                self.area_mouse_move((800,600,1000,700))
                return True

    def ingame(self):
        img = self.screen_shot()
        locations = self.locateAllOnScreen("Champions/"+ self.champions+".png",img)
        for x, y in locations:
            self.area_click((x+10,y-40,x+150,y+40),False)
            time.sleep(0.3 + random.random())
        time.sleep(0.5)

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
            self.ingame()
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
    
    


