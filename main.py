# -*- coding: utf-8 -*-

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import pars
import formation
import generate

title = "PLUG v1.0.6"
icon = "icon.ico"
size_window = "1000x600"


def display_information(txt):
    info_label.config(text=txt)
    print(txt)


def add_channel(event):
    name = name_entry.get()
    link = addr_combobox.get()
    if name != "":
        if name in output_channels:
            display_information("Канал уже добавлен")
            if link != output_channels[name][0]:
                output_channels[name][0] = link
                display_information("поменял ссылку")
        else:
            x = [link, ""]
            output_channels[name] = x
            channel_listbox.insert(tk.END, name)
            display_information("добавил канал " + name)
        change_group(None)  # None - заглушка
    else:
        display_information("Ничего не выбрано")
    for i in range(channel_listbox.size()):
        if name == channel_listbox.get(i):
            channel_listbox.select_set(i)
            select_channel("<<ListboxSelect>>")


def del_channel(event):
    index = channel_listbox.curselection()
    if index != ():
        name = channel_listbox.get(index[0])
        channel_listbox.delete(index[0])
        output_channels.pop(name)
        if index[0] != channel_listbox.size():
            channel_listbox.select_set(index[0])
        else:
            channel_listbox.select_set(index[0] - 1)
        display_information("удалил " + name)
    else:
        display_information("Ничего не выбрано")


def up_channel(event):
    index = channel_listbox.curselection()
    if index != ():
        if index[0] != 0:
            over_name = channel_listbox.get(index[0] - 1)
            name = channel_listbox.get(index[0])
            channel_listbox.delete(index[0] - 1)
            channel_listbox.insert(index[0] - 1, name)
            channel_listbox.delete(index[0])
            channel_listbox.insert(index[0], over_name)
            channel_listbox.select_set(index[0] - 1)
    else:
        display_information("Ничего не выбрано")


def down_channel(event):
    index = channel_listbox.curselection()
    if index != ():
        if index[0] < channel_listbox.size() - 1:
            under_name = channel_listbox.get(index[0] + 1)
            name = channel_listbox.get(index[0])
            channel_listbox.delete(index[0] + 1)
            channel_listbox.insert(index[0] + 1, name)
            channel_listbox.delete(index[0])
            channel_listbox.insert(index[0], under_name)
            channel_listbox.select_set(index[0] + 1)
    else:
        display_information("Ничего не выбрано")


def change_group(event):
    name = name_entry.get()
    if name in channel_listbox.get(0, tk.END):
        group_name = group_combobox.get().strip()
        if group_combobox.current() == -1 and group_name != "":
            groups.append(group_name)
            group_combobox.config(values=groups)
        if output_channels[name][1] != group_name:
            display_information("Группа изменена")
        output_channels[name][1] = group_name


def update_playlists(event):
    global stuck
    stuck = pars.extract_source()
    fill_origin_listbox(1)
    sources_combobox.config(values=stuck["sources"])


def open_playlist():
    file_name = fd.askopenfilename(filetypes=(("m3u files", "*.m3u"), ("m3u8 files", "*.m3u8"), ("All files", "*.*")))
    global output_channels, groups
    output_channels, names, groups = formation.reading_playlist(file_name)
    channel_listbox.delete(0, tk.END)
    for chanel in names:
        channel_listbox.insert(tk.END, chanel)
        group_combobox.config(values=groups)


def export_playlist():
    file_name = fd.asksaveasfilename(filetypes=(("m3u files", "*.m3u"), ("m3u8 files", "*.m3u8"), ("All files", "*.*")),
                                     defaultextension=".m3u")
    names = channel_listbox.get(0, tk.END)
    generate.generate_out_file(file_name, names, output_channels)


def fill_origin_listbox(event):
    origin_channel_listbox.delete(0, tk.END)
    global channels
    channels = formation.generate_base(stuck[sources_combobox.get()])
    names = formation.dictKeys_to_sortList(channels)
    for i in names:
        origin_channel_listbox.insert(tk.END, i)


def select_channel(event):
    index = channel_listbox.curselection()
    if not index == ():
        name = channel_listbox.get(index[0])
        links = [output_channels[name][0]]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        try:
            for link in channels[name]:
                if link != output_channels[name][0]:
                    links.append(link)
        except:
            display_information("Канал не найден в базе")
        addr_label.config(text="Адрес:(" + str(len(links)) + ")")
        addr_combobox.config(values=links)
        addr_combobox.current(newindex=0)
        group_combobox.current(groups.index(output_channels[name][1]))


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


def play_link(event):
    link = addr_combobox.get()
    file_name = 'check_link.m3u'
    link_file = open(file_name, "w", encoding="utf-8")
    link_file.write("#EXTM3U\n")
    link_file.write("#EXTINF:-1," + link + "\n")
    link_file.write(link)
    link_file.close()
    os.startfile(file_name)
    display_information("Не все плееры поддерживают потоковое видео...")


def search_channel(event):
    origin_count = 0
    out_count = 0
    origin_size = origin_channel_listbox.size()
    channel_size = channel_listbox.size()
    name = search_entry.get()
    for i in range(origin_size):
        if name.upper() in origin_channel_listbox.get(i).upper():
            origin_channel_listbox.itemconfig(i, bg="YELLOW")
            select_channel("<<ListboxSelect>>")
            try:
                origin_channel_listbox.yview_moveto(1 / (origin_size / i))
            except ZeroDivisionError:
                origin_channel_listbox.yview_moveto(0)
            origin_count += 1
        else:
            origin_channel_listbox.itemconfig(i, bg="WHITE")
    for i in range(channel_size):
        if name.upper() in channel_listbox.get(i).upper():
            channel_listbox.itemconfig(i, bg="YELLOW")
            select_channel("<<ListboxSelect>>")
            try:
                channel_listbox.yview_moveto(1 / (channel_size / i))
            except ZeroDivisionError:
                channel_listbox.yview_moveto(0)
            out_count += 1
        else:
            channel_listbox.itemconfig(i, bg="WHITE")
    display_information("Нашёл " + str(origin_count) + " в исходн. / " + str(out_count) + " в листе.")


def auto_update(event):
    channel_size = channel_listbox.size()
    for i in range(channel_size):
        name = channel_listbox.get(i)
        find = False
        not_find = False
        try:
            for link in channels[name]:
                if link == output_channels[name][0]:
                    find = True
                else:
                    not_find = True
        except:
            channel_listbox.itemconfig(i, bg="tomato")
        if find == True and not_find == True:
            channel_listbox.itemconfig(i, bg="SkyBlue")
        elif find == True and not_find == False:
            channel_listbox.itemconfig(i, bg="SeaGreen1")
        elif find == False and not_find == True:
            channel_listbox.itemconfig(i, bg="tomato")


stuck = pars.extract_source()
channels = dict()
output_channels = dict()
groups = [""]

root = tk.Tk()
try:
    root.iconbitmap(icon)
except:
    print("нет иконки")
root.title(title)
root.geometry(size_window)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Открыть...", command=open_playlist)
file_menu.add_command(label="Экспортровать как...", command=export_playlist)
file_menu.add_command(label="Экспорт (пока не пашет)")  # ----

top_frame = tk.Frame(root, height=30)

list_frame = tk.Frame(root)

left_frame = tk.Frame(list_frame)
sources_head_frame = tk.Frame(left_frame)
sources_combobox = ttk.Combobox(sources_head_frame, values=stuck["sources"])
sources_combobox.current(newindex=0)
sources_combobox.bind("<<ComboboxSelected>>", fill_origin_listbox)
update_btn = tk.Button(sources_head_frame, text="UPDATE")
update_btn.bind("<Button-1>", update_playlists)

origin_channel_listbox = tk.Listbox(left_frame)
ocl_scroll = tk.Scrollbar(left_frame)
ocl_scroll["command"] = origin_channel_listbox.yview
origin_channel_listbox["yscrollcommand"] = ocl_scroll.set
origin_channel_listbox.bind("<<ListboxSelect>>", select_origin_channel)

right_frame = tk.Frame(list_frame)
output_head_frame = tk.Frame(right_frame)
search_entry = tk.Entry(output_head_frame)
search_btn = tk.Button(output_head_frame, text="FIND")
search_btn.bind("<Button-1>", search_channel)
search_entry.bind("<Return>", search_channel)

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
down_btn = tk.Button(sort_frame, text="\\/")
down_btn.bind("<Button-1>", down_channel)
del_btn = tk.Button(sort_frame, text="del")
del_btn.bind("<Button-1>", del_channel)

edit_frame = tk.Frame(root)
action_areas_frame = tk.Frame(edit_frame)
name_label = tk.Label(action_areas_frame, text="Название:")
name_entry = tk.Entry(action_areas_frame, width=60)
name_entry.bind("<Return>", add_channel)
addr_label = tk.Label(action_areas_frame, text="Адрес:")
addr_combobox = ttk.Combobox(action_areas_frame)
addr_combobox.bind("<Return>", add_channel)

group_label = tk.Label(action_areas_frame, text="Группа:")
group_combobox = ttk.Combobox(action_areas_frame, values=groups)
group_combobox.bind("<Return>", change_group)

buttons_frame = tk.Frame(edit_frame)
check_btn = tk.Button(buttons_frame, text="Смотреть")
check_btn.bind("<Button-1>", play_link)
apply_btn = tk.Button(buttons_frame, text="Применить")
apply_btn.bind("<Button-1>", add_channel)

auto_update_btn = tk.Button(root, text="Найти\nобновы")
auto_update_btn.bind("<Button-1>", auto_update)
info_label = tk.Label(root, text="...")

# packs
top_frame.pack(side=tk.TOP, fill="x", expand=False)
list_frame.pack(side=tk.LEFT, fill="both", expand=True)

left_frame.pack(side=tk.LEFT, fill="both", expand=True)
sources_head_frame.pack()
sources_combobox.pack(side=tk.LEFT)
update_btn.pack(side=tk.RIGHT)
right_frame.pack(side=tk.RIGHT, fill="both", expand=True)
output_head_frame.pack()
search_entry.pack(side=tk.LEFT)
search_btn.pack(side=tk.RIGHT)
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
action_areas_frame.pack(side=tk.TOP, fill="both", expand=True)
group_label.pack()
group_combobox.pack()
buttons_frame.pack()
check_btn.pack(side=tk.LEFT)
apply_btn.pack()
auto_update_btn.pack(side=tk.TOP)
info_label.pack(side=tk.BOTTOM, fill="both")

fill_origin_listbox(1)
root.mainloop()
