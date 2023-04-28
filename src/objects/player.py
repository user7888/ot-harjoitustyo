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

    def damage_player(self, damage):
        self.life_total -= damage
        print("player took damage, current life:", self.life_total)
        if self.life_total < 0:
            print("dead")


