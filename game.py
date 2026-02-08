from pygame import *
from random import randint
import sounddevice as sd
import numpy as np

init()
window_size = 1200, 800

window = display.set_mode(window_size)
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

fs = 16000
block = 256
mic_level = 0.0
gravity = 0.6
THRESH = 0.01
IMPULSE = -8.0
wait = 40

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
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()

        if mic_level > THRESH:
            y_vel = IMPULSE

        y_vel += gravity
        play_rect.y += int(y_vel)

        window.fill("sky blue")
        draw.rect(window, "yellow", play_rect)

        for pipe in pipes[:]:
            if not lose:
                pipe.x -= 10

            draw.rect(window, "green", pipe)

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

        if play_rect.y > window_size[1] - play_rect.h:
            lose = True

        if lose and wait > 1:
            for pipe in pipes:
                pipe.x += 8
            wait -= 1
        else:
            wait = 40