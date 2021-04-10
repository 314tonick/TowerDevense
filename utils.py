import pygame
import sys
import os


def resource_path(*relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'resources', *relative_path)


def load_img(*file_name):
    return pygame.image.load(resource_path(*file_name))


def open_file(*file_name):
    return open(resource_path(*file_name))


pygame.init()
