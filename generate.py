# -*- coding: utf-8 -*-


def generate_out_file2(file_name, names, channels):
    """Вариант создания файла вида:
    #EXTINF:-1 ,112 Украина
    #EXTGRP:УКРАИНА
    http://112hd-hls3.cosmonova.net.ua/hls/112hd_ua_hi/index.m3u8
    """
    out_file = open(file_name, "w", encoding="utf-8")
    out_file.write("#EXTM3U\n")
    for name in names:
        out_file.write("#EXTINF:-1," + name + "\n")
        if channels[name][1] != "":
            out_file.write("#EXTGRP:" + channels[name][1] + "\n")
        out_file.write(channels[name][0] + "\n")
    out_file.close()
    print("Сохранил файл " + file_name)


def generate_out_file(file_name, names, channels):
    """Вариант создания файла вида:
    #EXTINF:-1 group-title="Охуенные мультики",Cartoon Network HD
    https://user11183.clients-cdnnow.ru/hls/Cartoon_Network_HD/master.m3u8
    """
    out_file = open(file_name, "w", encoding="utf-8")
    out_file.write("#EXTM3U\n")
    for name in names:
        if channels[name][1] == "":
            out_file.write("#EXTINF:-1," + name + "\n")
        else:
            out_file.write("#EXTINF:-1 group-title=\"" + channels[name][1] + "\"," + name + "\n")
        out_file.write(channels[name][0] + "\n")
    out_file.close()
    print("Сохранил файл " + file_name)
