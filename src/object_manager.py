'''
object_manager.py - various stuff for loading assets and handling objects   

Original author: enbyte

SPRUCE
 _/\_
/____\ 
  ||
  ||

ENGINE

'''

import pygame
import operator
pygame.init()
pygame.font.init()
pygame.mixer.init()

from pygame.image import load as il
from pygame.mixer import Sound



def get_extension(file):
    return file.split('.')[-1]

class DirtyObject:
    def __init__(self, dirty=False):
        self.dirty = dirty

    def set_dirty(self):
        self.dirty = True

    def set_clean(self):
        self.dirty = False

    def get_dirty(self):
        return self.dirty

    def toggle_dirty(self):
        self.dirty = not self.dirty

class Loader:
    def __init__(self, loaders):
        self.loaders = loaders

    def load(self, file):
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
    def __init__(self):
        self.loaders = default_loaders




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
     
     
class Registry:
    '''
    create a registry of objects, for example tiles or all objects or ui elements
    '''
    def __init__(self, objs=[]):
        self.objs = objs
        if not isinstance(objs, list):
            raise TypeError("objs must be a list")


    def __contains__(self, obj):
        return obj in self.objs or id(obj) in list(map(id, self.objs))

    def __add__(self, other):
        return Registry(self.objs + other.objs)

    def __iter__(self):
        for obj in self.objs:
            yield obj
    
    def __len__(self):
        return len(self.objs)

    def __repr__(self):
        return "Registry(%s)" % self.objs

    def add(self, obj):
        self.objs.append(obj)

    def get(self, id_):
        for obj in self.objs:
            if id(obj) == id_:
                return obj
        return None

    def get_all(self):
        return self.objs

    def remove(self, id_):
        for obj in self.objs:
            if id(obj) == id_:
                self.objs.remove(obj)
                return True
        return False

    def remove_all(self):
        self.objs = []

    def update(self, *pargs, **kwargs):
        for obj in self.objs:
            obj.update(*pargs, **kwargs)

    def draw_on_screen(self, surface):
        for obj in self.get_on_screen(surface.get_rect()):
            try:
                obj.draw(surface)
            except AttributeError:
                print("spruce warning: object %s has no draw method" % obj)

    def draw_all(self, surface):
        for obj in self.objs:
            try:
                obj.draw(surface)
            except AttributeError:
                print("spruce warning: object %s has no draw method" % obj)

    def draw_sorted_on_screen(self, surface):
        for obj in self.sorted_on_screen(surface.get_rect()):
            try:
                obj.draw(surface)
            except AttributeError:
                print("spruce warning: object %s has no draw method" % obj)

    def get_on_screen(self, screen_rect):
        for obj in self.objs:
            if obj.rect.colliderect(screen_rect):
                yield obj

    def sorted_on_screen(self, screen_rect):
        return sorted(self.get_on_screen(screen_rect), key=operator.methodcaller('get_depth')) # the cause of so much pain... it was literally rect.y instead of y and I spent thirty minuted trying to fix this

    def sort_all(self):
        self.objs = sorted(self.objs, key=operator.methodcaller('get_depth'))

    def get_sorted_on_screen(self, screen_rect):
        return sorted(self.get_on_screen(screen_rect), key=operator.methodcaller('get_depth'))

    def get_all_for_condition(self, condition):
        for obj in self.objs:
            if condition(obj):
                yield obj

    def insert_into_sorted_objs(self, objs, key, do_sort=True):
        if do_sort:
            objs = sorted(objs, key=operator.methodcaller('get_depth'))
            


    
