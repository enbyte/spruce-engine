import pygame
import pygame.freetype
import copy
import random

pygame.init()


def longest_rendered_width(list_, font):
    width = 0
    for i in list_:
        c = font.get_rect(i).width
        if c > width:
            width = c

    return width


class _GUIParent:
    '''
    Simple parent class for all other gui objects with blank methods.
    '''
    def draw(self, *pargs, **kwargs):
        pass

    def check(self, *pargs, **kwargs):
        pass

    def update(self, *pargs, **kwargs):
        pass

    def set_option(self, option, val):
        if not option in self.gui_skin.options.keys():
            print('Invalid option %s to set' % option)
            return
        else:
            self.gui_skin.options[option] = val

        self._rerender_surface()

    def get_option(self, option):
        if not option in self.gui_skin.options.keys():
            print('Invalid option %s to get' % option)
            return
        else:
            return self.gui_skin.options[option]

    def set_skin(self, skin):
        self.gui_skin = skin

    def center(self, rect):
        self.rect.center = rect.center

    def center_x(self, rect):
        self.rect.center = (rect.center[0], self.rect.center[1])

    def center_y(self, rect):
        self.rect.center = (self.rect.center[0], rect.center[1])

    def _rerender_surface(self):
        pass


class Font:
    '''
    Wrapper and loader class for fonts
    '''
    def __init__(self, filename, size, bold=False, italic=False):
        if len(filename.split('.')) == 1:
            self.font = pygame.freetype.SysFont(filename, size=size, bold=bold, italic=italic)
        else:
            self.font = pygame.freetype.Font(filename, size=size)

        print(self.font.size)

    def render(self, text, color, antialias=False):
        if color == (0, 0, 0):
            c = (1, 1, 1) # cheap hack for colorkeying
        else:
            c = color
        lines = text.splitlines()
        height = self.font.size
        width = longest_rendered_width(lines, self.font)
        line_ctr = 0
        surface = pygame.Surface((width, len(lines) * height))
        for line in lines:
            if not line == '':
                surface.blit(self.font.render(line, fgcolor=c)[0], (0, (height * line_ctr)))
            line_ctr += 1

        surface.set_colorkey((0, 0, 0))
        return surface

    def get_size(self):
        return self.font.size
    
    def get_path(self):
        return self.font.path

    def __repr__(self):
        return '[Font size=%s, path=%s]' % (self.font.size, self.font.path)

    def __str__(self):
        return self.__repr__()

class GUISkin():
    def __init__(self):
        self.options = {
            'foreground': pygame.Color('black'),
            'background': pygame.Color('white'),
            'font': Font('assets/alagard.ttf', 24 * 4/3),
            'margin': 10,
            'button-inactive-background': pygame.Color('black'),
            'button-inactive-foreground': pygame.Color('white'),
            'button-active-background': pygame.Color('#333333'),
            'button-active-foreground': pygame.Color('white'),
        }

    def set_option(self, option, val):
        if not option in self.options.keys():
            print('Invalid option %s to set' % option)
            return
        else:
            self.options[option] = val

    def get_option(self, option):
        if not option in self.options.keys():
            print('Invalid option %s to get' % option)
            return
        else:
            return self.options[option]

    def copy(self):
      g = GUISkin()
      o = self.options
      new_opts = {}
      for key in o:
          try:
              new_opts[key] = copy.deepcopy(o[key])
          except TypeError:
              # is a font
              new_opts[key] = Font(o[key].get_path(), o[key].get_size())
      g.options = new_opts
      return g

    def __repr__(self):
        return 'GUISkin: %s' % self.options

    def __str__(self):
        return self.__repr__()

    
class Button(_GUIParent):
    def __init__(self, text, gui_skin, on_click, x=0, y=0):
        self.text = text
        self.gui_skin = gui_skin.copy()
        self.on_click = on_click
        _margin = self.gui_skin.get_option('margin')
        size_rect = self.gui_skin.get_option('font').render(text, (0, 0, 0)).get_rect()
        size_rect.width += (2 * _margin)
        size_rect.height += (2 * _margin)
        self.inactive_surf = pygame.Surface((size_rect.width, size_rect.height))
        pygame.draw.rect(self.inactive_surf, self.gui_skin.get_option('button-inactive-background'), size_rect)
        self.inactive_surf.blit(self.gui_skin.get_option('font').render(text, self.gui_skin.get_option('button-inactive-foreground')), (_margin, _margin))
        self.active_surf = pygame.Surface((size_rect.width, size_rect.height))
        pygame.draw.rect(self.active_surf, self.gui_skin.get_option('button-active-background'), size_rect)
        self.active_surf.blit(self.gui_skin.get_option('font').render(text, self.gui_skin.get_option('button-active-foreground')), (_margin, _margin))
        size_rect.x = x
        size_rect.y = y
        self.rect = size_rect
        self.active = False
        self.prev = False

    def _rerender_surface(self):
        _margin = self.gui_skin.get_option('margin')
        size_rect = self.gui_skin.get_option('font').render(self.text, (0, 0, 0)).get_rect()
        size_rect.width += (2 * _margin)
        size_rect.height += (2 * _margin)
        self.inactive_surf = pygame.Surface((size_rect.width, size_rect.height))
        pygame.draw.rect(self.inactive_surf, self.gui_skin.get_option('button-inactive-background'), size_rect)
        self.inactive_surf.blit(self.gui_skin.get_option('font').render(self.text, self.gui_skin.get_option('button-inactive-foreground')), (_margin, _margin))
        self.active_surf = pygame.Surface((size_rect.width, size_rect.height))
        pygame.draw.rect(self.active_surf, self.gui_skin.get_option('button-active-background'), size_rect)
        self.active_surf.blit(self.gui_skin.get_option('font').render(self.text, self.gui_skin.get_option('button-active-foreground')), (_margin, _margin))

    def update(self, mousepos=None, keyboard=None, mousedown=None):
        if not mousepos == None:
            mp = pygame.mouse.get_pos()
        else:
            mp = mousepos

        if self.rect.collidepoint(mp):
            self.active = True
        else:
            self.active = False

        if not mousedown == None:
            if mousedown[0] and self.active:
                if not self.prev:
                    self.on_click()
                self.prev = True
            else:
                self.prev = False

    def draw(self, surface, active=None):
        if active:
            surface.blit(self.active_surf, self.rect)
        elif active == False:
            surface.blit(self.inactive_surf, self.rect)
        else:
            if self.active:
                surface.blit(self.active_surf, self.rect)
            else:
                surface.blit(self.inactive_surf, self.rect)

class Text(_GUIParent): # this one will be simple, right? right?...
    def __init__(self, text, gui_skin, x=0, y=0):
        self.text = text
        self.gui_skin = gui_skin.copy() # so it doesn't refer to the global copy of the gui_skin and modify other objects
        assert self.gui_skin != gui_skin
        self.surf = gui_skin.get_option('font').render(text, gui_skin.get_option('foreground'))
        self.rect = self.surf.get_rect() # OHHHHHHHHHH get_rect
        self.rect.x = x
        self.rect.y = y

    def _rerender_surface(self):
        w = self.rect.width
        h = self.rect.height
        color = self.gui_skin.get_option('foreground')
        font = self.gui_skin.get_option('font')
        text = self.text
        self.surf = font.render(text, color)
        x, y = self.rect.x, self.rect.y
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.surf, self.rect)

    def set_color(self, color):
        '''
      breaking?
        '''
        print(self.gui_skin)
        self.gui_skin.set_option('foreground', color)
        self._rerender_surface()
        print(self.gui_skin)

    def set_font(self, font):
        self.gui_skin.set_option('font', font)
        self._rerender_surface()

    def set_text(self, text):
        self.text = text
        self._rerender_surface()

class FillBar(_GUIParent):
    def __init__(self, gui_skin, x=0, y=0, width=0, height=0, value=0, max_value=100):
        self.gui_skin = gui_skin.copy()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.max_value = max_value
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False
        self.prev = False

    def update(self, mousepos=None, keyboard=None, mousedown=None):
        if not mousepos == None:
            mp = pygame.mouse.get_pos()
        else:
            mp = mousepos

        if self.rect.collidepoint(mp):
            self.active = True
        else:
            self.active = False

        if not mousedown == None:
            if mousedown[0] and self.active:
                if not self.prev:
                    self.change_value(5 * random.choice([-1, 1]))
                    if self.value > self.max_value:
                        self.value = self.max_value
                self.prev = True
            else:
                self.prev = False

    def set_value(self, value):
        if value > self.max_value:
            self.value = self.max_value
        elif value < 0:
            self.value = 0
        else:
            self.value = value

    def change_value(self, value):
        self.set_value(self.value + value)

    def draw(self, surface):
        pygame.draw.rect(surface, self.gui_skin.get_option('background'), self.rect)
        if self.value > 0:
            pygame.draw.rect(surface, self.gui_skin.get_option('foreground'), (self.x, self.y, self.width * (self.value / self.max_value), self.height))

class Frame(_GUIParent):
    def __init__(self):
        self.children = []

    def update(self, mousepos=None, mousedown=None, keyboard=None):
        for child in self.children:
            child.update(mousepos=mousepos, mousedown=mousedown, keyboard=keyboard)

    def draw(self, surface):
        for child in self.children:
            child.draw(surface)

    def add_child(self, child):
        self.children.append(child)


    def add_children(self, children):
        self.children.extend(children)

    def get_child(self, idnum):
        return self.children[idnum]

    def set_option(self, option, val):
        for child in self.children:
            child.set_option(option, val)
    
def main():
    pygame.init()
    gs = GUISkin()
    screen = pygame.display.set_mode((500, 500))
    screen.fill(pygame.Color('white'))
    main_frame = Frame()
    b = Button("Play", gs, lambda: t.set_color((255, 0, 0)), x=0, y=0)
    b.center(screen.get_rect())
    print("fsz==:", b.gui_skin.get_option('font').get_size())
    t = Text("AweSome Game", gs, x=200, y=10)
    t.center_x(screen.get_rect())
    t2 = Text("that is cool", gs, x=0, y=50)
    t2.set_font(Font('assets/alagard.ttf', 100)) # re-render
    t2.center_x(screen.get_rect())
    f = FillBar(gs, x=10, y=300, width=screen.get_width() - 20, height=50, value=50, max_value=100)
    f.set_option('foreground', (0, 255, 0))
    f.set_option('background', (255, 0, 0))
    main_frame.add_children([b, t, t2, f])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        mousepos = pygame.mouse.get_pos()
        mousedown = pygame.mouse.get_pressed()
        main_frame.update(mousepos=mousepos, mousedown=mousedown)
        screen.fill(pygame.Color('white'))
        main_frame.draw(screen)
        pygame.display.update()



if __name__ == '__main__':
    main()
