import  pygame
from pygame.sprite import Sprite

class Ship():

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞船图像并且获取其外界矩阵
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.moving_right = False
        self.moving_left = False

        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 将飞船的属性centerx中存储小数值
        self.center = float(self.rect.centerx)

    def blitme(self):
        ''' 在指定位置绘制飞船 '''   
        self.screen.blit(self.image, self.rect)
    def update(self):
        ''' 根据移动标识调整飞船的位置 '''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def center_ship(self):
        ''' 让飞船在屏幕上居中 '''
        self.center = self.screen_rect.centerx