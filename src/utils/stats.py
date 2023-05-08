tower_types = {"arrow": {"damage": 20,
                         "range": 130, 
                         "attack_speed": 800, 
                         "size": (75, 75),
                         "cost": 70 },
               "wizard": {"damage": 20, 
                          "range": 90, 
                          "attack_speed": 1200,
                          "size": (70, 70),
                          "cost": 250},
               "poison": {"damage": 20, 
                          "range": 130, 
                          "attack_speed": 1000, 
                          "size": (70, 70),
                          "cost": 150}}

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
                    "poison": {"damage": 5, 
                               "effect": 
                                    {"area": 0,
                                     "slow": 50, 
                                     "dot": 0, 
                                     "duration": 600}}}

monster_types = {"normal": {"damage": 2,
                            "movement_speed": 1, 
                            "movement_interval": 10, 
                            "hitpoints": 20 },
                 "fast":   {"damage": 2, 
                            "movement_speed": 1,
                            "movement_interval": 10, 
                            "hitpoints": 20 },
                 "big":    {"damage": 2, 
                            "movement_speed": 1,
                            "movement_interval": 30, 
                            "hitpoints": 20 }}
