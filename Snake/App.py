import time
import random
import pygame


class App:
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.mylist = [(650, 300), (600, 300), (550, 300), (500, 300), (450, 300)]
        self.direction = "right"
        self.food = None
        self.foodisthere = False
        self.death = False
        self.soundon = None
        self.background = None

    def run(self):
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("jojo.mp3"), -1)
        pygame.mixer.Channel(0).set_volume(0.3)
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("The Great Serpent")
        self.clock = pygame.time.Clock()
        self.running = True
        self.getfood()
        self.soundon = True
        self.background = pygame.image.load("sans.jpg")

    def update(self):
        self.events()
        if self.direction == "right":
            self.mylist.insert(0, (self.mylist[0][0] + 50, self.mylist[0][1]))
            self.mylist = self.mylist[:-1]
        if self.direction == "left":
            self.mylist.insert(0, (self.mylist[0][0] - 50, self.mylist[0][1]))
            self.mylist = self.mylist[:-1]
        if self.direction == "up":
            self.mylist.insert(0, (self.mylist[0][0], self.mylist[0][1] - 50))
            self.mylist = self.mylist[:-1]
        if self.direction == "down":
            self.mylist.insert(0, (self.mylist[0][0], self.mylist[0][1] + 50))
            self.mylist = self.mylist[:-1]
        time.sleep(0.2)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.direction != "down":
                    self.direction = "up"
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.direction != "up":
                    self.direction = "down"
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.direction != "right":
                    self.direction = "left"
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.direction != "left":
                    self.direction = "right"
                if event.key == pygame.K_m:
                    if self.soundon is True:
                        self.soundon = False
                        pygame.mixer.Channel(0).pause()
                    else:
                        self.soundon = True
                        pygame.mixer.init()
                        pygame.mixer.Channel(0).unpause()

        if self.mylist[0][1] < 0 or self.mylist[0][1] + 50 > 700 or self.mylist[0][0] < 0 or \
                self.mylist[0][0] + 50 > 1200:
            self.death = True

        for i in range(1, len(self.mylist)):
            if self.mylist[0][0] == self.mylist[i][0] and self.mylist[0][1] == self.mylist[i][1]:
                self.death = True

        # if (self.mylist[0][0] + 25, self.mylist[0][1] + 25) == self.food:  # for circle
        if (self.mylist[0][0], self.mylist[0][1]) == self.food:
            self.foodisthere = False
            self.mylist.append((self.mylist[-1][0], self.mylist[-1][1]))

    def render(self):
        self.screen.blit(self.background, [0, 0])
        if self.foodisthere:
            # pygame.draw.circle(self.screen, "green", self.food, 20)  # for circle
            self.screen.blit(pygame.image.load("apple.png"), self.food)
        else:
            self.getfood()
            # pygame.draw.circle(self.screen, "green", self.food, 20)  # for circle
            self.screen.blit(pygame.image.load("apple.png"), self.food)
            self.foodisthere = True

        for i in self.mylist:
            if self.mylist[0] == i:
                color = "cyan"
            else:
                color = "red"
            pygame.draw.rect(self.screen, color, (i[0], i[1], 50, 50), 2)
        if self.death:
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("deathsound.mp3"))
            self.screen.blit(pygame.image.load("death.jpg"), (0, 0))
        pygame.display.flip()
        self.clock.tick(60)
        if self.death:
            time.sleep(5)
            self.running = False

    def getfood(self):
        # foodlistx = [x for x in range(1201) if x % 25 == 0 and str(x)[-1] != "0"]  # for circle
        # foodlisty = [x for x in range(701) if x % 25 == 0 and str(x)[-1] != "0"]
        foodlistx = [x for x in range(1200) if x % 50 == 0]  # for image (square)
        foodlisty = [x for x in range(700) if x % 50 == 0]
        self.foodx = foodlistx[random.randint(0, len(foodlistx) - 1)]
        self.foody = foodlisty[random.randint(0, len(foodlisty) - 1)]
        mylistx = [x[0] for x in self.mylist]
        mylisty = [x[1] for x in self.mylist]
        # while self.foodx - 25 in mylistx and self.foody - 25 in mylisty:  # for circle
        while self.foodx in mylistx and self.foody in mylisty:
            self.foodx = foodlistx[random.randint(0, len(foodlistx) - 1)]
            self.foody = foodlisty[random.randint(0, len(foodlisty) - 1)]
        self.food = (self.foodx, self.foody)

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
