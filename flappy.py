import pygame
import random
import sys
import os 


try:
    
    pygame.mixer.init() 
    
  
    sound_file_path = os.path.join('.', 'jump_sound.mp3.mpeg')

  
    JUMP_SOUND = pygame.mixer.Sound(sound_file_path)
    SOUND_LOADED = True
    print("Sound loaded successfully.")

except pygame.error as e:
  
    print(f"Could not load sound file. Make sure 'jump_sound.mp3' exists in the script directory and is a valid format (like OGG or MP3). Error: {e}")
    JUMP_SOUND = None
    SOUND_LOADED = False

try:
    background_music_path = os.path.join('.', 'background music.mp3')
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)
    BACKGROUND_MUSIC_LOADED = True
    print("Background music loaded successfully.")
except pygame.error as e:
    print(f"Could not load background music file. Make sure 'background music.mp3' exists in the script directory. Error: {e}")
    BACKGROUND_MUSIC_LOADED = False

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60


WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)


font = pygame.font.SysFont("Arial", 32)
large_font = pygame.font.SysFont("Arial", 48)


try:
    bird_image = pygame.image.load(os.path.join('.', 'bird.png')).convert_alpha()
    
    BIRD_WIDTH = 34
    BIRD_HEIGHT = 24 
    bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
    
except pygame.error as e:
    print(f"Could not load bird.png. Using a placeholder circle. Error: {e}")
    bird_image = None
    BIRD_WIDTH = 20
    BIRD_HEIGHT = 20
    bird_radius = 10


bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -8


pipe_width = 70
pipe_gap = 150 
pipe_velocity = 3
pipes = []


score = 0
score_can_increase = True 



def create_pipe():
    
    height = random.randint(150, HEIGHT - 200) 
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_rect = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_rect, bottom_rect, False


def reset_game():
    global bird_y, bird_velocity, pipes, score, time_since_last_pipe, game_active
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = [create_pipe()]
    score = 0
    time_since_last_pipe = 0
    game_active = True

def draw_pipes(pipes):
    for top, bottom, _ in pipes:
        pygame.draw.rect(screen, GREEN, top)
      
        pygame.draw.rect(screen, DARK_GREEN, top, 3) 
        
        pygame.draw.rect(screen, GREEN, bottom)
        pygame.draw.rect(screen, DARK_GREEN, bottom, 3)

def check_collision(bird_rect, pipes):
    for top, bottom, _ in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            return True
   
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    return False

def draw_button(rect, text):
    pygame.draw.rect(screen, DARK_GREEN, rect)
    pygame.draw.rect(screen, BLACK, rect, 3)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def start_screen():
    while True:
        screen.fill(BLUE)
        title = large_font.render("Flappy Bird", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

     
        instruction = font.render("Press SPACE to Jump!", True, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 200))
        
        play_button = pygame.Rect(WIDTH // 2 - 75, 350, 150, 60)
        draw_button(play_button, "Play")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return 
        pygame.display.flip()
        clock.tick(30)


start_screen()


bird_y = HEIGHT // 2
bird_velocity = 0
pipes = [create_pipe()] 
score = 0
time_since_last_pipe = 0
pipe_frequency = 1500 


running = True
game_active = True

while running:
   
    dt = clock.tick(FPS)
    screen.fill(BLUE)

    restart_button = None
    if not game_active:
        restart_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 80, 150, 60)
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_active:
            bird_velocity = jump_strength
           
            if SOUND_LOADED and JUMP_SOUND:
                JUMP_SOUND.play()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_active and restart_button is not None:
            if restart_button.collidepoint(event.pos):
                reset_game()

    if game_active:
       
        bird_velocity += gravity
        bird_y += bird_velocity
        
     
        bird_rect = pygame.Rect(
            bird_x - BIRD_WIDTH // 2, 
            bird_y - BIRD_HEIGHT // 2, 
            BIRD_WIDTH, 
            BIRD_HEIGHT
        )
        
        if bird_image:
            screen.blit(bird_image, bird_rect.topleft)
        else:
           
            pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)
        

        time_since_last_pipe += dt
        
        if time_since_last_pipe > pipe_frequency:
            pipes.append(create_pipe())
            time_since_last_pipe = 0

        temp_pipes = []
        for top, bottom, scored in pipes:
            top.x -= pipe_velocity
            bottom.x -= pipe_velocity
            
            if top.right < bird_x and not scored:
                 score += 1
                 scored = True
                 
            if top.right > 0:
                temp_pipes.append((top, bottom, scored))
            
        pipes = temp_pipes
        draw_pipes(pipes)

        if check_collision(bird_rect, pipes):
            game_active = False 

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    
    else: 
        game_over_text = large_font.render("GAME OVER", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 20))
        
        if restart_button is not None:
            draw_button(restart_button, "Restart")
                
    pygame.display.flip()

pygame.quit()
sys.exit()