'''
asset_manager.py - various stuff for loading assets

Original author: enbyte

SPRUCE
 _/\_
/____\ 
  ||
  ||

ENGINE

'''

import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

from pygame.image import load as il
from pygame.mixer import Sound

def get_extension(file):
    return file.split('.')[-1]

class Loader:
    def __init__(self, loaders):
        self.loaders = loaders

    def load(file):
        '''
        Load a file.
        If it has a known type, load it, otherwise error.
        '''
        ext = get_extension(file.lower())
        if ext in self.loaders.keys(): # known file extension
            return self.loaders[ext](file.lower())
        else:
            print("spruce warning: unknown file extension %s" % ext)
            raise FileNotFoundError("unknown file extension")

    def add(extension, func):
        self.loaders[extension] = func

default_loaders = {'png': il, 'jpg': il, 'tga': il, 'bmp': il, 'ogg': Sound, 'mp3': Sound}

class BasicLoader(Loader):
    '''
    Same loader but with a few defaults.
    '''
    def __init__(self, additional):
        self.loaders = default_loaders + additional




class AssetManager:
    def __init__(self):
        self.textures = {}
        self.fonts = {}
        self.sounds = {}

    def add_texture(self, filename, id_):
        self.textures[id_] = pygame.image.load(filename)

    def get_texture(self, id_):
        return self.textures[id_]

    def add_font(self, filename, fontsize, id_):
        if '.' in filename: # is a file
            self.fonts[id_] = pygame.font.Font(filename, fontsize)
        else:
            self.fonts[id_] = pygame.font.SysFont(filename, fontsize)

    def get_font(self, id_):
        return self.fonts[id_]

    def add_sound(self, filename, id_):
        self.sounds[id_] = Sound(filename)

    def get_sound(self, id_):
        return self.sounds[id_]