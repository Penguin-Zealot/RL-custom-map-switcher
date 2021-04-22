import tkinter as tk
from tkinter import filedialog
import os
import shutil
import sys

maps_folder = "/workshop/content/252950"
mods_folder = "/common/rocketleague/TAGame/CookedPCConsole/mods"

class RLMapSwitcher(tk.Tk):
    def __init__(self):
        super(RLMapSwitcher, self).__init__()
        self.title("RL Map Switcher")

        self.rl_path = self.find_rl_path()
        self.maps = self.find_maps()
        self.labs_file = self.rl_path + mods_folder + "/Labs_Underpass_P.upk"

        # widgets
        # TODO: add labels and confirmation text
        self.selected_map = tk.StringVar(self)
        self.selected_map.set("choose a map")
        self.selected_map.trace_add('write', self.change_map)

        self.maps_drop_down = tk.OptionMenu(self, self.selected_map, "none", *self.maps.keys())
        self.maps_drop_down.config(width=20, font=("Helvetica", "18"))
        self.maps_drop_down.pack(expand=True, fill=tk.Y)

        self.refresh_button = tk.Button(self, text="Refresh Maps", command=self.set_maps)
        self.refresh_button.config(fg="green", font=("Helvetica", "18"))
        self.refresh_button.pack(side=tk.LEFT, fill=tk.Y)

        self.clear_button = tk.Button(self, text="Clear Map", command=self.clear_map)
        self.clear_button.config(fg="red", font=("Helvetica", "18"))
        self.clear_button.pack(side=tk.RIGHT, fill=tk.Y)

    
    def find_rl_path(self):
        rl_path = ""
        rl_path_save = os.path.expanduser("~/MyRLPath.txt")
        # check saved location
        if os.path.exists(rl_path_save):
            with open(rl_path_save, 'r') as f:
                rl_path = f.readline()
        else:
            # open file explorer
            rl_path = filedialog.askopenfilename(
                initialdir =  "/", 
                title = "Find RocketLeague.exe", 
                filetype = (("exe files","*.exe"),("all files","*.*")))
            # TODO: check if path is legit, re-open file explorer if not (put in while loop)

            # save path
            rl_path = rl_path.split('/common')[0]
            with open(rl_path_save, 'w+') as f:
                f.write(rl_path)

        # create mods folder if it doesnt exist
        if not os.path.exists(rl_path + mods_folder):
            try:
                os.mkdir(rl_path + mods_folder)
            except OSError as error:
                print(error)
        
        return rl_path

    # get all workshop maps {"name":"path"} 
    # BUG: if two workshop maps have the same name one will be overwritten in the dict
    def find_maps(self):
        maps = {} 
        for root, _, files in os.walk(self.rl_path + maps_folder):
            for fn in files:
                if fn.endswith('.udk'):
                    maps[fn.split('.')[0]] = os.path.join(root, fn)

        return maps

    def set_maps(self):
        self.maps = self.find_maps()
        self.selected_map.set("choose a map")

    # copy selected map to mods folder and renames
    def change_map(self, *args):
        if (self.selected_map.get() == "choose a map" or "none"): return
        try:
            shutil.copyfile(self.maps[self.selected_map.get()], self.labs_file)
        except OSError as error:
            print(error)
        except KeyError as error:
            print(error)

    # remove custom map
    def clear_map(self):
        try:
            os.remove(self.labs_file)
            self.selected_map.set("choose a map")
        except OSError as error:
            print(error)


if __name__ == "__main__":
    app = RLMapSwitcher()
    app.mainloop()