import pygame as pg
from number import Number

# TODO6 完成記分板物件
"""
記分板物件需至少支援三個方法
1. __init__(): constructor, 用來建構一個記分板物件實體
2. update(): 用來作為遊戲迴圈中每次更新呼叫的更新函式, 更新記分板物件中的邏輯部分(分數部分)
3. draw(screen): 遊戲迴圈更新後將記分板畫到視窗中的函式
"""

"""
hint: 可以利用實作好的Number物件幫忙
"""

# TODO6-3
from config import *

class Scoreboard:
    def __init__(self):
        self.score = Number((SCREEN_WIDTH/2, SCREEN_HEIGHT/8), -1)

    def update(self):
          new_score = (int(self.score.number) + 1) % 10
          self.score.update(new_score)

    def draw(self, screen: pg.Surface):
        self.score.draw(screen)

