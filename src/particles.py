import pygame
import random
from math import radians, sin, cos, degrees, pi

pygame.init()




class _Particle:
    '''
    class to represent a particle in the world
    '''
    def __init__(self, x, y, decay=500, angle=0, color='white', speed=10, size=10):
        '''
        angle is IN RADIANS
        '''
        self.decay = decay
        self.curangle = 0
        self._health = decay
        self.rect = pygame.Rect(x, y, size, size)
        self.surf = pygame.Surface((size, size))
        self.surf.fill(color)
        self.og_surf = self.surf.copy()
        self.x_vel = cos(angle) * speed
        self.y_vel= sin(angle) * speed
        self.origin_x = x
        self.origin_y = y

    def _get_pos_at_tick(self, tick):
        return (self.origin_x + self.x_vel * tick, self.origin_y + self.y_vel * tick)

    def _move(self):
        self.rect.topleft = self._get_pos_at_tick(self.decay - self._health)

    def _decay(self, _decay=1):
        self._health -= 1
        if self._health <= 0:
            self.kill()

    def update(self, blue=0):
        '''
        self.curangle += 10
        self.surf  = pygame.transform.rotate(self.og_surf, self.curangle)
        '''
        r_color = int((self.rect.x / 800) * 255) % 255
        g_color = int((self.rect.y / 800) * 255) % 255
        b_color = blue
        self.surf.fill((r_color, g_color, b_color))
        self._move()
        self._decay()

    def draw(self, screen):
        screen.blit(self.surf, (self.rect.x, self.rect.y))

    def kill(self):
        del self

class _FireParticle(_Particle):
    def update(self):
        tick_pct = self._health / self.decay
        color = pygame.Color.lerp(pygame.Color('#000000'), pygame.Color('cornflowerblue'), tick_pct)
        self.surf.fill(color)
        self._move()
        self._decay()
    

class Particle:
    '''
    class to represent a type of particle'''
    def __init__(self, color, _particle_creation_class=_Particle, _tick=0):
        self.color = color
        self._particle_creation_class = _particle_creation_class
        self.tick = _tick

    def create(self, x, y, angle, decay=5, speed=10, *pargs, **kwargs):
        return self._particle_creation_class(x, y, decay, angle, self.color, speed, *pargs, **kwargs)
    
FireParticle = Particle(pygame.Color('black'), _FireParticle)



class ParticleEmitter:
    def __init__(self, x, y, angle, particle):
        '''
        angle is IN RADIANS'''
        self.angle = angle
        self.x = x
        self.y = y
        self.particle = particle
        self.particles = []

    def update(self, *args, **kwargs):
        for particle in self.particles:
            particle.update(*args, **kwargs)
        self.particles = [particle for particle in self.particles if particle._health > 0]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)




    def add_particle(self, angle, *pargs, **kwargs):
        self.particles.append(
            self.particle.create(
                self.x,
                self.y,
                self.angle + angle,
                *pargs,
                **kwargs,
            )
        )

    def move_x(self, x):
        self.x += x
    
    def move_y(self, y):
        self.y += y
    
    def move(self, x, y):
        self.x += x
        self.y += y

    def goto(self, x, y):
        self.x = x
        self.y = y


def main():
    screen = pygame.display.set_mode((800, 600), flags=pygame.SCALED)
    pygame.display.set_caption('Particles')
    clock = pygame.time.Clock()
    running = True

    sample_particle = Particle(pygame.Color('red'))
    fire_particle = FireParticle

    fire_emitter = ParticleEmitter(400, 300, -1.57, fire_particle)
    

    frame_no = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(pygame.Color('black'))
        if frame_no % 1 == 0:
            for i in range(250):
                fire_emitter.add_particle(random.uniform(pi, -pi), decay=10, size=2, speed=100      )
            print(int(clock.get_fps()))
        fire_emitter.goto(*pygame.mouse.get_pos())
        fire_emitter.update()
        fire_emitter.draw(screen)
        pygame.display.update()
        clock.tick(60)
        frame_no += 1



if __name__ == '__main__':
    main()

    

    
