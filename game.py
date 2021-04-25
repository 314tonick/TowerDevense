from constants import FREEZE_COST, LENGTH_OF_FREEZE
from utils import *

stars = open_file('history.txt').read()

try:
    def concatSurfaces(s1: pygame.Surface, s2: pygame.Surface, s2_coords: tuple, make_copy=True):
        if make_copy:
            s1 = s1.copy()
        s1.blit(s2, s2_coords)
        return s1


    def whatTheNewTower():
        keys = pygame.key.get_pressed()
        for b in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
            if keys[b]:
                return {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4}[b]
        return 0


    def get_distant(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


    def load_images(root, lst, width: float = 1, height: float = 1):
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
        global stars
        from os import listdir
        import pygame

        from constants import PRICES, STONE_TOWER_CLASSES
        from enemy import Enemy
        from tower import StoneTower, StoneTowerSecondType, Button, StoneTowerThirdType
        import sys
        from constants import WIDTH, HEIGHT, HERO_WIDTH, HERO_HEIGHT, GOBLIN, SCORPION, STONE_TOWERS, \
            OLD_MAN, DELAY, LIVES, STONE_TOWER, STONE_TOWER_IMG, TOWER_WIDTH, TOWER_HEIGHT, \
            WAIT_BETWEEN_WAVES, STONE_IMGS, COINS, LEVELS, NUMBER_OF_LEVELS

        def reset_level(lev):
            nonlocal iteration_number
            nonlocal geroes
            nonlocal selected_tower
            nonlocal wave_number

            geroes.clear()
            bashni.clear()
            iteration_number = 0
            selected_tower = None
            wave_number = 0
            LEVELS[lev].reset()

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

        # Подготовка остального
        plus = None
        WAVES = LEVELS[0].waves
        pygame.init()
        pygame.mixer.music.load(resource_path('fone.wav'))
        geroes = []
        images = {}
        bashni = []
        addStoneTowerButtons = []
        addStoneTowerTowers = []
        TowerPlaces = eval(open_file('TowerPlaces.txt').read())
        level = 0
        number_of_lost = 0
        state = "IN_START_MENU"  # NORMAL, PAUSE, WIN, LOST, IN_START_MENU, IN_CHOOSE_LEVEL_MENU
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

        freeze = 0
        background = load_img('game_background.png')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        font = pygame.font.Font(resource_path('font.ttf'), 60)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)
        isend = False
        page = 0
        iteration_number = 0
        wave_number = 0
        paths = [[tuple(map(int, line.split())) for line in open_file(
            'paths', pathname).read().splitlines()] for pathname in listdir(resource_path('paths'))]
        cnt_stars = 0
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Создание UI
        UI_elements = addStoneTowerButtons
        button_destroy_everyone = Button(pygame.transform.scale(load_img('buttons', 'destroy_everyone.png'), (80, 80)),
                                         WIDTH - 210, 180)
        button_freeze = Button(pygame.transform.scale(load_img('buttons', 'freeze.png'), (80, 80)), WIDTH - 210,
                               180 + 100, FREEZE_COST)
        button_pause = Button(pygame.transform.scale(load_img('buttons', 'pause.png'), (80, 80)), WIDTH - 110,
                              180 + 2 * 100)
        button_pause = Button(pygame.transform.scale(load_img('buttons', 'pause.png'), (80, 80)), WIDTH - 110,
                              180 + 3 * 100)
        button_pause = Button(pygame.transform.scale(load_img('buttons', 'pause.png'), (80, 80)), WIDTH - 110,
                              180 + 3 * 100)

        UI_elements.append(button_pause)
        UI_elements.append(button_destroy_everyone)
        UI_elements.append(button_freeze)
        selected_tower = None
        for hero_name in [GOBLIN, SCORPION, OLD_MAN]:
            images.update(
                {hero_name: [pygame.transform.scale(load_img(hero_name, 'walk', filename), (HERO_WIDTH, HERO_HEIGHT))
                             for filename in listdir(resource_path(hero_name, 'walk'))]})
        button_start = Button(pygame.transform.scale(load_img('buttons', 'start.png'), (400, 400)), 350, 250)
        coin = pygame.transform.scale(load_img('buttons', 'money.png'), (180, 80))
        cerdce = pygame.transform.scale(load_img('buttons', 'lives.png'), (180, 80))
        while True:
            if state == 'PAUSE' or state == 'NORMAL':
                screen.blit(background, (0, 0))
                # -----------О-Б-Н-О-В-Л-Е-Н-И-Е--Э-Л-Е-М-Е-Н-Т-О-В--U-I-----------
                try:
                    button_destroy_everyone.cost = sum([ene.lives for ene in geroes]) // len(geroes) * 2
                    button_destroy_everyone.is_normally = bool(button_destroy_everyone.cost)
                except ZeroDivisionError:
                    button_destroy_everyone.is_normally = False
                button_freeze.is_normally = len(geroes) and (not freeze)

                # ----------------------О-Т-Р-И-С-О-В-К-А--U-I---------------------
                for UI_element in UI_elements:
                    UI_element.draw(screen)
                screen.blit(cerdce, (WIDTH - 190, 4))
                screen.blit(font.render(str(LIVES), True, (180, 0, 0)), (WIDTH - 165, 4))
                screen.blit(coin, (WIDTH - 190, 90))
                screen.blit(font.render(str(COINS), True, (180, 180, 0)), (WIDTH - 165, 90))

                # ------О-Т-Р-И-С-О-В-К-А--О-С-Т-А-Л-Ь-Н-Ы-Х---Э-Л-М-Е-Н-Т-О-В------
                for geroy in geroes:
                    geroy.draw()
                for bas in bashni:
                    bas.draw(screen)
                for button in addStoneTowerButtons:
                    button.draw(screen)
                if state == 'NORMAL':
                    if freeze:
                        freeze -= 1
                    if selected_tower:
                        selected_tower.x, selected_tower.y = pygame.mouse.get_pos()
                        selected_tower.x -= selected_tower.width // 2
                        selected_tower.y -= selected_tower.height // 2
                        selected_tower.draw(screen)
                    # Добавление врагов, обработка выигрыша.
                    iteration_number += 1
                    if isend and len(geroes):
                        iteration_number -= 1
                    elif isend:
                        isend = False
                    try:
                        if iteration_number >= 0 and iteration_number % WAVES[wave_number].wait == 0:
                            try:
                                path, name, speed, lives, fine, reward = WAVES[wave_number].next()
                                geroes.append(
                                    Enemy(images[name], screen, paths[path], name, speed, lives, fine, reward))
                            except StopIteration:
                                wave_number += 1
                                iteration_number = - WAIT_BETWEEN_WAVES
                                isend = True
                    except IndexError:
                        state = 'WIN'
                        cnt_stars = 1
                        if LIVES >= LEVELS[level].onThree:
                            cnt_stars = 3
                        elif LIVES >= LEVELS[level].onTwo:
                            cnt_stars = 2
                        if int(stars[level]) < cnt_stars:
                            plus = LEVELS[level].getCoins[cnt_stars - 1] - (
                                0 if not int(stars[level]) else LEVELS[level].getCoins[int(stars[level]) - 1])
                            stars = stars[:level] + str(max(cnt_stars, int(stars[level]))) + stars[level + 1:]
                        print(int(stars[NUMBER_OF_LEVELS + 1:]))
                        if plus:
                            stars = stars[:NUMBER_OF_LEVELS + 1] + str(
                                int(stars[NUMBER_OF_LEVELS + 1:]) + plus)
                        print(stars.find('X'))
                        if level + 1 == stars.find('X'):
                            stars = stars.replace('X', '0', 1)
                    # Enemy.move
                    if not freeze:
                        for geroy in geroes:
                            if geroy.move():
                                LIVES -= geroy.fine
                                geroes.remove(geroy)
                    # StoneTower.update
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
                    # StoneTower.attack
                    for bas in bashni:
                        for geroy in geroes:
                            x, y = geroy.get_pos(95)
                            bx, by = bas.x + bas.width // 2, bas.y + bas.height // 2
                            if get_distant(x, y, bx, by) <= bas.range and geroy.lives - geroy.now_uron > 0:
                                bas.attack(geroy)
                                break
                    if LIVES <= 0:
                        if number_of_lost >= len(LEVELS[level].ifLost) or int(stars[NUMBER_OF_LEVELS + 1:]) < \
                                LEVELS[level].ifLost[number_of_lost]:
                            state = 'LOST'
                        else:
                            if input(LEVELS[level].ifLost[number_of_lost]) == 'y':
                                print(stars)
                                stars = stars[:NUMBER_OF_LEVELS + 1] + str(
                                    int(stars[NUMBER_OF_LEVELS + 1:]) - LEVELS[level].ifLost[number_of_lost])
                                print(stars)
                                number_of_lost += 1
                                LIVES = 5
                            else:
                                state = 'LOST'
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if selected_tower:
                                if addStoneTower(selected_tower.type):
                                    COINS -= PRICES[selected_tower.type][0]
                                selected_tower = None
                            else:
                                print(pygame.mouse.get_pos())
                        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                            state = 'PAUSE'
                    if button_destroy_everyone.try_push(events) and COINS >= button_destroy_everyone.cost:
                        COINS -= sum([ene.lives for ene in geroes]) // 3
                        geroes.clear()
                    if button_pause.try_push(events):
                        state = 'PAUSE'
                    if button_freeze.try_push(events) and COINS >= FREEZE_COST:
                        freeze = LENGTH_OF_FREEZE
                        COINS -= FREEZE_COST
                    for number in range(3):
                        if addStoneTowerButtons[number].try_push(events, eventTypeRequire=pygame.MOUSEBUTTONDOWN):
                            selected_tower = addStoneTowerTowers[number]
                    for bas in bashni:
                        if pygame.rect.Rect(bas.x, bas.y, bas.width, bas.height + 50).collidepoint(
                                *pygame.mouse.get_pos()):
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
                            state = 'NORMAL'
                        elif e.type == pygame.KEYUP:
                            state = 'NORMAL'
            elif state == 'WIN':
                screen.blit(background, (0, 0))
                table, button_menu, arrow_right, molnya = load_images('win', ['table.png',
                                                                              'button_menu.png', 'arrow_right.png',
                                                                              'zip.png'], 0.70, 0.70)
                screen.blit(table, (340, 80))
                next_level, to_menu = Button(arrow_right, 588, 558), Button(button_menu, 414, 558)
                next_level.draw(screen)
                to_menu.draw(screen)
                stars_imgs = {i: pygame.transform.scale(load_img('level_buttons', f'star{i}.png'), (300, 164)) for i
                              in [0, 1, 2, 3]}
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit()
                screen.blit(stars_imgs[cnt_stars], (406, 210))
                _font1 = pygame.font.Font(resource_path('font.ttf'), 35)
                _font2 = pygame.font.Font(resource_path('font.ttf'), 30)
                _font3 = pygame.font.Font(resource_path('font.ttf'), 70)
                screen.blit(_font1.render('CONGRATULATIONS!', True, (219, 200, 153)), (414, 381))
                screen.blit(_font2.render('LEVEL COMPLETE', True, (219, 200, 153)), (454, 421))
                if plus:
                    screen.blit(_font3.render('+' + str(plus), True, (219, 200, 153)),
                                (458, 462))
                    screen.blit(molnya, (585, 472))
                if to_menu.try_push(events):
                    state = 'IN_CHOOSE_LEVEL_MENU'
                    reset_level(level)
                elif next_level.try_push(events):
                    state = 'NORMAL'
                    reset_level(level)
                    level += 1
                    WAVES = LEVELS[level].waves
                    LIVES = LEVELS[level].lives
                    COINS = LEVELS[level].coins
            elif state == 'LOST':
                screen.blit(background, (0, 0))
                table, button_menu, restart = load_images('failed', ['table.png',
                                                                     'button_menu.png', 'button_restart.png',
                                                                     ], 0.70, 0.70)
                screen.blit(table, (340, 80))
                restart, to_menu = Button(restart, 588, 538), Button(button_menu, 414, 538)
                restart.draw(screen)
                to_menu.draw(screen)
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit()
                _font2 = pygame.font.Font(resource_path('font.ttf'), 35)
                _font1 = pygame.font.Font(resource_path('font.ttf'), 70)
                screen.blit(_font1.render('SORRY :(', True, (219, 200, 153)), (435, 383))
                screen.blit(_font2.render('LEVEL FAILED', True, (219, 200, 153)), (466, 460))
                if to_menu.try_push(events):
                    state = 'IN_CHOOSE_LEVEL_MENU'
                elif restart.try_push(events):
                    state = 'NORMAL'
                    reset_level(level)
                    WAVES = LEVELS[level].waves
                    LIVES = LEVELS[level].lives
                    COINS = LEVELS[level].coins
            elif state == 'IN_START_MENU':
                screen.blit(background, (0, 0))
                font_ = pygame.font.Font(resource_path('font.ttf'), 150)
                screen.blit(font_.render('TOWER DEVENSE', True, (100, 49, 33)), (50, 20))
                button_start.draw(screen)
                events = pygame.event.get()
                for e in events:
                    if e.type == pygame.QUIT:
                        sys.exit()
                if button_start.try_push(events):
                    state = 'IN_CHOOSE_LEVEL_MENU'
            elif state == 'IN_CHOOSE_LEVEL_MENU':
                screen.blit(background, (0, 0))
                table, level_imgs, arrow_left, arrow_right = load_images('level_buttons', ['table.png',
                                                                                           [str(i) + '.png' for i in
                                                                                            range(1, NUMBER_OF_LEVELS +
                                                                                                  1)],
                                                                                           'left.png', 'right.png'],
                                                                         0.90, 0.90)
                screen.blit(table, (140, 30))
                stars_imgs = {str(i): pygame.transform.scale(load_img('level_buttons', f'star{i}.png'), (90, 50)) for i
                              in [0, 1, 2, 3, 'X']}
                level_buttons = [
                    Button(concatSurfaces(level_imgs[i], stars_imgs[stars[i]], (30, 85)), i % 4 * 200 + 190,
                           180 if i // 4 % 2 == 0 else 380, id=i) for i in
                    range(NUMBER_OF_LEVELS)]
                next_button, prev_button = Button(arrow_right, 936, 531), Button(arrow_left, 50, 531)
                # (966, 561)
                # (106, 549)
                for btn in level_buttons[8 * page:8 * page + 8]:
                    btn.draw(screen)
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit()
                if page != 0:
                    if prev_button.try_push(events):
                        page -= 1
                    prev_button.draw(screen)
                elif page != NUMBER_OF_LEVELS // 8 - 1:
                    if next_button.try_push(events):
                        page += 1
                    next_button.draw(screen)
                for btn in level_buttons[8 * page:8 * page + 8]:
                    if btn.try_push(events) and stars[btn.kwargs['id']] != 'X':
                        WAVES = LEVELS[btn.kwargs['id']].waves
                        COINS = LEVELS[btn.kwargs['id']].coins
                        LIVES = LEVELS[btn.kwargs['id']].lives
                        level = btn.kwargs['id']
                        state = 'NORMAL'
            pygame.time.delay(DELAY)
            pygame.display.flip()


    if __name__ == '__main__':
        main()
except SystemExit:
    v = open(resource_path('history.txt'), 'w')
    v.write(stars)
    v.close()
    print('done')

except Exception as error:
    v = open(resource_path('history.txt'), 'w')
    v.write(stars)
    v.close()
    print('done')
    from tkinter.messagebox import showerror

    showerror('Error:', str(error.__class__) + str(error.args))
    raise error
