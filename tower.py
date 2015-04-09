import pygame
import copy
import os
import sys
import time
import argparse
# Colors
#http://www.raywenderlich.com/24252/beginning-game-programming-for-teens-with-python
#http://hasgraphics.com/danc-planet-cute-tileset/
#http://www.lostgarden.com/2009/03/dancs-miraculously-flexible-game.html
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
BLUE = ( 0, 0, 255)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
"""
arg1 = 0
parser = argparse.ArgumentParser
parser.add_argument('integers', type=int, dest=arg1)
"""
parser = argparse.ArgumentParser(description="stuff!")
parser.add_argument('-i', type=int, dest='arg1', default=0)
options = parser.parse_args()



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image, image.get_rect()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		self.money = 150
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([8, 8])
		self.image.fill((255,255,0))
		self.rect = self.image.get_rect()
	def update(self):
		pos = pygame.mouse.get_pos()
		self.rect.x = pos[0]-4
		self.rect.y = pos[1]-4
	def kill(self):
		pygame.sprite.Sprite.kill(self)

class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height):
		""" Constructor for the wall that the player can place towers on. """
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill((131,72,55))
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
	def kill(self):
		pygame.sprite.Sprite.kill(self)


class LTower(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.clock=0
		self.image, self.rect = load_image('bunny_2.png', -1)
		self.area = 4
	def update(self):
		enemiesInArea =  pygame.sprite.spritecollide(self, current_level.enemy_list, False, pygame.sprite.collide_circle_ratio(self.area))                    
		if enemiesInArea:
			pygame.draw.line(screen, WHITE, self.rect.center, enemiesInArea[0].rect.center, 5)
			self.clock += 1
			if self.clock % 50 == 0:
				enemiesInArea[0].health -= 1
	def kill(self):
		pygame.sprite.Sprite.kill(self)
			
class ETower(pygame.sprite.Sprite):
	def __init__(self):
		self.clock=0
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('tower_bunnies.png',-1)
		self.rect = self.image.get_rect()
		self.myclock = 0
	def update(self):
		self.myclock += 1
		if self.myclock % 150 == 0:
			explosion = TowerExplosion()
			explosion.rect.center = self.rect.center
			all_sprites_list.add(explosion)
			explosion_list.add(explosion)
	def kill(self):
		pygame.sprite.Sprite.kill(self)
		

class TowerExplosion(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)	
		self.already_hit = pygame.sprite.Group()
		self.myexpclock =0
		self.image = pygame.Surface([200, 200])
		self.image.fill(RED)
		self.rect = self.image.get_rect()

	def update(self):
		self.myexpclock += 1
		if self.myexpclock % 15 == 0:
			pygame.sprite.Sprite.kill(self)	
		hit_enemy_list = pygame.sprite.spritecollide(self, current_level.enemy_list, False)
		for hit in hit_enemy_list :
				if hit not in self.already_hit:
					hit.health -= 2
					self.already_hit.add(hit)	
	def kill(self):
		pygame.sprite.Sprite.kill(self)

class HealthBar(pygame.sprite.Sprite):
	def __init__(self,x,y, health, RoG):
		pygame.sprite.Sprite.__init__(self)
		if RoG == 1:
			self.image, self.rect = load_image('healthbar.png',-1)
		if RoG == 0:
			self.image, self.rect = load_image('healthbarg.png',-1)
		self.rect = self.image.get_rect()
		self.fullhealth = health
		healthbar_list.add(self)
		
			
	def update(self, x, y, health, RoG):
		if RoG == 1:
			if health <=  (.25 * self.fullhealth):
				self.image, self.rect = load_image('healthbar14.png',-1)
			elif health <= (.5 * self.fullhealth):
				self.image, self.rect = load_image('healthbar12.png',-1)
			elif health <= (.75 * self.fullhealth):
				self.image, self.rect = load_image('healthbar34.png',-1)
		if RoG == 0:
			if health <=  (.25 * self.fullhealth):
				self.image, self.rect = load_image('healthbarg14.png',-1)
			elif health <= (.5 * self.fullhealth):
				self.image, self.rect = load_image('healthbarg12.png',-1)
			elif health <= (.75 * self.fullhealth):
				self.image, self.rect = load_image('healthbarg34.png',-1)
		self.rect.x = x
		self.rect.y = y - 20
	def kill(self):
		pygame.sprite.Sprite.kill(self)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, health, speed, path, size):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('badguydown.png', -1)
		self.up, self.vertrect = load_image('badguyup.png',-1)
		self.left, self.horizrect = load_image('badguyleft.png',-1)
		self.down = self.image
		self.right, self.horizrect = load_image('badguyright.png',-1)
		self.health = health
		self.speed = speed
		self.path = path
		self.healthbar = HealthBar(self.rect.x,self.rect.y,self.health, 1)
	def update(self):
		if self.health <= 0:
			pygame.sprite.Sprite.kill(self.healthbar)
			pygame.sprite.Sprite.kill(self)
			player.money += 10
		if len(self.path[0]) == 1:
			if self.path[0][0] > self.rect.y:
				self.rect.y += self.speed
				self.image = self.down 
			if self.path[0][0] < self.rect.y:
				self.rect.y -= self.speed
				self.image = self.up  
			if self.rect.y == self.path[0][0]:
				self.path.pop(0)
				if not self.path:
					pygame.sprite.Sprite.kill(self.healthbar)
					pygame.sprite.Sprite.kill(self)
		elif len(self.path[0]) == 2:
			if self.path[0][0] < self.rect.x :
				self.rect.x -= self.speed
				self.image = self.left  
			if  self.path[0][0] > self.rect.x:
				self.rect.x += self.speed
				self.image = self.right  
			if self.path[0][1] > self.rect.y:
				self.rect.y += self.speed
				self.image = self.down  
			if self.path[0][1] < self.rect.y:
				self.rect.y -= self.speed
				self.image = self.up  
			if self.rect.collidepoint(self.path[0][0],self.path[0][1]):
				self.path.pop(0)
				if not self.path:
					pygame.sprite.Sprite.kill(self.healthbar)
					pygame.sprite.Sprite.kill(self)

		self.healthbar.update(self.rect.x, self.rect.y,self.health, 1)
	def kill(self):
		pygame.sprite.Sprite.kill(self)

class Castle(pygame.sprite.Sprite):
	def __init__(self,x,y, health):
		pygame.sprite.Sprite.__init__(self)
		self.clock = 0
		self.image, self.rect = load_image('Wall_Block_Tall.png',-1)
		self.health = health
		self.rect.centerx=x
		self.rect.centery=y
		self.healthbar = HealthBar(self.rect.x+25,self.rect.y-20,self.health, 0)
		
	def update(self):
		if self.health <= 0:
			pygame.sprite.Sprite.kill(self.healthbar)
			pygame.sprite.Sprite.kill(self)
		self.clock +=1
		castle_attacked = pygame.sprite.spritecollide(self, current_level.enemy_list, False)
		for enemy in castle_attacked:
			if self.clock % 125 == 0 : 
				self.health -= 5
		self.healthbar.update(self.rect.x +25, self.rect.y - 20, self.health, 0)
	def kill(self):
		pygame.sprite.Sprite.kill(self.healthbar)
		pygame.sprite.Sprite.kill(self)


class Level():
	def __init__(self):
		self.youwin = False
		self.nextlevel = False
		self.platform_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player
		grass, grassrect = load_image('grass.png')
		self.castle_list =pygame.sprite.Group()
		self.grass = grass 
		self.wave_list=[]
		self.healthbar_list =pygame.sprite.Group()
		self.gameover = False
	def update(self):
		if not self.castle_list:
			self.gameover = True
		if not self.enemy_list:
			if self.wave_list:
				self.wave_list[0].start()
				self.wave_list.pop(0)
				player.money+=20
			else:
				self.nextlevel = True				
				for tower in tower_list:
					tower.kill()
				for castle in self.castle_list:
					castle.kill()
				self.kill
				del self
				return
				
				
		self.platform_list.update()
		self.enemy_list.update()
		self.castle_list.update()
	def draw(self, screen):
		""" Draw everything on this level. """
		for x in range(SCREEN_WIDTH/(self.grass.get_width())):
       			 for y in range(SCREEN_HEIGHT/(self.grass.get_height())):
            			screen.blit(self.grass,(x*100,y*100))
		self.platform_list.draw(screen)
		if self.enemy_list:
			self.enemy_list.draw(screen)
		self.castle_list.draw(screen)
	def kill(self):
		for enemy in self.enemy_list:
			enemy.kill()
		for castle in self.castle_list:
			castle.kill()
		for platform in self.platform_list:
			platform.kill()

class Level01(Level):
	def __init__(self):
		""" Create level 1. """
		Level.__init__(self)
			#x,y,width,height
		
		level = [ [400, 100, 20, 700],
			[600, 100, 20, 700],
			]
		for platform in level:
			block = Platform(platform[0], platform[1], platform[2], platform[3])
			self.platform_list.add(block)
		self.wave_list.append(L1W1())
		self.wave_list.append(L1W2())
		self.wave_list.append(L1W3())	
		castles = [[SCREEN_WIDTH/2, SCREEN_HEIGHT-30, 25],
			]
		for castle in castles:
			cast = Castle(castle[0],castle[1],castle[2])
			self.castle_list.add(cast)

class Level02(Level):
	def __init__(self):
		""" Create level 2. """
		Level.__init__(self)
		level = [ [200, 100, 20, 200],
			[SCREEN_WIDTH-200, 100, 20, 200],
			[220, 300, 20, 175],
			[SCREEN_WIDTH-220, 300, 20, 200],
			[240, 475, 20, 50],
			[SCREEN_WIDTH-240, 475,20,50],
			[260, 525, 20, 100],
			[SCREEN_WIDTH-260,525, 20, 100],
			[280, 625, 20, 50],
			[SCREEN_WIDTH-280, 625, 20, 50],
			[300, 675, 20 , 200],
			[SCREEN_WIDTH-300, 675, 20, 200],

			[425, 100, 20, 600],
			[SCREEN_WIDTH-425, 100, 20, 600],
			]
		for platform in level:
			block = Platform(platform[0], platform[1], platform[2], platform[3])
			self.platform_list.add(block)

		self.wave_list.append(L2W1())
		self.wave_list.append(L2W2())
		self.wave_list.append(L2W3())
		self.wave_list.append(L2W4())
		castles = [[SCREEN_WIDTH/2, SCREEN_HEIGHT-30, 25],
			]

		for castle in castles:
			cast = Castle(castle[0],castle[1],castle[2])
			self.castle_list.add(cast)

class Level03(Level):
	def __init__(self):
		Level.__init__(self)
		level = [[ 200, 100, 60, 20],
			[SCREEN_WIDTH - 200,  100, 60, 20],
			[375, 325, 100, 20],
			[SCREEN_WIDTH - 450, 325, 100, 20],
			[500, 390, 20, 300],
			[200, 650, 145, 20],
			[SCREEN_WIDTH - 300, 650, 145, 20],
			[90, 600, 100, 20],
			[SCREEN_WIDTH - 130, 600, 100, 20],
			[175, 300, 20, 115],
			[SCREEN_WIDTH - 200, 300, 20, 115],
			]
		for platform in level:
			block = Platform(platform[0], platform[1], platform[2], platform[3])
			self.platform_list.add(block)
		castles = [[SCREEN_WIDTH/2, SCREEN_HEIGHT-30, 25],
			]

		self.wave_list.append(L3W1())
		self.wave_list.append(L3W2())
		self.wave_list.append(L3W3())
		for castle in castles:
			cast = Castle(castle[0],castle[1],castle[2])
			self.castle_list.add(cast)

		
class Wave():	
	def __init__(self):
		self.enemies= []
		self.path = []
class L1W1(Wave):
	def __init__(self):
		Wave.__init__(self)
		self.name = "L1W1"
	def start(self):
		self.enemies =[ [-  5, 140, 6, 1, 1],
			  			[-105, -70, 6, 1, 1],
			  	        [- 55,  70, 6, 1, 1],
			        	[-205, -70, 6, 1, 1],
			  	        [-255,  70, 6, 1, 1],
			  	        [-305, -70, 6, 1, 1],
			  	        [-155,  70, 6, 1, 1],
			  			]	
		self.path =  [ [(SCREEN_WIDTH/2)+15,70],
				[SCREEN_HEIGHT],
				
			
				]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

class L1W2(Wave):
	def __init__(self):
		Wave.__init__(self)
		self.name = "L1W2"
	def start(self):
		self.enemies =[ [SCREEN_WIDTH+  5, 140, 6, 1, 1],
			  			[SCREEN_WIDTH+105, -70, 6, 1, 1],
			  			[SCREEN_WIDTH+ 55,  70, 6, 1, 1],
			  			[SCREEN_WIDTH+205, -70, 6, 1, 1],
			 		 	[SCREEN_WIDTH+255,  70, 6, 1, 1],
			 		 	[SCREEN_WIDTH+305, -70, 6, 1, 1],
			 		 	[SCREEN_WIDTH+155,  70, 6, 1, 1],
			 		 	]	
		self.path =  [ [SCREEN_WIDTH/2,70],
				[SCREEN_HEIGHT],
				
			
				]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

class L1W3(Wave):
	
	def __init__(self):
		Wave.__init__(self)
		self.name = "L1W3"
	def start(self):
		self.enemies =[ [(SCREEN_WIDTH/2)-25, -140, 6, 1,1],
			  	[SCREEN_WIDTH/2,      -140, -6, 1,1],
			  	[(SCREEN_WIDTH/2)+25, -140, 6, 1,1],
			  	[(SCREEN_WIDTH/2)-25, -220, 6, 1,1],
			  	[SCREEN_WIDTH/2,      -220, -6, 1,1],
			  	[(SCREEN_WIDTH/2)+25, -220, 6, 1,1],
			  	[(SCREEN_WIDTH/2)-25,    0, 6, 1,1],
			  	]	
		self.path =  [ 
				[SCREEN_HEIGHT],
				
			
				]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)
		

class L2W1(Wave):
	
	def __init__(self):
		Wave.__init__(self)
		self.name = "L2W1"
	def start(self):
		self.enemies =[ [-55, 400, 12,1, 1],
						]
		self.path =  [ [155, 45],
				[400, 45],
				[400, SCREEN_HEIGHT-30],
				[500,SCREEN_HEIGHT-30],
				[600,SCREEN_HEIGHT-30],
				[400,SCREEN_HEIGHT-30],
				[500,SCREEN_HEIGHT-30],
				[SCREEN_HEIGHT],		
				]

		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

		self.enemies =[ [SCREEN_WIDTH+55, 400, 12,1, 1],
				#[SCREEN_WIDTH+55, 500, 12, 1, 1],
				]

		self.path =  [ [SCREEN_WIDTH-155, 45],
				[SCREEN_WIDTH-400, 45],
				[SCREEN_WIDTH-400, SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-500,SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-600,SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-400,SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-500,SCREEN_HEIGHT-30],
				[SCREEN_HEIGHT],
				]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

class L2W2(Wave):
	
	def __init__(self):
		Wave.__init__(self)
		self.name = "L2W2"
	def start(self):
		self.enemies =[ [-55, 400, 12,1, 1],
				[-55, 1000, 12, 1, 1],
				]
		self.path =  [ [155, 45],
				[300, 45],
				[300, 550],
				[360, SCREEN_HEIGHT-30],
				
				[500,SCREEN_HEIGHT-30],
				[600,SCREEN_HEIGHT-30],
				[400,SCREEN_HEIGHT-30],
				[500,SCREEN_HEIGHT-30],
				[SCREEN_HEIGHT],		
				]

		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

		self.enemies =[ [SCREEN_WIDTH+55, 400, 12,1, 1],
				[SCREEN_WIDTH+55, 1000, 12, 1, 1],
				]

		self.path =  [ [SCREEN_WIDTH-155, 45],
				[SCREEN_WIDTH-300, 45],
				[SCREEN_WIDTH-300,550],
				[SCREEN_WIDTH-360, SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-500,SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-600,SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-400,SCREEN_HEIGHT-30],
				[SCREEN_WIDTH-500,SCREEN_HEIGHT-30],
				[SCREEN_HEIGHT],
				]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)
class L2W3(Wave):
	
	def __init__(self):
		Wave.__init__(self)
		self.name = "L2W3"
	def start(self):
		self.enemies =[ [365, -20, 12,1, 1],
				[SCREEN_WIDTH-365, -20 , 12, 1, 1],
				]
		self.path =  [ [SCREEN_HEIGHT -30]]
	
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

class L2W4(Wave):
	
	def __init__(self):
		Wave.__init__(self)
		self.name = "L2W4"
	def start(self):
		self.enemies =[[SCREEN_WIDTH/2, -50, 30, 1, 2]]

		self.path =  [ [SCREEN_HEIGHT -30],
						[600,SCREEN_HEIGHT-30],
					[400,SCREEN_HEIGHT-30],
					[500,SCREEN_HEIGHT-30],
					]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

class L3W1(Wave):
	def __init__(self):
		Wave.__init__(self)
		self.name = "L3W1"
	def start(self):
		self.enemies =[[SCREEN_WIDTH/2, -50, 12, 1, 1],
						[SCREEN_WIDTH/2, -150, 12, 1, 1],
					
						]

		self.path =  [ [SCREEN_WIDTH/2, 85],
						[300, 95],
						
						[SCREEN_HEIGHT -250],
						[600,SCREEN_HEIGHT-30],
						[400,SCREEN_HEIGHT-30],
						[500,SCREEN_HEIGHT-30],
						]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

		self.enemies =[[SCREEN_WIDTH/2, -100, 12, 1, 1],
						[SCREEN_WIDTH/2, -200, 12, 1, 1],
					
						]
		
		self.path =  [ [SCREEN_WIDTH/2, 85],
						[SCREEN_WIDTH -300, 95],
						[SCREEN_HEIGHT -250],
						[600,SCREEN_HEIGHT-30],
						[400,SCREEN_HEIGHT-30],
						[500,SCREEN_HEIGHT-30],
						]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

class L3W2(Wave):
	def __init__(self):
		Wave.__init__(self)
		self.name = "L3W1"
	def start(self):
		self.enemies =[[-200,  SCREEN_HEIGHT - 325, 12, 1, 1],
						[-250,  SCREEN_HEIGHT - 325, 14, 1, 1],
					
						]

		self.path =  [ [300, SCREEN_HEIGHT - 325],
						
						
						[SCREEN_HEIGHT -250],
						[600,SCREEN_HEIGHT-30],
						[400,SCREEN_HEIGHT-30],
						[500,SCREEN_HEIGHT-30],
						]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

		self.enemies =[[SCREEN_WIDTH+200,  SCREEN_HEIGHT - 325, 12, 1, 1],
						[SCREEN_WIDTH+250,  SCREEN_HEIGHT - 325, 12, 1, 1],
					
						]

		self.path =  [ [SCREEN_WIDTH-300, SCREEN_HEIGHT - 325],
						
						
						[SCREEN_HEIGHT -250],
						[SCREEN_WIDTH-600,SCREEN_HEIGHT-30],
						[SCREEN_WIDTH-400,SCREEN_HEIGHT-30],
						[SCREEN_WIDTH-500,SCREEN_HEIGHT-30],
						]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

class L3W3(Wave):
	def __init__(self):
		Wave.__init__(self)
		self.name = "L3W3"
	def start(self):
		self.enemies =[[-300,-105  , 14, 1, 1],
						[SCREEN_WIDTH+300, - 105, 14, 1, 1],
					
						]
		self.path =  [	[SCREEN_WIDTH/2, SCREEN_HEIGHT-30],
						[SCREEN_WIDTH-600,SCREEN_HEIGHT-30],
						[SCREEN_WIDTH-400,SCREEN_HEIGHT-30],
						[SCREEN_WIDTH-500,SCREEN_HEIGHT-30],
						]
		for guy in self.enemies:
			dude = Enemy(guy[2],guy[3], copy.copy(self.path), guy[4])
			dude.rect.x = guy[0]
			dude.rect.y = guy[1]
			current_level.enemy_list.add(dude)

all_sprites_list = pygame.sprite.Group()
explosion_list = pygame.sprite.Group()
tower_list = pygame.sprite.Group()
healthbar_list = pygame.sprite.Group()
player = Player()
all_sprites_list.add(player)
pygame.init()
pygame.mouse.set_visible(False)
level_list = []
level_list.append(Level01())
level_list.append(Level02())
level_list.append(Level03())
current_level_no = 0
current_level = level_list[current_level_no]
if options.arg1 > 0:
	level_list.pop(0)
	if options.arg1 > 1:
		level_list.pop(0)
	current_level = level_list[current_level_no]
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tower Attempt 1")


def main():
	global current_level
	global current_level_no
	global level_list
	global all_sprites_list
	global explosion_list
	global tower_list
	global healthbar_list
	global castle_list
	global player
	
	""" Main Program """
	costL = 20.0
	costE = 20.0
	done = False
	clock = pygame.time.Clock()
	mainmenu = True
	
	# -------- Main Program Loop -----------
	while not done:
		while mainmenu:
			helpmenu=True
			screen.fill(BLACK)
			pygame.mouse.set_visible(True)

			if pygame.font:
				font = pygame.font.Font(None, 55)
				text = font.render( "Bunny Defense" , 1, (255,215,0))
				textpos = text.get_rect(center=(SCREEN_WIDTH/2,45))
				screen.blit(text, textpos)

				font = pygame.font.Font(None, 32)
				text = font.render("Play" , 1, (255,215,0))
				textposplay = text.get_rect(center=(SCREEN_WIDTH/2,240))
				screen.blit(text, textposplay)
				
				font = pygame.font.Font(None, 32)
				text = font.render("Controls! -->" , 1, (255,215,0))
				textposhelp = text.get_rect(center=(200,360))
				screen.blit(text, textposhelp)
			
				if helpmenu:
					font = pygame.font.Font(None, 25)
					line1 = font.render("Left-click on platforms to create EXPLOSIVE TOWERS", 1, (255,215,0))
					line2 = font.render("Right-click on platforms to make LASER TOWERS", 1,(255,215,0))
					line3 = font.render("Don't let the enemies get to your castle!" , 1, (255,215,0))
					textpos1 = line1.get_rect(center=(550,360))
					screen.blit(line1, textpos1)
					textpos2 = line2.get_rect(center=(550,400))
					screen.blit(line2, textpos2)
					textpos3 = line3.get_rect(center=(550,440))
					screen.blit(line3,textpos3)
					

			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					done = True
					mainmenu =False	
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if textposplay.collidepoint(pygame.mouse.get_pos()):
						mainmenu=False
						pygame.mouse.set_visible(False)
					if textposhelp.collidepoint(pygame.mouse.get_pos()):
						helpmenu = False
					


			pygame.display.flip()
		if  current_level.gameover:
			font = pygame.font.Font(None, 55)
			text = font.render( "GAME OVER", 1, (0,0,0))
			textpos = text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
			screen.blit(text, textpos)
			pygame.display.flip()
			time.sleep(3)
			mainmenu = True
			costL = 20.0
			costE = 20.0
			for tower in tower_list:
				tower.kill()
			for healthbar in healthbar_list:
				healthbar.kill()
			for level in level_list:
				level.kill()
			del level_list[:]
			level_list.append(Level01())
			level_list.append(Level02())
			player.money = 150
			current_level = level_list[current_level_no]
		if current_level.nextlevel:		
			level_list.pop(0)
			if level_list:
				current_level = level_list[current_level_no]
				all_sprites_list.add(player)
				player.money += 70
			else: 
				youwin = True
				font = pygame.font.Font(None, 55)
				text = font.render( "YOU WIN", 1, (0,0,0))
				textpos = text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
				screen.blit(text, textpos)
				pygame.display.flip()
				time.sleep(3)
				mainmenu = True
				for healthbar in healthbar_list:
					healthbar.kill()
				for level in level_list:
					level.kill()
				del level_list[:]
				level_list.append(Level01())
				level_list.append(Level02())
				current_level = level_list[current_level_no]
			

		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				done = True 
			elif event.type == pygame.KEYDOWN :
               			if event.key == pygame.K_ESCAPE:
					mainmenu=True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button ==1:
					platform_hit_list = pygame.sprite.spritecollide(player, current_level.platform_list, False)

				
					if platform_hit_list: 
							tower = ETower()
							tower.rect.centerx = player.rect.centerx
							tower.rect.centery =  player.rect.centery
							tower_hit_list = pygame.sprite.spritecollide(tower, tower_list, False)
							if not tower_hit_list:
								if player.money > costE:

									player.money -= costE
									costE = costE + 5
									tower_list.add(tower)
									all_sprites_list.add(tower)
							else:
								pygame.sprite.Sprite.kill(tower_hit_list[0])
								player.money +=20
				if event.button == 3:
					platform_hit_list = pygame.sprite.spritecollide(player, current_level.platform_list, False)

				
					if platform_hit_list:
							tower = LTower()
							tower.rect.centerx = platform_hit_list[0].rect.centerx
							tower.rect.y =  player.rect.y
							tower_hit_list = pygame.sprite.spritecollide(tower, tower_list, False)
							if not tower_hit_list: 
								if player.money > costL:
									player.money -= costL
									costL = costL + 5

									tower_list.add(tower)
									all_sprites_list.add(tower)
							else:
								pygame.sprite.Sprite.kill(tower_hit_list[0])
								player.money += 20		
			
		current_level.update()
		current_level.draw(screen)
		all_sprites_list.update()
		all_sprites_list.draw(screen)
		healthbar_list.draw(screen)
		clock.tick(60)
		
		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render( "$"+"%d" % (player.money), 1, (255,215,0))
			textpos = text.get_rect(bottomleft=(10,SCREEN_HEIGHT-15))
			screen.blit(text, textpos)
			text = font.render( "Explosion Tower = $"+"%d" % (costE), 1, (255,215,0))
			textpos = text.get_rect(topleft=(10,15))
			screen.blit(text, textpos)
			text = font.render( "Laser Tower = $"+"%d" % (costL), 1, (255,215,0))
			textpos = text.get_rect(topleft=(10,35))
			screen.blit(text, textpos)
		pygame.display.flip()
	pygame.quit ()

if __name__ == "__main__":
	main()
