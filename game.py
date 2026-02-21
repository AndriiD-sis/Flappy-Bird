from pygame import *
from pygame import quit as pg_quit
from random import randint
import sounddevice as sd
import numpy as np

init()
window_size = 1200, 800

window = display.set_mode(window_size)
display.set_caption("Flappy Bird")
clock = time.Clock()

play_rect = Rect(150, window_size[1]//2 -100, 100, 100)

def generete_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_pipe = Rect(
            start_x,
            height + gap,
            pipe_width,
            window_size[1] - (height + gap)
        )
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

pipes = generete_pipes(150)
main_font = font.Font(None, 100)
score = 0
lose = False
y_vel = 0.0

bird_img = image.load("bird.png").convert_alpha()
bird_img = transform.scale(bird_img, (play_rect.width, play_rect.height))
pipe_up_img = image.load("pipe_up.png").convert_alpha()
pipe_down_img = image.load("pipe_down.png").convert_alpha()
bg_img = image.load("bg.jpg").convert()
bg_img = transform.scale(bg_img, window_size)

fs = 16000
block = 256
mic_level = 0.0
gravity = 0.6
THRESH = 0.01
IMPULSE = -8.0
wait = 40
running = True

def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

with sd.InputStream(
    samplerate=fs,
    channels=1,
    blocksize=block,
    callback=audio_cb
):
    while running:
        for e in event.get():
            if e.type == QUIT:
                    running = False

        if mic_level > THRESH:
            y_vel = IMPULSE

        y_vel += gravity
        play_rect.y += int(y_vel)

        if play_rect.top < 0:
            play_rect.top = 0
            y_vel = 0

        if play_rect.bottom > window_size[1]:
            play_rect.bottom = window_size[1]
            y_vel = 0

        window.blit(bg_img, (0, 0))
        window.blit(bird_img, play_rect)

        for pipe in pipes[:]:
            if not lose:
                pipe.x -= 10

            if pipe.top == 0:
                pipe_img = transform.scale(pipe_up_img, (pipe.width, pipe.height))
            else:
                pipe_img = transform.scale(pipe_down_img, (pipe.width, pipe.height))

            window.blit(pipe_img, pipe)

            if pipe.x <= 100:
                pipes.remove(pipe)
                score += 0.5

            if play_rect.colliderect(pipe):
                lose = True

        if len(pipes) < 8:
            pipes += generete_pipes(150)

        score_text = main_font.render(f"{int(score)}", 1, "black")
        center_text = window_size[0]//2 - score_text.get_rect().w
        window.blit(score_text, (center_text, 40))

        display.update()
        clock.tick(60)

        keys = key.get_pressed()
        if keys[K_r] and lose:
            lose = False
            pipes = generete_pipes(150)
            play_rect.y = window_size[1]//2 -100
            score = 0
            y_vel = 0
            wait = 40

        if lose:
            if wait > 0:
                for pipe in pipes:
                    pipe.x += 8
                wait -= 1
pg_quit()