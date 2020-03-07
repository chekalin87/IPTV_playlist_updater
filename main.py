import requests
import os

channels = {}


def create_playlist():
    all_channels_file = open('all_channels.m3u', "w", encoding="utf-8")
    all_channels_file.write("#EXTM3U\n")
    for key in channels:
        key = key.strip()
        channels[key] = channels[key].strip()
        all_channels_file.write(key + "\n")
        all_channels_file.write(channels[key] + "\n")
    all_channels_file.close()
    list_file = open('list.txt', "r", encoding="utf-8")


    out_file = open('iptvchannels.m3u', "w", encoding="utf-8")
    out_file.write("#EXTM3U\n")
    for line in list_file:
        if "#EXTINF:" in line:
            for key in channels:
                if key.strip() == line.strip():
                    out_file.write(key + "\n")
                    out_file.write(channels[key] + "\n")
    list_file.close()
    out_file.close()


def update():  # Создаёт общий словарь с каналами channels ПЕРЕДЕЛАТЬ имена файлов!!!
    stuck = []

    i = 0
    list_file = open('list.txt', "r", encoding="utf-8")
    stuck = list_file.readlines()
    list_file.close()
    while os.path.exists('sources/' + str(i) + '.txt'):
        source_file_r = open('sources/' + str(i) + '.txt', "r", encoding="utf-8")
        stuck = stuck + source_file_r.readlines()
        source_file_r.close()
        i += 1

    for line in stuck:
        if "#EXTINF:" in line:
            if "#EXTGRP:" in stuck[stuck.index(line) + 1]:
                channels[line.strip()] = stuck[stuck.index(line) + 2]
            else:
                channels[line.strip()] = stuck[stuck.index(line) + 1]


def search_links():
    try:
        links_file = open('links.txt', "r", encoding="utf-8")
    except:
        print("Не смог открыть файл links.txt")
    else:
        return links_file.readlines()
    finally:
        links_file.close()


def downloading_playlists():  #Качает (перезаписывает) файлы исходных плейлистов ПЕРЕДЕЛАТЬ имена файлов!!!
    try:
        os.mkdir("sources")
    except:
        pass
    else:
        print("Нет папки \"sources\", создал")

    files = os.listdir("sources")
    print(files)
    for var in files:
        try:
            os.remove("sources/" + var)
        except:
            print("Не могу удалить: sources/" + var)
        else:
            print("удалил: sources/" + var)

    for i in range(len(links)):
        try:
            ufr = requests.get(links[i].strip())
        except:
            print("Сервис " + links[i].strip() + " не отвечает")
        else:
            print("скчал плейлист " + links[i].strip())
            source_file = open("sources/" + str(i) + ".txt", "wb")
            source_file.write(ufr.content)
        finally:
            source_file.close()


links = search_links()
downloading_playlists()
update()
create_playlist()
print("Общая база каналов: " + str(channels))
print("END")


