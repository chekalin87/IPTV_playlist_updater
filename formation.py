
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


def create_playlist(file_name):
    out_file = open(file_name, "w", encoding="utf-8")
    out_file.close()