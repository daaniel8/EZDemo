import gzip
import shutil
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import Menu
from tkinter import simpledialog
import config
import string
import random
import re
import requests
import json
import numpy as np
import os

API_KEY = config.api_key

def set_filepath():
    with open('config.txt','w') as f:
        f.write(simpledialog.askstring(title="Test", prompt="set filepath"))


def commence():
    Output.delete('1.0', END)
    filetypes = (('text files', '*.gz'),('All files', '*.*'))

    demo = fd.askopenfilename(title='Open a file',initialdir='/downloads',filetypes=filetypes)
    unzip_save(demo)

def unzip_save(demo):
    name = name_var.get()
    name_var.set("")
    playerz = []

    if os.path.isfile('config.txt'):
        with open('config.txt','r') as f:
            inputt = f.read()
    else:
        print('enter path to replays in menu')

    replaysf = inputt.replace('\\', '/')
    csgof = replaysf.split('csgo/', 1)[1]

    with gzip.open(demo, 'rb') as f_in:
        with open(replaysf + '/' + str(name) + '.dem', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    lineslist = []
    ids = []

    f = open(replaysf + '/' + str(name) + '.dem', encoding='ANSI', errors='ignore')

    for line in f:
        z = re.findall(r"[0-9]{17}", line)
        if len(z) == 2:
            if z[1] not in ids:
                ids.append(z[1])

    for l in ids:
        api_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+ str(API_KEY) + '&steamids=' + str(l)
        response = requests.get(api_url)
        my_json = response.json()
        playerz.append(my_json['response']['players'][0]['personaname'] + ': ' + str(l))

    print('worked')
    for i in playerz:
        Output.insert(END, i + "\n")

    Output.insert(END, "\n" + 'playdemo ' + csgof + '/' + name + '.dem')

root= Tk()
root.title("EZDemo")
root.geometry("750x350")

menubar = Menu(root)
root.config(menu=menubar)

# create a menu
file_menu = Menu(menubar)

# add a menu item to the menu
file_menu.add_command(
    label='Config',
    command=set_filepath
)


# add the File menu to the menubar
menubar.add_cascade(
    label="Settings",
    menu=file_menu
)

name_var=tk.StringVar()

name_label = tk.Label(root, text = 'Demo save name', font=('calibre',10, 'bold'))
name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))

name_label.pack()
name_entry.pack()

Output = Text(root, height = 15,
              width = 40,
              )
Output.pack()

open_button = ttk.Button(root,text='Choose demo file',command=commence)
open_button.pack(expand=True)

root.mainloop()