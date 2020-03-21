# -*- coding: utf-8 -*-


import os
import requests


def search_links():
    try:
        links_file = open('links.txt', "r", encoding="utf-8")
    except:
        links_file = open('links.txt', "w", encoding="utf-8")
        print(
            "Нет файла \"links.txt\"...\nне переживай, я его уже создал,\nтебе нужно записать туда хоть одну ссылку "
            "на плейлист.")
    else:
        links_list = links_file.readlines()
        if links_list == []:
            print("\"links.txt\"пуст,\nтебе нужно записать туда хоть одну ссылку на плейлист.")
        return links_list
    finally:
        links_file.close()


def downloading_playlists():  # Качает (перезаписывает) файлы исходных плейлистов
    links = search_links()
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
        file_name = sp_l[-1]
        try:
            ufr = requests.get(link)
        except:
            print("Сервис " + link + " не отвечает")
        else:
            source_file = open("sources/" + file_name, "wb")
            source_file.write(ufr.content)
            print("скчал плейлист " + link)
        finally:
            source_file.close()


def extract_source():
    """Возвращает словарь, в словаре имена файлов, all и sources. all - обьединённый венигрет из файлов, sources -
    имена файлов"""
    downloading_playlists()
    stuck = {"all": [], "sources": ["all"]}
    for file in os.listdir("sources/"):
        source_file_r = open('sources/' + file, "r", encoding="utf-8")
        stuck[file] = source_file_r.readlines()
        stuck["all"] += stuck[file]
        stuck["sources"].append(file)
        source_file_r.close()
    return stuck
