# -*- coding: utf-8 -*-


def generate_out_file(file_name, names, channels):
    out_file = open(file_name, "w", encoding="utf-8")
    out_file.write("#EXTM3U\n")
    for name in names:
        out_file.write("#EXTINF:-1," + name + "\n")
        if channels[name][1] != "":
            out_file.write("#EXTGRP:" + channels[name][1] + "\n")
        out_file.write(channels[name][0] + "\n")
    out_file.close()
    print("Сохранил файл " + file_name)
