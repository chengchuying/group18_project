import pygame
import random
import sys
from os import path

black = (0, 0, 0)
white = (255, 255, 255)
         

class Player():
    def __init__(self, text, x, y, font):
        self.hand = []  # 玩家手中的牌
        self.point = 0  # 玩家的點數
        self.surface = font.render(text + str(self.point), True, white)
        self.rect = self.surface.get_rect()
        self.x = x
        self.y = y

    def add_card(self, card):
        self.hand.append(card)
        # 更新玩家的點數

    def calculate_points(self):
        # 計算玩家的點數
        pass

    def reset(self):
        self.hand = []
        self.point = 0

class Guest(Player):
    def __init__(self, font):
        super().__init__("Guset", 100, 100, font)
        

class Dealer(Player):
    def __init__(self, font):
        super().__init__("Dealer", 100, 130, font)


class Card(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def flip(self):
        # 翻轉牌的狀態（正面或背面）
        pass
    # 其他牌的操作...

class Button(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.clicked = False
       

class StartButton(Button):
    def __init__(self):
        self.photos_dir = path.join(path.dirname(__file__), 'photos')
        image = pygame.image.load(path.join(self.photos_dir, 'start.png')).convert()
        image = pygame.transform.scale(image, (400, 200))
        position = (400, 300)
        super().__init__(image, position)

    def update(self):
        if self.clicked:
            self.kill()

    def draw(self, screen):
        if not self.clicked:
            screen.blit(self.image, self.rect) 


class FinishButton(Button):
    def __init__(self):
        self.cards_dir = path.join(path.dirname(__file__), 'cards')
        image = pygame.image.load(path.join(self.cards_dir, 'finish-button-png-2.png')).convert()
        image = pygame.transform.scale(image, (100, 40))
        position = (700, 150)
        super().__init__(image, position)

    def update(self):
        if self.clicked:
            self.kill()

    def draw(self, screen):
        if not self.clicked:
            screen.blit(self.image, self.rect)        


class PickButton(Button):
    def __init__(self):
        self.cards_dir = path.join(path.dirname(__file__), 'cards')
        image = pygame.image.load(path.join(self.cards_dir, 'pick.png')).convert()
        image = pygame.transform.scale(image, (100, 100))
        position = (650, 320)
        super().__init__(image, position)

    def update(self):
        pass


class BlackjackGame:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.run = False
        self.runs = True
        self.card1 = (400, 440)
        self.card2 = (430, 440)
        self.card3 = (460, 440)
        self.card4 = (490, 440)
        self.card5 = (520, 440)

    def load_resources(self):
        self.photos_dir = path.join(path.dirname(__file__), 'photos')
        self.cards_dir = path.join(path.dirname(__file__),'cards')
        self.background = pygame.image.load(path.join(self.photos_dir, '21points.jpg')).convert()
        self.background = pygame.transform.scale(self.background,(800,600))
        self.back = pygame.image.load(path.join(self.cards_dir,'{}.png'.format('back'))).convert()
        self.back = pygame.transform.scale(self.back,(80,150))
        self.Lose_png = pygame.image.load(path.join(self.cards_dir,'{}.png'.format('lose'))).convert_alpha()
        self.Lose_png = pygame.transform.scale(self.Lose_png,(800,600))
        self.Win_png = pygame.image.load(path.join(self.cards_dir,'{}.png'.format('win'))).convert_alpha()
        self.Win_png = pygame.transform.scale(self.Win_png,(800,600))
        self.Even_png = pygame.image.load(path.join(self.cards_dir,'{}.png'.format('even'))).convert_alpha()
        self.Even_png = pygame.transform.scale(self.Even_png,(300,150))
        
    def game_loop(self):
        self.all_sprites = pygame.sprite.Group()
        self.start_button = StartButton()
        self.finish_button = FinishButton()
        self.pick_button = PickButton()
        self.all_sprites.add(self.start_button)

        while self.runs:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runs = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.rect.collidepoint(mouse_pos):
                        # 點擊了開始按鈕的邏輯處理...
                        self.start_button.clicked = True
                        self.start_button.update()
                        self.all_sprites.add(self.pick_button)
                        self.all_sprites.update()
                    if self.pick_button.rect.collidepoint(mouse_pos):
                        # 點擊了抽牌按鈕的邏輯處理...
                        self.pick_button.clicked = True
                        self.pick_button.update()
                        self.update_game()
                        if self.finish_button not in self.all_sprites:
                            self.all_sprites.add(self.finish_button)
                        self.all_sprites.update()
                    if self.finish_button.rect.collidepoint(mouse_pos):
                        self.finish_button.clicked = True
                        self.finish_button.update()
                        self.update_game()
                        self.all_sprites.update()             

            self.screen.fill(black)
            self.screen.blit(self.background, (0, 0))

            if not self.start_button.clicked:
                font = pygame.font.Font(None, 36)
                text_surface = font.render("Welcome to Blackjack!!!!", True, white)
                text_rect = text_surface.get_rect()
                text_rect.center = (400, 150)
                self.screen.blit(text_surface, text_rect)
                self.start_button.draw(self.screen)
            else:
                self.guest = Guest(self.font)
                self.dealer = Dealer(self.font)
                


            self.start_button.draw(self.screen)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            pygame.display.flip()


    def update_game(self): 
    # 更新遊戲狀態和物件
        guest_points = self.guest.calculate_points()
        dealer_points = self.dealer.calculate_points()

        # 判斷輸贏條件
        if len(self.guest.hand)>=5 and guest_points <= 21:
            self.screen.blit(self.Win_png, (0, 0))
        elif guest_points > 21:
            self.screen.blit(self.Lose_png, (0, 0))
            # 顯示玩家勝利的畫面，或執行相應的遊戲邏輯
        elif dealer_points > 21:
            self.screen.blit(self.Win_png, (0, 0))
            # 顯示莊家勝利的畫面，或執行相應的遊戲邏輯
        elif guest_points < dealer_points:
            self.screen.blit(self.Lose_png, (0, 0))
            # 顯示莊家勝利的畫面，或執行相應的遊戲邏輯
        elif guest_points > dealer_points:
            self.screen.blit(self.Lose_png, (0, 0))
            # 顯示玩家勝利的畫面，或執行相應的遊戲邏輯
        else:
            print("It's a tie!")
            # 顯示平局的畫面，或執行相應的遊戲邏輯

        self.pick_button.kill()
        self.finish_button.kill()

    def draw_game(self):
        # 繪製遊戲畫面
        self.all_sprites.draw(self.screen)

        

# 主程式
def main():
    game = BlackjackGame()
    game.load_resources()
    game.game_loop()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

