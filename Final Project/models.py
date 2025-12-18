from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import colors


def drawPlanet(radius, pos_x=0, pos_y=0, pos_z=0):

    glPushMatrix()
    glTranslatef(pos_x, pos_y, pos_z) # Planet x, y, z
    
    glColor3f(colors.URANUS_BLUE[0], colors.URANUS_BLUE[1], colors.URANUS_BLUE[2])
    
    glutSolidSphere(radius, 50, 50)  # Radius, Stack space x, y
    
    glPopMatrix()

# Body parts start
def drawUfoBody():
    glColor3f(colors.UFO_BLACK[0], colors.UFO_BLACK[1], colors.UFO_BLACK[2])
    glutSolidSphere(50, 30, 30) 

def drawUfoHand():
    glColor3f(colors.UFO_WHITE[0], colors.UFO_WHITE[1], colors.UFO_WHITE[2])
    gluCylinder(gluNewQuadric(), 5, 3, 60, 10, 10)  

def drawUfoCircle():
    glColor3f(colors.UFO_LIGHT_GREY[0], colors.UFO_LIGHT_GREY[1], colors.UFO_LIGHT_GREY[2])
    glutSolidSphere(30, 20, 20)

def drawUfoGun():
    glColor3f(colors.UFO_GUN_GREY[0], colors.UFO_GUN_GREY[1], colors.UFO_GUN_GREY[2])
    glTranslatef(0, 0, 30)  
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 8, 4, 50, 10, 10)  # Gun: base radius 8, top 4, length 50
    glRotatef(90, 1, 0, 0)
    
# Body parts end

def drawHeroUfo(pos_x=0, pos_y=0, pos_z=120, rotation=0):
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotation, 0, 0, 1)
    
    drawUfoBody()
    
    # Hand 1 (Right)
    glPushMatrix()
    glTranslatef(60, 0, 0)
    glRotatef(90, 0, 1, 0)
    drawUfoHand()
    glPopMatrix()
    
    # Hand 2 (Left)
    glPushMatrix()
    glTranslatef(-60, 0, 0)  
    glRotatef(-90, 0, 1, 0)  
    drawUfoHand()
    glPopMatrix()
    
    # Hand Balls
    glPushMatrix()
    glTranslatef(120, 0, 0)  # Right hand ball
    drawUfoCircle()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-120, 0, 0)  # Left hand ball
    drawUfoCircle()  
    glPopMatrix()
    
    glPushMatrix()
    drawUfoGun()
    glPopMatrix()
    
    glPopMatrix()
    
    
# Hero Attacker Enemy
def drawEnemyBody():
    glColor3f(colors.ENEMY_BLUE[0], colors.ENEMY_BLUE[1], colors.ENEMY_BLUE[2])
    glutSolidSphere(40, 30, 30) 

def drawEnemyLeg():
    glColor3f(colors.ENEMY_BLACK[0], colors.ENEMY_BLACK[1], colors.ENEMY_BLACK[2])
    gluCylinder(gluNewQuadric(), 6, 3, 50, 10, 10)  

def drawEnemyTurret():
    glColor3f(colors.ENEMY_YELLOW[0], colors.ENEMY_YELLOW[1], colors.ENEMY_YELLOW[2])
    glTranslatef(0, 0, 30)  
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 8, 4, 40, 10, 10)
    glRotatef(90, 1, 0, 0)

def drawHeroAttacker(pos_x=0, pos_y=0, pos_z=120, rotation=0):
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotation, 0, 0, 1)
    
    drawEnemyBody()
    
    # Leg 1 (Right, 180 degrees backwards)
    glPushMatrix()
    glTranslatef(30, 0, -40)  
    glRotatef(180, 0, 0, 1)  
    drawEnemyLeg()
    glPopMatrix()
    
    # Leg 2 (Left, 180 degrees backwards)
    glPushMatrix()
    glTranslatef(-30, 0, -40)  
    glRotatef(180, 0, 0, 1)  
    drawEnemyLeg()
    glPopMatrix()
    
    # Turret
    glPushMatrix()
    drawEnemyTurret()
    glPopMatrix()
    
    glPopMatrix()
    
    
# Planet Attacker Enemy
def drawPlanetAttackerBody():
    glColor3f(colors.PLANET_ATTACKER_ORANGE[0], colors.PLANET_ATTACKER_ORANGE[1], colors.PLANET_ATTACKER_ORANGE[2])
    glutSolidSphere(35, 30, 30) 

def drawPlanetAttackerSword():
    glColor3f(colors.PLANET_ATTACKER_GREEN[0], colors.PLANET_ATTACKER_GREEN[1], colors.PLANET_ATTACKER_GREEN[2])
    glTranslatef(0, 0, 30)  
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 10, 2, 60, 10, 10)  # Pusher, Wide base (10), narrow tip (2), length 60
    glRotatef(90, 1, 0, 0)

def drawPlanetAttacker(pos_x=0, pos_y=0, pos_z=120, rotation=0):
    glPushMatrix()
    
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotation, 0, 0, 1)
    
    drawPlanetAttackerBody()
    
    # Sword/wood for pushing planet
    glPushMatrix()
    drawPlanetAttackerSword()
    glPopMatrix()
    
    glPopMatrix()