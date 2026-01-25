from pygame import *
from random import randint

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
y_vel = 2

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
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
    if keys[K_UP]:
        play_rect.y -= 10

    if keys[K_DOWN]:
        play_rect.y += 10
    
    if keys[K_r] and lose:
        lose = False
        pipes = generete_pipes(150)
        play_rect.y = window_size[1]//2 -100
        score = 0

    if play_rect.y > window_size[1] - play_rect.h:
        lose = True

    if lose:
        play_rect.y += y_vel
        y_vel *= 1.1