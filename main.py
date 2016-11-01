
#shmup game
#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

import pygame;
import random;
import os;
import glob;
POWERUP_TIME=1000*10;
harder=0;
WIDTH=480;
HEIGHT=600;
FPS=60;
MAX_VOLUME=0.1;
#define color
WHITE=[255,255,255];
BLACK=[0,0,0];
RED=[255,0,0];
GREEN=[0,255,0]; 
BLUE=[0,0,255];
YELLOW=[255,255,0];
img_dir=os.path.join(os.path.dirname(__file__),"img");
sound_dir=os.path.join(os.path.dirname(__file__),"audio");
animation_dir=os.path.join(os.path.dirname(__file__),"img/Explosions_kenney")
sonic_exp_dir=os.path.join(os.path.dirname(__file__),"Shmup_player_expl");
total_frams=0;
pygame.init();
pygame.mixer.init();
screen=pygame.display.set_mode((WIDTH,HEIGHT));
pygame.display.set_caption("Shmup!");
clock=pygame.time.Clock();
#load all game grapicj
background=pygame.image.load(os.path.join(img_dir,"background.png")).convert();
background_rect=background.get_rect();
mob_image=pygame.image.load(os.path.join(img_dir,"p1_jump.png")).convert();
player_img=pygame.image.load(os.path.join(img_dir,"playerShip1_orange.png")).convert();
player_mini_img=pygame.transform.scale(player_img,(25,19));
player_mini_img.set_colorkey(BLACK);
player_die_sound=pygame.mixer.Sound("Shmup_player_expl/rumble1.ogg");
bullet_img=pygame.image.load(os.path.join(img_dir,"laserRed16.png")).convert();
meteor_images=glob.glob(os.path.join(img_dir,"meteorBrown_*.png"));
list_exp_sound=glob.glob(os.path.join(sound_dir,"Explosion*.wav"));
player_hide_sound=pygame.mixer.Sound("power_up/player_exp.wav");
laser_2_sound=pygame.mixer.Sound("audio/Laser_Shoot8_2.wav");
coins_tileSheet=pygame.image.load("coin/coins.png")#.convert();
exp_sound=[];
for p in list_exp_sound:
	exp_sound.append(pygame.mixer.Sound(p));

list_exp_animation_player=glob.glob(os.path.join(sonic_exp_dir,"sonicExplosion*.png"));
list_exp_animation=glob.glob(os.path.join(animation_dir,"*.png"));
exp_animation={};
exp_animation["lg"]=[];
exp_animation["sm"]=[];
exp_animation["player"]=[];
for path in list_exp_animation_player:
	img=pygame.image.load(path).convert();
	img.set_colorkey(BLACK);
	exp_animation["player"].append(img);

for path in list_exp_animation:
	img=pygame.image.load(path).convert();
	img.set_colorkey(BLACK);
	img_lg=pygame.transform.scale(img,(75,75));
	exp_animation["lg"].append(img_lg);
	img_sm=pygame.transform.scale(img,(32,32));
	exp_animation["sm"].append(img_sm);
#set upte address
#player class
powerup_images={};
powerup_images["shield"]=pygame.image.load("power_up/shield_silver.png").convert();
powerup_images["gun"]=pygame.image.load("power_up/bolt_gold.png").convert();
powerup_images["newLife"]=player_mini_img;
powerup_images["coin"]=pygame.image.load("power_up/coin.png")#.convert();
powerup_images["coin"]=pygame.transform.scale(powerup_images["coin"],(20,20));

powerup_sound={};
powerup_sound["shield"]=pygame.mixer.Sound("power_up/shield.wav");
powerup_sound["gun"]=pygame.mixer.Sound("power_up/gun.wav");
powerup_sound["coin"]=pygame.mixer.Sound("power_up/coin.wav");
powerup_sound["newLife"]=pygame.mixer.Sound("power_up/newLife.wav");



class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player,self).__init__();
		self.image=pygame.transform.scale( player_img,(50,38 ) );
		self.image.set_colorkey(BLACK);
		self.rect=self.image.get_rect();
		self.radius=(21);
		self.shot_sound=pygame.mixer.Sound(os.path.join(sound_dir,"Laser_Shoot8.wav"));
		self.shot_sound.set_volume(MAX_VOLUME);
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius);
		self.rect.centerx=WIDTH//2;
		self.rect.bottom=HEIGHT-10;
		self.shield=100;
		self.max_sheild=100;
		self.speedx=0;
		self.shoot_delay=250;
		self.last_shot=pygame.time.get_ticks();
		self.lives=3;
		self.hidden=False;
		self.hide_timer=pygame.time.get_ticks();
		self.power=1;
		self.power_timer=pygame.time.get_ticks();
	

	def powerup(self):
		self.power+=1;
		self.power_timer=pygame.time.get_ticks();	

	def update(self):
		#timout for powerup
		if self.power>1:
			if pygame.time.get_ticks()-self.power_timer>POWERUP_TIME:
				self.power_timer=pygame.time.get_ticks();
				self.power-=1;

		if self.hidden:
			if pygame.time.get_ticks()-self.hide_timer>1000:
				self.hidden=False;
				self.rect.centerx=WIDTH//2;
				self.rect.bottom=HEIGHT-10;
		
		self.speedx=0;
		keystate=pygame.key.get_pressed();
		if keystate[pygame.K_LEFT]:
			self.speedx=-8;
		if keystate[pygame.K_RIGHT]:
			self.speedx=8;	
		if keystate[pygame.K_SPACE]:
			self.shoot();	
		self.rect.x+=self.speedx;	
		if self.rect.right>WIDTH:
			self.rect.right=WIDTH;
		if self.rect.left<0:
			self.rect.left=0;	
		self.draw_sheild_bar();			
		
		
		
	def draw_sheild_bar(self):
		bar_lenght=100;
		bar_height=10;
		if self.shield<0:
			self.shield=0;
		width_heilght=(self.shield*bar_lenght)//self.max_sheild;

		sur=pygame.Surface((bar_lenght,bar_height));
		sur.set_colorkey(BLACK);
		rect=sur.get_rect();
		pygame.draw.rect(sur,WHITE,rect,2);	
		pygame.draw.rect(sur,GREEN,(rect.x,rect.y,width_heilght,10));		
		draw_text(sur, str(player.shield),18,rect.centerx,0,color=RED);
		screen.blit(sur,(10,20));	
				
	def shoot(self):
		self.shot_sound.set_volume(MAX_VOLUME);
		now=pygame.time.get_ticks();
		if now-self.last_shot>self.shoot_delay:
			self.last_shot=now;
			if self.power==1:
				bullet=Bullet(self.rect.centerx,self.rect.top);
				all_sprite.add(bullet);
				Bullets.add(bullet);
				self.shot_sound.play();
			if self.power==2:
				bullet1=Bullet(self.rect.left,self.rect.centery);
				bullet2=Bullet(self.rect.right,self.rect.centery);
				all_sprite.add(bullet1);
				all_sprite.add(bullet2);
				Bullets.add(bullet1);
				Bullets.add(bullet2);
				self.shot_sound.play();	
			if self.power==3:
				bullet1=Bullet(self.rect.left,self.rect.centery);
				bullet2=Bullet(self.rect.right,self.rect.centery);
				bullet3=Bullet(self.rect.centerx,self.rect.top);
				all_sprite.add(bullet1);
				all_sprite.add(bullet2);
				all_sprite.add(bullet3);
				Bullets.add(bullet1);
				Bullets.add(bullet2);
				Bullets.add(bullet3);
				self.shot_sound.play();	
			if self.power>=4:
				bullet1=Bullet(self.rect.left,self.rect.centery);
				bullet2=Bullet(self.rect.right,self.rect.centery);
				bullet3=Bullet(self.rect.centerx,self.rect.top);
				all_sprite.add(bullet1);
				all_sprite.add(bullet2);
				all_sprite.add(bullet3);
				Bullets.add(bullet1);
				Bullets.add(bullet2);
				Bullets.add(bullet3);
				if self.power-3>2:
					repeat=2;
				else:
					repeat=self.power-3;		
				for i in range(repeat):
						bullet=Bullet(self.rect.centerx,self.rect.top,type_="random");
						bullet.speedx=random.randrange(-8,8);
						if bullet.speedx==0:
							bullet.speedx=random.randrange(1,8);
						Bullets.add(bullet);
						all_sprite.add(bullet);	
				laser_2_sound.play();					
				
	def hide(self):
		self.hidden=True;
		self.hide_timer=pygame.time.get_ticks();
		self.rect.center=(WIDTH//2,HEIGHT+200);

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		super(Mob,self).__init__();
		path=random.choice(meteor_images);
		self.image_org=pygame.image.load(path).convert();
		self.image_org.set_colorkey(BLACK);
		self.image=self.image_org.copy();
		self.rect=self.image.get_rect();
		self.radius=int(self.rect.width*0.85//2);
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius);
		self.rect.x=random.randrange(0,WIDTH-self.rect.width);
		self.rect.y=random.randrange(-150,-100);
		self.speedy=random.randrange(1+harder,8+harder);
		self.speedx=random.randrange(-3,3);
		self.rot=0;
		self.rot_speed=random.randrange(-8,8);
		self.last_update=pygame.time.get_ticks();
		self.damage=random.randrange(10,40);
		self.score=random.randrange(10,100);

	def rotate(self):
		new=pygame.time.get_ticks();
		if new-self.last_update>50:
			self.last_update=new;
			self.rot+=self.rot_speed;
			self.rot%=360;
			new_image=pygame.transform.rotate(self.image_org,self.rot);
			old_center=self.rect.center;
			self.image=new_image;
			self.rect=self.image.get_rect();
			self.rect.center=old_center;
			 

	def update(self):
		self.rotate();
		self.rect.x+=self.speedx;
		self.rect.y+=self.speedy;
		if (self.rect.top>HEIGHT) or (self.rect.right<0) or (self.rect.left>(WIDTH)):
			self.rect.x=random.randrange(0,WIDTH-self.rect.width);
			self.rect.y=random.randrange(-100,-40);
			#self.speedy=random.randrange(1,8);
			self.speedy=random.randrange(1+harder,8+harder);
			#self.speedx=random.randrange(-3,3);


	
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y,type_=None):
		super(Bullet,self).__init__();
		if type_==None:
			self.image=pygame.transform.scale(bullet_img,(7,27));
		else:
			path=random.choice(["img/laserBlue16.png","img/laserGreen10.png"]);
			self.image=pygame.transform.scale(pygame.image.load(path),(7,27));	
		self.image.set_colorkey(BLACK);
		self.rect=self.image.get_rect();
		self.rect.bottom=y;
		self.rect.centerx=x;	
		self.speedy=-10;
		self.speedx=0;
		


	def update(self):
		self.rect.y+=self.speedy;
		self.rect.x+=self.speedx;
		#kill the bollt
		if self.rect.right<0 or self.rect.left>WIDTH or self.rect.bottom<0:
			self.kill();			

class Explosion(pygame.sprite.Sprite):
	def __init__(self,center,size):
		super(Explosion,self).__init__();
		self.size=size;
		self.image=exp_animation[self.size][0];
		self.rect=self.image.get_rect();
		self.rect.center=center;
		self.frame=0;
		self.last_update=pygame.time.get_ticks();
		self.frame_rate=75;
	def update(self):
			now=pygame.time.get_ticks();
			if now-self.last_update>self.frame_rate:
				self.last_update=now;
				self.frame+=1;
				if self.frame==len(exp_animation[self.size]):
					self.kill();
				else:
					center=self.rect.center;
					self.image=exp_animation[self.size][self.frame];
					self.rect=self.image.get_rect();
					self.rect.center=center;




	
class Powerup(pygame.sprite.Sprite):
	def __init__(self,center,type_=None):
		super(Powerup,self).__init__();
		if type_==None:
			self.type = random.choice(["shield","gun"]);
		else:
			self.type=type_;	
		self.image=powerup_images[self.type];
		self.image.set_colorkey(BLACK);
		self.rect=self.image.get_rect();
		self.rect.center=center;
		self.speedy=2;
		self.score=random.randrange(20,100);
		self.animated=self.type=="coin";
		self.animat_time=pygame.time.get_ticks();
		self.animated_index=0;
		self.animated_max=4;
		


	def update(self):
		self.rect.y+=self.speedy;
		#kill the bollti
		if self.animated:
			now=pygame.time.get_ticks();
			if now-self.animat_time>200:
				self.animat_time=now;
				center=self.rect.center;
				img=pygame.surface.Surface((40, 44))
				img.blit(coins_tileSheet,(0,0),(0,self.animated_index*44,40,44));
				self.image=pygame.transform.scale(img,(20,20));
				self.image.set_colorkey(BLACK);
				# self.rect=self.image.get_rect();
				# self.rect.center=center;
				self.animated_index+=1;
				self.animated_index%=self.animated_max;

		if self.rect.top>HEIGHT:
			self.kill();			

def newmobe(all_sprite,mobs):
		m=Mob();
		all_sprite.add(m);
		mobs.add(m);

def restart_values():		
	all_sprite=pygame.sprite.Group();
	mobs=pygame.sprite.Group();
	Bullets=pygame.sprite.Group();
	powerUPGroup=pygame.sprite.Group();
	player=Player();
	all_sprite.add(player);
	for i in range(8):
		newmobe(all_sprite,mobs);
	return all_sprite,mobs,Bullets,powerUPGroup,player;	
all_sprite,mobs,Bullets,powerUPGroup,player=restart_values();		
pygame.mixer.music.load(os.path.join(sound_dir,"tgfcoder-FrozenJam-SeamlessLoop.ogg"));
pygame.mixer.music.set_volume(MAX_VOLUME)
pygame.mixer.music.play();



font_name=pygame.font.match_font("arial");
def draw_text(surf,text,size,x,y,color=WHITE):
	font=pygame.font.SysFont(font_name,size);
	text_surface=font.render(text,True,color);
	text_rect=text_surface.get_rect();
	text_rect.midtop=(x,y);
	surf.blit(text_surface,text_rect);


def draw_lives(surf,x,y,lives,img):
	for i in range(lives):
		img_rect=img.get_rect();
		img_rect.x=x+30*i;
		img_rect.y=y;
		surf.blit(img,img_rect);

#Game loop
running=True;
game_over=True;
score=0;

def show_game_over_screen():
	screen.blit(background,(0,0))
	draw_text(screen, "SHMUP!", 64, WIDTH//2,HEIGHT//4);
	draw_text(screen, "Arrow keys move , space to fire", 22, WIDTH//2,HEIGHT//2);
	draw_text(screen, "Press a Key to begin", 18, WIDTH//2,HEIGHT*3//4);
	pygame.display.flip();
	wating=True;
	while wating:
		clock.tick(FPS);
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit();
			if event.type==pygame.KEYUP:
				wating=False;
					


while running:
	if game_over:
		show_game_over_screen();
		game_over=False;
		all_sprite,mobs,Bullets,powerUPGroup,player=restart_values();
		score=0;
		harder=0;



	screen.fill(BLACK);
	screen.blit(background,background_rect);
	#processes input
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False;



	#update
	all_sprite.update();

	#check to see if mob hit the player
	hits=pygame.sprite.spritecollide(player, mobs, True,pygame.sprite.collide_circle);
	for hit in hits:
		player.shield-=hit.damage;
		exp_an=Explosion(player.rect.center,"sm");
		all_sprite.add(exp_an);
		player_hide_sound.set_volume(MAX_VOLUME);
		player_hide_sound.play();

		if player.shield<=0:
			player_die_sound.set_volume(MAX_VOLUME);
			player_die_sound.play();
			dead_exp=Explosion(player.rect.center,"player");
			all_sprite.add(dead_exp);
			player.hide();
			player.lives-=1;
			player.shield=100;
			player.power=1;



	for hit in hits:
		newmobe(all_sprite,mobs);
    #check if bollt hite mobs
	hites=pygame.sprite.groupcollide(mobs, Bullets, True, True);
	for hit in hites:

		exp=random.choice(exp_sound);
		exp.set_volume(MAX_VOLUME);
		exp.play();
		exp_an=Explosion(hit.rect.center,"lg");
		all_sprite.add(exp_an);
		#score+=hit.score;

		#if random.random()>0.1:
		rand_number=random.randrange(1,1000);
		if rand_number>=950:#//1/20 7/20% 			
			pow=Powerup(hit.rect.center);
			all_sprite.add(pow);
			powerUPGroup.add(pow);
		elif (rand_number>155 and rand_number<160) and (player.lives<3):
			pow=Powerup(hit.rect.center,"newLife");
			all_sprite.add(pow);
			powerUPGroup.add(pow);	
		else:
			pow=Powerup(hit.rect.center,"coin");
			all_sprite.add(pow);
			powerUPGroup.add(pow);	
		newmobe(all_sprite,mobs);
	

	if player.lives==0 and not dead_exp.alive():
		game_over=True;
	hits=pygame.sprite.spritecollide(player, powerUPGroup, True);
	for hit in hits:
		if hit.type=="shield":
			player.shield+=random.randrange(5,20);
			powerup_sound["shield"].set_volume(MAX_VOLUME);
			powerup_sound["shield"].play();
			if player.shield>100:
				player.shield=100;

		if hit.type=="gun":
			player.powerup();
			powerup_sound["gun"].set_volume(MAX_VOLUME);
			powerup_sound["gun"].play();	
		if hit.type=="coin":
			score+=hit.score;	
			powerup_sound["coin"].set_volume(MAX_VOLUME);
			powerup_sound["coin"].play();	
		if hit.type=="newLife":
			player.lives+=1;
			if player.lives>3:
				player.lives=3;
			powerup_sound["newLife"].set_volume(MAX_VOLUME);	
			powerup_sound["newLife"].play();					
	#draw/render

	draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)
	all_sprite.draw(screen);
	draw_text(screen, str(score), 18, WIDTH//2, 10)
	
	#after drawing every thing flip to display the new chnge
	pygame.display.flip();
	clock.tick(FPS);
	total_frams+=1;
	if total_frams%(20*FPS)==0:
		harder+=1;
	print("bolts:",len(Bullets))	
pygame.quit();
quit();	
