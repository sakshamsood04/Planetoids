"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

# Harshvardhan Maskara (hm475) and Sia Chitnis (sc2665)
# 08-Dec-2022
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the ship attribute of this class.

        The ship attribute is an instance of the Ship class.
        """
        return self._ship

    def getLives(self):
        """
        Returns the number of lives left of the ship.

        The value lives is an int >=0 and <=3
        """
        return self._lives
    
    def getAstLen(self):
        """
        Return the length of the asteroids attribute of this class.

        The length is an int>=0
        """
        return len(self._asteroids)

    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self, data):
        """
        Initializes a wave object from the given data. 

        Parameter data: the dictionary defining the wave
        Precondition: data is a JSON file
        """
        self._lives=3
        self._data=data
        ship=self._data["ship"]
        position=ship["position"]
        angle=ship["angle"]
        self._ship=Ship(position, angle)
        self._asteroids=[]
        asteroids_list=self._data["asteroids"]
        for asteroid in asteroids_list:
            size=asteroid["size"]
            pos=asteroid["position"]
            dir=asteroid["direction"]
            self._asteroids.append(Asteroid(size, pos, dir))
        self._bullets=[]
        self._firerate=0
        
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, input):
        """
        Animates a single frame in the game.

        Parameter input: the user input
        Precondition: input is an instance of GInput
        """
        if self._ship!=None:
            self._firerate+=1
            if input.is_key_down('left'):
                self._ship.turn(True)
            if input.is_key_down('right'):
                self._ship.turn(False)
            if input.is_key_down('up'):
                self._ship.velocity()
            self._ship.move()
            for asteroid in self._asteroids:
                asteroid.move()
            if input.is_key_down('spacebar'):
                if self._firerate>=BULLET_RATE:
                    self._bullets.append(Bullet(self._ship.getFacing(),\
                    self._ship.getPosition()))
                    self._firerate=0
            for bullet in self._bullets:
                bullet.move()
            self._deleteBullet()
            self._detectBulletCollision()
            self._detectShipCollision()
        
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self, view):
        """
        Draws the game objects to the view.

        Parameter view: the game view
        Precondition: view is an instance of GView
        """
        self._ship.draw(view)
        for asteroid in self._asteroids:
            asteroid.draw(view)
        for bullet in self._bullets:
            bullet.draw(view)

    # RESET METHOD FOR CREATING A NEW LIFE
    def reset(self):
        """
        Assigns the ship attribute to a new instance of the Ship class
        with the original features. 
        """
        ship=self._data["ship"]
        position=ship["position"]
        angle=ship["angle"]
        self._ship=Ship(position, angle)

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def _deleteBullet(self):
        """
        Checks if the bullet is to be deleted. If it does, then it modifies 
        the list attribute _bullets by deleting the particular element.
        """
        i=0
        while i<len(self._bullets):
            if self._bullets[i].isDelete(): 
                del self._bullets[i]
            else:
                i+=1
    
    def _detectBulletCollision(self):
        """
        Checks if the bullet has collided with an asteroid and modifies the 
        list attribute _asteroids. 

        If there is a collision then it deletes the bullet and the asteroid which collided.
        If the asteroid was sized medium, then three new small asteroids are created,
        whereas, if the asteroid was sized large, three new medium asteroids are created.
        """
        i=0
        while i<(len(self._bullets)):
            j=0
            while j<(len(self._asteroids)):
                distance=math.dist([self._bullets[i].x,self._bullets[i].y],\
                [self._asteroids[j].x,self._asteroids[j].y])
                if distance<=(self._asteroids[j].getRadius()+BULLET_RADIUS):
                    temp=self._bullets[i]
                    del self._bullets[i]
                    if self._asteroids[j].getSize()==SMALL_ASTEROID:
                        del self._asteroids[j]
                        break
                    elif self._asteroids[j].getSize()==MEDIUM_ASTEROID:
                        old_center=(self._asteroids[j].x,self._asteroids[j].y)
                        del self._asteroids[j]
                        pos=self._bulletCollisionVector(temp)
                        new_center=self._newCenter(old_center, pos, SMALL_RADIUS)
                        self._insert(j, SMALL_ASTEROID, new_center, pos)
                        break
                    else:
                        old_center=(self._asteroids[j].x,self._asteroids[j].y)
                        del self._asteroids[j]
                        pos=self._bulletCollisionVector(temp)
                        new_center=self._newCenter(old_center, pos, MEDIUM_RADIUS)
                        self._insert(j, MEDIUM_ASTEROID, new_center, pos)
                        break
                j+=1
            i+=1

    def _detectShipCollision(self):
        """
        Checks if the ship has collided with an asteroid and modifies the 
        list attribute _asteroids. 

        If there is a collision then it reduces the lives attribute by 1,
        sets the ship to None and deletes the asteroid with which the ship collided.
        If the asteroid was sized medium, then three new small asteroids are created,
        whereas, if the asteroid was sized large, three new medium asteroids are created.
        """
        i=0
        while i<len(self._asteroids):
            distance=math.dist([self._ship.x,self._ship.y],\
            [self._asteroids[i].x,self._asteroids[i].y])
            if distance<=(self._asteroids[i].getRadius()+SHIP_RADIUS):
                temp=self._ship
                self._lives-=1
                self._ship=None
                if self._asteroids[i].getSize()==SMALL_ASTEROID:
                    del self._asteroids[i]
                    break
                elif self._asteroids[i].getSize()==MEDIUM_ASTEROID:
                    old_center=(self._asteroids[i].x,self._asteroids[i].y)
                    del self._asteroids[i]
                    pos=self._shipCollisionVector(temp)
                    new_center=self._newCenter(old_center, pos, SMALL_RADIUS)
                    self._insert(i, SMALL_ASTEROID, new_center, pos)
                    break
                else:
                    old_center=(self._asteroids[i].x,self._asteroids[i].y)
                    del self._asteroids[i]
                    pos=self._shipCollisionVector(temp)
                    new_center=self._newCenter(old_center, pos, MEDIUM_RADIUS)
                    self._insert(i, MEDIUM_ASTEROID, new_center, pos)
                    break
            i+=1

    def _bulletCollisionVector(self, bullet):
        """
        Returns a tuple of Vector2 objects which represent the resultant vectors
        of the new asteroids created after the collision with the bullet.

        Parameter bullet: the element of the _bullets attribute which collided
        with the asteroid.
        Precondition: bullet is an instance of the Bullet class.
        """
        col_vec=bullet.getVelocity().normalize()
        result1=col_vec
        result2_x=(col_vec.x*math.cos(degToRad(120)))-(col_vec.y*math.sin(degToRad(120)))
        result2_y=(col_vec.x*math.sin(degToRad(120)))+(col_vec.y*math.cos(degToRad(120)))
        result2=introcs.Vector2(result2_x,result2_y)
        result2=result2.normalize()
        result3_x=(col_vec.x*math.cos(degToRad(240)))-(col_vec.y*math.sin(degToRad(240)))
        result3_y=(col_vec.x*math.sin(degToRad(240)))+(col_vec.y*math.cos(degToRad(240)))
        result3=introcs.Vector2(result3_x,result3_y)
        result3=result3.normalize()
        return (result1, result2, result3)
    
    def _shipCollisionVector(self, ship):
        """
        Returns a tuple of Vector2 objects which represent the resultant vectors
        of the new asteroids created after the collision with the ship.

        Parameter ship: the _ship attribute at the moment of the collision.
        Preconditio: ship is an instance of the Ship class.
        """
        if ship.getVelocity().length()==0:
            col_vec=ship.getFacing()
        else:
            col_vec=ship.getVelocity()
        result1=col_vec
        result2_x=(col_vec.x*math.cos(degToRad(120)))-(col_vec.y*math.sin(degToRad(120)))
        result2_y=(col_vec.x*math.sin(degToRad(120)))+(col_vec.y*math.cos(degToRad(120)))
        result2=introcs.Vector2(result2_x,result2_y)
        result2=result2.normalize()
        result3_x=(col_vec.x*math.cos(degToRad(240)))-(col_vec.y*math.sin(degToRad(240)))
        result3_y=(col_vec.x*math.sin(degToRad(240)))+(col_vec.y*math.cos(degToRad(240)))
        result3=introcs.Vector2(result3_x,result3_y)
        result3=result3.normalize()
        return (result1, result2, result3)

    def _newCenter(self, old, pos, radius):
        """
        Returns a tuple containing the centers of the three new asteroids 
        to be created. 

        Parameter old: the original center of the Asteroid
        Precondition: old is a tuple 

        Parameter pos: the direction of the Asteroid being inserted
        Precondition: pos is a tuple of Vector2 objects

        Parameter radius: the radius of the new Asteroid
        Precondition: radius is an int
        """
        new_center1=((pos[0].x*radius)+old[0],(pos[0].y*radius)+old[1])
        new_center2=((pos[1].x*radius)+old[0],(pos[1].y*radius)+old[1])
        new_center3=((pos[2].x*radius)+old[0],(pos[2].y*radius)+old[1])
        return (new_center1, new_center2, new_center3)

    def _insert(self, index, size, new, pos):
        """
        Modifies the list attribute _asteroids by inserting three new 
        instances of the Asteroid class.

        Parameter index: index to insert at
        Precondition: index is an int

        Parameter size: size of the Asteroid being inserted
        Precondition: size is a string

        Parameter new: the position of the Asteroid being inserted
        Precondition: new is a tuple of tuples

        Parameter pos: the direction of the Asteroid being inserted
        Precondition: pos is a tuple of Vector2 objects
        """
        self._asteroids.insert(index,Asteroid(size, new[0], [pos[0].x,pos[0].y]))
        self._asteroids.insert(index+1,Asteroid(size, new[1], [pos[1].x,pos[1].y]))
        self._asteroids.insert(index+2,Asteroid(size, new[2], [pos[2].x,pos[2].y]))