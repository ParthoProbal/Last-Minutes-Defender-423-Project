from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def drawHealthbar(player_x, player_y, PLAYER_HEIGHT, life, game_over, HEALTH_ORANGE):
    if game_over:
        return
    
    glPushMatrix()
    
    glTranslatef(player_x, player_y, 120 + PLAYER_HEIGHT + 50)
    
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-30, -5, 0)
    glVertex3f(30, -5, 0)
    glVertex3f(30, 5, 0)
    glVertex3f(-30, 5, 0)
    glEnd()
    
    glColor3f(HEALTH_ORANGE[0], HEALTH_ORANGE[1], HEALTH_ORANGE[2])
    health_width = 60 * (life / 5.0)
    
    glBegin(GL_QUADS)
    glVertex3f(30 - health_width, -4, 1)
    glVertex3f(30, -4, 1)
    glVertex3f(30, 4, 1)
    glVertex3f(30 - health_width, 4, 1)
    glEnd()
    
    glPopMatrix()
    
# Planet Health Bar (Big and Fat)
def drawPlanetHealthBar(planet_health, planet_max_health=100, HEALTH_ORANGE=(1, 0.65, 0)):
    if planet_health <= 0:
        return
    
    glPushMatrix()
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1250, 0, 1000)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    
    bar_x = 625
    bar_y = 950   
    
    # bg (gray)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(bar_x - 200, bar_y - 20)
    glVertex2f(bar_x + 200, bar_y - 20)
    glVertex2f(bar_x + 200, bar_y + 20)
    glVertex2f(bar_x - 200, bar_y + 20)
    glEnd()
    
    # Health fill (orange)
    health_percentage = planet_health / planet_max_health
    health_width = 400 * health_percentage
    
    glColor3f(HEALTH_ORANGE[0], HEALTH_ORANGE[1], HEALTH_ORANGE[2])
    glBegin(GL_QUADS)
    glVertex2f(bar_x - 200, bar_y - 15)
    glVertex2f(bar_x - 200 + health_width, bar_y - 15)
    glVertex2f(bar_x - 200 + health_width, bar_y + 15)
    glVertex2f(bar_x - 200, bar_y + 15)
    glEnd()
    
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glPopMatrix()

# Enemy Health Bar (Small Red Bar)
def drawEnemyHealthbar(enemy_x, enemy_y, enemy_z):
    glPushMatrix()
    
    glTranslatef(enemy_x, enemy_y, enemy_z + 100)  # Above enemy
    
    # Bg (smaller than player bar)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-20, -3, 0)
    glVertex3f(20, -3, 0)
    glVertex3f(20, 3, 0)
    glVertex3f(-20, 3, 0)
    glEnd()
    
    # Health fill (red for enemies)
    glColor3f(1, 0, 0)  # Red
    glBegin(GL_QUADS)
    glVertex3f(-20, -2, 1)
    glVertex3f(20, -2, 1)
    glVertex3f(20, 2, 1)
    glVertex3f(-20, 2, 1)
    glEnd()
    
    glPopMatrix()

# Planet Attacker Health Bar (Small Orange Bar)
def drawPlanetAttackerHealthbar(enemy_x, enemy_y, enemy_z):
    glPushMatrix()
    
    glTranslatef(enemy_x, enemy_y, enemy_z + 80)  # Above planet attacker
    
    # Background
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-15, -3, 0)
    glVertex3f(15, -3, 0)
    glVertex3f(15, 3, 0)
    glVertex3f(-15, 3, 0)
    glEnd()
    
    # Health full for planet attackers
    glColor3f(1, 0.5, 0)  # Orange color
    glBegin(GL_QUADS)
    glVertex3f(-15, -2, 1)
    glVertex3f(15, -2, 1)
    glVertex3f(15, 2, 1)
    glVertex3f(-15, 2, 1)
    glEnd()
    
    glPopMatrix()