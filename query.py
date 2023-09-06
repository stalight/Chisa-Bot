import os
import fnmatch

# For Querying Music From E Drive
#Anime/Bocchi the Rock/光の中へ
def find_music(query_name):
    items = os.walk("E:/Music")
    matched_files = []
    for i in items:
        for filename in i[2]:
            pattern = "*"+query_name+"*"
            if filename[-3:] != "jpg" and fnmatch.fnmatch(filename, pattern):
                matched_files.append((i[0], filename))

    return matched_files

