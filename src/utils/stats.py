tower_types = {"arrow": {"damage": 20,
                         "range": 130, 
                         "attack_speed": 1000, 
                         "size": (75, 75),
                         "cost": 70 ,
                         "sell_value": 40},
               "wizard": {"damage": 20, 
                          "range": 90, 
                          "attack_speed": 1200,
                          "size": (70, 70),
                          "cost": 400,
                          "sell_value": 40},
               "poison": {"damage": 20, 
                          "range": 130, 
                          "attack_speed": 1000, 
                          "size": (70, 70),
                          "cost": 150,
                          "sell_value": 100}}

projectile_types = {"arrow": {"damage": 15,
                              "effect":
                                    {"area": 0,
                                     "slow": 0, 
                                     "dot": 0, 
                                     "duration": 0}},
                    "wizard": {"damage": 10, 
                               "effect": 
                                    {"area": 50,
                                     "slow": 0, 
                                     "dot": 0, 
                                     "duration": 0}},
                    "poison": {"damage": 2, 
                               "effect": 
                                    {"area": 0,
                                     "slow": 50, 
                                     "dot": 0, 
                                     "duration": 600}}}

monster_types = {"normal": {"damage": 2,
                            "movement_speed": 1, 
                            "movement_interval": 10, 
                            "hitpoints": 20,
                            "gold_reward": 5 },
                 "fast":   {"damage": 2, 
                            "movement_speed": 2,
                            "movement_interval": 5, 
                            "hitpoints": 20,
                            "gold_reward": 10 },
                 "big":    {"damage": 2, 
                            "movement_speed": 1,
                            "movement_interval": 30, 
                            "hitpoints": 20,
                            "gold_reward": 50 }}

waves = [
            {'normal': 3, 'fast':0, 'big':0, 'frequency': 500},
            {'normal': 5, 'fast':0, 'big':0, 'frequency': 500},
            {'normal': 10, 'fast':2, 'big':0, 'frequency': 500},
            {'normal': 12, 'fast':2, 'big':0, 'frequency': 500},
            {'normal': 15, 'fast':2, 'big':0, 'frequency': 500},
            {'normal': 25, 'fast':4, 'big':0, 'frequency': 500},
            {'normal': 0, 'fast':10, 'big':0, 'frequency': 500},
            {'normal': 30, 'fast':4, 'big':0, 'frequency': 400},
            {'normal': 35, 'fast':6, 'big':0, 'frequency': 400},
            {'normal': 50, 'fast':10, 'big':0, 'frequency': 400},
            {'normal': 60, 'fast':15, 'big':0, 'frequency': 400},
            {'normal': 80, 'fast':20, 'big':0, 'frequency': 400},
        ]
