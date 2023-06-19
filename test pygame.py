import pygame
import random
import sys
from os import path

pygame.init()
photos_dir = path.join(path.dirname(__file__),'photos')
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
Fps = 60
run = False
runs = True
Black = (0,0,0)
Card1=(400,440)
Card2=(430,440)
Card3=(460,440)
Card4=(490,440)
Card5=(520,440)
White = (255,255,255)
show_result = True
#load poke
background = pygame.image.load(path.join(photos_dir,'21points.jpg')).convert()
startbutton = pygame.image.load(path.join(photos_dir,'start.png')).convert()
startbutton = pygame.transform.scale(startbutton,(400,200))
background = pygame.transform.scale(background,(800,600))
cards_dir = path.join(path.dirname(__file__),'cards')
back = pygame.image.load(path.join(cards_dir,'{}.png'.format('back'))).convert()
back = pygame.transform.scale(back,(80,150))
finish_png = pygame.image.load(path.join(cards_dir,'{}.png'.format('finish-button-png-2'))).convert()
finish_png = pygame.transform.scale(finish_png,(100,40))
Lose_png = pygame.image.load(path.join(cards_dir,'{}.png'.format('lose'))).convert_alpha()
Lose_png = pygame.transform.scale(Lose_png,(800,600))
Win_png = pygame.image.load(path.join(cards_dir,'{}.png'.format('win'))).convert_alpha()
Win_png = pygame.transform.scale(Win_png,(800,600))
Even_png = pygame.image.load(path.join(cards_dir,'{}.png'.format('even'))).convert_alpha()
Even_png = pygame.transform.scale(Even_png,(300,150))
pick_card_png = pygame.image.load(path.join(cards_dir,'{}.png'.format('pick'))).convert()
pick_card_png = pygame.transform.scale(pick_card_png,(100,100))

#輸贏
Lose = False
Win = False
Even = False
global Ace
Ace = False
Five = False
#抽牌
pickcard = True
pos = 1
poke_list = [str(x) for x in range(1,53)]
player1 = []
player2 = []
for i in range(5):
    id = random.choice(poke_list)
    img = pygame.image.load(path.join(cards_dir,'{}.png'.format(id))).convert()
    img = pygame.transform.scale(img,(80,150))
    poke_list.remove(id)
    if int(id)%13 == 0 or int(id)%13 == 12 or int(id)%13 == 11:
        id = 10
    elif int(id)%13 == 1:
        id = 11
    else:
        id = int(id)%13
    img = (img,id)
    player1.append(img)
for i in range(5):
    id = random.choice(poke_list)
    img = pygame.image.load(path.join(cards_dir,'{}.png'.format(id))).convert()
    img = pygame.transform.scale(img,(70,150))
    poke_list.remove(id) 
    if int(id)%13 == 0 or int(id)%13 == 11 or int(id)%13 == 12:
        id = 10
    elif int(id)%13 == 1:
        id = 11
    else:
        id = int(id)%13
    img = (img,id)
    player2.append(img)
player1_point = 0
player2_point = 0

card_pos = [Card1,Card2,Card3,Card4,Card5]
class Start(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = startbutton
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = (400,300)
        self.clicked = False
    def update(self):
        global player1_point
        global player2_point
        global player1_rect
        global player1_surface
        global player2_rect
        global player2_surface
        global F
        global Ace
        self.mouse_x,self.mouse_y = pygame.mouse.get_pos()
        if self.mouse_x > self.rect.left and self.mouse_x < self.rect.right and self.mouse_y < self.rect.bottom and self.mouse_y > self.rect.top:
            self.clicked = True
            player1_surface = font.render("Guest:"+str(player1_point),True, (255, 255, 255))
            player1_rect = player1_surface.get_rect()
            player1_rect.centerx = 100
            player1_rect.centery = 100
            player2_surface = font.render("Dealer:"+str(player2_point),True, (255, 255, 255))
            player2_rect = player2_surface.get_rect()
            player2_rect.centerx = 100
            player2_rect.centery = 130
            card = Card(player2[0][0],(399,185))
            card2 = Card(back,(450,185))
            all_sprite.add(card)
            all_sprite.add(card2)
            card = Card(player1[0][0],card_pos[0])
            card2 = covercard(back,player1[1][0],card_pos[1],player1[1][1])
            all_sprite.add(card)
            all_sprite.add(card2)
            player1_point = player1[0][1]
            if player1_point ==11:
                Ace=True
            player2_point = player2[0][1] 
            self.kill()

class pick_card(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pick_card_png
        self.rect = self.image.get_rect()
        self.rect.center = (650,320)
    def update(self):
        global player1_point,Lose,pos,F,Ace,Five
        self.mouse_x,self.mouse_y = pygame.mouse.get_pos()
        if self.mouse_x > self.rect.left and self.mouse_x < self.rect.right and self.mouse_y < self.rect.bottom and self.mouse_y > self.rect.top:
            if int(player1[pos][1])==11:
                Ace=True
            pos += 1
            card  = Card(player1[pos][0],card_pos[pos])
            all_sprite.add(card)
            player1_point = player1_point + int(player1[pos][1])
            if player1_point >21:
                if Ace==True:
                    player1_point-=10
                    Ace=False
                    if player1_point >21:
                        print('Lose')
                        Lose = True
                        self.kill()
                        F.kill()
                else:
                    print('Lose')
                    Lose = True
                    self.kill()
                    F.kill()
            if pos == 4:
                Five = True
                self.kill()
            

class Card(pygame.sprite.Sprite):
    def __init__(self,image,position):
       pygame.sprite.Sprite.__init__(self)
       self.image = image
       self.rect = self.image.get_rect()
       self.rect.center = position
class covercard(pygame.sprite.Sprite):
    def __init__(self,back_image,image,position,point):
       pygame.sprite.Sprite.__init__(self)
       self.image = back_image
       self.rect = self.image.get_rect()
       self.rect.center = position
       self.point = point
       self.image_org = image
    def update(self):
        global player1_point,Lose,pick,pickcard,F,Ace,Win
        if pickcard:
            self.mouse_x,self.mouse_y = pygame.mouse.get_pos()
            if self.mouse_x > self.rect.left and self.mouse_x < self.rect.right and self.mouse_y < self.rect.bottom and self.mouse_y > self.rect.top:
                pick = pick_card()
                all_sprite.add(pick)
                F = Finish()
                all_sprite.add(F)
                pickcard = False
                self.image = self.image_org
                player1_point = player1_point + int(self.point)
                if self.point==11:
                    Ace = True
                self.point =  0
                if player1_point ==21:
                    print('Win')
                    Win = True
                if len(player1) >= 5 and player1_point <= 21:
                    Five = True    
                if player1_point >21:
                    if Ace==True:
                        player1_point -= 10
                        Ace=False
                        if player1_point >21:
                            print('Lose')
                            Lose = True
                    else:    
                        print('Lose')
                        Lose = True
class Finish(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = finish_png
       self.rect = self.image.get_rect()
       self.rect.center = (700,150)
    def update(self):
        global player2_point,Win,Lose,Even,pick,Ace
        self.mouse_x,self.mouse_y = pygame.mouse.get_pos()
        if self.mouse_x > self.rect.left and self.mouse_x < self.rect.right and self.mouse_y < self.rect.bottom and self.mouse_y > self.rect.top:
            player2_point += player2[1][1]
            if player2[1][1]==11:
                Ace=True
            for i in range(2,5):
                if  player2_point < 17:
                     player2_point += player2[i][1]
                     if player2[i][1]==11:
                         Ace=True
            if player2_point > 21:
                if Ace == True:
                    player2_point -=10
                    Ace = False
                    if player2_point > 21:
                        print('Win')
                        Win = True
                else:
                    print('Win')
                    Win = True
            elif Five:
                print('Win')
                Win = True        
            elif player1_point < player2_point:
                print('Lose')
                Lose = True
            elif player1_point > player2_point:
                print('Win')
                Win = True
            else:
                print('even')
                Even =True
            self.kill()
            pick.kill()
all_sprite = pygame.sprite.Group()
start = Start()
startbuttons = pygame.sprite.Group()
all_sprite.add(start)
startbuttons.add(start)
v = False
while runs:
    clock.tick(Fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runs = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            startbuttons.update()
            all_sprite.update()
            #show_result = False
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    if not start.clicked:
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Welcome to Blackjack!!!!", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (400, 150)
        screen.blit(text_surface, text_rect)
    if start.clicked:
        player1_surface = font.render("Guest:"+str(player1_point),True, (255, 255, 255))
        screen.blit(player1_surface, player1_rect)
        player2_surface = font.render("Dealer:"+str(player2_point),True, (255, 255, 255))
        screen.blit(player2_surface, player2_rect)
    startbuttons.draw(screen)
    all_sprite.draw(screen)
    if show_result:
        if Win:
            screen.blit(Win_png, (0, 0))
        elif Lose:
            screen.blit(Lose_png, (0, 0))
        elif Even:
            screen.blit(Even_png, (0, 0))
    

    #print(pygame.mouse.get_pos())
    #print(player1_point)
    #print(player2_point)
    pygame.display.flip()
print('Player:',player1_point,'Bookmaker:',player2_point)

pygame.quit()
