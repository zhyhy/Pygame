import sys
import pygame
from Settings import  Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
import game_functions as gf
from button import Button
from game_stats import GameStas
from scoreboard import Scoreboard
def run_game():

    pygame.init()       # 初始化背景设置
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    stats = GameStas(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    pygame.display.set_caption("Ailen Invasion")
    # 创建按钮
    play_button = Button(ai_settings,screen,'play')
    # 创建一个用于存储子弹的编组
    bullets = Group()

    aliens = Group()
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建外星人群
    gf.creat_fleet(ai_settings, screen, ship, aliens)



    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,bullets,aliens,stats,sb)
            gf.update_alien(ai_settings, stats, screen, bullets, aliens,ship,sb)
        gf.update_screec(ai_settings, screen, ship, aliens, bullets,play_button, stats,sb)

run_game()