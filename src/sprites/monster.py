import os
import pygame
from utils.stats import monster_types

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class
class Monster(pygame.sprite.Sprite):
    """A Class for the Monster Sprite of the game. Functionality
    for the movement of monsters, damaging the player, and updating
    the status of a monster (used for a slow effect) is located in 
    this class.

    Attributes:
        type: Type of this monster (normal, fast, big)
        x_coordinate: x coordinates for the sprite.
        y_coordinate: y coordinates for the sprite.
    """
    def __init__(self, monster_type, x_coordinate=0, y_coordinate=0):
        """ Class constructor for creating a new Monster Sprite. Monster
        type is given as a parameter and used to define the attributes
        of this monster. All attributes are located in utils.stats.

        Args:
            type: Type of this monster (normal, fast, big)
            x_coordinate: x coordinate for the sprite.
            y_coordinate: y coordinate for the sprite.
        """
        super().__init__()
        self.monster_types = monster_types
        self.stats = {"damage": self.monster_types[monster_type]["damage"],
                      "movement_speed": self.monster_types[monster_type]["movement_speed"], 
                      "movement_interval": self.monster_types[monster_type]["movement_interval"], 
                      "hitpoints": self.monster_types[monster_type]["hitpoints"],
                      "gold_reward": self.monster_types[monster_type]["gold_reward"]}
        self.type = monster_type
        self.status_effect_time = (0, 0)
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", f'monster_{self.type}.png')
        )
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate
        self.center = ((self.rect.left+self.rect.right)/2,
                       (self.rect.top+self.rect.bottom)/2 )
        # Movement
        self.set_destination_reached_x = False
        self.set_destination_reached_y = False
        self.current_waypoint = 1
        self.current_destination = (0, 0)
        self.neg_y = False
        self.neg_x = False

        self.time_of_previous_move = 0
    
    def move(self, current_time):
        """ This function is used for moving the monster sprites
        by calling it from the GameMap. Monsters are moved incrementally
        at the speed of their 'movement_speed' stat. 
        
        Movement is based on waypoints. When a monster reaches its current 
        waypoint, a second waypoint is set and the monster begins to move towards it. 

        Args:
            current_time: Used for keeping track of when this monster was last moved.
        """
        self._check_destination_reached()
        self.time_of_previous_move = current_time
        negative_x = False
        negative_y = False

        if self.current_destination[0] < self.rect.x:
            negative_x = True
        if self.current_destination[1] < self.rect.y:
            negative_y = True

        if abs(self.rect.x - self.current_destination[0]) > 0:
            if not negative_x:
                self.rect.x += self.stats['movement_speed']
            else:
                self.rect.x -= self.stats['movement_speed']

        if abs(self.rect.y - self.current_destination[1]) > 0:
            if not negative_y:
                self.rect.y += self.stats['movement_speed']
            else:
                self.rect.y -= self.stats['movement_speed']

    def _check_destination_reached(self):
        """ Used in the movement functionality to check if a monster has reached
        its destination. 
        """
        waypoints = {1: (6, 510),
                     2: (190, 510),
                     3: (196, 60),
                     4: (700, 60),
                     5: (700, 190),
                     6: (320, 190),
                     7: (320, 510),
                     8: (450, 510),
                     9: (450, 380),
                     10: (570, 380),
                     11: (570, 500),
                     12: (700, 500)}
        self.current_destination = waypoints[self.current_waypoint]


        if not self.neg_x and self.rect.x >= waypoints[self.current_waypoint][0]:
            self.set_destination_reached_x = True
        elif self.neg_x and self.rect.x <= waypoints[self.current_waypoint][0]:
            self.set_destination_reached_x = True

        if not self.neg_y and self.rect.y >= waypoints[self.current_waypoint][1]:
            self.set_destination_reached_y = True
        elif self.neg_y and self.rect.y <= waypoints[self.current_waypoint][1]:
            self.set_destination_reached_y = True

        if self.set_destination_reached_x is True and self.set_destination_reached_y is True:
            self._update_destination(waypoints)

    def _update_destination(self, waypoints):
        """ This function is used to update the destination of a monster.

        Args:
            waypoints: Waypoints of the monster movement path.
        """
        if self.set_destination_reached_x is True and self.set_destination_reached_y is True:
            if self.current_waypoint <= 11:
                self.current_waypoint += 1

            self.set_destination_reached_x = False
            self.set_destination_reached_y = False
            self.current_destination = waypoints[self.current_waypoint]

            if self.current_destination[0] < self.rect.x:
                self.neg_x = True
            else:
                self.neg_x = False

            if self.current_destination[1] < self.rect.y:
                self.neg_y = True
            else:
                self.neg_y = False

    def damage(self, damage, effect, current_time, player):
        """ This function is called when a tower projectile hits a monster
        and is used to lower its hitpoints. Monster is deleted when it's
        hitpoints reach 0. This function also checks if the
        projectile should apply a status effect (slow).

        Args:
            damage: Damage dealt by the projectile.
            effect: Effect of the projectile.
            current_time: Used for duration of the effect.
            player: Player object.
        """
        self.stats["hitpoints"] -= damage
        if effect["duration"] > 0:
            self.stats['movement_interval'] = effect['slow']
            self.status_effect_time = (current_time, effect["duration"])

        if self.stats["hitpoints"] <= 0:
            player.increase_gold(self.stats["gold_reward"])
            self.delete()

    def update_status(self, current_time):
        """ A function for updating the status of a monster. If enough
        time has passed since the application of the status effect (slow), 
        monster movement is restored back to normal.
    
        Args:
            current_time: Used for duration of the effect.
        """
        if current_time - self.status_effect_time[0] >= self.status_effect_time[1]:
            self.stats['movement_interval'] = self.monster_types[self.type]['movement_interval']

    def current_location(self):
        """ This function returns the coordinates of a monster.

        Returns:
            tuple: A tuple with x and y coordinates.
        """
        return (self.rect.x, self.rect.y)

    def delete(self):
        """ A function for deleting a monster when it comes in contact with
        the Hearth sprite or when it's hitpoints reach 0.
        """
        self.kill()

    def should_move(self, current_time):
        """ This function uses current time to check if a monster should
        move, based on "movement_interval" stat of the monster. Movement
        interval was added to the movement system mainly for the Poison towers,
        as it makes movement speeds lesser than 1 pixel per cycle of game loop
        easier to implement.

        Args:
            current_time: Current game time.

        Returns:
            True, if enough time has passed. Else value False is returned.
        """
        return current_time - self.time_of_previous_move >= self.stats["movement_interval"]
    