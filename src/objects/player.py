class Player():
    def __init__(self, player_life, player_gold):
        self.life_total = player_life
        self.gold = player_gold

    def buy(self, amount):
        if self.gold - amount >= 0:
            print("used gold", amount)
            self.gold -= amount
            return True
        return False
    
    def increase_gold(self, amount):
        self.gold += amount

    def damage_player(self, damage):
        self.life_total -= damage
        print("player took damage, current life:", self.life_total)
        if self.life_total < 0:
            print("dead")

    def current_health(self):
        return self.life_total

    def current_gold(self):
        return self.gold
    
    def is_alive(self):
        if self.life_total > 0:
            return  True
        return False
    