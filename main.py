# -*- coding: utf-8 -*-

import sys
import requests
import os
import math
import tkinter as tk
import tkinter.ttk as ttk
import pars
import formation

stuck = pars.extract_source()
source = "all"
channels = dict()
output_channels = dict()
groups = ["Ублюдские", "Тошнотворные", "Дибильные", "Конченные", "Ебанутые"]

root = tk.Tk()
root.title("PLUG v G0.3")
root.geometry("800x600+200+200")


def get_geometry():
    """Returns the tuple: (<width>, <height>, <width_position>, <height_position>)
    можно вот так: print(get_geometry()[2])"""
    root.update_idletasks()
    string = root.geometry()
    size, pos = string.split("+", 1)
    x, y = size.split("x")
    px, py = pos.split("+")
    x = int(x)
    y = int(y)
    px = int(px)
    py = int(py)
    return x, y, px, py


def add_channel(event):
    name = name_entry.get()
    link = addr_combobox.get()
    if name != "":
        if name in output_channels:
            print("Канал уже добавлен")
            if link != output_channels[name][0]:
                output_channels[name][0] = link
                print("меняю ссылку")
        else:
            x = [link]
            output_channels[name] = x
            channel_listbox.insert(tk.END, name)
            print("добавляю канал " + name)
        print(output_channels)
    else:
        print("Ничего не выбрано")


def del_channel(event):
    index = channel_listbox.curselection()
    if index != ():
        name = channel_listbox.get(index[0])
        print(name)
        channel_listbox.delete(index[0])
        output_channels.pop(name)
        channel_listbox.select_set(index[0])
    else:
        print("Ничего не выбрано")


def up_channel(event):
    index = channel_listbox.curselection()
    if index != ():
        if index[0] != 0:
            over_name = channel_listbox.get(index[0]-1)
            name = channel_listbox.get(index[0])
            channel_listbox.delete(index[0]-1)
            channel_listbox.insert(index[0]-1, name)
            channel_listbox.delete(index[0])
            channel_listbox.insert(index[0], over_name)
            channel_listbox.select_set(index[0]-1)
    else:
        print("Ничего не выбрано")


def down_channel(event):
    index = channel_listbox.curselection()
    if index != ():
        if index[0] < channel_listbox.size()-1:
            under_name = channel_listbox.get(index[0] + 1)
            name = channel_listbox.get(index[0])
            channel_listbox.delete(index[0] + 1)
            channel_listbox.insert(index[0] + 1, name)
            channel_listbox.delete(index[0])
            channel_listbox.insert(index[0], under_name)
            channel_listbox.select_set(index[0] + 1)
    else:
        print("Ничего не выбрано")


def change_name(event):
    """ЗАГЛУШКА"""
    print(name_entry.get())


def change_addr(event):
    """ЗАГЛУШКА"""
    print(addr_combobox.get())


def update_playlists(event):
    global stuck
    stuck = pars.extract_source()
    fill_origin_listbox(1)
    sources_combobox.config(values=stuck["sources"])


def fill_origin_listbox(event):
    origin_channel_listbox.delete(0, tk.END)
    global channels
    channels = formation.generate_base(stuck[sources_combobox.get()])
    names = formation.dictKeys_to_sortList(channels)
    for i in names:
        origin_channel_listbox.insert(tk.END, i)
    print(sources_combobox.get())


def select_channel(event):
    index = channel_listbox.curselection()
    if not index == ():
        links = []
        name = channel_listbox.get(index[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        links.append(output_channels[name][0])
        addr_label.config(text="Адрес:(" + str(len(links)) + ")")
        addr_combobox.config(values=links)
        addr_combobox.current(newindex=0)


def select_origin_channel(event):
    index = origin_channel_listbox.curselection()
    if not index == ():
        links = []
        name = origin_channel_listbox.get(index[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        for link in channels[name]:
            links.append(link)
        addr_label.config(text="Адрес:(" + str(len(links)) + ")")
        addr_combobox.config(values=links)
        addr_combobox.current(newindex=0)


def check_link(event):
    link = addr_combobox.get()
    file_name = 'check_link.m3u'
    link_file = open(file_name, "w", encoding="utf-8")
    link_file.write("#EXTM3U\n")
    link_file.write("#EXTINF:-1," + link + "\n")
    link_file.write(link)
    link_file.close()
    os.startfile(file_name)


top_frame = tk.Frame(root, height=30)

list_frame = tk.Frame(root)

left_frame = tk.Frame(list_frame)
sources_combobox = ttk.Combobox(left_frame, values=stuck["sources"])
sources_combobox.current(newindex=0)
sources_combobox.bind("<<ComboboxSelected>>", fill_origin_listbox)

origin_channel_listbox = tk.Listbox(left_frame)
ocl_scroll = tk.Scrollbar(left_frame)
ocl_scroll["command"] = origin_channel_listbox.yview
origin_channel_listbox["yscrollcommand"] = ocl_scroll.set
origin_channel_listbox.bind("<<ListboxSelect>>", select_origin_channel)

right_frame = tk.Frame(list_frame)
channel_listbox = tk.Listbox(right_frame)
channel_listbox.bind("<<ListboxSelect>>", select_channel)
cl_scroll = tk.Scrollbar(right_frame)
cl_scroll["command"] = channel_listbox.yview
channel_listbox["yscrollcommand"] = cl_scroll.set

sort_frame = tk.Frame(root)
add_btn = tk.Button(sort_frame, text="add")
add_btn.bind("<Button-1>", add_channel)
up_btn = tk.Button(sort_frame, text="/\\")
up_btn.bind("<Button-1>", up_channel)
down_btn = tk.Button(sort_frame, text="\/")
down_btn.bind("<Button-1>", down_channel)
del_btn = tk.Button(sort_frame, text="del")
del_btn.bind("<Button-1>", del_channel)

edit_frame = tk.Frame(root)
name_label = tk.Label(edit_frame, text="Название:")
name_entry = tk.Entry(edit_frame, width=60)
name_entry.bind("<Return>", change_name)
addr_label = tk.Label(edit_frame, text="Адрес:")
addr_combobox = ttk.Combobox(edit_frame)
addr_combobox.bind("<Return>", change_addr)
action_addr_frame = tk.Frame(edit_frame)
check_btn = tk.Button(action_addr_frame, text="Смотреть")
check_btn.bind("<Button-1>", check_link)

group_label = tk.Label(edit_frame, text="Группа:")
group_menu = tk.Menu(edit_frame)
root.config(menu=group_menu)
group_menu.add_command(label="test")
group_combobox = ttk.Combobox(edit_frame, values=groups)
update_btn = tk.Button(root, text="UPDATE")
update_btn.bind("<Button-1>", update_playlists)

# packs
top_frame.pack(side=tk.TOP, fill="x", expand=False)
list_frame.pack(side=tk.LEFT, fill="both", expand=True)

left_frame.pack(side=tk.LEFT, fill="both", expand=True)
sources_combobox.pack()
right_frame.pack(side=tk.RIGHT, fill="both", expand=True)
origin_channel_listbox.pack(side=tk.LEFT, fill="both", expand=True)
ocl_scroll.pack(side=tk.LEFT, fill="both")
channel_listbox.pack(side=tk.LEFT, fill="both", expand=True)
cl_scroll.pack(side=tk.LEFT, fill="both")

sort_frame.pack()
add_btn.pack(side=tk.LEFT)
up_btn.pack(side=tk.LEFT)
down_btn.pack(side=tk.LEFT)
del_btn.pack(side=tk.LEFT)
edit_frame.pack()
name_label.pack()
name_entry.pack(fill="both", expand=True)
addr_label.pack()
addr_combobox.pack(fill="both", expand=True)
action_addr_frame.pack(side=tk.TOP, fill="both", expand=True)
check_btn.pack(side=tk.LEFT)
group_label.pack()
group_combobox.pack()

update_btn.pack(side=tk.BOTTOM)

fill_origin_listbox(1)
root.mainloop()
