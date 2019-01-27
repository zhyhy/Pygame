class Settings():
    '''存储《外星人入侵》的所有设置的类 '''
    def __init__(self):
        ''' 初始化游戏的设置 '''
    # 计分
        self.alien_point = 50
        self.score_scale = 1.5
    # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

    # 子弹设置
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3
    # 外星人设置
    # fleet_drop_speed指的是有外星人撞到屏幕的边缘时，外星人群向下移动的速度
        self.fleet_drop_speed = 30
    # 飞船设置
        self.ship_limit = 5
    # 设置最高得分
        self.high_score = 0

    # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1

    def increase_speed(self):
        ''' 提高游戏速度 '''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.score_scale)





        

