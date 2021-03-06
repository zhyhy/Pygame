import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_event(event, ai_settings, screen, ship, bullets):
    ''' 按响应键 '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 创建一颗子弹，并将其加入到编组bullets中
        if len(bullets) < ai_settings.bullet_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    ''' 按响应键 '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def ship_hit(ai_seetings, stats, screen, ship, aliens, bullets,sb):
    ''' 响应外星人碰撞到飞船 '''
    if stats.ship_left > 0:

        # 将ship_left 减1
        stats.ship_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        creat_fleet(ai_seetings,screen,ship,aliens)
        ship.center_ship()

        #更新计分牌
        sb.prep_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_events(ai_settings, screen, ship, bullets,stats,play_button,alien,sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y,alien,bullets,ai_settings,ship,screen,sb)

def check_play_button(stats, play_button, mouse_x, mouse_y,alien,bullets,ai_settings,ship,screen, sb):

    ''' 让玩家单击play按钮时开始新游戏 '''
    button_cliked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_cliked and not stats.game_active:
        # 重置游戏速度
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 清空外星人列表和子弹
        alien.empty()
        bullets.empty()
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        # 创建一批新的外星人，并让其居中
        creat_fleet(ai_settings,screen, ship, alien)
        ship.center_ship()



def update_alien(ai_seetings, satas, screen, bullets, aliens,ship,sb):
    ''' 更新外星人群中所外星人的位置 '''
    check_fleet_edges(ai_seetings,aliens)
    aliens.update()
    # 检查飞船和外星人是否碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
       ship_hit(ai_seetings, satas, screen, ship, aliens, bullets,sb)
    # 检查是否有外星人到达屏幕底部
    check_aliens_bottom(ai_seetings, satas, screen, ship, aliens, bullets,sb)

def update_bullets(ai_seetings, screen, ship, bullets, aliens,stats,sb):
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中了外星人，如果击中了，就删除对应的子弹和外星人
    check_bullet_alien_collisions(ai_seetings, screen, ship, aliens, bullets,stats,sb)

def check_bullet_alien_collisions(ai_seetings, screen, ship, aliens, bullets,stats,sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_seetings.alien_point * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人,同时加快游戏节奏，并创建一群新的外星人
        bullets.empty()
        ai_seetings.increase_speed()
        creat_fleet(ai_seetings, screen, ship, aliens)
        # 提高等级
        stats.level += 1
        sb.prep_level()


def update_screec(ai_settings, screen, ship, aline, bullets,play_button,stats,sb):
    # 每次循环的时候都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重修绘制所以子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aline.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def get_number_alien_x(ai_settings, alien_width):
    # 求一行可以容纳多少个外星人
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
def ger_number_rows(ai_settings,ship_height, alien_height):
    # 求可以容纳多少行外星人
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height

    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows



def creat_alien(ai_settings, screen, aliens, alien_number,row_number):
    # 创建一个外星人并将其加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def creat_fleet(ai_settings, screen,ship, aliens):
    ''' 创建外星人群 '''
    # 创建一个挖信任，并计算一行可以容纳多少外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_aliens_rows = ger_number_rows(ai_settings,ship.rect.height, alien.rect.height)
    # 创建一行外星人
    for row_number in range(number_aliens_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number,row_number)


def check_fleet_edges(ai_seetings, aliens):
    ''' 如果有外星人到大边缘 '''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_seetings,aliens)
            break

def change_fleet_direction(ai_seetings, aliens):
    ''' 将郑群外星人下移，并且改变他们的方向  '''
    for alien in aliens.sprites():
        alien.rect.y += ai_seetings.fleet_drop_speed
    ai_seetings.fleet_direction *= -1

def check_aliens_bottom(ai_seetings, stats,screen, ship, aliens, bullets,sb):
    ''' 检查是否有外星人到达屏幕底部，响应和有外星人撞到飞船一样 '''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_seetings,stats,screen,ship,aliens,bullets,sb)
            break



def check_high_score(stats, sb):
    ''' 检查是否诞生了新的最高分 '''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
