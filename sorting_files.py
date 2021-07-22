#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sorting_files.py
#  Johnny Pan <codeskill@gmail.com>
#

import os
import unicodedata
import re
import shutil

def remove_accents(filename, allow_unicode=False):
    value = str(filename)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    return value

def sanitize_filename(filename):
    under_score = ['<','>','%','$','&','?','(',')','[',']',',',':',';','=','-','.',' '] 
    filename = remove_accents(filename).lower()
    for char in filename:
        if (char in under_score): filename = filename.replace(char,'_')
    filename = re.sub(r'\_{2,}', '_',filename )
    return filename

def report(sorting_files):
    print ("{:<13} {:<5}".format('Extension','Files'))
    print ("{:<13} {:<5}".format('-------------','-----'))
    for key, value in sorted(sorting_files.items(), key=lambda t: (-t[1], t[0])):
        print ("{:<13} {:<5}".format(key, value))

def main():

    total = {}
    sorting_files = {}
    no_extension = 'no_ext'
    sorting_files[no_extension] = 0
    directory = os.getcwd()
    files = os.listdir(directory)
    for f in files:
        old_filename = f
        base = os.path.splitext(old_filename)[0]
        ext = os.path.splitext(old_filename)[1]
        folder = ext[1:]
        new_filename = sanitize_filename(base)+ext
        os.rename(old_filename,new_filename)
        if folder == "":
            sorting_files.update({no_extension: sorting_files[no_extension]+ 1})
            continue
        if os.path.exists(directory + '/' + folder ):
            sorting_files.update({folder: sorting_files[folder] + 1})
            shutil.move(directory + '/' + new_filename, directory + '/' + folder + '/' + new_filename )
        else:
            sorting_files.update({folder: 1})
            os.makedirs( directory + '/' + folder )
            shutil.move( directory + '/' + new_filename, directory + '/' + folder + '/' + new_filename )
    report(sorting_files)
   

if __name__ == "__main__":
    main()
