import random
import pygame as pg
import math as math
import patterns as pt

pg.init()
pg.font.init()


class Board:    # This controlls everything that happens on the display
    def __init__(self):
        self.balls = []  # contains all the balls on the screen
        self.screen = None
        self.settings = True # Settings mode
        self.beginning = True   # The menu will be shown if its the beginning
        self.switch = None  # A pic taken before switching modes
        self.end = False    # game ends
        self.help = False   # when user clicks help
        self.played = False # prevents an error occuring when clicking back
        self.stage = None   # current stage
        self.stage2_unlocked = False
        self.stage3_unlocked = False
        self.stage4_unlocked = False
        self.stage5_unlocked = False
        self.stage6_unlocked = False
        self.s1_highscore = 0
        self.s2_highscore = 0
        self.s3_highscore = 0
        self.s4_highscore = 0
        self.s5_highscore = 0
        self.s6_highscore = 0
        self.bonus = 0
        self.state = 'RUNNING'
        self.gun = Gun()    # the deck
        self.radius = 20  # radius of circle
        self.colours = [pg.Color('red'), pg.Color('yellow'), pg.Color('green'), pg.Color('skyblue'), pg.Color(
                        'purple'), pg.Color('brown')]  # all the colours for the balls
        self.points = []  # all the points where the balls can be located
        self.next_colour1 = random.choice(self.colours)  # the next three colours of the ball
        self.next_colour2 = random.choice(self.colours)
        self.next_colour3 = random.choice(self.colours)
        self.width = 2 * self.radius * 10  # size of the screen
        self.height = int(20 * 3 ** 0.5 * self.radius)
        self.angle = math.pi / 2
        self.score = 0

        # buttons
        self.settings_rect = pg.Rect(self.width - 40, self.height - 40, 30, 30)
        self.pause_rect = pg.Rect(self.width - 80, self.height - 40, 30, 30)

        # pictures
        self.music_icon = pg.transform.scale(pg.image.load('music_icon.jpg'), (30, 30))
        self.settings_icon = pg.transform.scale(pg.image.load('settings_icon.png'), (30, 30))
        self.pause_icon = pg.transform.scale(pg.image.load('pause_icon.jpg'), (30, 30))
        self.gameover_icon = pg.transform.scale(pg.image.load('game_over.png'), (320, 240))
        self.help_icon = pg.transform.scale(pg.image.load('help.png'), (self.width, self.height))

        # words
        self.comic_sans = pg.font.SysFont("comic Sans MS", 15)

        #sounds
        self.collide_sound = pg.mixer.Sound("collide.wav")

    def background_functions(self): # this function draws the background
        if not self.end:
            if self.settings:
                settings.draw()
                if self.help:
                    self.screen.blit(self.help_icon, (0, 0))
            else:
                self.screen.blit(settings.b_pic(), (0, 0))

    def draw(self, settings):
        if not self.settings:
            for ball in self.balls: # draw each ball at its current location
                ball.draw()
            self.gun.draw(self.screen, self.next_colour1, self.next_colour2, self.next_colour3, int(self.width / 2),
                          self.height, self.radius, self.angle) # draws the deck

            pg.draw.line(self.screen, (255, 255, 255),
                         (self.points[0][0][0] - self.radius, self.points[0][0][1] - self.radius),
                         (self.points[0][-1][0] + self.radius, self.points[0][-1][1] - self.radius), 3)  # the 'ceiling'

            # the buttons
            self.screen.blit(self.settings_icon, (self.settings_rect.x, self.settings_rect.y))
            self.screen.blit(self.pause_icon, (self.pause_rect.x, self.pause_rect.y))
            self.screen.blit(self.comic_sans.render("score: " + str(self.score), True, (255, 255, 255)),
                             (5, self.height - 30))
            self.screen.blit(
                self.comic_sans.render('highest score: ' + str(eval('self.s' + str(self.stage) + '_highscore')), True,
                                       (255, 255, 255)), (5, self.height - 60))
            self.screen.blit(self.comic_sans.render("Stage: " + str(self.stage), True, (255, 255, 255)),
                             (5, self.height - 90))

    def add_ball(self, ball):
        ball.board = self
        self.balls.append(ball)

    def mouse_down(self, event, mx, my, settings):
        if not self.end:
            mode = []  # the user will select the game mode
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.settings:
                    if self.beginning:
                        if settings.play_rect.collidepoint(mx, my): # the button to begin the game
                            self.beginning = False
                    elif self.help:
                        self.help = False
                    else:
                        if settings.music_rect.collidepoint(mx, my): # the button to pause or play music
                            if settings.music:
                                settings.music = False
                            else:
                                settings.music = True

                        elif settings.slide_rect.collidepoint(mx, my): # the button to adjust difficulty
                            settings.difficulty = round(
                                (mx - settings.slide_rect.x) / settings.slide_rect.width * 5 + 1, 0)

                        elif settings.mode1_rect.collidepoint(mx, my): # the buttons to select mode
                            mode = pt.normal
                            self.stage = 1
                        elif settings.mode2_rect.collidepoint(mx, my) and self.stage2_unlocked:
                            mode = pt.pyrimid
                            self.stage = 2
                        elif settings.mode3_rect.collidepoint(mx, my) and self.stage3_unlocked:
                            mode = pt.hexagon
                            self.stage = 3
                        elif settings.mode4_rect.collidepoint(mx, my) and self.stage4_unlocked:
                            mode = pt.star
                            self.stage = 4
                        elif settings.mode5_rect.collidepoint(mx, my) and self.stage5_unlocked:
                            mode = pt.poles
                            self.stage = 5
                        elif settings.mode6_rect.collidepoint(mx, my) and self.stage6_unlocked:
                            mode = pt.x
                            self.stage = 6

                        elif settings.back_rect.collidepoint(mx, my) and not self.beginning: # the button to exit setting
                            if self.played:
                                self.settings = False
                                screen.blit(self.switch, (0, 0))
                            else:
                                self.beginning = True

                        elif settings.help_rect.collidepoint(mx, my): # the button for help
                            if not self.help:
                                self.help = True

                    if mode != []: # if the user selects a new mode
                        self.beginning = False
                        self.played = True
                        self.balls = []
                        self.points = []
                        refresh_points(self)
                        for x in range(int(len(self.points) / 2.5)):
                            for y in range(len(self.points[x])):
                                if mode[x][y] == 1: # the balls will be placed according to the stage layout
                                    ball = Ball(self.screen, random.choice(self.colours), 0, self.radius)
                                    ball.x, ball.y = self.points[x][y]
                                    ball.speed = 0
                                    ball.board = board
                                    board.balls.append(ball)
                        self.settings = False
                        self.score = 0

                else:
                    if self.settings_rect.collidepoint(mx, my) and self.state == 'RUNNING': # the button to enter settings
                        self.settings = True
                        self.switch = self.screen.copy()

                    if self.pause_rect.collidepoint(mx, my): # the button to pause game
                        if self.state == 'RUNNING':
                            self.state = 'PAUSE'
                        else:
                            self.state = 'RUNNING'

    def mouse_move(self, mx, my, settings): # the buttons are highlighted when the mouse touches it
        if self.settings:
            if self.beginning:
                if settings.play_rect.collidepoint(mx, my):
                    pg.draw.rect(self.screen, (255, 0, 0), settings.play_rect, 3)
            elif not self.beginning and not self.help:
                if settings.mode1_rect.collidepoint(mx, my):
                    pg.draw.rect(self.screen, (255, 0, 0), settings.mode1_rect, 3)
                elif settings.mode2_rect.collidepoint(mx, my) and self.stage2_unlocked:
                    pg.draw.rect(self.screen, (255, 0, 0), settings.mode2_rect, 3)
                elif settings.mode3_rect.collidepoint(mx, my) and self.stage3_unlocked:
                    pg.draw.rect(self.screen, (255, 0, 0), settings.mode3_rect, 3)
                elif settings.mode4_rect.collidepoint(mx, my) and self.stage4_unlocked:
                    pg.draw.rect(self.screen, (255, 0, 0), settings.mode4_rect, 3)
                elif settings.mode5_rect.collidepoint(mx, my) and self.stage5_unlocked:
                    pg.draw.rect(self.screen, (255, 0, 0), settings.mode5_rect, 3)
                elif settings.mode6_rect.collidepoint(mx, my) and self.stage6_unlocked:
                    pg.draw.rect(self.screen, (255, 0, 0), settings.mode6_rect, 3)
                elif settings.back_rect.collidepoint(mx, my) and not self.beginning:
                    pg.draw.circle(self.screen, (255, 0, 0), (int(settings.back_rect.x + settings.back_rect.width / 2),
                                                              int(
                                                                  settings.back_rect.y + settings.back_rect.height / 2)),
                                   int(settings.back_rect.height / 2), 3)  # the back button is a circle
                elif settings.help_rect.collidepoint(mx, my):
                    pg.draw.rect(self.screen, (255, 0, 0), settings.help_rect, 3)
        else:
            if self.settings_rect.collidepoint(mx, my):
                pg.draw.rect(self.screen, (255, 0, 0), self.settings_rect, 3)
            elif self.pause_rect.collidepoint(mx, my):
                pg.draw.rect(self.screen, (255, 0, 0), self.pause_rect, 3)

    def aim(self): # this allows the user to aim the gun with arrow keys
        if not self.settings:
            left = pg.key.get_pressed()[pg.K_LEFT]
            right = pg.key.get_pressed()[pg.K_RIGHT]
            if left == 1 and self.angle > math.pi / 6:
                self.angle -= math.pi / 90 * 1.5 # multiply by 1.5 to move it faster
            elif right == 1 and self.angle < 5 * math.pi / 6:
                self.angle += math.pi / 90 * 1.5

    def key_pressed(self, event, settings, backgrounds, music):
        if not self.end:
            if not self.settings:
                shot = True
                if event.key == pg.K_SPACE: # adds a moving ball to the list when space key is pressed
                    for b in self.balls:
                        if b.speed == 1:
                            shot = False  # will not shoot again if a ball is already shot
                    if shot:
                        ball = Ball(self.screen, self.next_colour1, self.angle, self.radius)
                        ball.x = self.width / 2
                        ball.y = self.height
                        self.add_ball(ball)
                        self.next_colour1 = self.next_colour2  # the colours up next are shifted
                        self.next_colour2 = self.next_colour3
                        self.next_colour3 = random.choice(self.colours)  # no more shifts, takes a new tuple
        else:
            if event.key == pg.K_r:  # everything will be reset when user clicks r after the game ends
                self.end = False
                self.settings = True
                self.balls = []
                self.points = []
                settings.background = pg.image.load(random.choice(backgrounds))

    def collide(self):
        deletes = []  # the balls in contact that need to be deleted
        for ball in self.balls:
            if ball.speed == 1:
                if 0 > ball.x - self.radius or ball.x + self.radius > self.width:
                    ball.angle = math.pi - ball.angle  # the ball will bounce of the wall until it hits the top
                if self.points[0][0][1] >= ball.y:  # the ball will not go further than the first row
                    ball.speed = 0
                    self.ball_in_place(ball)  # moves the ball into the nearest point
                    self.mark_ball(ball)

                self.collide_ball(ball)

            for b in self.balls:
                if b.mark:
                    deletes.append(b)   # all the balls marked will be deleted
            if len(deletes) >= 3:   # only delete balls if 3 or more will be deleted
                self.collide_sound.play()
                self.bonus = len(deletes)-3 # bonus points are given for shooting down more than 3 balls
                for b in deletes:
                    b.speed = -1
                if self.row_one() != []:
                    for b in self.row_one():
                        if b.speed == 0:
                            self.hang_ball(b)   # the balls left in space will be deleted too
                for b in self.balls:
                    if not b.hang and b not in deletes:
                        b.speed = -1
                        self.bonus += 1

        for b in self.balls:
            b.mark = False
            b.hang = False

    def collide_ball(self, ball):
        for ball2 in self.balls:  # checks the collision of the ball to other balls
            if ball != ball2 and ball2.speed == 0:
                distance = math.hypot((ball.x - ball2.x), (ball.y - ball2.y))  # finds the distance between the balls
                if distance <= self.radius * 2:  # if distance is less than diameter, the balls have touched
                    ball.speed = 0
                    self.ball_in_place(ball)
                    self.mark_ball(ball)

    def ball_in_place(self, ball):
        dis = 100
        pos = []
        for x in range(len(self.points)):
            for y in range(len(self.points[x])):
                dif = math.hypot((ball.x - ball.board.points[x][y][0]), (ball.y - ball.board.points[x][y][1]))
                if dif <= dis:  # finds the nearest point and move the ball there
                    dis = dif
                    pos = self.points[x][y]
                    ball.row = x
                    ball.col = y
        ball.collide = False
        ball.x, ball.y = pos

    def move_ball(self):    # moves the balls with a speed of 1
        for ball in self.balls:
            if ball.speed == 1:
                ball.x -= 10 * math.cos(ball.angle)
                ball.y -= 10 * math.sin(ball.angle)

    def mark_ball(self, ball):
        ball.mark = True
        for b in ball.neighbour():
            if not b.mark and b.colour == ball.colour:  # balls with the same colour that touch the selected ball will be marked
                self.mark_ball(b)

    def row_one(self):  # finds the balls in the first row
        balls = []
        for b in self.balls:
            for i in range(len(self.points[0])):
                if b.x == self.points[0][i][0] and b.y == self.points[0][i][1]:
                    balls.append(b)
        return balls

    def hang_ball(self, ball):  # finds the balls that are not in mid air
        ball.hang = True
        for b in ball.neighbour():
            if not b.hang and b.speed == 0:
                self.hang_ball(b)

    def drop_ball(self):
        drop = 0
        for b in self.balls:    # balls with speed -1 means that it will be deleted
            if b.speed < 0:
                drop += 1
                b.y += 15   # the deleted balls will drop to the bottom of the screen
                if b.y >= self.height:
                    self.balls.remove(b)
                    self.score += 100 + 50*self.bonus  # each ball eliminated counts as a score of 100, bonus if >3 balls
                    if self.score > self.s1_highscore and self.stage == 1:  # updates the high score
                        self.s1_highscore = self.score
                    elif self.score > self.s2_highscore and self.stage == 2:
                        self.s2_highscore = self.score
                    elif self.score > self.s3_highscore and self.stage == 3:
                        self.s3_highscore = self.score
                    elif self.score > self.s4_highscore and self.stage == 4:
                        self.s4_highscore = self.score
                    elif self.score > self.s5_highscore and self.stage == 5:
                        self.s5_highscore = self.score
                    elif self.score > self.s6_highscore and self.stage == 6:
                        self.s6_highscore = self.score
        if drop == 0:
            self.bonus = 0

    def game_over(self): # determines when will the game end
        game_ball = len(self.balls)
        end_point = int(self.height * 5 / 6)
        if not self.settings:
            pg.draw.line(self.screen, (255, 255, 255), (0, end_point), (self.width, end_point),
                         3)  # the game will end if a ball touches this line
        for b in self.balls:
            if b.speed == 0 and b.y + self.radius > end_point:
                self.end = True
        if game_ball == 0 and not self.settings:  # the game ends when there is no balls
            self.end = True
            if self.stage == 1:
                self.stage2_unlocked = True
            elif self.stage == 2:
                self.stage3_unlocked = True
            elif self.stage == 3:
                self.stage4_unlocked = True
            elif self.stage == 4:
                self.stage5_unlocked = True
            elif self.stage == 5:
                self.stage6_unlocked = True

        if self.end:
            self.screen.blit(self.gameover_icon, (self.width / 2 - 160, self.height / 2 - 120))


class Ball: # each of the balls in Board
    def __init__(self, screen, colour, angle, radius):
        self.speed = 1  # speed 1 = moving, speed 0 = not moving, speed -1 = dropping
        self.colour = colour # the ball's colour
        self.angle = angle # the angle the ball will be moving in when speed = 1
        self.x = 0  # the coordinates of the ball
        self.y = 0
        self.radius = radius
        self.screen = screen
        self.board = None
        self.collide = False
        self.mark = False
        self.hang = False
        self.board = None
        self.row = 0
        self.col = 0

    def draw(self): # draws itself
        pg.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.radius)
        pg.draw.circle(self.screen, (255, 255, 255), (int(self.x + self.radius / 2), int(self.y - self.radius / 2)),
                       int(self.radius / 4))
        pg.draw.circle(self.screen, 0, (int(self.x), int(self.y)), self.radius, 1)

    def neighbour(self):    # find the neighbouring spots
        pos = [0, 0]
        poses = []
        balls = []
        for i in range(len(self.board.points)): # finds where in the point is the selected ball
            for ii in range(len(self.board.points[i])):
                if self.board.points[i][ii] == [self.x, self.y]:
                    pos = [i, ii]
                    break

        if pos[0] % 2 == 0: # find all the points that are next to the points of the current ball
            if pos[0] == 0: # if first row
                if pos[1] == 0:     # if first ball in row
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] + 1, pos[1]])
                elif pos[1] == 9:   # if last point in row
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0] + 1, pos[1] - 1])
                else:
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] + 1, pos[1]])
                    poses.append([pos[0] + 1, pos[1] - 1])

            else:
                if pos[1] == 0: # if first ball in row
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] + 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1]])
                elif pos[1] == 9: # if last point in row
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0] + 1, pos[1] - 1])
                    poses.append([pos[0] - 1, pos[1] - 1])
                else:
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] + 1, pos[1]])
                    poses.append([pos[0] + 1, pos[1] - 1])
                    poses.append([pos[0] - 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1] - 1])
        else:
            if pos[0] == 19: # if last row
                if pos[1] == 0: # if first ball in row
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] - 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1] + 1])
                elif pos[1] == 9: # if last point in row
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0] - 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1] + 1])
                else:
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] - 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1] + 1])

            else:
                if pos[1] == 0: # if first ball
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] + 1, pos[1]])
                    poses.append([pos[0] + 1, pos[1] + 1])
                    poses.append([pos[0] - 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1] + 1])
                elif pos[1] == 8: # if last point in row
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0] + 1, pos[1]])
                    poses.append([pos[0] + 1, pos[1] + 1])
                    poses.append([pos[0] - 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1] + 1])
                else:
                    poses.append([pos[0], pos[1] - 1])
                    poses.append([pos[0], pos[1] + 1])
                    poses.append([pos[0] + 1, pos[1]])
                    poses.append([pos[0] + 1, pos[1] + 1])
                    poses.append([pos[0] - 1, pos[1]])
                    poses.append([pos[0] - 1, pos[1] + 1])

        for i in range(len(poses)): # determine if there is a ball in the neibouring points
            index1 = poses[i][0]
            index2 = poses[i][1]
            for b in self.board.balls:
                if b.x == self.board.points[index1][index2][0] and b.y == self.board.points[index1][index2][1]:
                    balls.append(b)
        return balls


class Gun:
    def __init__(self):
        self.length = 100    # the length of the gun

    def draw(self, screen, colour1, colour2, colour3, x, y, radius, angle): # draws the gun
        pg.draw.circle(screen, colour1, (x, y), radius)
        pg.draw.circle(screen, colour2, (x - radius * 2, y), radius)
        pg.draw.circle(screen, colour3, (x - radius * 4, y), radius)
        if angle == math.pi / 2:    # if the gun points at a 90 degree angle from bottom screen
            pg.draw.line(screen, 0, (x, y), (x, y - self.length), 5)
        else:
            new_x, new_y = x - self.length * math.cos(angle), y - self.length * math.sin(angle)
            pg.draw.line(screen, 0, (x, y), (new_x, new_y), 5)


class Settings: # this is where the user gets to personalize the game
    def __init__(self, board):
        self.background = None  # the background image
        self.music = True   # if music is playing or not
        self.difficulty = 1 # how fast the balls move downwards
        self.board = board
        self.play_music = 0

        # buttons
        self.music_rect = pg.Rect(10, 10, 50, 50)
        self.difficulty_rect = pg.Rect(70, 10, 150, 50)
        self.slide_rect = pg.Rect(80, 33, 130, 4)
        self.mode1_rect = pg.Rect(board.width / 2 - 110, 100, 100, 40)
        self.mode2_rect = pg.Rect(board.width / 2 + 10, 100, 100, 40)
        self.mode3_rect = pg.Rect(board.width / 2 - 110, 160, 100, 40)
        self.mode4_rect = pg.Rect(board.width / 2 + 10, 160, 100, 40)
        self.mode5_rect = pg.Rect(board.width / 2 - 110, 220, 100, 40)
        self.mode6_rect = pg.Rect(board.width / 2 + 10, 220, 100, 40)
        self.back_rect = pg.Rect(20, board.height - 60, 50, 50)
        self.play_rect = pg.Rect(board.width / 2 - 100, board.height * 3 / 4 - 50, 200, 100)
        self.help_rect = pg.Rect(board.width - 30, 10, 20, 20)

        # pictures
        self.menu = pg.transform.scale(pg.image.load('bubbles.png'), (self.board.width, self.board.height))
        self.music_icon = pg.transform.scale(pg.image.load('music_icon.jpg'), (50, 50))
        self.back_icon = pg.transform.scale(pg.image.load('back_icon.png'), (50, 50))
        self.play_game_icon = pg.transform.scale(pg.image.load('play_game_icon.png'), (200, 100))
        self.mode1_icon = pg.transform.scale(pg.image.load('stage1.png'), (100, 40))
        self.mode2_icon = pg.transform.scale(pg.image.load('stage2.png'), (100, 40))
        self.mode3_icon = pg.transform.scale(pg.image.load('stage3.png'), (100, 40))
        self.mode4_icon = pg.transform.scale(pg.image.load('stage4.png'), (100, 40))
        self.mode5_icon = pg.transform.scale(pg.image.load('stage5.png'), (100, 40))
        self.mode6_icon = pg.transform.scale(pg.image.load('stage6.png'), (100, 40))
        self.help_icon = pg.transform.scale(pg.image.load('help_icon.png'), (20, 20))
        self.lock_icon = pg.transform.scale(pg.image.load('lock.png'), (40, 40))

    def b_pic(self): # transforms the scale of the background image to fit the screen
        background = pg.transform.scale(self.background, (self.board.width, self.board.height))
        return background

    def draw(self):# draws itself
        if not self.board.beginning:    # the settings screen
            self.board.screen.blit(self.b_pic(), (0, 0))

            circle_x = int(self.slide_rect.x + self.slide_rect.width / 5 * (self.difficulty - 1))
            circle_y = int(self.slide_rect.y + self.slide_rect.height / 2)  # a circle will indicate the difficulty
            self.board.screen.blit(self.music_icon, (self.music_rect.x, self.music_rect.y))
            pg.draw.rect(self.board.screen, (255, 255, 255), self.difficulty_rect)
            pg.draw.rect(self.board.screen, (100, 100, 100), self.difficulty_rect, 3)
            pg.draw.rect(self.board.screen, (100, 100, 100), self.slide_rect)
            pg.draw.circle(self.board.screen, 0, (circle_x, circle_y), 7)

            self.board.screen.blit(self.mode1_icon, (self.mode1_rect.x, self.mode1_rect.y))  # all the game modes
            self.board.screen.blit(self.mode2_icon, (self.mode2_rect.x, self.mode2_rect.y))
            self.board.screen.blit(self.mode3_icon, (self.mode3_rect.x, self.mode3_rect.y))
            self.board.screen.blit(self.mode4_icon, (self.mode4_rect.x, self.mode4_rect.y))
            self.board.screen.blit(self.mode5_icon, (self.mode5_rect.x, self.mode5_rect.y))
            self.board.screen.blit(self.mode6_icon, (self.mode6_rect.x, self.mode6_rect.y))

            self.board.screen.blit(self.back_icon, (self.back_rect.x, self.back_rect.y))
            self.board.screen.blit(self.help_icon, (self.help_rect.x, self.help_rect.y))

            if not self.board.stage2_unlocked:  # draw a lock on the game mode that the user cannot play
                self.board.screen.blit(self.lock_icon, (self.mode2_rect.x + 30, self.mode2_rect.y))
            if not self.board.stage3_unlocked:
                self.board.screen.blit(self.lock_icon, (self.mode3_rect.x + 30, self.mode3_rect.y))
            if not self.board.stage4_unlocked:
                self.board.screen.blit(self.lock_icon, (self.mode4_rect.x + 30, self.mode4_rect.y))
            if not self.board.stage5_unlocked:
                self.board.screen.blit(self.lock_icon, (self.mode5_rect.x + 30, self.mode5_rect.y))
            if not self.board.stage6_unlocked:
                self.board.screen.blit(self.lock_icon, (self.mode6_rect.x + 30, self.mode6_rect.y))

        else:  # the menu screen
            self.board.screen.blit(self.menu, (0, 0))
            self.board.screen.blit(self.play_game_icon, (self.play_rect.x, self.play_rect.y))

        if not self.music: # crosses out the music button if music is paused
            pg.draw.line(self.board.screen, (255, 0, 0), (self.music_rect.x + self.music_rect.width, self.music_rect.y),
                         (self.music_rect.x, self.music_rect.y + self.music_rect.height), 3)




def refresh_points(board):
    x = board.radius
    y = board.radius
    column = [[x, y]]
    while True:
        while True:  # this loop uses similar triangles to calculate the points of where the balls can be located
            x += board.radius * 2
            if x > board.width - board.radius:
                x = board.radius * 2
                y += int(3 ** (1 / 2) * board.radius)
                board.points.append(column)
                column = []
                break
            else:
                column.append([x, y])
        if y > board.height - board.radius:
            break
        column.append([x, y])
        while True:
            x += board.radius * 2
            if x > board.width - board.radius:
                x = board.radius
                y += int(3 ** (1 / 2) * board.radius)
                board.points.append(column)
                column = []
                break
            else:
                column.append([x, y])
        if y > board.height - board.radius:
            break
        column.append([x, y])


board = Board()
settings = Settings(board)
screen = pg.display.set_mode((board.width, board.height))
angle = math.pi / 2 # the gun will point upwards at the start
b_pics = ['b_pic1.jpg', 'b_pic2.jpg', 'b_pic3.jpg', 'b_pic4.jpg', 'b_pic5.jpg', 'b_pic6.jpg','b_pic7.jpg','b_pic8.jpg'] # background images
settings.background = pg.image.load(random.choice(b_pics)) # takes a image randomly to be the background
board.screen = screen
t = 0 # time
pg.mixer.music.load("bgm.mp3") # music
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(50)

run = True
while run:
    board.background_functions()
    l_click = False
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        if e.type == pg.MOUSEBUTTONUP:
            board.mouse_down(e, mx, my, settings)
        if e.type == pg.MOUSEMOTION:
            mx, my = pg.mouse.get_pos()
        if e.type == pg.KEYDOWN:
            board.key_pressed(e, settings, b_pics, None)

    if not board.end:
        if board.state == 'RUNNING':
            board.aim()

            if pg.time.get_ticks() - t > 2000 - settings.difficulty * 200:  # move the balls toward the bottom, the rate of movements depend on the difficulty
                for i in range(len(board.points)):
                    for ii in range(len(board.points[i])):
                        board.points[i][ii][1] += 1
                for i in board.balls:
                    i.y += 1
                t = pg.time.get_ticks()

            board.collide() # detects for collision
            board.move_ball()   # move the ball that is shot
            board.drop_ball()   # drop the balls that will be deleted
            board.draw(settings) # draw the screen
            board.mouse_move(mx, my, settings)  # highlight buttons touched by mouse
            board.game_over()   # detects if game is over
        else:
            screen.blit(pic, (0, 0))
        pic = screen.copy()
    else:
        pass  # nothing will happen until user presses 'r' to restart

    if settings.music:
        pg.mixer.music.unpause()
    else:
        pg.mixer.music.pause()

    pg.time.Clock().tick(100) # frames per second
    pg.display.flip()
quit()
