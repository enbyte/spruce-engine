import pygame
from pygame.locals import *
pygame.init()

if not __name__ == '__main__':
    from . import tilemap
    from . import ui
    from . import drops
    from . import inventory
    from . import rotate
    from . import object_manager
    from . import btm_tools as tools
else:
    import tilemap
    import ui
    import drops
    import inventory
    import rotate
    import object_manager
    import btm_tools as tools


# HANDLER FUNCS SETUP

def remove_tile(tile):
    tile.update_tiletype(NullTile)

# ASSETS SETUP

manager = object_manager.AssetManager()

manager.add_texture("assets/player.png", "player")
manager.add_texture("assets/dirt.png", "dirt")
manager.add_texture("assets/grass.png", "grass")
manager.add_texture("assets/tree.png", "tree")
manager.add_texture("assets/wooden_axe.png", "axe")    

# SCREEN SETUP
SCREEN_WIDTH = 10 * 32
SCREEN_HEIGHT = 10 * 32
SCREEN_FLAGS = SCALED | DOUBLEBUF

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=SCREEN_FLAGS)

# OBJECT CREATION
PLAYER_INITIAL_X = 100
PLAYER_INITIAL_Y = 100
player = tilemap.CollidableObject(manager.get_texture('player'), PLAYER_INITIAL_X, PLAYER_INITIAL_Y, subsurface_rect_args=[20, 0, 32, 12])

# TILES CREATION

dirt = tilemap.Tile(manager.get_texture('dirt'), name='dirt')
grass = tilemap.Tile(manager.get_texture('grass'), name='grass')
tree = tilemap.HittableDemoObject(manager.get_texture('tree'), num_hits=10, destroy_callback=remove_tile, name='tree', subsurface_rect_args=[11, 93, 8, 3])

# TILEMAP CREATION

ground_tmap = tilemap.Tilemap(tools.load_mat('assets/level.txt'), [dirt, grass])
trees_tmap = tilemap.Tilemap(tools.load_mat('assets/flags_mat.txt'), [tilemap.NullTile(), tree])


# MAIN LOOP SETUP

global running
running = True

pygame.event.set_allowed([QUIT, KEYDOWN])


def main():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        display.fill((0, 0, 0))
        ground_tmap.draw(display)
        trees_tmap.draw(display)
        player.draw(display)

        pygame.display.update()
        

if __name__ == "__main__":
    main()