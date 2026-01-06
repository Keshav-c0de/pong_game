import pygame
import sys
import random


pygame.init()

w = 800
h = 400
font = pygame.font.Font(None,74)
score_a =0
score_b =0
cpu_speed = 0
game_active = True
CPU_mode = True

window = pygame.display.set_mode((w,h))
pygame.display.set_caption("pong_game")
background = pygame.image.load("background.png")
background_rect=background.get_rect()
background_rect.center = (w//2,h//2)


clock = pygame.time.Clock()

# Rect(x, y, width, height)
ball = pygame.Rect(400, 200, 20, 20)
paddle_a = pygame.Rect(20, 160, 20, 80)
paddle_b = pygame.Rect(760, 160, 20, 80)

speed_x = random.choice([-5, -4, 4, 5])
speed_y = random.choice([-5, -4, 4, 5])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_active = True
                score_a = 0
                score_b = 0
                ball.center = (w//2, h//2)
                speed_x = random.choice([-5, -4, 4, 5])
                speed_y = random.choice([-5, -4, 4, 5])
                paddle_a.x=20
                paddle_a.y=160
                paddle_b.x=760
                paddle_b.y=160


   
    keys = pygame.key.get_pressed()
    
    # Move Paddle B (Right)
    if keys[pygame.K_UP]:
        paddle_b.y -= 5
    if keys[pygame.K_DOWN]:
        paddle_b.y += 5

    # Move Paddle A (Left)
    if CPU_mode:
        # control by CPU 
        paddle_a.y += cpu_speed
        if speed_x < 0 :
            if paddle_a.centery > ball.centery:
                cpu_speed= -4
            if paddle_a.centery < ball.centery:
                cpu_speed= 4
    else:
        # control by Player(Left)
        if keys[pygame.K_w]:
            paddle_a.y -= 5
        if keys[pygame.K_s]:
            paddle_a.y += 5


    # Move Ball
    ball.x += speed_x
    ball.y += speed_y

   # --- boundary ---
    screen_rect = window.get_rect()
    paddle_a.clamp_ip(screen_rect) 
    paddle_b.clamp_ip(screen_rect)

    # ---  Wall Bouncing ---
    if ball.top <= 0 or ball.bottom >= h:
        speed_y = -speed_y
    
    # --- Scoring and reset ---
    if ball.left <= 0:
        score_a += 1
        ball.center = (400,200)     
        speed_x = 5 * random.choice([1, -1])
        speed_y = 5 * random.choice([1, -1])
        pygame.time.delay(500)
    if ball.right >= w:
        score_b += 1
        ball.center = (400,200)
        speed_x = -5 * random.choice([1, -1]) 
        speed_y = 5 * random.choice([1, -1])
        pygame.time.delay(500)

    # ---  PADDLE COLLISION ---
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        speed_x = -speed_x

    # --- Game Over ---
    if score_a == 10 or score_b == 10:
       game_active = False


    # --- Drawing ---
    window.fill((0,0,0))
    window.blit(background,background_rect)
    if game_active:
       
        pygame.draw.ellipse(window, (255,255,255), ball) 
        pygame.draw.rect(window, (255,255,255), paddle_a)
        pygame.draw.rect(window, (255,255,255), paddle_b)

        text_a = font.render(str(score_a), True, (255, 255, 255))
        text_b = font.render(str(score_b), True, (255, 255, 255))
        window.blit(text_a, (250, 10))
        window.blit(text_b, (510, 10))
    
    else:
       
        text ="GAME OVER"
        game_over_message=font.render(text,True,(225, 225, 225))
        window.blit(game_over_message,game_over_message.get_rect(center =(w//2, h//2)))

        if score_a <= score_b:
            message = "YOU LOSE ! :("
        else :
            message = "YOU WIN!"
        
        winner_msg = font.render(message, True, (255, 255, 255))
        window.blit(winner_msg, winner_msg.get_rect(center=(w//2, h//2 + 60)))

        Font = pygame.font.Font(None,18)
        restart_mes = "PRESS SPACEBAR TO RESTART"
        mes=Font.render(restart_mes,True, (255,255,255))
        window.blit(mes,mes.get_rect(center=(w//2, h//2 + 180)))
           
    pygame.display.update()
    clock.tick(60)
