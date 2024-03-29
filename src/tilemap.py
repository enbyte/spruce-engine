import pygame
from pygame.locals import *
import logging
from . import btm_tools as tools
import copy
from . import object_manager

COLLIDE_NONE = 0
COLLIDE_X = (1 << 1)
COLLIDE_Y = (1 << 2)

logging.basicConfig(format='Spruce Tilemap %(levelname.capital())s at %(asctime)s: %(message)s') # setup logging as 'Spruce Tilemap Warning at 1:32:00: Bing bong'

pygame.init()

_tile_registry = object_manager.Registry()


def _sticky_load_image(image):
    '''
    If the image is a string, return pygame.image.load() for that image.
    If it is a pygame.Surface, return it.
    Otherwise, throw an error.
    '''
    if type(image) == str:
      try:
        return pygame.image.load(image).convert()
      except pygame.error:
        print("No video mode! Make sure to initialize the display before calling Tile()!")
        return pygame.image.load(image)
    elif type(image) == pygame.Surface:
        return image
    else:
        logging.error('Unrecognized type in _sticky_load_image: %s' % type(image))
        raise TypeError

class Tile:
    '''
    A class to represent a specfic _type_ of tile, i.e. lava, or grass.
    '''
    def __init__(self, image, subsurface_rect_args=None, name=""):
        self._tile_creation_class = _Tile
        self.image = _sticky_load_image(image)
        if name == "":
            logging.error('Name cannot be a blank string for a Tile')
            raise NameError
        elif name in _tile_registry:
            logging.error('Name %s for a tile is already in use')
            raise NameError
        else:
            self.name = name
            _tile_registry.add(self)
        self.has_rect = True
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if subsurface_rect_args is None:
          self.sra = [0, 0, self.width, self.height]
        else:
          self.sra = subsurface_rect_args
    def __str__(self):
        return '[Tiletype name=%s; image=%s; has_rect=%s; width=%s; height=%s]' % (self.name, self.image, self.has_rect, self.width, self.height)

class NullTile:
    '''
    Class to represent a blank tile with no image and no rect.
    '''
    def __init__(self):
        self.name = 'NullTile'
        self.image = pygame.Surface((0, 0))
        self.has_rect = False
        self.width = 0
        self.height = 0
        self.sra = [0, 0, 0, 0]
        self._tile_creation_class = _Tile

    def __str__(self):
        return '[Null-tiletype <no data>]'


        

class _Tile(object_manager.DirtyObject):
    '''
    Internal base class used to represent a specific tile in the world.

    The superclass parameter is not used here, but can be used in custom tile children.
    '''
    def __init__(self, tiletype, tilemap, x, y, superclass=None):
        object_manager.DirtyObject.__init__(self)
        self.tilemap = tilemap
        self.name = tiletype.name
        self.image = tiletype.image
        self.tiletype = tiletype #keep track of it
        self.sra = tiletype.sra
        self.x = x
        self.y = y
        self.generate_rect()
        self.has_rect = tiletype.has_rect
        self.width = self.rect.width
        self.height = self.rect.height

    def __str__(self):
        if self.has_rect and self.rect.width > 0 and self.rect.height > 0:
            return '[Tile rect=%s; tiletype=%s]' % (str(self.rect), str(self.tiletype))
        else:
            return '[NullTile]'

    def __repr__(self):
        return self.__str__()

    def draw(self, surface):
        '''
        Draw the tile to the surface.
        '''
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        '''
        Get the rect of the tile.
        '''
        return self.rect

    def generate_rect(self):
        '''
        (Re)generate the rect of the tile.
        '''
        
        self.rect = pygame.Rect(self.x + self.sra[0], self.y + self.sra[1], self.sra[2], self.sra[3])


    def update_tiletype(self, new_tiletype, tilemap):
        '''
        Update the tiletype of the tile.
        '''
        self.tilemap.tile_list.remove(self)
        print("update:", new_tiletype, tilemap)
        new = new_tiletype._tile_creation_class(new_tiletype, tilemap, x=self.x, y=self.y)
        self = new
        self.tiletype = new_tiletype
        self.tilemap = tilemap
        self.tilemap.tile_list.append(self)
        self.tilemap.update_registry()


        self.set_dirty()

    def move_x(self, amount):
        '''
        Move the tile horizontally.
        '''
        self.rect.x += amount
        self.x += amount
    
    def move_y(self, amount):
        '''
        Move the tile vertically.
        '''
        self.rect.y += amount
        self.y += amount

    def move_xy(xamount, yamount):
        '''
        Move the tile horizontally and vertically.
        '''
        self.move_x(xamount)
        self.move_y(yamount)

    def goto(self, x, y):
        '''
        Move the tile to a specific location.
        '''
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return '[_Tile rect=%s; tiletype=%s]' % (str(self.rect), str(self.tiletype))

    def colliderect(self, other):
        '''
        Check if the tile collides with another rect.
        '''
        return self.rect.colliderect(other)

    def get_depth(self):
        return self.rect.y

class _HittableDemoObject(_Tile):
    def __init__(self, superclass=None, *pargs, **kwargs):
        '''
        Used as a dummy class to represent what can be done with inheritance from _Tile.
        superclass is a class, not an instance, with data.
        '''
        _Tile.__init__(self, *pargs, **kwargs)
        self.hits = superclass.hits
        self.superclass = superclass
    
    def hit(self, damage):
        '''
        Subtract damage damage from the object.
        '''
        print("Oof! You hit me for %s damage! " % damage)
        self.hits -= damage
        print("I have %s hits left!" % self.hits)
        if self.hits <= 0:
            self.superclass.destroy_callback(self)
        return self.hits

class Tilemap:
    def __init__(self, matrix, tile_list, TILE_SIZE=32):
        self.matrix = matrix
        self.TILE_SIZE = TILE_SIZE
        self.tile_list = []
        x, y = 0, 0
        for row in matrix:
            for thing in row:
                tp = tile_list[thing]._tile_creation_class
                z = tp(tiletype=tile_list[thing], tilemap=self, x=TILE_SIZE * x, y=TILE_SIZE * y, superclass=tile_list[thing])
                self.tile_list.append(z)
                x += 1
            x = 0
            y += 1
           
        self.tiletype_list = tile_list
        self.tile_registry = object_manager.Registry(self.get_list_of_tiles())
        self.x = 0
        self.y = 0
    def update_registry(self):
        print("update registry")
        self.tile_registry = object_manager.Registry(self.get_list_of_tiles())

    def get_list_of_tiles(self):
        '''
        Concatenate the entire matrix of tiles into one list, for individual operations on them.
        '''
        return self.tile_list

    def move_x(self, amount):
        '''
        Move the tilemap and all of the tiles on the x-axis by a given amount.
        '''
        self.x += amount
        for tile in self.get_list_of_tiles(): tile.move_x(amount)

    def move_y(self, amount):
        '''
        Move the tilemap and all of the tiles on the y-axis by a given amount.
        '''
        self.y += amount
        for tile in self.get_list_of_tiles(): tile.move_y(amount)

    def move_xy(self, xamount, yamount):
        '''
        Move the tilemap and all of the tiles on the x-axis and the y-axis by a given amount.
        '''
        self.move_x(xamount)
        self.move_y(yamount)

    def goto(self, x, y):
        '''
        Move the tilemap and all of the tiles to a given position.
        '''
        self.x = x
        self.y = y
        for tile in self.get_list_of_tiles():
            tile.goto(x, y)

    def goto_x(self, x):
        '''
        Move the tilemap and all of the tiles to a given x-position.
        '''
        self.x = x

        for tile in self.get_list_of_tiles():
            tile.goto(x, self.y)

    def goto_y(self, y):
        '''
        Move the tilemap and all of the tiles to a given y-position.
        '''
        self.y = y

        for tile in self.get_list_of_tiles():
            tile.goto(self.x, y)

    def collision_test(self, rect, ignore_tiletypes=[], ignore_names=[]):
        '''
        For each tile in the tilemap, test if it collides with a given pygame.Rect.
        '''
        hit_list = [] # we gonna murder these tiles
        for x in self.get_list_of_tiles():
            if x.rect.colliderect(rect):
                if x.tiletype in ignore_tiletypes: continue
                if x.name in ignore_names: continue
                hit_list.append(x)
        hit_list = [x for x in hit_list if x.name not in ignore_names and x.tiletype not in ignore_tiletypes]
        return hit_list

    def get_tile_at(self, x, y):
        '''
        Return the tile at x, y in screenspace
        '''
        for tile in self.tile_list:
            if tile.rect.collidepoint(x, y):
                return tile

    def get_names(self):
        return [x.name for x in self.tiletype_list]

    def get_tile(self, name):
        for x in self.tiletype_list:
            if x.name == name:
                return x

    def get_matrix(self):
        '''
        Get the non-tile matrix, with the numbers or whatever.
        '''
        return self.matrix

    def get_tiles_on_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        for tile in self.tile_list:
            if not (tile.x + tile.width < 0 or tile.x > SCREEN_WIDTH or tile.y + tile.height < 0 or tile.y > SCREEN_HEIGHT):
                yield tile

    def draw(self, surface):
        '''
        Draw all of the tiles on a given surface.
        '''
        for tile in self.get_tiles_on_screen(surface.get_width(), surface.get_height()):
            tile.draw(surface)

    def get_registry(self):
        return self.tile_registry

    def get_tiles_of_type(self, tiletype):
        for tile in self.tile_list:
            if tile.tiletype == tiletype:
                yield tile



class CollidableObject(object_manager.DirtyObject):
    def __init__(self, image, x, y, subsurface_rect_args=None):
        '''
      subsurface_rect_args format: [x (on image), y (on image), width, height]
        '''
        object_manager.DirtyObject.__init__(self)
        self.image = _sticky_load_image(image)
        self.x, self.y = x, y
        
        if not subsurface_rect_args == None:
          self.sra = subsurface_rect_args
          self.rect = pygame.Rect(self.x + subsurface_rect_args[0], self.y + subsurface_rect_args[1], subsurface_rect_args[2], subsurface_rect_args[3])
        else:
          self.rect = self.image.get_rect()
          self.rect.x = x
          self.rect.y = y
          self.sra = [0, 0, self.rect.width, self.rect.height]
        self.xvel = 0
        self.yvel = 0
        self.precollisions = {}
        self.aftercollisions = {}
        self.r = object_manager.Registry([self]) # dummy registry for depth sorting

    def goto_x(self, x):
        self.x = x
        self.rect.x = x + self.sra[0]

    def goto_y(self, y):
        self.y = y
        self.rect.y = y + self.sra[1]
    
    def goto(self, x, y):
        self.goto_x(x)
        self.goto_y(y)

    def move_x(self, x):
        self.x += x
        self.rect.x += x

    def move_y(self, y):
        self.y += y
        self.rect.y += y

    def move_xy(self, x, y):
        self.move_x(x)
        self.move_y(y)

    def collide_rect(self, rect):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.y += self.yvel 
        if self.rect.colliderect(rect):
            if self.xvel > 0:
                self.rect.right = rect.left
                collision_types['right'] = True
            if self.xvel < 0:
                self.rect.left = rect.right
                collision_types['left'] = True
        self.rect.x += self.xvel
        if self.rect.colliderect(rect):
            if self.yvel > 0:
                self.rect.bottom = rect.top
                collision_types['bottom'] = True
            if self.yvel < 0:
                self.rect.top = rect.bottom
                collision_types['top'] = True

        return collision_types

    def collide_tmap(self, tilemap, ignore_tiletypes=[], ignore_names=[]):
        '''
        Move the player, with the velocity member attributes and the tilemap to collide with.
        :param self Duh
        :param tilemap Tilemap to collide with
        :param ignore_tiletypes a list of tiletypes that the object should ignore and not collide with.
        :param ignore_names same, except with names.
        '''
        #print("collide-pre:", self.rect, self.rect.y==self.y)
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.xvel
        hit_list = tilemap.collision_test(self.rect, ignore_tiletypes=ignore_tiletypes, ignore_names=ignore_names)
        for x in filter(lambda z: z.tiletype in self.precollisions.keys(), hit_list):
            for func in self.precollisions[x.tiletype]:
                func(x)
        for t in hit_list:
            tile = t.rect
            if self.xvel > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.xvel < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        self.rect.y += self.yvel
        hit_list = tilemap.collision_test(self.rect, ignore_tiletypes=ignore_tiletypes, ignore_names=ignore_names) #recheck after moving along x-axis
        for t in hit_list:
            tile = t.rect
            if self.yvel > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.yvel < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        self.x = self.rect.x - self.sra[0]
        self.y = self.rect.y - self.sra[1]
        for x in filter(lambda z: z.tiletype in self.aftercollisions.keys(), hit_list):
            for func in self.aftercollisions[x.tiletype]:
                func(x)
        #print('collide-after:', self.rect, self.rect.y==self.y)
        return collision_types

    def draw(self, surface):
        '''
        Draw the object on a given surface
        '''
        surface.blit(self.image, (self.x, self.y))

    def add_tile_collision(self, tile, func, cols=COLLIDE_NONE):
        if cols >> 1 & 1: # collide before
            try:
                self.precollisions[tile].append(func)
            except KeyError:
                print("Key error")
                self.precollisions[tile] = [func]
                print(self.precollisions)

        elif cols >> 2 & 1:
            try:
                self.aftercollisions[tile].append(func)
            except KeyError:
                self.aftercollisions[tile] = [func]

    def zero_velocities(self):
      self.xvel = 0
      self.yvel = 0

    def set_velocities(self, xvel, yvel):
        self.xvel = xvel
        self.yvel = yvel

    def get_registry(self):
        return self.r

    def get_depth(self):
        return self.rect.y

    def move_to_rect(self, ignore_sra=False):
        if ignore_sra:
            self.x = self.rect.x
            self.y = self.rect.y
        else:
            self.x = self.rect.x - self.sra[0]
            self.y = self.rect.y - self.sra[1]

    def get_walls(self, screen_rect):
        walls = {'top': False, 'bottom': False, 'right': False, 'left': False}
        if self.rect.top <= screen_rect.top:
            walls['top'] = True
        if self.rect.bottom >= screen_rect.bottom:
            walls['bottom'] = True
        if self.rect.right >= screen_rect.right:
            walls['right'] = True
        if self.rect.left <= screen_rect.left:
            walls['left'] = True
        return walls

    def __str__(self):
        return "[CollidableObject rect=" + str(self.rect) + "]"
    
    def __repr__(self):
        return "[CollidableObject rect=" + str(self.rect) + "]"

class HittableDemoObject(Tile):
    def __init__(self, image, num_hits, destroy_callback, subsurface_rect_args=None, name="hittabledemoobject"):
        print("sra: %s" % subsurface_rect_args)
        Tile.__init__(self, image, name=name, subsurface_rect_args=subsurface_rect_args)
        self._tile_creation_class = _HittableDemoObject
        self.hits = num_hits
        self.destroy_callback = destroy_callback
        
    def hit(self, amount):
        self.num_hits -= amount
        if self.num_hits <= 0:
            self.destroy_callback(self)

def sample_callback(tile):
    print("Sample callback for %s" % tile)

    





def main():
  pygame.init()
  screen = pygame.display.set_mode((320, 320), flags=pygame.SCALED)
  dirt = Tile('assets/dirt.png', name="Dirt")
  grass = Tile('assets/grass.png', name="Grass")
  tree = HittableDemoObject('assets/tree.png', 10, sample_callback, name="Tree", subsurface_rect_args=[11, 93, 8, 3])
  ground_tmap = Tilemap(tools.load_mat('assets/level.txt'), [dirt, grass])
  flags_tmap = Tilemap(tools.load_mat('assets/flags_mat.txt'), [NullTile(), tree])
  player = CollidableObject('assets/player.png', x=100, y=100, subsurface_rect_args=[8, 29, 16, 3])
  player.image.set_colorkey((0, 0, 0))
  tree.image.set_colorkey((0, 0, 0))
  p = player
  clock = pygame.time.Clock()
  numframes = 0
  hit_objs = list(flags_tmap.tile_registry.get_all_for_condition(lambda x: x.tiletype == tree)) # sneaky generator!

  box = CollidableObject('assets/stone_path.png', x=100, y=100)

  running = True

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                for thing in hit_objs:
                    thing.hit(4)
      
    keys = pygame.key.get_pressed()

    if keys[K_UP]:
          p.yvel -= 3
    if keys[K_DOWN]:
          p.yvel += 3
    if keys[K_LEFT]:
          p.xvel -= 3
    if keys[K_RIGHT]:
          p.xvel += 3

    if keys[K_p]:
      print(p.rect, p.x, p.y)

    if p.xvel > 5:
      p.xvel = 5
    if p.xvel < -5:
      p.xvel = -5
    if p.yvel > 5:
      p.yvel = 5
    if p.yvel < -5:
      p.yvel = -5

    player.collide_tmap(flags_tmap)
    player.collide_rect(box.rect)

    player.zero_velocities()


    ground_tmap.draw(screen)
    combined_registries = player.get_registry() + flags_tmap.get_registry()
    combined_registries.draw_sorted_on_screen(screen)
    box.draw(screen)
    pygame.display.update()
    numframes += 1
    clock.tick(30)

if __name__ == '__main__':
  main()
