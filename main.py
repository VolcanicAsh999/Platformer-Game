import pygame
import random

screen = pygame.display.set_mode((1000, 700))

class Player:
    def __init__(self, x, y):
        self.drect = pygame.Rect(x, y, 20, 20)
        self.rect = pygame.Rect(x, y - 5, 20, 20)
        self.color = pygame.Color('red')
        self.dy = 0
        self.jumping = False
        self.ypos = 0
        self.padx = 300
        self.pady = 200

    def render(self, game):
        self.draw(game)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move(game, -1)
        if keys[pygame.K_d]:
            self.move(game, 1)
        if keys[pygame.K_w]:
            self.jump(game)
        if pygame.sprite.collide_rect(self, game.goal):
            game.levelup()
            return
        self.fall(game)
        self.check_out_of_bounds(game)
        self.check_stuck(game)

    def draw(self, game):
        pygame.draw.rect(game.screen, self.color, self.drect)

    def move(self, game, x):
        """self.rect = self.rect.move(x, 0)
        for platform in game.platforms:
            if platform.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y - 10, 20, 20)):
                self.rect = self.rect.move(-x, 0)
                return
        self.drect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)""" #for no scrolling
        dx = x
        for platform in game.platforms:
            if platform.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y - 10, 20, 20)):
                dx = 0
                return
        if (self.rect.x < self.padx and dx < 0) or (self.rect.x > game.width - self.padx and dx > 0):
            game.scroll(x=-dx)
        else:
            self.rect = self.rect.move(dx, 0)
            self.drect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)

    def fall(self, game):
        if self.jumping:
            self.dy += 0.02
            self.rect = self.rect.move(0, int(self.dy))
            for platform in game.platforms:
                if platform.rect.colliderect(pygame.Rect(self.rect.x + 3, self.rect.y + 20, 13, 1)):
                    self.rect = self.rect.move(0, -int(self.dy))
                    self.dy = 0
                    self.jumping = False
                    return
                if platform.rect.colliderect(pygame.Rect(self.rect.x + 3, self.rect.y - 1, 13, 1)):
                    self.rect = self.rect.move(0, -int(self.dy))
                    self.dy = 0
                    self.jumping = False
                    return
            self.ypos -= int(self.dy)
            self.drect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)
        else:
            self.dy += 0.02
            self.rect = self.rect.move(0, int(self.dy))
            for platform in game.platforms:
                if platform.rect.colliderect(pygame.Rect(self.rect.x + 3, self.rect.y + 20, 13, 1)):
                    self.rect = self.rect.move(0, -int(self.dy))
                    self.dy = 0
                    return
            self.ypos -= int(self.dy)
            self.drect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)
        if (self.rect.y < self.pady and self.dy < 0) or (self.rect.y > game.height - self.pady and self.dy > 0):
            self.rect = self.rect.move(0, -int(self.dy))
            self.drect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)
            game.scroll(y=-int(self.dy))
            self.ypos += int(self.dy)

    def jump(self, game):
        self.jumping = True
        for platform in game.platforms:
            if platform.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + 10, 20, 20)):
                self.dy = -3
                self.ypos += 3
                self.rect = self.rect.move(0, self.dy)
                self.drect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)

    def check_out_of_bounds(self, game):
        count = 0
        for platform in game.platforms:
            if platform.rect.y < -100:
                count += 1
        if count >= len(game.platforms):
            game.die()
            return
        for enemy in game.enemies:
            if self.rect.colliderect(enemy.rect):
                game.die()
                return

    def check_stuck(self, game):
        for platform in game.platforms:
            if platform.rect.colliderect(pygame.Rect(self.rect.x + 10, self.rect.y - 1, 1, 1)):
                self.rect = self.rect.move(0, 10)
                self.drect = self.drect.move(0, 10)
        
class Platform:
    def __init__(self, x, y, width):
        self.rect = pygame.Rect(x, y, width, 10)
        self.color = pygame.Color('black')

    def render(self, game):
        self.draw(game)

    def draw(self, game):
        pygame.draw.rect(game.screen, self.color, self.rect)

class Wall(Platform):
    def __init__(self, x, y, height):
        self.rect = pygame.Rect(x, y, 10, height)
        self.color = pygame.Color('black')

class Goal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = pygame.Color('blue')

    def render(self, game):
        self.draw(game)

    def draw(self, game):
        pygame.draw.rect(game.screen, self.color, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = pygame.Color(random.choice(['yellow', 'green', 'purple']))
        self.dx = 1
        self.speed = 1
        self.delay = 0
        self.mdelay = 3
        self.dy = 0

    def render(self, game):
        self.delay += 1
        if self.delay >= self.mdelay:
            self.rect = self.rect.move(self.dx * self.speed, 0)
            self.delay = 0
        count = 0
        for platform in game.platforms:
            if platform.rect.colliderect(pygame.Rect(self.rect.x + 3, self.rect.y + 19, 13, 1)):
                count += 1
            if platform.rect.colliderect(pygame.Rect(self.rect.x - 1, self.rect.y + 3, 1, 13)):
                self.dx = 1
                self.rect = self.rect.move(self.dx * self.speed, 0)
                return
            if platform.rect.colliderect(pygame.Rect(self.rect.x + 20, self.rect.y + 3, 1, 13)):
                self.dx = -1
                self.rect = self.rect.move(self.dx * self.speed, 0)
                return
        if count == 0:
            self.dx *= -1
            self.rect = self.rect.move(self.dx * self.speed, 0)
        self.draw(game)
        self.fall(game)

    def draw(self, game):
        pygame.draw.rect(game.screen, self.color, self.rect)

    def fall(self, game):
        count = 0
        for platform in game.platforms:
            if platform.rect.colliderect(pygame.Rect(self.rect.x + 3, self.rect.y + 19, 13, 1)):
                count += 1
        if count > 0:
            self.dy = 0
            return
        self.dy += 0.02
        self.rect = self.rect.move(0, int(self.dy))

class Lava:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('red')

    def render(self, game):
        self.draw(game)

    def draw(self, game):
        pygame.draw.rect(game.screen, self.color, self.rect)
        
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.platforms = []
        self.enemies = []
        self.lava = []
        self.level = 1
        self.setup_level_1()

    @property
    def height(self): return self.screen.get_height()
    @property
    def width(self): return self.screen.get_width()

    def setup_level_1(self):
        """self.goal = Goal(self.width - 100, 100)
        self.player = Player(100, self.height - 100)
        self.platforms.append(Platform(30, 630, 300))
        self.platforms.append(Platform(300, 500, 140))
        self.platforms.append(Platform(200, 400, 30))
        self.platforms.append(Platform(400, 300, 50))
        self.platforms.append(Platform(600, 250, 60))""" #for a non-scrolling game
        self.player = Player(100, self.height - 100)
        self.goal = Goal(self.width + 2000, -200)
        self.platforms.append(Platform(30, 630, 300))
        self.platforms.append(Platform(300, 500, 140))
        self.platforms.append(Platform(200, 400, 30))
        self.platforms.append(Platform(400, 300, 50))
        self.platforms.append(Platform(600, 250, 60))
        self.platforms.append(Platform(self.width - 100, 400, 300))
        self.platforms.append(Platform(self.width + 250, 300, 60))
        self.platforms.append(Platform(self.width + 570, 650, 100))
        self.platforms.append(Platform(self.width + 700, 600, 300))
        self.platforms.append(Platform(self.width + 900, 500, 100))
        self.platforms.append(Platform(self.width + 600, 400, 100))
        self.platforms.append(Platform(self.width + 800, 300, 100))
        self.platforms.append(Platform(self.width + 1000, 200, 300))
        self.platforms.append(Platform(self.width + 1200, 0, 200))
        self.platforms.append(Platform(self.width + 1500, -100, 100))
        self.platforms.append(Platform(self.width + 1800, -200, 50))
        self.platforms.append(Platform(self.width + 490, 0, 120))
        self.platforms.append(Wall(self.width + 1150, 0, 200))
        self.platforms.append(Wall(self.width + 590, 0, 600))
        self.enemies.append(Enemy(self.width - 100, 370))
        self.enemies.append(Enemy(self.width + 1170, -30))
        self.enemies.append(Enemy(self.width + 1110, -30))
        self.enemies.append(Enemy(self.width + 750, 550))

    def setup_level_2(self):
        self.goal = Goal(self.width + 700, -800)
        self.player = Player(100, self.height - 100)
        self.platforms.append(Platform(80, self.height - 70, 40))
        self.platforms.append(Platform(300, self.height - 150, 100))
        self.platforms.append(Platform(550, self.height - 230, 30))
        self.platforms.append(Platform(720, 0, 100))
        self.platforms.append(Platform(800, -100, 250))
        self.platforms.append(Platform(750, -200, 200))
        self.platforms.append(Platform(800, -300, 200))
        self.platforms.append(Platform(1050, -400, 50))
        self.platforms.append(Platform(900, -500, 100))
        self.platforms.append(Platform(-100, -600, 900))
        self.platforms.append(Platform(50, -750, 1000))
        self.platforms.append(Platform(self.width + 100, -800, 200))
        self.platforms.append(Platform(self.width + 200, -900, 50))
        self.platforms.append(Platform(self.width + 300, -1000, 200))
        self.platforms.append(Platform(self.width + 695, -779, 30))
        self.platforms.append(Wall(700, 0, self.height - 260))
        self.platforms.append(Wall(1050, -200, 100))
        self.platforms.append(Wall(750, -300, 100))
        self.enemies.append(Enemy(100, -780))
        self.enemies.append(Enemy(500, -780))
        self.enemies.append(Enemy(900, -780))
        self.enemies.append(Enemy(50, -630))
        self.enemies.append(Enemy(650, -630))
        self.enemies.append(Enemy(self.width + 200, -830))
        self.enemies.append(Enemy(self.width + 400, -1030))

    def win(self):
        ...

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.levelup()
        self.render()

    def render(self):
        self.screen.fill(pygame.Color('white'))
        self.player.render(self)
        self.goal.render(self)
        for platform in self.platforms:
            platform.render(self)
        for enemy in self.enemies:
            enemy.render(self)
        for lava in self.lava:
            lava.render(self)
        pygame.display.update()

    def loop(self):
        while True:
            self.update()

    def levelup(self):
        self.platforms.clear()
        self.enemies.clear()
        self.lava.clear()
        self.player = self.goal = None
        if self.level == 1:
            self.setup_level_2()
            self.level = 2
        else:
            self.win()

    def die(self):
        self.platforms.clear()
        self.enemies.clear()
        self.lava.clear()
        self.player = self.goal = None
        if self.level == 1:
            self.setup_level_1()
        elif self.level == 2:
            self.setup_level_2()
        else:
            self.win()

    def scroll(self, x=0, y=0):
        for platform in self.platforms:
            platform.rect = platform.rect.move(x, y)
        for enemy in self.enemies:
            enemy.rect = enemy.rect.move(x, y)
        for lava in self.lava:
            lava.rect = lava.rect.move(x, y)
        self.goal.rect = self.goal.rect.move(x, y)

def main():
    game = Game(screen)
    game.loop()

if __name__ == "__main__":
    main()
