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
class var: pass

# UI SETUP
var.gs = ui.GUISkin()
var.fps_counter = ui.Text('FPS: 0', var.gs, 10, 10)

# DROPS SETUP
tree_drops = drops.ItemDrops('assets/tree_drops.json', name='drops_tree')


# HANDLER FUNCS SETUP

def remove_tile(tile):
    m = tile.tilemap
    print(get_trees(m))
    print("len:", len(m.get_registry()))
    tile.update_tiletype(tilemap.NullTile(), m)
    m.update_registry()
    #print(get_trees(m))
    print("len 2:", len(m.get_registry()))

get_trees = lambda tmap: list(tmap.tile_registry.get_all_for_condition(lambda x: x.tiletype == tree))

# ASSETS SETUP

manager = object_manager.AssetManager()

manager.add_texture("assets/player.png", "player")
manager.add_texture("assets/dirt.png", "dirt")
manager.add_texture("assets/grass.png", "grass")
manager.add_texture("assets/tree.png", "tree")
manager.add_texture("assets/wooden_pickaxe.png", "axe") 
manager.textures["axe"] = pygame.transform.scale(manager.get_texture('axe'), (32, 32))
# SCREEN SETUP
SCREEN_WIDTH = 10 * 32
SCREEN_HEIGHT = 10 * 32
SCREEN_FLAGS = DOUBLEBUF

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=SCREEN_FLAGS)

# OBJECT CREATION

var.FPS = 60
var.PLAYER_INITIAL_X = 100
var.PLAYER_INITIAL_Y = 100
var.PLAYER_YVEL = 0
var.PLAYER_XVEL = 0
var.PLAYER_YVEL_CAP = 5
var.PLAYER_XVEL_CAP = 5
player = tilemap.CollidableObject(manager.get_texture('player'), var.PLAYER_INITIAL_X, var.PLAYER_INITIAL_Y, subsurface_rect_args=[0, 29, 32, 3])
axe = tilemap.CollidableObject(manager.get_texture('axe'), 0, 0)
var.axe_rotation_point = player.rect.center
var.axe_rotator = rotate.Rotator(axe.rect.center, axe.rect.midbottom, image_angle=45)
var.axe_angle = 0
var.axe_rotation_steps = var.FPS
var.axe_step = 0
var.axe_is_rotating = False

def axe_get_depth():
    return axe.rect.center[1]

axe.get_depth = axe_get_depth

def get_angle(axe_step):
    global var
    return int(360 * (var.axe_step / var.axe_rotation_steps))

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
    axe_center_points = []
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    var.axe_is_rotating = True
                    var.axe_step = 0
                    axe.rect.midbottom = (player.x + player.image.get_width() / 2, player.y + player.image.get_height() / 2)
                    var.axe_rotator = rotate.Rotator(axe.rect.center, (player.x + player.image.get_width() / 2, player.y + player.image.get_height() / 2), image_angle=45)
                    print('space down')

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
        if var.axe_is_rotating and not var.axe_step == var.axe_rotation_steps + 1:
            angle = get_angle(var.axe_step)
            axe.image = pygame.transform.rotate(manager.get_texture('axe'), angle)
            axe.rect.center = var.axe_rotator(angle, (player.x + player.image.get_width() / 2, player.y + player.image.get_height() / 2))
            axe.move_to_rect(ignore_sra=True)
            var.axe_step += 1
            a_s = manager.get_texture('axe').get_rect(center=axe.rect.center)
            axe_center_points.append(axe.rect.center)
        else:
            var.axe_is_rotating = False
        '''
        if var.axe_is_rotating and not var.axe_step == var.axe_rotation_steps:
            angle = get_angle(var.axe_step)
            axe.image = pygame.transform.rotate(manager.get_texture('axe'), angle)
            var.axe_step += 1
            axe.rect.center = player.rect.center
        else:
            var.axe_is_rotating = False
        '''

        ground_tmap.draw(display)
        combined_registries = player.get_registry() + trees_tmap.get_registry()
        if var.axe_is_rotating:
            combined_registries += axe.get_registry()
        combined_registries.draw_sorted_on_screen(display)
        if var.axe_is_rotating:
            #pygame.draw.rect(display, (0, 255, 0), a_s, width=3)

            for tree in get_trees(trees_tmap):
                if tree.rect.colliderect(axe.rect):
                    print("ye hit me!")
                    tree.hit(3)
                    ui.FillBar(var.gs, x=0, y=50, width=100, height=10, value=tree.hits, max_value=10).draw(display)
                    var.axe_is_rotating = False
                    var.axe_step = 0

        for point in axe_center_points:
            pass#pygame.draw.line(display, (0, 255, 0), point, point, width=3)
        var.fps_counter.set_text("FPS: %s" % int(clock.get_fps()))
        var.fps_counter.draw(display)


        pygame.display.update()
        clock.tick_busy_loop(var.FPS)
        

if __name__ == "__main__":
    main()