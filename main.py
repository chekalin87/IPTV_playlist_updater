import requests
import os


def find_chanels(name):
    i = 0
    for line in source:
        i += 1
        if line.strip() == name.strip():
            address = source[i]

            return address
    return "\n"


def update():
    list_file = open('list.txt', "r", encoding="utf-8")
    out_file = open('iptvchannels.m3u', "w", encoding="utf-8")
    out_file.write("#EXTM3U\n")

    for line in list_file.readlines():
        out_file.write(line)
        out_file.write(find_chanels(line))

    list_file.close()
    out_file.close()


def downloading_playlists():
    try:
        ufr = requests.get("https://smarttvnews.ru/apps/iptvchannels.m3u")
    except:
        print("Сервис не отвечает")
    else:
        print("скчал плейлист с https://smarttvnews.ru/apps/iptvchannels.m3u")

    try:
        os.mkdir("source")
    except:
        pass
    else:
        print("Нет папки \"source\", создаю...")
    source_file = open('source/source.txt', "wb")
    source_file.write(ufr.content)
    source_file.close()

downloading_playlists()
source_file_r = open('source/source.txt', "r", encoding="utf-8")
source = source_file_r.readlines()
update()
source_file_r.close()
