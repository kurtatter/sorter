#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import logging
import argparse

# вывод списка с именами файлов и папок 
# в текущей директории
# !Я пока что не знаю от отличить по названию
# !это папка или просто файл без разширения
# 
# os.listdir()


LOG_NAME = 'last_change.log'

def get_folder_names_for_create():
    files = []
    fl_names = set()

    for i in os.listdir():
        if os.path.isfile(i):
            files.append(i)

    for i in files:
        fl_names.add(i.split('.')[-1])

    try:
        fl_names.remove('log')
    except KeyError:
        pass

    return fl_names

def get_folder_names_for_remove():
    files = get_files(os.listdir())
    folders = []
    if LOG_NAME in files:
        with open(LOG_NAME) as log:
            folders_line = log.readline()
            fl1 = folders_line.split("|")[1:]
            for i in fl1:
                folders.append(i.split("\n")[0])
    return folders


FOLDER_NAMES = get_folder_names_for_create()

def get_folders(listdir):
    folders = []
    for f in listdir:
        if os.path.isdir(f):
            folders.append(f)
    return folders

def get_files(listdir):
    files = []
    for f in listdir:
        if os.path.isfile(f):
            files.append(f)
    return files

def passage(file_name, folder):
    for element in os.scandir(folder):
        if element.is_file():
            if element.name == file_name:
                yield folder
        else:
            yield from passage(file_name, element.path)

def sort_extension(listdir):
    # make folders
    for i in get_folder_names_for_create():
        if not os.path.exists(i):
            os.mkdir(i)
        else:
            continue

    # move files to folders
    logging.basicConfig(filename=LOG_NAME, level=logging.INFO, filemode='w', format='%(asctime)s |%(message)s')
    logging.info("|".join(get_folder_names_for_create()))
    for i in get_files(listdir):
        if i != os.path.basename(__file__) and i.split('.')[-1] != 'log':
            shutil.move(i, i.split('.')[-1])
            logging.info("{0}---{1}---{2}".format(i, os.getcwd(), os.path.abspath(i.split('.')[-1]+'/'+i)))

def undo_operation():
    now_path = ''
    last_path = ''
    print(get_folder_names_for_remove())

    try:
        with open(LOG_NAME) as logs:
            for log in logs.readlines()[1:]:
                now_path = log.split('---')[-1].split('\n')[0]
                last_path = log.split('---')[1]
                print(now_path, last_path)
                shutil.move(now_path, last_path)
    except IOError as e:
        print(e.with_traceback)

    for f in get_folder_names_for_remove():
        os.rmdir(f)

    if os.path.exists(LOG_NAME):
        os.remove(LOG_NAME)
    else:
        pass
#    shutil.move('/home/sam/love/sorter/md/Python_sorter.md', '/home/sam/love/sorter')


def main():
    listdir = os.listdir()
    now_dir = os.getcwd()


    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--extension", action="store_true")
    parser.add_argument("-u", "--undo", help="undo last operation", action="store_true")

    args = parser.parse_args()

    if args.extension:
        sort_extension(listdir)
    elif args.undo:
        undo_operation()
    else:
        print("OOOOPS!")



    # make folders
#    for i in get_folder_names(listdir):
#        if not os.path.isdir(i) and i != 'log':
#            os.mkdir(i)

    # move files to folders
#    for i in get_files(listdir):
#        if i != os.path.basename(__file__) and i.split('.')[-1] != 'log':
#            shutil.move(i, i.split('.')[-1])
#            logging.info("{0}---{1}---{2}".format(i, now_dir, os.path.abspath(i.split('.')[-1]+'/'+i)))
#    for i in os.walk('.'):
#        print(i)

if __name__ == '__main__':
    main()
