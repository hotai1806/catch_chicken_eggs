import pyglet
import datetime
import random
from pyglet.window import key
from pyglet.gl import *


pyglet.options['audio'] = ('directsound', 'openal', 'pulse')

player = pyglet.media.Player()
sound = pyglet.media.load('ver1.mp3')
player.queue(sound)

# keep playing for as long as the app is running (or you tell it to stop):
player.eos_action = pyglet.media.SourceGroup.loop

player.play()
alive = 3
background = pyglet.image.load('bg.png')
back = pyglet.sprite.Sprite(background,0,0)
background1 = pyglet.image.load_animation('lvel2.gif')
back1 = pyglet.sprite.Sprite(background1,0,0)
window = pyglet.window.Window(width=600, height=900)
bin = pyglet.resource.image('basket.png')
bin.anchor_x = bin.width // 2
bin.anchor_y = 0
start = 0
res = 0
egg = pyglet.resource.image('egg.png')
egg.anchor_x = egg.width // 2
egg.anchor_y = egg.height
broken_egg = pyglet.resource.image('splash.png')
startimage =  pyglet.image.load_animation('1.gif')
startgame = pyglet.sprite.Sprite(startimage)
youdie =  pyglet.image.load_animation('restart.gif')
end = pyglet.sprite.Sprite(youdie)

class Game(object):
    def __init__(self):
        self.bin_x = window.width // 2
        self.bin_y = 0
        self.egg_x = window.width // 2
        self.egg_y = window.height
        self.score = 0
        self.gameover = False

game = Game()

score_label = pyglet.text.Label(str(game.score),
                                x=window.width // 2,
                                y=window.height // 2,
                                anchor_x='center',
                                anchor_y='center',
                                color=(255, 0, 255, 255),
                                font_size = 40)



@window.event
def on_key_press(motion, modifiers):
    global start
    if motion == key.MOTION_RIGHT:
        game.bin_x += 25
    if motion == key.MOTION_LEFT:
        game.bin_x -= 25
    if motion == key.SPACE:
        start += 1
    if motion == key.R:
        reload()
def reload():
    game.bin_x = window.width // 2
    game.bin_y = 0
    game.egg_x = window.width // 2
    game.egg_y = window.height
    game.score = 0
    game.gameover = False
    pass




def soundPoint():
    point_music = pyglet.media.load('chicken.mp3', streaming = False)
    point_music.play()
def sound_end():
    end_sound = pyglet.media.load('mix09.mp3', streaming = False)
    end_sound.play()

@window.event
def on_draw():
    if start == 0:
        window.clear()
        startgame.draw()

    elif (not game.gameover and start != 0 and game.score <= 5):
        window.clear()
        back.draw()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        egg.blit(game.egg_x, game.egg_y)
        bin.blit(game.bin_x, game.bin_y)
        score_label.text = str(game.score)
        score_label.draw()
    elif not game.gameover and game.score > 5 and start != 0:
        window.clear()
        back1.draw()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        egg.blit(game.egg_x, game.egg_y)
        bin.blit(game.bin_x, game.bin_y)
        score_label.text = str(game.score)
        score_label.draw()
    elif game.gameover and start != 0:
        sound_end()
        window.clear()
        back.draw()
        broken_egg.blit(game.egg_x -10, game.egg_y- 60)
        score_label.text = 'Game Over\nScore: %d' % game.score
        score_label.draw()
        end.draw()
score = 0

def egg_drop(dt):
    # if colision?
    global start

    if game.egg_y <= 75:


        game.gameover = True
        return

    # if we need to reset the egg?
    if abs(game.egg_x - game.bin_x) < 50 and abs(game.egg_y -
            game.bin_y) < 80:

        game.egg_x = random.randint(50, window.width - 50)
        game.egg_y = window.height - 2
        game.score += 1
        soundPoint()
    if start > 0 :
        if game.score <= 5:
            game.egg_y -= 6
        else:

            game.egg_y -= 7



pyglet.clock.schedule(egg_drop)
pyglet.app.run()
pass
