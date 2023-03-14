import pygame, sys, random

#Tạo hàm cho game

#hàm vẽ sàn
def draw_floor():
    screen.blit(floor,(floor_x_pos,325))
    screen.blit(floor,(floor_x_pos+216, 325))

#tạo ống
def create_pipe():
    random_pipe_pos =random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (250, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (250, random_pipe_pos-360))

    return bottom_pipe, top_pipe

#làm cho ống di chuyển
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=2
    
    return pipes 

#vẽ ống dài ngắn
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 300:
            screen.blit(pipe_surface,pipe)
        else:
            #hàm flip để lật ngược ống đối với ống phía trên
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

#check va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom>=336:
        return False
    return True

#giúp chim đập cánh
def rotate_bird(bird1): #rotozoom : giúp tạo hiệu ứng xoay chim
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*4, 1)
    return new_bird
def bird_animation():
    new_bird =bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

#Hiển thị điểm
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (108,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (108,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (108,315))
        screen.blit(high_score_surface,high_score_rect)  

#Update điểm
def update_score(score, high_score):
    if score>high_score:
        high_score=score
    return high_score

pygame.init()
screen=pygame.display.set_mode((216, 384))
clock = pygame.time.Clock()
game_font= pygame.font.Font('04B_19.ttf', 20)

#thêm trọng lực để chim bay
gravity = 0.12
bird_movement = 0
game_active = True
score = 0
high_score=0

#chèn background
bg = pygame.image.load('assets/background-night.png').convert()

#bg = pygame.transform.scale2x(bg)

#Chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor_x_pos = 0

#Tạo chim
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down, bird_mid, bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]

bird_rect = bird.get_rect(center = (50, 192))

#Tạo timer cho chim để tạo hiệu ứng đập cánh
birdflap=pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

#Tạo ống chướng ngại vật
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
pipe_height = [100, 150, 200]

#tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1400)

#Tạo màn hình kết thúc
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (108,192))

while True:     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #bắt sự kiện chim nhảy lên xuống
        if event.type == pygame.KEYDOWN: #khi có phím nào đó đc ấn xuống thì...
            if event.key == pygame.K_SPACE and game_active:
                #chọn phím
                bird_movement = 0
                bird_movement = -4 
            
            #reset lại khi trò chơi kết thúc
            if event.key == pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center = (50,192)
                bird_movement= 0
                score=0
                 
        #bắt sự kiện hiển thị chướng ngại vật
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index <2:
                bird_index+=1
            else:
                bird_index= 0
            bird, bird_rect= bird_animation()    
    
    screen.blit(bg,(0,0))

    if game_active: 
    #Hiển thị trọng lực của chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active=check_collision(pipe_list)

    #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        #check tính điểm
        score +=0.01
        score_display('main game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score=update_score(score, high_score)
        score_display('game_over') 
#sản
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos<= -216:
        floor_x_pos=0

    pygame.display.update()
    clock.tick(120)
