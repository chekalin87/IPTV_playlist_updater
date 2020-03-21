# -*- coding: utf-8 -*-


def dictKeys_to_sortList(mixed_dict):
    names = list(mixed_dict.keys())
    names.sort()
    return names


def generate_base(source_text):  # Принимает значение словаря (stuck[k])
    base = {}
    for line in source_text:
        if "#EXTINF:" in line:
            splited_line = line.split(",", 1)
            name = splited_line[1].strip()
            if "#EXTGRP:" in source_text[source_text.index(line) + 1]:
                if not (name in base):
                    base[name] = set()
                link = source_text[source_text.index(line) + 2].strip()
                base[name].add(link)
            else:
                if not (name in base):
                    base[name] = set()
                link = source_text[source_text.index(line) + 1].strip()
                base[name].add(link)
    return base


def reading_playlist(file_name):
    source_file_r = open(file_name, "r", encoding="utf-8")
    stuck = source_file_r.readlines()
    source_file_r.close()
    base = {}
    names = []
    groups = [""]
    for line in stuck:
        if "#EXTINF:" in line:
            splited_line = line.split(",", 1)
            name = splited_line[1].strip()
            names.append(name)
            if "#EXTGRP:" in stuck[stuck.index(line) + 1]:
                if not (name in base):
                    base[name] = []
                splited_group = stuck[stuck.index(line) + 1].split(":", 1)
                group = splited_group[1].strip()
                if not group in groups:
                    groups.append(group)
                link = stuck[stuck.index(line) + 2].strip()
                base[name].insert(0, link)
                base[name].insert(1, group)
            else:
                if not (name in base):
                    base[name] = []
                link = stuck[stuck.index(line) + 1].strip()
                base[name].insert(0, link)
                base[name].insert(1, "")
    return base, names, groups
