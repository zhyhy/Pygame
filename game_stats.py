class GameStas():
    ''' 跟踪游戏的统计信息 '''
    def __init__(self,ai_seetings):
        ''' 初始化统计信息 '''
        self.ai_seetings = ai_seetings
        self.reset_stats()
        # 游戏刚启动时处于活动状态
        self.game_active = False
        self.high_score = 0


    def reset_stats(self):
        ''' 初始化在有序运行期间可能变化的统计信息 '''
        self.ship_left = self.ai_seetings.ship_limit
        self.score = 0
        self.level = 1

