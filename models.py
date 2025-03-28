"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

# Harshvardhan Maskara (hm475) and Sia Chitnis (sc2665)
# 08-Dec-2022
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180
# END REMOVE


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: the velocity vector of the Bullet object
    # Invariant: _velocity is a Vector2 object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns the velocity of a Bullet object. 

        The velocity is a Vector2 object.
        """
        return self._velocity
    
    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, facing, pos):
        """
        Initializes a Bullet object.
        
        Parameter facing: the facing attribute of the ship
        Precondition: facing is a Vector2 object

        Parameter pos: the position of the ship
        Precondition: pos is a tuple with the x and y attribute of the ship
        """
        tip_x=(facing.x*SHIP_RADIUS)+pos[0]
        tip_y=(facing.y*SHIP_RADIUS)+pos[1]
        super().__init__(x=tip_x, y=tip_y)
        self.fillcolor=BULLET_COLOR
        self.width=BULLET_RADIUS*2
        self.height=BULLET_RADIUS*2
        self._velocity=introcs.Vector2(facing.x*BULLET_SPEED,facing.y*BULLET_SPEED)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def move(self):
        """
        Modifies the x and y attributes of the bullet based on its velocity.
        """
        self.x+=self._velocity.x
        self.y+=self._velocity.y
    
    def isDelete(self):
        """
        Returns True if the bullet has passed the boundaries of the game.
        Returns False otherwise. 
        """
        if self.x>GAME_WIDTH+BULLET_RADIUS or self.x<-BULLET_RADIUS:
            return True
        if self.y>GAME_HEIGHT+BULLET_RADIUS or self.y<-BULLET_RADIUS:
            return True
        return False


class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vecotr (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: the velocity vector of the Ship object
    # Invariant: _velocity is a Vector2 object
    #
    # Attribute _facing: the facing vector of the Ship object
    # Invariant: _facing is a Vector2 object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns the velocity of a Ship object. 

        The velocity is a Vector2 object.
        """
        return self._velocity

    def getFacing(self):
        """
        Returns the facing of a Ship object. 

        The facing is a Vector2 object.
        """
        return self._facing
    
    def getPosition(self):
        """
        Return the position of a Ship object as a tuple.

        The tuple contains the x atrribute and the y attribute.
        """
        return (self.x,self.y)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, pos, ang):
        """
        Initializes a Ship object.

        Parameter pos: the position of the ship
        Precondition: pos is a list with two values

        Parameter ang: the angle of the ship
        Precondition: ang is an int
        """
        super().__init__(angle=ang, x=pos[0], y=pos[1], source=SHIP_IMAGE)
        self.width=SHIP_RADIUS*2
        self.height=SHIP_RADIUS*2        
        self._velocity=introcs.Vector2(0.0,0.0)
        self._facing=introcs.Vector2(math.cos(degToRad(ang)),math.sin(degToRad(ang)))
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self, dir):
        """
        Modifies the angle by the ship's turn rate and updates its facing.

        Parameter dir: indicates the direction of turning
        Precondition: dir is a boolean
        """
        if dir:
            self.angle+=SHIP_TURN_RATE
        if not dir:
            self.angle-=SHIP_TURN_RATE
        self._facing.x=math.cos(degToRad(self.angle))
        self._facing.y=math.sin(degToRad(self.angle))

    def velocity(self):
        """
        Modifies the velocity of the ship.
        """
        self._velocity=self._velocity+(self._facing*(SHIP_IMPULSE))
        if self._velocity.length()>SHIP_MAX_SPEED:
            self._velocity.normalize()
            self._velocity=self._velocity*SHIP_MAX_SPEED
    
    def move(self):
        """
        Modifies the x and y attributes of the ship based on its velocity.
        """
        self.x+=self._velocity.x
        self.y+=self._velocity.y
        if self.x<-DEAD_ZONE:
            self.x+=GAME_WIDTH+(2*DEAD_ZONE)
        if self.x>(GAME_WIDTH+DEAD_ZONE):
            self.x-=GAME_WIDTH+(2*DEAD_ZONE)
        if self.y<-DEAD_ZONE:
            self.y+=GAME_WIDTH+(2*DEAD_ZONE)
        if self.y>(GAME_WIDTH+DEAD_ZONE):
            self.y-=GAME_WIDTH+(2*DEAD_ZONE)


class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: the velocity vector of the Asteroid object
    # Invariant: _velocity is a Vector2 object
    #
    # Attribute _radius: the radius of the Asteroid  object
    # Invariant: _radius is an int
    #
    # Attribute _size: the size of the Asteroid object
    # Invariant: _size is a string

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getRadius(self):
        """
        Return the radius of an Asteroid object.

        The radius is an int.
        """
        return self._radius

    def getSize(self):
        """
        Return the size of an Asteroid object.

        The size is a string.
        """
        return self._size

    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, size, pos, dir):
        """
        Initializes an Asteroid object.

        Parameter size: size of the asteroid
        Precondition: size is a string

        Parameter pos: position of the asteroid
        Precondition: pos is a tuple

        Parameter dir: the direction of movemement of the asteroid
        Precondition: dir is a list
        """
        if size==SMALL_ASTEROID:
            img=SMALL_IMAGE
            radius=SMALL_RADIUS
            speed=SMALL_SPEED
        elif size==MEDIUM_ASTEROID:
            img=MEDIUM_IMAGE
            radius=MEDIUM_RADIUS
            speed=MEDIUM_SPEED
        else:
            img=LARGE_IMAGE
            radius=LARGE_RADIUS
            speed=LARGE_SPEED
        super().__init__(source=img, x=pos[0], y=pos[1])
        self.width=radius*2
        self.height=radius*2
        self._radius=radius
        self._size=size
        if dir==[0,0]:
                self._velocity = Vector2(0,0)
        else:
            magnitude = ((dir[0]**2)+(dir[1]**2))**0.5
            self._velocity = Vector2((dir[0]/magnitude)*speed, (dir[1]/magnitude)*speed)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def move(self):
        """
        Modifies the x and y attributes of the asteroid based on its velocity
        """
        self.x+=self._velocity.x
        self.y+=self._velocity.y
        if self.x<-DEAD_ZONE:
            self.x+=GAME_WIDTH+(2*DEAD_ZONE)
        if self.x>(GAME_WIDTH+DEAD_ZONE):
            self.x-=GAME_WIDTH+(2*DEAD_ZONE)
        if self.y<-DEAD_ZONE:
            self.y+=GAME_WIDTH+(2*DEAD_ZONE)
        if self.y>(GAME_WIDTH+DEAD_ZONE):
            self.y-=GAME_WIDTH+(2*DEAD_ZONE)

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE