try:
    from utils import *


    def whatTheNewTower():
        keys = pygame.key.get_pressed()
        for b in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
            if keys[b]:
                return {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4}[b]
        return 0


    def get_distant(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


    def load_images(root, lst, width=1, height=1):
        r = []
        if isinstance(lst, str):
            img = load_img(root, lst)
            img = pygame.transform.scale(img, (int(img.get_width() * width), int(img.get_height() * height)))
            return img
        for img_name in lst:
            if isinstance(img_name, str):
                img = load_img(root, img_name)
                img = pygame.transform.scale(img, (int(img.get_width() * width), int(img.get_height() * height)))
                r.append(img)
            else:
                r.append([load_images(root, i, width, height) for i in img_name])
        return r


    def main():
        from os import listdir
        import pygame
        from pygame import font

        from constants import PRICES, STONE_TOWER_CLASSES
        from enemy import Enemy
        from tower import StoneTower, StoneTowerSecondType, Button, StoneTowerThirdType
        import sys
        from constants import WIDTH, HEIGHT, HERO_WIDTH, HERO_HEIGHT, GOBLIN, SCORPION, STONE_TOWERS, \
            OLD_MAN, DELAY, LIVES, STONE_TOWER, STONE_TOWER_IMG, TOWER_WIDTH, TOWER_HEIGHT, WAVES, \
            WAIT_BETWEEN_WAVES, STONE_IMGS, COINS

        def addStoneTower(num):
            px, py = pygame.mouse.get_pos()
            if num + 1 and COINS >= PRICES[num][0]:
                bashni.append(
                    STONE_TOWER_CLASSES[num](px, py, load_images(STONE_TOWER, STONE_TOWER_IMG[num], TOWER_WIDTH,
                                                                 TOWER_HEIGHT),
                                             *load_images(STONE_TOWER, STONE_IMGS[num],
                                                          TOWER_WIDTH if num != 2 else 1.3,
                                                          TOWER_HEIGHT if num != 2 else 1.3),
                                             **STONE_TOWERS[num])
                )
                bashni[-1].x -= bashni[-1].width // 2
                bashni[-1].y -= bashni[-1].height // 2
                newbas = bashni[-1]
                rect = pygame.rect.Rect(newbas.x, newbas.y, newbas.width, newbas.height)
                for tower in bashni[:-1]:
                    if pygame.rect.Rect(tower.x, tower.y, tower.width, tower.height).colliderect(rect):
                        bashni.pop()
                        return False

                try:
                    for px in range(newbas.x // 10, (newbas.x + newbas.width) // 10):
                        if not TowerPlaces[(newbas.y + newbas.height) // 10][px]:
                            bashni.pop()
                            return False
                except IndexError:
                    bashni.pop()
                    return False
                return True

        pygame.init()
        pygame.mixer.music.load(resource_path('fone.wav'))
        geroes = []
        images = {}
        bashni = []
        addStoneTowerButtons = []
        addStoneTowerTowers = []
        TowerPlaces = eval(open_file('TowerPlaces.txt').read())
        pause = False
        for number in range(3):
            x, y = pygame.mouse.get_pos()
            addStoneTowerTowers.append(
                STONE_TOWER_CLASSES[number](x, y, load_images(STONE_TOWER, STONE_TOWER_IMG[number], TOWER_WIDTH,
                                                              TOWER_HEIGHT),
                                            *load_images(STONE_TOWER, STONE_IMGS[number], TOWER_WIDTH, TOWER_HEIGHT),
                                            **STONE_TOWERS[number])
            )
            addStoneTowerTowers[-1].x -= addStoneTowerTowers[-1].width // 2
            addStoneTowerTowers[-1].y -= addStoneTowerTowers[-1].height // 2
            addStoneTowerButtons.append(
                Button(pygame.transform.scale(load_img('buttons', f'tower{number}.png'), (80, 80)), WIDTH - 110,
                       180 + 100 * number, PRICES[number][0]))
        UI_elements = addStoneTowerButtons
        button_pause = Button(pygame.transform.scale(load_img('buttons', 'pause.png'), (80, 80)), WIDTH - 110,
                              180 + 3 * 100)
        UI_elements.append(button_pause)
        selected_tower = None
        for hero_name in [GOBLIN, SCORPION, OLD_MAN]:
            images.update(
                {hero_name: [pygame.transform.scale(load_img(hero_name, 'walk', filename), (HERO_WIDTH, HERO_HEIGHT))
                             for filename in listdir(resource_path(hero_name, 'walk'))]})

        coin = pygame.transform.scale(load_img('buttons', 'money.png'), (180, 80))
        cerdce = pygame.transform.scale(load_img('buttons', 'lives.png'), (180, 80))

        background = load_img('game_background.png')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font_ = font.Font(resource_path('font.ttf'), 60)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)
        isend = False
        iteration_number = 0
        wave_number = 0
        paths = [[tuple(map(int, line.split())) for line in open_file(
            'paths', pathname).read().splitlines()] for pathname in listdir(resource_path('paths'))]
        while True:
            screen.blit(background, (0, 0))

            # ----------------------О-Т-Р-И-С-О-В-К-А--U-I---------------------
            for UI_element in UI_elements:
                UI_element.draw(screen)
            screen.blit(cerdce, (WIDTH - 190, 4))
            screen.blit(font_.render(str(LIVES), True, (180, 0, 0)), (WIDTH - 165, 4))
            screen.blit(coin, (WIDTH - 190, 90))
            screen.blit(font_.render(str(COINS), True, (180, 180, 0)), (WIDTH - 165, 90))
            # -----О-Т-Р-И-С-О-В-К-А--О-С-Т-А-Л-Ь-Н-Ы-Х---Э-Л-М-Е-Н-Т-О-В-------
            for geroy in geroes:
                geroy.draw()
            for bas in bashni:
                bas.draw(screen)
            for button in addStoneTowerButtons:
                button.draw(screen)
            if selected_tower:
                selected_tower.draw(screen)

            if not pause:
                if selected_tower:
                    # bashni[-1].x -= bashni[-1].width // 2
                    #                 bashni[-1].y -= bashni[-1].height // 2
                    selected_tower.x, selected_tower.y = pygame.mouse.get_pos()
                    selected_tower.x -= selected_tower.width // 2
                    selected_tower.y -= selected_tower.height // 2
                    selected_tower.draw(screen)
                iteration_number += 1
                if isend and len(geroes):
                    iteration_number -= 1
                elif isend:
                    isend = False
                try:
                    if iteration_number >= 0 and iteration_number % WAVES[wave_number].wait == 0:
                        try:
                            path, name, speed, lives, fine, reward = WAVES[wave_number].next()
                            geroes.append(Enemy(images[name], screen, paths[path], name, speed, lives, fine, reward))
                        except StopIteration:
                            wave_number += 1
                            iteration_number = - WAIT_BETWEEN_WAVES
                            isend = True
                except IndexError:
                    print('В Ы   В Ы И Г Р А Л И ! ! !')
                    sys.exit()
                for geroy in geroes:
                    if geroy.move():
                        LIVES -= geroy.fine
                        geroes.remove(geroy)
                for bas in bashni:
                    for enemy in bas.update() + bas.update():
                        try:
                            enemy.lives -= bas.uron
                            enemy.now_uron -= bas.uron
                            if enemy.lives <= 0:
                                geroes.remove(enemy)
                                COINS += enemy.reward
                        except ValueError:
                            pass
                for bas in bashni:
                    for geroy in geroes:
                        x, y = geroy.get_pos(95)
                        bx, by = bas.x + bas.width // 2, bas.y + bas.height // 2
                        if get_distant(x, y, bx, by) <= bas.range and geroy.lives - geroy.now_uron > 0:
                            print(geroy.lives, geroy.now_uron)
                            bas.attack(geroy)
                            break
                if LIVES <= 0:
                    print('В Ы   П Р О И Г Р А Л И  ! ! !')
                    sys.exit()
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if selected_tower:
                            if addStoneTower(selected_tower.type):
                                COINS -= PRICES[selected_tower.type][0]
                            selected_tower = None
                for number in range(3):
                    if addStoneTowerButtons[number].try_push(events, eventTypeRequire=pygame.MOUSEBUTTONDOWN):
                        selected_tower = addStoneTowerTowers[number]
                    # elif event.type == pygame.KEYUP and event.key == pygame.K_z:
                    #     print(bashni[0].x, bashni[0].y)
                    #     self = bashni[0]
                    #     print(self.x, self.y + self.pos + self.imgs[self.level][0].get_height() - 2)
                if button_pause.try_push(events):
                    pause = True
                for bas in bashni:
                    if pygame.rect.Rect(bas.x, bas.y, bas.width, bas.height + 50).collidepoint(*pygame.mouse.get_pos()):
                        bas.draw_circle(screen)
                        radius = bas.range
                        if bas.sellButton.try_push(events, bas.x + bas.width // 2 - radius,
                                                   bas.y + bas.height // 2 - radius):
                            bashni.remove(bas)
                            COINS += PRICES[bas.type][3]
                        elif bas.upgradeButton.try_push(events, bas.x + bas.width // 2 - radius,
                                                        bas.y + bas.height // 2 - radius) and bas.level <= 1 and COINS >= \
                                PRICES[bas.type][bas.level + 1]:
                            COINS -= PRICES[bas.type][bas.level + 1]
                            bas.upgrade()
                for y in range(len(TowerPlaces)):
                    for x in range(len(TowerPlaces[0])):
                        if TowerPlaces[y][x]:
                            pass
                            # pygame.draw.rect(screen, (0, 255, 0), (x * 10, y * 10, 10, 10))
            else:
                surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                surface.fill((0, 0, 0, 100))
                screen.blit(surface, (0, 0))
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                    elif e.type == pygame.MOUSEBUTTONUP:
                        pause = False
            pygame.time.delay(DELAY)
            pygame.display.flip()


    if __name__ == '__main__':
        main()
finally:
    pass
