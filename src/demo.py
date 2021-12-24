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

# DROPS SETUP
tree_drops = drops.ItemDrops('assets/tree_drops.json', name='tree_drops')


# HANDLER FUNCS SETUP

def remove_tile(tile):
    tile.update_tiletype(NullTile)

get_trees = lambda tmap: list(tmap.tile_registry.get_all_for_condition(lambda x: x.tiletype == tree))

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
class var: pass
var.PLAYER_INITIAL_X = 100
var.PLAYER_INITIAL_Y = 100
var.PLAYER_YVEL = 0
var.PLAYER_XVEL = 0
var.PLAYER_YVEL_CAP = 5
var.PLAYER_XVEL_CAP = 5
player = tilemap.CollidableObject(manager.get_texture('player'), var.PLAYER_INITIAL_X, var.PLAYER_INITIAL_Y, subsurface_rect_args=[0, 29, 32, 3])

axe = tilemap.CollidableObject(manager.get_texture('axe'), PLAYER_INITIAL_X)

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

clock = pygame.time.Clock()


def main():
    global running, var
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            var.PLAYER_YVEL -= 3
        if keys[K_DOWN]:
            var.PLAYER_YVEL += 3
        if keys[K_LEFT]:
            var.PLAYER_XVEL -= 3
        if keys[K_RIGHT]:
            var.PLAYER_XVEL += 3

        if keys[K_p]:
            print(player.rect, player.x, player.y)

        if var.PLAYER_XVEL > var.PLAYER_XVEL_CAP:
            var.PLAYER_XVEL = 5
        if var.PLAYER_XVEL < -1 * var.PLAYER_XVEL_CAP:
            var.PLAYER_XVEL = -5
        if var.PLAYER_YVEL > var.PLAYER_YVEL_CAP:
            var.PLAYER_YVEL = 5
        if var.PLAYER_YVEL < -1 * var.PLAYER_YVEL_CAP:
            var.PLAYER_YVEL = -5
        
        player.set_velocities(var.PLAYER_XVEL, var.PLAYER_YVEL)

        player.collide(trees_tmap)

        player.zero_velocities()
        var.PLAYER_XVEL, var.PLAYER_YVEL = 0, 0


        ground_tmap.draw(display)
        combined_registries = player.get_registry() + trees_tmap.get_registry()
        combined_registries.draw_sorted_on_screen(display)
        pygame.display.update()
        clock.tick(30)
        

if __name__ == "__main__":
    main()