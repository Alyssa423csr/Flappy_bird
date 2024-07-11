import pygame as pg
from config import *
from helper import image_loader

from base import Base
from bird import Bird
from pipe import Pipes
from scoreboard import Scoreboard


class Game:
    """
    遊戲控制物件

    Attributes:
        screen (pg.Surface): 視窗物件
        background_image (pg.Surface): 背景圖片物件
    Methods:
        run(): 開始遊戲(進入遊戲迴圈)
    """

    def __init__(self, surface: pg.surface):
        """
        初始化函式

        Args:
            surface (pg.surface): 視窗物件
        """
        self.screen = surface
        self.background_image = image_loader(
            BACKGROUND_IMG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    # TODO7 讓遊戲流程更豐富
    # TODO7-1 讓遊戲開始前有點擊畫面，結束時有結束畫面，以及案右上角可以暫停再按一次則繼續
    def run(self):
        clock = pg.time.Clock() # 創建遊戲時鐘物件
        running = True
        paused = False  # 初始狀態下遊戲不暫停
        base = pg.sprite.GroupSingle(Base()) # 創建地面物件
        bird = pg.sprite.GroupSingle(Bird((SCREEN_WIDTH / 10, HEIGHT_LIMIT / 2)))
        pipes = Pipes()
        scoreboard = Scoreboard() # 創建計分板物件
        
        game_started = False # 初始遊戲狀態為未開始  

        # 顯示開始畫面提示
        self.show_start_screen()

        # game loop
        
        # TODO6-1
        current_pipes_counter = 0

        while running:
            clock.tick(FPS) # 控制遊戲迴圈的速度，以每秒幀數為基準

            for event in pg.event.get(): # 遍歷事件列表
                if event.type == pg.QUIT:  # 如果事件為視窗關閉
                    running = False # 遊戲運行標誌為 False，退出遊戲

                elif event.type == pg.MOUSEBUTTONDOWN:  # 玩家點擊
                    if not game_started:  # 如果遊戲還未開始
                        game_started = True  # 開始遊戲

                    elif self.is_mouse_in_pause_area(event.pos):  # 點擊位置在暫停區域
                        paused = not paused  # 切換暫停狀態
                        pause_changed = True  # 暫停狀態改變

            
            if not game_started:  # 如果遊戲還未開始，不執行遊戲
                continue
            
            if paused:
                # 在暫停狀態下只顯示暫停畫面
                if pause_changed:
                    self.show_pause_screen()
                    pause_changed = False
               
            else:
                base.update()
                bird.update()
                pipes.update()
                
                # TODO6-2
                ##scoreboard.update()
                if pipes.pipes_counter > current_pipes_counter :
                    current_pipes_counter = pipes.pipes_counter
                    scoreboard.update()
            
            '''
            # 更新遊戲
            base.update()
            bird.update()
            pipes.update()
            scoreboard.update()
            '''
            ## 遊戲結束與否
            ### 碰撞發生
            if pg.sprite.groupcollide(bird, pipes.pipes, False, False):
                running = False

            # 畫背景、物件
            self.screen.blit(self.background_image, (0, 0))
            bird.draw(self.screen)
            pipes.draw(self.screen)
            base.draw(self.screen)
            scoreboard.draw(self.screen)
            
            self.draw_pause_indicator(paused)
            
            if paused:  # 如果暫停，則在螢幕中間顯示 "Continue"
                self.show_continue_screen()
            
            pg.display.update()

        self.show_end_screen()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return

    def show_start_screen(self):
        # 清除背景
        self.screen.fill((0, 0, 0))
        
        # 開始提示文字
        font = pg.font.Font(None, 50)  # 創建字體物件，None 表示使用默認字體；而 36 則是字體的大小，表示字體大小為 36 像素。
        text = font.render("Click to Start", True, (255,240,245	))  #將文字顯示在畫面上
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) # 取得文字圖像的矩形區域，並將其置中於視窗的中心位置
        self.screen.blit(text, text_rect) # 在畫面上繪製文字圖像
        
        # 更新畫面
        pg.display.flip() # 更新整個畫面以顯示文字


    def show_end_screen(self):
    # 清除背景
        self.screen.fill((0, 0, 0))
        
        # 結束提示文字
        font = pg.font.Font(None, 50)  
        text = font.render("Game Over", True, (255,240,245)) # 將文字 "Game Over" 渲染為圖像
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) # 取得文字圖像的矩形區域，並將其置中於視窗的中心位置
        self.screen.blit(text, text_rect) # 在畫面上繪製文字圖像

        # 提示重新開始
        font = pg.font.Font(None, 30)
        restart_text = font.render("Right-click to restart", True, (255, 240, 245)) # 提示改為右鍵重新開始
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        # 更新畫面
        pg.display.flip()

        # 等待玩家按滑鼠右鍵
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:  # 按下滑鼠右鍵
                    waiting = False

        # 重新開始遊戲
        self.run()



    def draw_pause_indicator(self, paused):
        # 在右上角繪製暫停指示
        indicator_text = "Pause" if not paused else "CONTINUE"
        font = pg.font.Font(None, 30)
        text = font.render(indicator_text, True, (0, 0, 0))  #黑色字體
        text_rect = text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(text, text_rect)

    def is_mouse_in_pause_area(self, pos):
        # 檢查滑鼠點擊是否在暫停區域內
        pause_button_rect = pg.Rect(SCREEN_WIDTH - 70, 10, 60, 30)  # 暫停按鈕的位置和大小
        return pause_button_rect.collidepoint(pos)

    def show_pause_screen(self):
        # 顯示暫停畫面
        self.screen.fill((0, 0, 0))
        font = pg.font.Font(None, 36)
        text = font.render("Paused", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)
        pg.display.flip()

    def show_continue_screen(self):
        # 顯示繼續遊戲提示
        font = pg.font.Font(None, 24)
        text = font.render("Click to Continue", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
        self.screen.blit(text, text_rect)