import sys
import requests
import os

channels = {}
not_finded_channels =[]

def close_program(code=0):
    input("\nВведи букву Хуй чтобы выйти: ")
    sys.exit(code)


def create_playlist():
    list = []
    all_channels_file = open('all_channels.m3u', "w", encoding="utf-8")
    all_channels_file.write("#EXTM3U\n")
    for key in channels:
        key = key.strip()
        channels[key] = channels[key].strip()
        all_channels_file.write(key + "\n")
        all_channels_file.write(channels[key] + "\n")
    all_channels_file.close()

    try:
        list_file = open('list.txt', "r", encoding="utf-8")
    except:
        list_file = open('list.txt', "w", encoding="utf-8")
        print("Нет файла \"list.txt\"...\nне переживай, я его уже создал,\nтебе нужно записать туда\nканалы со ссылками, короче ты понял.")
        close_program(1)
    else:
        list = list_file.readlines()
    finally:
        list_file.close()
    if list == []:
        print("Ну бля...\nпустой \"list.txt\"...\nТы читал README?!!!")
        close_program(1)

    out_file = open('OUT.m3u', "w", encoding="utf-8")
    out_file.write("#EXTM3U\n")
    for line in list:
        find_channel = False
        if "#EXTINF:" in line:
            splited_line = line.split(",", 1)
            formating_line = splited_line[0].strip() + "," + splited_line[1].strip()
            for key in channels:
                if key == formating_line:
                    out_file.write(key + "\n")
                    out_file.write(channels[key] + "\n")
                    find_channel = True
            if not find_channel:
                not_finded_channels.append(formating_line)
                out_file.write(line.strip() + "\n")
                out_file.write(list[list.index(line)+1].strip() + "\n")
    out_file.close()


def update():  # Создаёт общий словарь с каналами channels
    stuck = []

    for file in os.listdir("sources/"):
        source_file_r = open('sources/' + file, "r", encoding="utf-8")
        stuck = stuck + source_file_r.readlines()
        source_file_r.close()
    for line in stuck:
        if "#EXTINF:" in line:
            splited_line = line.split(",", 1)
            formating_line = splited_line[0].strip() + "," + splited_line[1].strip()
            if "#EXTGRP:" in stuck[stuck.index(line) + 1]:
                channels[formating_line.strip()] = stuck[stuck.index(line) + 2]
            else:
                channels[formating_line.strip()] = stuck[stuck.index(line) + 1]


def search_links():
    try:
        links_file = open('links.txt', "r", encoding="utf-8")
    except:
        links_file = open('links.txt', "w", encoding="utf-8")
        print(
            "Нет файла \"links.txt\"...\nне переживай, я его уже создал,\nтебе нужно записать туда хоть одну ссылку на плейлист.")
        close_program(1)
    else:
        links_list = links_file.readlines()
        if links_list == []:
            print("\"links.txt\"пуст,\nтебе нужно записать туда хоть одну ссылку на плейлист.")
            close_program(1)
        return links_list
    finally:
        links_file.close()


def downloading_playlists():  # Качает (перезаписывает) файлы исходных плейлистов
    try:
        os.mkdir("sources")
    except:
        pass
    else:
        print("Нет папки \"sources\", создал")

    files = os.listdir("sources")
    for var in files:
        try:
            os.remove("sources/" + var)
        except:
            print("Не могу удалить: sources/" + var)
        else:
            print("удалил: sources/" + var)

    for i in range(len(links)):
        link = links[i].strip()
        sp_l = link.split("/")
        name = sp_l[-1]
        try:
            ufr = requests.get(link)
        except:
            print("Сервис " + link + " не отвечает")
        else:
            source_file = open("sources/" + name, "wb")
            source_file.write(ufr.content)
            print("скчал плейлист " + link)
        finally:
            source_file.close()


links = search_links()
downloading_playlists()
update()
create_playlist()
print("Общая база каналов:")
for key in channels:
    print(key + " >> " + channels[key])
if not_finded_channels != []:
    print("Каналы:")
    for i in not_finded_channels:
        print(i)
    print("не были найдены.")
    print("Это конец ;)")
close_program(0)
