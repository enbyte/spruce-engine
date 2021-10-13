import pygame
import logging

COLLIDE_NONE = 0
COLLIDE_X = (1 << 1)
COLLIDE_Y = (1 << 2)

logging.basicConfig(format='Spruce %(levelname)s at %(asctime)s: %(message)s') # setup logging as 'Spruce WARNING at 1:32:00: Bing bong'

pygame.init()

_tile_registry = [] # registry of the names of all of the created tiles

def _sticky_load_image(image):
    '''
    If the image is a string, return pygame.image.load() for that image.
    If it is a pygame.Surface, return it.
    Otherwise, throw an error.
    '''
    if type(image) == str:
        return pygame.image.load(image).convert()
    elif type(image) == pygame.Surface:
        return image
    else:
        logging.error('Unrecognized type in _sticky_load_image: %s' % type(image))
        raise TypeError

class Tile:
    '''
    A class to represent a specfic _type_ of tile, i.e. lava, or grass.
    '''
    def __init__(self, image, name="", size=32):
        self.image = _sticky_load_image(image)
        if name == "":
            logging.error('Name cannot be a blank string for a Tile')
            raise NameError
        elif name in _tile_registry:
            logging.error('Name %s for a tile is already in use')
            raise NameError
        else:
            self.name = name
            _tile_registry.append(name)
        self.has_rect = True
        self.size = size

    def __str__(self):
        return '[Tiletype name=%s; image=%s; has_rect=%s; size=%s]' % (self.name, self.image, self.has_rect, self.size)

class NullTile:
    '''
    Class to represent a blank tile with no image and no rect.
    '''
    def __init__(self):
        self.name = 'NullTile'
        self.image = pygame.Surface((0, 0))
        self.has_rect = False
        self.size = 0

    def __str__(self):
        return '[Null-tiletype <no data>]'


        

class _Tile:
    '''
    Internal class used to represent a specific tile in the world.
    '''
    def __init__(self, tiletype, x, y):
        assert type(tiletype) == Tile or type(tiletype) == NullTile
        self.name = tiletype.name
        self.image = tiletype.image
        self.tiletype = tiletype #keep track of it
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.has_rect = tiletype.has_rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

    def generate_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


    def update_tiletype(self, new_tiletype):
        self.tiletype = new_tiletype
        self.image = new_tiletype.image
        self.name = new_tiletype.name
        self.size = new_tiletype.size
        if not self.has_rect and new_tiletype.has_rect: # was a nulltile, converting to a tile
            self.generate_rect()
        elif self.has_rect and not new_tiletype.has_rect: # converting to nulltile
            self.rect.width = 0
            self.rect.height = 0
        self.has_rect = new_tiletype.has_rect
        print("Done with update_tiletype")

    def move_x(self, amount):
        self.rect.x += amount
        self.x += amount
    
    def move_y(self, amount):
        self.rect.y += amount
        self.y += amount

    def move_xy(xamount, yamount):
        self.move_x(xamount)
        self.move_y(yamount)

    def goto(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return '[_Tile rect=%s; tiletype=%s]' % (str(self.rect), str(self.tiletype))

    def colliderect(self, other):
        return self.rect.colliderect(other)


class Tilemap:
    def __init__(self, matrix, tile_list, TILE_SIZE=32):
        self.matrix = matrix
        self.TILE_SIZE = TILE_SIZE
        self.tile_matrix = copy.deepcopy(matrix)
        x, y = 0, 0
        for row in self.tile_matrix:
            for thing in row:
                z = _Tile(tile_list[thing], TILE_SIZE * x, TILE_SIZE * y)
                self.tile_matrix[y][x] = z
                x += 1
            x = 0
            y += 1
           
        self.tile_list = tile_list
        self.x = 0
        self.y = 0

    def get_list_of_tiles(self):
        '''
        Concatenate the entire matrix of tiles into one list, for individual operations on them.
        '''
        z = []
        for row in self.tile_matrix:
            z.extend(row) # add the current row to z

        return z

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
        ydiff = abs(y - self.y)
        xdiff = abs(x - self.x)
        print("Diff:", xdiff, ydiff)
        ytile = int(ydiff // self.TILE_SIZE)
        xtile = int(xdiff // self.TILE_SIZE)
        print("xt type:", type(xtile))
        print("Tile:", xtile, ytile)
        print("Matrix size:", len(self.tile_matrix), len(self.tile_matrix[0]))
        print("tile_matrix tile:", self.tile_matrix[ytile][xtile])
        return self.tile_matrix[ytile][xtile]

    def get_names(self):
        return [x.name for x in self.tile_list]

    def get_tile(self, name):
        for x in self.tile_list:
            if x.name == name:
                return x

    def get_matrix(self):
        '''
        Get the non-tile matrix, with the numbers or whatever.
        '''
        z = tools.matrix(0, len(self.tile_matrix[0]),  len(self.tile_matrix))
        x, y = 0, 0
        for i in z:
            for p in i:
                print('y, x:', y, x)
                t = self.get_tile(self.tile_matrix[y][x].name)
                z[y][x] = self.tile_list.index(t)
                x += 1
            x = 0
            y += 1

        return z

    def get_tiles_on_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        tiles = []
        for tile in self.get_list_of_tiles():
            if tile.colliderect(screen_rect):
                tiles.append(tile)
        return tiles

    def draw(self, surface):
        '''
        Draw all of the tiles on a given surface.
        '''
        for tile in self.get_tiles_on_screen(surface.get_width(), surface.get_height()):
            tile.draw(surface)



class CollidableObject:
    def __init__(self, image, x, y):
        self.image = _sticky_load_image(image)
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.yvel = 0
        self.precollisions = {}
        self.aftercollisions = {}

    def goto_x(self, x):
        self.x = x
        self.rect.x = x

    def goto_y(self, y):
        self.y = y
        self.rect.y = y
    
    def goto(self, x, y):
        self.goto_x(x)
        self.goto_y(y)

    def move_x(self, x):
        self.x += x
        self.rect.x += x

    def move_y(self, y):
        self.y = y
        self.rect.y = y

    def move_xy(self, x, y):
        self.move_x(x)
        self.move_y(y)

    def collide(self, tilemap, ignore_tiletypes=[], ignore_names=[]):
        '''
        Move the player, with the velocity member attributes and the tilemap to collide with.
        :param self Duh
        :param tilemap Tilemap to collide with
        :param ignore_tiletypes a list of tiletypes that the object should ignore and not collide with.
        :param ignore_names same, except with names.
        '''
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
        self.x = self.rect.x
        self.y = self.rect.y
        for x in filter(lambda z: z.tiletype in self.aftercollisions.keys(), hit_list):
            for func in self.aftercollisions[x.tiletype]:
                func(x)
        return collision_types

    def draw(self, surface):
        '''
        Draw the object on a given surface
        '''
        surface.blit(self.image, self.rect)

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