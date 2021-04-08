import tkinter as tk
import os
import shutil

common_paths = ["C:\\Program Files (x86)\\Steam\\steamapps","D:\\SteamLibrary\\steamapps","D:\\Program Files (x86)\\Steam\\steamapps"]

maps_folder = "\\workshop\\content\\252950"
mods_folder = "\\common\\rocketleague\\TAGame\\CookedPCConsole\\mods"

rl_path = ""

# find rocket league path (assumes game is installed)
for path in common_paths:
    if os.path.exists(path + "\\common\\rocketleague"):
        rl_path = path
        break

# TODO: if folder not found use manual input (exit otherwise)
if rl_path == "": exit

# create mods folder if it doesnt exist
if not os.path.exists(rl_path + mods_folder):
    try:
        os.mkdir(rl_path + mods_folder)
    except OSError as error:
        print(error)

labs_path = rl_path + mods_folder + "\\Labs_Underpass_P.upk"

# get all workshop maps {"name":"path"} 
# BUG: if two workshop maps have the same name one will be overwritten in the dict
maps = {} 
for root, dirs, files in os.walk(rl_path + maps_folder):
    for fn in files:
      if fn.endswith('.udk'):
        maps[fn.split('.')[0]] = os.path.join(root, fn)

# TODO: get current map
curr_map = list(maps)[0]

# copy selected map to mods folder and renames
def change_map():
    try:
        shutil.copyfile(maps[selected_map.get()], labs_path)
    except OSError as error:
        print(error)

# remove custom map
def clear_map():
    try:
        os.remove(labs_path)
    except OSError as error:
        print(error)

# GUI
# TODO: refresh maps button
# TODO: add labels and confirmation texts
window = tk.Tk()

window.title("RL Map Switcher")

selected_map = tk.StringVar(window)
selected_map.set(curr_map)

drop_down = tk.OptionMenu(window, selected_map, *maps.keys())
drop_down.config(width=18, font=("Helvetica", "18"))
drop_down.pack(expand=True, fill=tk.Y)

choose_map = tk.Button(window, text="Select Map", command=change_map)
choose_map.config(fg="green", font=("Helvetica", "18"))
choose_map.pack(side=tk.LEFT, fill=tk.Y)

clear_map = tk.Button(window, text="Clear Map", command=clear_map)
clear_map.config(fg="red", font=("Helvetica", "18"))
clear_map.pack(side=tk.RIGHT, fill=tk.Y)

window.mainloop()