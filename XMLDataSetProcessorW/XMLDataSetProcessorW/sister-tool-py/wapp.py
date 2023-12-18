import glob
import json
from tkinter import Tk, Label, filedialog
from tkinter.ttk import Button

from tkinter import ttk

import processor

window = Tk()


def start():
    style = ttk.Style()
    style.theme_use("clam")
    label_info = Label(window, text="Select a directory:")
    label_info.grid(column=0, row=2, padx=10)
    button_explore = Button(window, text="Browse Files", command=browse_files)
    button_explore.grid(column=1, row=2, pady=10, padx=10)
    window.mainloop()


def get_window_settings():
    """
    Fetch the window settings from the json file
    Returns: Settings dictionary
    """
    _settingsJSON = open('./wapp/stts/settings.json')
    _settings = json.load(_settingsJSON)
    window.title(_settings["title"])
    _geometry = f"{_settings["resolution"]["x"]}x{_settings["resolution"]["y"]}"
    window.geometry(_geometry)

    return _settings


def browse_files():
    _folder = filedialog.askdirectory(initialdir="./", title="Select a Folder")

    lbl_file_explorer = Label(window, text="File Explorer using Tkinter", width=100, height=4)
    for file in directory_files:
        print(f"Processing file: {file}")
        lbl_file_explorer.configure(text=f"Processing file: {file}")
        processor.start_processing(file)


if __name__ == '__main__':
    settings = get_window_settings()
    print(f"Fetched settings: {settings}")
    start()
