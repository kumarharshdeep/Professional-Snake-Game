import pygame
import random
import time
import sys
import os # Naya import

# Pygame ko initialize karein
pygame.init()
pygame.mixer.init()

# ---------------------------------------------------------------------------------------
# COLORS
# ---------------------------------------------------------------------------------------
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
light_green = (144, 238, 144)
red = (255, 0, 0)
light_blue = (135, 206, 250)
dark_blue = (30, 144, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
dark_purple = (100, 0, 100)
purple = (128, 0, 128)
dark_green = (0, 100, 0)
# ---------------------------------------------------------------------------------------

# Screen dimensions
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Professional Snake Game')

# Game settings
snake_block = 20

# Yeh function PyInstaller ke liye resources ka sahi path dhoondta hai
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Fonts (Updated to load from file with fallback)
try:
    font_style = pygame.font.Font(resource_path("PressStart2P.ttf"), 25)
    option_font = pygame.font.Font(resource_path("PressStart2P.ttf"), 20)
    score_font = pygame.font.Font(resource_path("PressStart2P.ttf"), 35)
    title_font = pygame.font.Font(resource_path("PressStart2P.ttf"), 45)
    instruction_font = pygame.font.Font(resource_path("PressStart2P.ttf"), 20)
except pygame.error as e:
    print(f"Error loading font file: {e}")
    print("Falling back to default system fonts.")
    font_style = pygame.font.SysFont("PressStart2P", 25)
    option_font = pygame.font.SysFont("PressStart2P", 20)
    score_font = pygame.font.SysFont("PressStart2P", 35)
    title_font = pygame.font.SysFont('PressStart2P', 45)
    instruction_font = pygame.font.SysFont('arial', 20, bold=True)

clock = pygame.time.Clock()

# Global variables
sound_enabled = True
selected_level_speed = 12 # Default speed
high_score = 0
fullscreen_active = False

# Level progression milestones
level_milestones = {
    2: 50,
    3: 100,
    4: 150,
    5: 200,
    6: 250,
    7: 300,
    8: 350,
    9: 400,
    10: 450
}

# --- UPDATED: Levels ke liye colors aur walls ka dictionary ---
level_colors = {
    1: {"background": (135, 206, 250), "snake_body": (0, 255, 0), "wall": (0, 0, 0)},
    2: {"background": (30, 144, 255), "snake_body": (255, 255, 0), "wall": (255, 255, 255)},
    3: {"background": (128, 0, 128), "snake_body": (144, 238, 144), "wall": (255, 255, 0)},
    4: {"background": (255, 0, 0), "snake_body": (255, 165, 0), "wall": (0, 0, 255)},
    5: {"background": (0, 0, 0), "snake_body": (255, 255, 255), "wall": (128, 128, 128)},
    6: {"background": (0, 100, 0), "snake_body": (255, 255, 0), "wall": (255, 0, 0)},
    7: {"background": (100, 50, 0), "snake_body": (255, 200, 100), "wall": (255, 255, 255)},
    8: {"background": (50, 50, 150), "snake_body": (200, 200, 255), "wall": (255, 0, 255)},
    9: {"background": (0, 0, 0), "snake_body": (255, 0, 0), "wall": (0, 255, 255)},
    10: {"background": (100, 0, 100), "snake_body": (255, 255, 0), "wall": (255, 255, 255)},
}

# Sounds (These files must be in the same directory)
try:
    eat_sound = pygame.mixer.Sound(resource_path('eat_sound.wav'))
    game_over_sound = pygame.mixer.Sound(resource_path('game_over.wav'))
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    print("Sounds will not be played. Please make sure sound files are in the same directory.")
    eat_sound, game_over_sound = None, None

# Load and scale images (with fallback to simple shapes)
try:
    snake_head_img = pygame.image.load(resource_path('snake_head.png')).convert_alpha()
    snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
    snake_body_img = pygame.image.load(resource_path('snake_body.png')).convert_alpha()
    snake_body_img = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
    food_img = pygame.image.load(resource_path('food.png')).convert_alpha()
    food_img = pygame.transform.scale(food_img, (snake_block, snake_block))
    power_up_img = pygame.image.load(resource_path('bonus_food.png')).convert_alpha()
    power_up_img = pygame.transform.scale(power_up_img, (snake_block, snake_block))
    trophy_img = pygame.image.load(resource_path('trophy.png')).convert_alpha()
    trophy_img = pygame.transform.scale(trophy_img, (60, 60))
    fruit_icon_img = pygame.image.load(resource_path('fruit_icon.png')).convert_alpha()
    fruit_icon_img = pygame.transform.scale(fruit_icon_img, (60, 60))
    snake_menu_img = pygame.image.load(resource_path('snake_menu.png')).convert_alpha()
    snake_menu_img = pygame.transform.scale(snake_menu_img, (int(dis_width * 0.7), int(dis_height * 0.2)))
    # Note: background_img is no longer loaded here, it will be loaded per-level

except pygame.error as e:
    print(f"Error loading static images: {e}")
    print("Falling back to colored blocks. Please download the images and place them in the same directory as the script for better visuals.")
    snake_head_img, snake_body_img, food_img, power_up_img, trophy_img, fruit_icon_img, snake_menu_img = None, None, None, None, None, None, None

def message(msg, color, y_offset=0, font=font_style):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 - mesg.get_height() / 2 + y_offset])

def our_snake(snake_list, level):
    if not snake_head_img or not snake_body_img:
        # Fallback to colored blocks with level-specific colors
        for i, x in enumerate(snake_list):
            if i == len(snake_list) - 1:
                pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])
                eye_radius = 2
                pygame.draw.circle(dis, black, (x[0] + 5, x[1] + 5), eye_radius)
                pygame.draw.circle(dis, black, (x[0] + snake_block - 5, x[1] + 5), eye_radius)
            else:
                body_color = level_colors.get(level, level_colors[1])["snake_body"]
                pygame.draw.rect(dis, body_color, [x[0], x[1], snake_block, snake_block])
        return

    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            dis.blit(snake_head_img, [x[0], x[1]])
        else:
            dis.blit(snake_body_img, [x[0], x[1]])

def your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [10, 10])

# --- UPDATED: draw_walls() function with 'level' argument ---
def draw_walls(walls, level):
    wall_color = level_colors.get(level, level_colors[1])["wall"]
    for wall in walls:
        pygame.draw.rect(dis, wall_color, wall)
# -----------------------------------------------------------

def generate_walls(level):
    walls = []
    
    if level == 1:
        pass
    elif level == 2:
        walls.append(pygame.Rect(dis_width / 4, dis_height / 3, snake_block, dis_height / 3))
        walls.append(pygame.Rect(3 * dis_width / 4 - snake_block, dis_height / 3, snake_block, dis_height / 3))
        walls.append(pygame.Rect(dis_width / 4, dis_height / 3, dis_width / 2, snake_block))
    elif level == 3:
        walls.append(pygame.Rect(dis_width / 3, 0, snake_block, dis_height / 2))
        walls.append(pygame.Rect(2 * dis_width / 3, dis_height / 2, snake_block, dis_height / 2))
        walls.append(pygame.Rect(2 * dis_width / 3, 0, snake_block, dis_height / 3))
    elif level == 4:
        walls.append(pygame.Rect(dis_width/2 - snake_block/2, dis_height/4, snake_block, dis_height/2))
        walls.append(pygame.Rect(dis_width/4, dis_height/2 - snake_block/2, dis_width/2, snake_block))
    elif level == 5:
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.2, 80, 80))
        walls.append(pygame.Rect(dis_width*0.6, dis_height*0.2, 80, 80))
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.6, 80, 80))
        walls.append(pygame.Rect(dis_width*0.6, dis_height*0.6, 80, 80))
    elif level == 6:
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.2, 400, 20))
        walls.append(pygame.Rect(dis_width*0.6, dis_height*0.3, 400, 20))
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.4, 400, 20))
        walls.append(pygame.Rect(dis_width*0.6, dis_height*0.5, 400, 20))
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.6, 400, 20))
        walls.append(pygame.Rect(dis_width*0.6, dis_height*0.7, 400, 20))
    elif level == 7:
        walls.append(pygame.Rect(dis_width*0.2, 0, 20, dis_height*0.7))
        walls.append(pygame.Rect(dis_width*0.4, dis_height*0.3, 20, dis_height*0.7))
        walls.append(pygame.Rect(dis_width*0.6, 0, 20, dis_height*0.7))
        walls.append(pygame.Rect(dis_width*0.8, dis_height*0.3, 20, dis_height*0.7))
    elif level == 8:
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.4, dis_width*0.6, 20))
    elif level == 9:
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.2, 40, 40))
        walls.append(pygame.Rect(dis_width*0.8, dis_height*0.8, 40, 40))
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.8, 40, 40))
        walls.append(pygame.Rect(dis_width*0.8, dis_height*0.2, 40, 40))
        walls.append(pygame.Rect(dis_width*0.5, dis_height*0.5, 40, 40))
    elif level == 10:
        walls.append(pygame.Rect(dis_width*0.2, 0, 20, dis_height*0.4))
        walls.append(pygame.Rect(dis_width*0.2, dis_height*0.6, 20, dis_height*0.4))
        walls.append(pygame.Rect(dis_width*0.8, 0, 20, dis_height*0.4))
        walls.append(pygame.Rect(dis_width*0.8, dis_height*0.6, 20, dis_height*0.4))
        walls.append(pygame.Rect(0, dis_height*0.2, dis_width*0.4, 20))
        walls.append(pygame.Rect(dis_width*0.6, dis_height*0.2, dis_width*0.4, 20))
        walls.append(pygame.Rect(0, dis_height*0.8, dis_width*0.4, 20))
        walls.append(pygame.Rect(dis_width*0.6, dis_height*0.8, dis_width*0.4, 20))
    return walls

def generate_food(walls, snake_list):
    """Return a (foodx, foody) that does not collide with walls or snake_list."""
    while True:
        foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
        food_rect = pygame.Rect(foodx, foody, snake_block, snake_block)

        if any(w.colliderect(food_rect) for w in walls):
            continue
        if [foodx, foody] in snake_list:
            continue
        return foodx, foody

def gameLoop(snake_speed):
    global sound_enabled, high_score
    game_over = False
    game_close = False
    paused = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0
    level = 1

    moving_wall_y_change = 2
    
    walls = generate_walls(level)

    start_pos_rect = pygame.Rect(x1, y1, snake_block, snake_block)
    while any(w.colliderect(start_pos_rect) for w in walls):
        x1 = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        y1 = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
        start_pos_rect = pygame.Rect(x1, y1, snake_block, snake_block)

    foodx, foody = generate_food(walls, snake_list)
    
    power_up_x = -1
    power_up_y = -1
    booster_timer_start = 0
    booster_duration = 8

    fruits_eaten_since_last_booster = 0
    fruits_needed_for_booster = random.randint(3, 7)

    while not game_over:
        if game_close:
            game_over_screen(score)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_LEFT and x1_change != snake_block:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change != snake_block:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                        y1_change = snake_block
                        x1_change = 0

        if paused:
            message("Game Paused", white, -50)
            message("Press 'Esc' to Resume", white, 0, instruction_font)
            pygame.display.update()
            clock.tick(5)
            continue

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block
        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block
        
        # Level ke hisaab se background image load karen
        background_path = f"background_level_{level}.png"
        try:
            current_bg_img = pygame.image.load(resource_path(background_path)).convert()
            current_bg_img = pygame.transform.scale(current_bg_img, (dis_width, dis_height))
            dis.blit(current_bg_img, (0, 0))
        except pygame.error:
            # Agar image load nahi hui to color fill karein
            current_bg_color = level_colors.get(level, level_colors[1])["background"]
            dis.fill(current_bg_color)
            
        if food_img:
            dis.blit(food_img, [foodx, foody])
        else:
            pygame.draw.rect(dis, orange, [foodx, foody, snake_block, snake_block])
            
        if level == 8:
            if len(walls) > 0:
                moving_wall = walls[0]  # Assuming first wall is the moving one
                moving_wall.y += moving_wall_y_change
                if moving_wall.top <= snake_block or moving_wall.bottom >= dis_height - snake_block:
                    moving_wall_y_change *= -1
        
        if power_up_x != -1:
            if power_up_img:
                dis.blit(power_up_img, [power_up_x, power_up_y])
            else:
                pygame.draw.rect(dis, purple, [power_up_x, power_up_y, snake_block, snake_block])

            time_left = max(0, booster_duration - (pygame.time.get_ticks() - booster_timer_start) / 1000)
            
            bar_width = 150
            bar_height = 20
            bar_x = dis_width // 2 - bar_width // 2
            bar_y = 10
            
            fill_width = (time_left / booster_duration) * bar_width
            
            start_color = pygame.Color(0, 255, 0)
            end_color = pygame.Color(255, 0, 0)
            
            lerp_factor = 1 - (time_left / booster_duration)
            current_bar_color = start_color.lerp(end_color, lerp_factor)
            
            pygame.draw.rect(dis, black, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
            pygame.draw.rect(dis, dark_blue, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(dis, current_bar_color, (bar_x, bar_y, fill_width, bar_height))

            if time_left <= 0:
                power_up_x = -1

        # --- UPDATED: 'level' argument pass kiya gaya hai ---
        draw_walls(walls, level)
        # ----------------------------------------------------

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
                if sound_enabled and game_over_sound:
                    game_over_sound.play()

        for wall in walls:
            if wall.colliderect(pygame.Rect(x1, y1, snake_block, snake_block)):
                game_close = True
                if sound_enabled and game_over_sound:
                    game_over_sound.play()
        
        our_snake(snake_list, level)
        your_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(walls, snake_list)
            length_of_snake += 1
            score += 1
            fruits_eaten_since_last_booster += 1
            if sound_enabled and eat_sound:
                eat_sound.play()
            
            if fruits_eaten_since_last_booster >= fruits_needed_for_booster and power_up_x == -1:
                power_up_x, power_up_y = generate_food(walls, snake_list)
                booster_timer_start = pygame.time.get_ticks()
                fruits_eaten_since_last_booster = 0
                fruits_needed_for_booster = random.randint(3, 7)

            if level < 10 and score >= level_milestones.get(level + 1, float('inf')):
                level += 1
                length_of_snake = 1
                x1 = dis_width / 2
                y1 = dis_height / 2
                x1_change = 0
                y1_change = 0
                snake_list = []
                walls = generate_walls(level)
                
                start_pos_rect = pygame.Rect(x1, y1, snake_block, snake_block)
                while any(w.colliderect(start_pos_rect) for w in walls):
                    x1 = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
                    y1 = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
                    start_pos_rect = pygame.Rect(x1, y1, snake_block, snake_block)
                    
                foodx, foody = generate_food(walls, snake_list)

        if x1 == power_up_x and y1 == power_up_y:
            score += 10
            length_of_snake += 3
            if sound_enabled and eat_sound:
                eat_sound.play()
            power_up_x = -1
            
        clock.tick(snake_speed)

    if score > high_score:
        high_score = score
        
    pygame.quit()
    sys.exit()

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_gradient_background(surface, color1, color2):
    for y in range(dis_height):
        color = (
            int(color1[0] + (color2[0] - color1[0]) * y / dis_height),
            int(color1[1] + (color2[1] - color1[1]) * y / dis_height),
            int(color1[2] + (color2[2] - color1[2]) * y / dis_height)
        )
        pygame.draw.line(surface, color, (0, y), (dis_width, y))

def draw_menu_panel(title_text, main_color, current_score, current_high_score):
    panel_rect = pygame.Rect(dis_width * 0.15, dis_height * 0.1, dis_width * 0.7, dis_height * 0.8)
    draw_rounded_rect(dis, main_color, panel_rect, 20)

    header_rect = pygame.Rect(panel_rect.x, panel_rect.y, panel_rect.width, panel_rect.height * 0.4)
    draw_rounded_rect(dis, light_blue, header_rect, 20)
    
    title_text_render = title_font.render(title_text, True, red)
    dis.blit(title_text_render, (header_rect.x + (header_rect.width / 2) - (title_text_render.get_width() / 2), header_rect.y + 20))
    
    if fruit_icon_img and trophy_img:
        fruit_icon_rect = fruit_icon_img.get_rect(center=(header_rect.x + (header_rect.width / 4), header_rect.y + 110))
        trophy_icon_rect = trophy_img.get_rect(center=(header_rect.x + (3 * header_rect.width / 4), header_rect.y + 110))
        dis.blit(fruit_icon_img, fruit_icon_rect)
        dis.blit(trophy_img, trophy_icon_rect)
        
        score_value_text = score_font.render(str(current_score), True, black)
        high_score_text = score_font.render(str(current_high_score), True, black)
        
        score_value_rect = score_value_text.get_rect(center=(fruit_icon_rect.centerx, fruit_icon_rect.y + 50))
        high_score_rect = high_score_text.get_rect(center=(trophy_icon_rect.centerx, trophy_icon_rect.y + 50))
        
        dis.blit(score_value_text, score_value_rect)
        dis.blit(high_score_text, high_score_rect)

    if snake_menu_img:
        snake_img_rect = snake_menu_img.get_rect(center=(header_rect.centerx, header_rect.y + header_rect.height - snake_menu_img.get_height() / 2 - 10))
        dis.blit(snake_menu_img, snake_img_rect)

def draw_button(text, rect, mouse_pos, is_selected=False, is_quit=False):
    button_color = dark_blue
    text_color = white
    
    if is_quit:
        button_color = blue
    
    if is_selected:
        button_color = green
        text_color = yellow
    elif rect.collidepoint(mouse_pos) and not is_quit:
        button_color = blue
        text_color = yellow
    
    draw_rounded_rect(dis, button_color, rect, 15)
    
    button_text = option_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=rect.center)
    dis.blit(button_text, text_rect)
    return rect

def game_over_screen(score):
    global high_score
    if score > high_score:
        high_score = score

    while True:
        overlay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        dis.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(dis_width * 0.25, dis_height * 0.2, dis_width * 0.5, dis_height * 0.6)
        draw_rounded_rect(dis, white, panel_rect, 20)

        title_text = title_font.render("Game Over!", True, red)
        title_rect = title_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 50))
        dis.blit(title_text, title_rect)

        score_text = font_style.render(f"Score: {score}", True, black)
        score_rect = score_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 120))
        dis.blit(score_text, score_rect)

        high_score_text = font_style.render(f"High Score: {high_score}", True, black)
        high_score_rect = high_score_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 160))
        dis.blit(high_score_text, high_score_rect)

        play_again_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 250, panel_rect.width - 100, 60)
        quit_rect = pygame.Rect(panel_rect.x + 50, panel_rect.y + 350, panel_rect.width - 100, 60)
        
        mouse_pos = pygame.mouse.get_pos()
        draw_button("Play Again", play_again_rect, mouse_pos)
        draw_button("Quit", quit_rect, mouse_pos, is_quit=True)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_rect.collidepoint(mouse_pos):
                    main_menu()
                    return
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def level_selection_menu():
    global selected_level_speed, high_score
    while True:
        mouse_pos = pygame.mouse.get_pos()
        draw_gradient_background(dis, light_blue, dark_blue)
        draw_menu_panel("PROFESSIONAL SNAKE GAME", white, 0, high_score)

        low_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.4, dis_width * 0.3, 60)
        medium_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.55, dis_width * 0.3, 60)
        hard_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.7, dis_width * 0.3, 60)
        back_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.85, dis_width * 0.3, 60)

        draw_button("Low (Slow)", low_rect, mouse_pos, selected_level_speed == 8)
        draw_button("Medium (Normal)", medium_rect, mouse_pos, selected_level_speed == 12)
        draw_button("Hard (Fast)", hard_rect, mouse_pos, selected_level_speed == 20)
        draw_button("Back", back_rect, mouse_pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if low_rect.collidepoint(mouse_pos):
                    selected_level_speed = 8
                elif medium_rect.collidepoint(mouse_pos):
                    selected_level_speed = 12
                elif hard_rect.collidepoint(mouse_pos):
                    selected_level_speed = 20
                elif back_rect.collidepoint(mouse_pos):
                    main_menu()
                    return

def settings_menu():
    global sound_enabled, high_score
    while True:
        mouse_pos = pygame.mouse.get_pos()
        draw_gradient_background(dis, light_blue, dark_blue)
        draw_menu_panel("PROFESSIONAL SNAKE GAME", white, 0, high_score)

        sound_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.4, dis_width * 0.3, 60)
        back_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.55, dis_width * 0.3, 60)

        sound_status = "On" if sound_enabled else "Off"
        draw_button(f"Sound: {sound_status}", sound_rect, mouse_pos)
        draw_button("Back", back_rect, mouse_pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if sound_rect.collidepoint(mouse_pos):
                    sound_enabled = not sound_enabled
                    if sound_enabled and pygame.mixer.get_init():
                        pygame.mixer.unpause()
                    else:
                        pygame.mixer.pause()
                elif back_rect.collidepoint(mouse_pos):
                    main_menu()
                    return

def main_menu():
    global selected_level_speed, high_score
    intro = True
    while intro:
        mouse_pos = pygame.mouse.get_pos()
        draw_gradient_background(dis, light_blue, dark_blue)
        draw_menu_panel("PROFESSIONAL SNAKE GAME", white, 0, high_score)

        play_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.4, dis_width * 0.3, 60)
        settings_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.55, dis_width * 0.3, 60)
        level_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.7, dis_width * 0.3, 60)
        quit_rect = pygame.Rect(dis_width * 0.35, dis_height * 0.85, dis_width * 0.3, 60)

        draw_button("Play", play_rect, mouse_pos)
        draw_button("Settings", settings_rect, mouse_pos)
        draw_button("Level", level_rect, mouse_pos)
        draw_button("Quit", quit_rect, mouse_pos, is_quit=True)
        
        level_name = "Low" if selected_level_speed == 8 else "Medium" if selected_level_speed == 12 else "Hard"
        selected_level_text = instruction_font.render(f"Level: {level_name}", True, white)
        dis.blit(selected_level_text, (dis_width/2 - selected_level_text.get_width()/2, level_rect.y + level_rect.height + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(mouse_pos):
                    gameLoop(selected_level_speed)
                elif settings_rect.collidepoint(mouse_pos):
                    settings_menu()
                elif level_rect.collidepoint(mouse_pos):
                    level_selection_menu()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

# Run the game
main_menu()
