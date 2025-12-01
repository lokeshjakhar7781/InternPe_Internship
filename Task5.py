import pygame
import random
import sys
pygame.init()
# --- CONFIG ---
WIDTH, HEIGHT = 1000, 600
FPS = 60
WIN_SCORE = 3
# choose gadget pair (1 or 2). Remove input() if running from some IDE without console.
try:
    ch = int(input("Enter your choice for gadget pair (1 or 2) :- ").strip() or "1")
    gadget_pair = 1 if ch != 2 else 2
except Exception:
    gadget_pair = 1
# --- WINDOW ---
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - Human (Left) vs Computer (Right) [EASY AI]")
# --- COLORS ---
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# --- BALL ---
radius = 15
def center_ball():
    return WIDTH/2, HEIGHT/2
ball_x, ball_y = center_ball()
ball_vel_x = 6 * random.choice([-1, 1])
ball_vel_y = random.choice([-4, -3, 3, 4])
# --- PADDLES ---
paddle_width, paddle_height = 20, 120
left_paddle_x = 100 - paddle_width/2
right_paddle_x = WIDTH - 100 - paddle_width/2
left_paddle_y = right_paddle_y = HEIGHT/2 - paddle_height/2
# optional second paddles (for gadgets)
second_left_paddle_x = left_paddle_x
second_right_paddle_x = right_paddle_x
second_left_paddle_y = left_paddle_y
second_right_paddle_y = right_paddle_y
# velocities
left_paddle_vel = right_paddle_vel = 0
second_left_paddle_vel = second_right_paddle_vel = 0
# --- GADGETS & SCORES ---
left_gadget = right_gadget = 0
left_gadget_remaining = right_gadget_remaining = 5
player_1 = player_2 = 0
# --- UTIL ---
clock = pygame.time.Clock()
font_small = pygame.font.SysFont('calibri', 32)
font_big = pygame.font.SysFont('calibri', 100)
def reset_ball(to_left=False):
    global ball_x, ball_y, ball_vel_x, ball_vel_y
    ball_x, ball_y = center_ball()
    ball_vel_y = random.choice([-4, -3, 3, 4])
    # send ball toward left when to_left True, else to right
    ball_vel_x = -6 if to_left else 6
    # small random vertical flip
    if random.random() < 0.5:
        ball_vel_y *= -1
def ball_rect():
    return pygame.Rect(int(ball_x - radius), int(ball_y - radius), radius*2, radius*2)
def paddle_rect(x, y):
    return pygame.Rect(int(x), int(y), paddle_width, paddle_height)
# --- EASY AI CONFIG ---
ai_counter = 0
easy_ai_speed = 3          # slow paddle speed
reaction_delay = 7         # update AI every 7 frames
ai_noise_strength = 40     # randomness magnitude (higher = worse accuracy)
# --- MAIN LOOP ---
run = True
while run:
    dt = clock.tick(FPS)
    wn.fill(BLACK)
    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            # LEFT (human) controls
            if event.key == pygame.K_w:
                left_paddle_vel = -8
                second_left_paddle_vel = -8
            if event.key == pygame.K_s:
                left_paddle_vel = 8
                second_left_paddle_vel = 8
            if event.key == pygame.K_d and left_gadget_remaining > 0:
                left_gadget = 1
            if event.key == pygame.K_a and left_gadget_remaining > 0:
                left_gadget = 2
            # Optional manual RIGHT gadget test (computer still controls movement)
            if event.key == pygame.K_UP and right_gadget_remaining > 0:
                right_gadget = 1
            if event.key == pygame.K_DOWN and right_gadget_remaining > 0:
                right_gadget = 2
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                left_paddle_vel = 0
                second_left_paddle_vel = 0
    # --- EASY COMPUTER AI for RIGHT PADDLE ---
    ai_counter += 1
    if player_1 < WIN_SCORE and player_2 < WIN_SCORE:
        if ai_counter >= reaction_delay:
            ai_counter = 0
            # make a noisy target (large noise -> easier)
            noisy_target = ball_y - paddle_height/2 + random.uniform(-ai_noise_strength, ai_noise_strength)
            diff = noisy_target - right_paddle_y
            # large deadzone so AI sometimes ignores small differences
            if abs(diff) > 15:
                # clamp movement to easy speed
                if diff > 0:
                    right_paddle_vel = min(easy_ai_speed, diff)
                else:
                    right_paddle_vel = max(-easy_ai_speed, diff)
            else:
                right_paddle_vel = 0
            # second paddle follows slowly (if used)
            sec_diff = right_paddle_y - second_right_paddle_y
            if abs(sec_diff) > 15:
                if sec_diff > 0:
                    second_right_paddle_vel = min(easy_ai_speed, sec_diff)
                else:
                    second_right_paddle_vel = max(-easy_ai_speed, sec_diff)
            else:
                second_right_paddle_vel = 0
    # --- UPDATE PADDLES ---
    left_paddle_y += left_paddle_vel
    right_paddle_y += right_paddle_vel
    second_left_paddle_y += second_left_paddle_vel
    second_right_paddle_y += second_right_paddle_vel
    # clamp paddles on screen
    left_paddle_y = max(0, min(HEIGHT - paddle_height, left_paddle_y))
    right_paddle_y = max(0, min(HEIGHT - paddle_height, right_paddle_y))
    second_left_paddle_y = max(0, min(HEIGHT - paddle_height, second_left_paddle_y))
    second_right_paddle_y = max(0, min(HEIGHT - paddle_height, second_right_paddle_y))
    # --- MOVE BALL ---
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    # wall bounce
    if ball_y - radius <= 0 or ball_y + radius >= HEIGHT:
        ball_vel_y *= -1
    # scoring
    if ball_x - radius >= WIDTH:
        # ball went off right side -> left player scores
        player_1 += 1
        second_left_paddle_y = left_paddle_y
        second_right_paddle_y = right_paddle_y
        reset_ball(to_left=False)  # serve to right (computer)
    elif ball_x + radius <= 0:
        # ball went off left side -> computer scores
        player_2 += 1
        second_left_paddle_y = left_paddle_y
        second_right_paddle_y = right_paddle_y
        reset_ball(to_left=True)  # serve to left (human)
    # --- COLLISIONS (rects) ---
    brect = ball_rect()
    left_rect = paddle_rect(left_paddle_x, left_paddle_y)
    right_rect = paddle_rect(right_paddle_x, right_paddle_y)
    second_left_rect = paddle_rect(second_left_paddle_x, second_left_paddle_y)
    second_right_rect = paddle_rect(second_right_paddle_x, second_right_paddle_y)
    # left paddle collisions (human)
    if brect.colliderect(left_rect) or brect.colliderect(second_left_rect):
        ball_x = left_paddle_x + paddle_width + radius
        ball_vel_x = abs(ball_vel_x)  # send right
        # adjust vertical speed based on hit position
        offset = (ball_y - (left_paddle_y + paddle_height/2)) / (paddle_height/2)
        ball_vel_y += offset * 2
    # right paddle collisions (computer)
    if brect.colliderect(right_rect) or brect.colliderect(second_right_rect):
        ball_x = right_paddle_x - radius
        ball_vel_x = -abs(ball_vel_x)  # send left
        offset = (ball_y - (right_paddle_y + paddle_height/2)) / (paddle_height/2)
        ball_vel_y += offset * 2
    # --- GADGETS (preserved behavior) ---
    if gadget_pair == 1:
        # gadget 1 = speed multiplier on hit, gadget 2 = teleport paddle to ball y
        if left_gadget == 1 and brect.colliderect(left_rect):
            ball_x = left_paddle_x + paddle_width + radius
            ball_vel_x *= -3.5
            left_gadget = 0
            left_gadget_remaining -= 1
        elif left_gadget == 2:
            left_paddle_y = max(0, min(HEIGHT - paddle_height, ball_y - paddle_height/2))
            left_gadget = 0
            left_gadget_remaining -= 1

        if right_gadget == 1 and brect.colliderect(right_rect):
            ball_x = right_paddle_x - radius
            ball_vel_x *= -3.5
            right_gadget = 0
            right_gadget_remaining -= 1
        elif right_gadget == 2:
            right_paddle_y = max(0, min(HEIGHT - paddle_height, ball_y - paddle_height/2))
            right_gadget = 0
            right_gadget_remaining -= 1
    else:
        # gadget_pair 2 behavior
        if left_gadget == 1 and brect.colliderect(left_rect):
            ball_x = left_paddle_x + paddle_width + radius
            ball_vel_x *= -1
            ball_vel_y *= -1
            left_gadget = 0
            left_gadget_remaining -= 1
        elif left_gadget == 2:
            second_left_paddle_y = left_paddle_y + 200
            second_left_paddle_y = max(0, min(HEIGHT - paddle_height, second_left_paddle_y))
            left_gadget = 0
            left_gadget_remaining -= 1

        if right_gadget == 1 and brect.colliderect(right_rect):
            ball_x = right_paddle_x - radius
            ball_vel_x *= -1
            ball_vel_y *= -1
            right_gadget = 0
            right_gadget_remaining -= 1
        elif right_gadget == 2:
            second_right_paddle_y = right_paddle_y + 200
            second_right_paddle_y = max(0, min(HEIGHT - paddle_height, second_right_paddle_y))
            right_gadget = 0
            right_gadget_remaining -= 1
    # --- DRAW UI ---
    score_1_surf = font_small.render("Player_1: " + str(player_1), True, WHITE)
    wn.blit(score_1_surf, (25, 25))
    score_2_surf = font_small.render("Player_2: " + str(player_2), True, WHITE)
    wn.blit(score_2_surf, (825, 25))
    gad_left_1 = font_small.render("Gad Left: " + str(left_gadget_remaining), True, WHITE)
    wn.blit(gad_left_1, (25, 65))
    gad_left_2 = font_small.render("Gad Left: " + str(right_gadget_remaining), True, WHITE)
    wn.blit(gad_left_2, (825, 65))
    pygame.draw.circle(wn, BLUE, (int(ball_x), int(ball_y)), radius)
    pygame.draw.rect(wn, RED, left_rect)
    pygame.draw.rect(wn, RED, right_rect)
    pygame.draw.rect(wn, RED, second_left_rect)
    pygame.draw.rect(wn, RED, second_right_rect)
    # gadget indicators
    if left_gadget == 1:
        pygame.draw.circle(wn, WHITE, (int(left_paddle_x + paddle_width/2), int(left_paddle_y + 10)), 4)
    if right_gadget == 1:
        pygame.draw.circle(wn, WHITE, (int(right_paddle_x + paddle_width/2), int(right_paddle_y + 10)), 4)
    # end screen
    if player_1 >= WIN_SCORE:
        wn.fill(BLACK)
        endscreen = font_big.render("PLAYER_1 WON!!!!", True, WHITE)
        wn.blit(endscreen, (200, 250))
    elif player_2 >= WIN_SCORE:
        wn.fill(BLACK)
        endscreen = font_big.render("PLAYER_2 WON!!!!", True, WHITE)
        wn.blit(endscreen, (200, 250))
    pygame.display.update()
# cleanup
pygame.quit()
sys.exit()