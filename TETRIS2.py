import pygame
import random
import TETRIS2_aux as aux
import math

ZERO = "0"
following_p = None
saved_p = None
active_p = None
frozen = [*list((( x,20), "black") for x in range(0, 10)), 
          *list((( x, 0), (30, 30, 30)) for x in range(0, 10)),  
          *list(((-1, x), "black") for x in range(0, 20)),  
          *list(((10, x), "black") for x in range(0, 20)),]

press_s = False
press_a = False
press_d = False
press_q = False
press_e = False
press_space = False
press_m = False
time = 0
points = 0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((aux.screen_x, aux.screen_y))
pygame.display.set_caption("Tetris")
        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    time+=1
    time_s = int(time%60**2/60**1)
    if time_s < 10:
        time_s = "0"+ str(time_s)
    else:
        time_s = str(time_s)
        
    time_min = int(time%60**3/60**2)
    if time_min < 10:
        time_min = "0"+ str(time_min)
    else:
        time_min = str(time_min)
        
    time_h = int(time%60**4/60**3)
    if time_h < 10:
        time_h = "0"+ str(time_h)
    else:
        time_h = str(time_h)
    
    keys = pygame.key.get_pressed()
    press_s_save = press_s
    press_a_save = press_a
    press_d_save = press_d
    press_q_save = press_q
    press_e_save = press_e
    press_space_save = press_space
    press_m_save = press_m
    press_s = keys[pygame.K_s]
    press_a = keys[pygame.K_a]
    press_d = keys[pygame.K_d]
    press_q = keys[pygame.K_q]
    press_e = keys[pygame.K_e]
    press_space = keys[pygame.K_SPACE]
    press_m = keys[pygame.K_m]
    
    if active_p == None:        
        #cierra el juego cuando perdes
        for x in aux.remove_outs(frozen):
            if x[0][1]==3:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    frozen.clear()
                    pygame.display.update()
                    clock.tick(60)    
        
        active_p = following_p
        following_p = None
        
    else:
        if press_s and not press_s_save:
            active_p.fall = True
            
        if press_a and not press_a_save:
            active_p.pos[0] -= 1
            if active_p.check_colision(frozen):
                active_p.pos[0] += 1
                
        if press_d and not press_d_save:
            active_p.pos[0] += 1
            if active_p.check_colision(frozen):
                active_p.pos[0] -= 1
                
        if press_q and not press_q_save:
            active_p.rotate += 1
            if active_p.check_colision(frozen):
                active_p.rotate -= 1
                active_p.refr()
                
        if press_e and not press_e_save:
            active_p.rotate -=1
            if active_p.check_colision(frozen):
                active_p.rotate += 1
                active_p.refr()
        
        if active_p.fall:
            active_p.pos[1] += 0.3
        else:
            active_p.pos[1] += 0.01+time/1800000
            
        if active_p.check_colision(frozen):
            relative_shape = []
            for x in active_p.rot_shape:
                x = ((active_p.pos[0]+x[0]), (active_p.pos[1]+x[1])//1)
                relative_shape.append(x)
            for x in relative_shape:
                frozen.append((x, active_p.colour))
            
            n_rows = 0
            for x in range(0,4):
                frozen, n = aux.full_line(frozen)
                n_rows += n
            match n_rows:
                case 0:
                    points += 0
                case 1:
                    points += 100
                case 2:
                    points += 300
                case 3:
                    points += 500
                case 4:
                    points += 1000
                
            active_p = None
            
        # frozen = {*list((( x,20), "black") for x in range(0, 10)), 
        #   *list((( x, 0), (30, 30, 30)) for x in range(0, 10)),  
        #   *list(((-1, x), "black") for x in range(0, 20)),  
        #   *list(((10, x), "black") for x in range(0, 20)),
        #   *frozen,}
        # frozen = list(frozen)
        
        if press_space and not press_space_save:
            if saved_p == None:
                saved_p, active_p = active_p, None
                saved_p.rotate = 0
                saved_p.fall = False
                saved_p.refr()
            else: 
                saved_p, active_p = active_p, saved_p
                saved_p.rotate = 0
                saved_p.refr()
                
    if following_p == None:
        following_p = aux.nu_p()
        
    aux.draw_all(screen, active_p, following_p, saved_p,frozen)
    aux.write(screen, f"{time_h}:{time_min}:{time_s}", aux.square*2, aux.square, aux.square*2, "white")
    try:
        aux.write(screen, f"{ZERO*(10-int(math.log(points, 10)))}{points}", aux.square*2, aux.square*2.5, aux.square*2, "white")
    except:
        aux.write(screen, f"{ZERO*10}", aux.square*2, aux.square*2.5, aux.square*2, "white")
    pygame.display.update()
    clock.tick(60)
