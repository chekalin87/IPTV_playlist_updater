# -*- coding: utf-8 -*-

import math
import tkinter as tk

root = tk.Tk()
root.title("PLUG v G0.1")
root.geometry("800x800+2000+100")


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
    """ЗАГЛУШКА"""
    channel_list.insert(tk.END, name_entry.get() + ">>>" + addr_entry.get())
    print("Шо я делаю?")


def change_name(event):
    """ЗАГЛУШКА"""
    print(name_entry.get())


def change_addr(event):
    """ЗАГЛУШКА"""
    print(addr_entry.get())


top_frame = tk.Frame(root, bg="green", height=30)

list_frame = tk.Frame(root, bg="white")
channel_list = tk.Listbox(list_frame)
scroll = tk.Scrollbar(list_frame)

sort_frame = tk.Frame(root)
add_btn = tk.Button(sort_frame, text="add")
add_btn.bind("<Button-1>", add_channel)
up_btn = tk.Button(sort_frame, text="/\\")
down_btn = tk.Button(sort_frame, text="\/")
del_btn = tk.Button(sort_frame, text="del")

edit_frame = tk.Frame(root)
name_label = tk.Label(edit_frame, text="Название:")
name_entry = tk.Entry(edit_frame)
name_entry.bind("<Return>", change_name)
addr_label = tk.Label(edit_frame, text="Адрес:")
addr_entry = tk.Entry(edit_frame)
addr_entry.bind("<Return>", change_addr)

# packs
top_frame.pack(side=tk.TOP, fill="x", expand=False)
list_frame.pack(side=tk.LEFT, fill="both", expand=True)
channel_list.pack(side=tk.LEFT, fill="both", expand=True)
scroll.pack(side=tk.RIGHT, fill="both")
sort_frame.pack()
add_btn.pack(side=tk.LEFT)
up_btn.pack(side=tk.LEFT)
down_btn.pack(side=tk.LEFT)
del_btn.pack(side=tk.LEFT)
edit_frame.pack()
name_label.pack()
name_entry.pack()
addr_label.pack()
addr_entry.pack()


root.mainloop()
