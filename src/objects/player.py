import pygame

class Player():
    def __init__(self):
        self.gold = 200
        self.life_total = 20
    
    def use_gold(self, amount):
        if self.gold - amount >= 0:
            print("used gold", amount)
            self.gold -= amount
        else:
            print("not enough gold")


