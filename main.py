import pygame #pygame 라이브러리

#필요한 라이브러리들

import random

from time import sleep



# 0. 기본값 설정

# 게임에 사용되는 전역 변수 정의

        #R  G  B 값

BLACK = (0, 0, 0)

RED   = (255, 0, 0)

WHITE = (255, 255, 255)

    #화면 크기

pad_width = 480

pad_height = 640

    #비행기 크기

fight_width = 36

fight_height = 38

    #사이드킥 크기

fighter2_width = 36 #플레이어2 크기______________________________________________________________________

fighter2_height = 38

    #적 크기

enemy_width = 26

enemy_height = 20





def gameover():

    global gamepad

    dispMessage('Game Over')





# 적을 맞춘 개수 계산

def drawScore(count):

    global gamepad



    font = pygame.font.SysFont('arial', 20)

    # text 객체 생성 (텍스트 내용, Anti-aliasing 사용 여부, 텍스트 컬러)

    text = font.render('Enemy Kills: ' + str(count), True, WHITE)

    gamepad.blit(text, (0, 0))





def drawPassed(count):

    global gamepad



    font = pygame.font.SysFont('arial', 20)

    text = font.render('Enemy Passed: ' + str(count), True, RED)

    gamepad.blit(text, (300, 0))





# 화면에 글씨 보이게 하기

def dispMessage(text):

    global gamepad

    textfont = pygame.font.SysFont('arial', 20)

    text = textfont.render(text, True, RED)

    textpos = text.get_rect() # 텍스트 객체의 출력 위치를 가져온다

    textpos.center = (pad_width / 2, pad_height / 2) # 텍스트 객체의 출력 중심 좌표를 설정한다

    gamepad.blit(text, textpos)

    pygame.display.update() #3. 게임 상태 업데이트

    sleep(2) #2초동안 일시중지

    runGame()





def crash():

    global gamepad

    dispMessage('Crashed!')





# 게임에 등장하는 객체를 그려줌

def drawObject(obj, x, y):

    global gamepad

    gamepad.blit(obj, (x, y))





# 게임 실행 메인 함수

def runGame():

    global gamepad, fighter, clock, fighter2 #플레이어2______________________________________________

    global bullet, enemy, bullet2 #총알2_______________________________________________________________



    isShot = False #적이 맞았는지 확인용

    shotcount = 0 #적 맞힌 횟수

    enemypassed = 0 #지나간 적 횟수



    #좌표값 지정

    x = pad_width * 0.45 #216

    y = pad_height * 0.9 #576

    x_change = 0

    x2_change = 0

    x2 = pad_width * 0.45  # 216

    y2 = pad_height * 0.9  # 576

    #총알 좌표 리스트

    bullet_xy = []

    bullet2_xy = []  #총알2 좌표________________________________________________________________________________

    #적의 좌표값 지정

    enemy_x = random.randrange(0, pad_width - enemy_width)

    enemy_y = 0

    enemy_speed = 2



    ongame = False #게임 실행되고있나 확인용



    #-(반복루프)-

    while not ongame:

        #2. fighter 사용자 입력 처리        ### fighter2 사용자 입력 처리 작업 진행중입니다. ###

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #마우스로 창 닫으면 while문 탈출

                ongame = True



            if event.type == pygame.KEYDOWN: #키를 눌렀을 때

                if event.key == pygame.K_LEFT:  # 왼쪽 방향키

                    x_change -= 5

                elif event.key == pygame.K_a: # 왼쪽 방향키 2  (_______________________________)

                    x2_change -= 5



                elif event.key == pygame.K_RIGHT: #오른쪽 방향키

                    x_change += 5

                elif event.key == pygame.K_d: #오른쪽 방향키 2  (______________________________________)

                    x2_change += 5



                elif event.key == pygame.K_LCTRL: # 플1 공격키 좌컨트롤

                    if len(bullet_xy) < 2:

                        bullet_x = x + fight_width / 2

                        bullet_y = y - fight_height

                        bullet_xy.append([bullet_x, bullet_y])

                elif event.key == pygame.K_SPACE:  #플2 공격키 스페이스바  (__________________________________________)

                    if len(bullet2_xy) < 2:

                        bullet_x = x2 + fighter2_width / 2

                        bullet_y = y2 + fighter2_height

                        bullet2_xy.append([bullet_x, bullet_y])





            if event.type == pygame.KEYUP: #키 누른 후

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

                    x_change = 0



                elif event.key == pygame.K_a or event.key == pygame.K_d: #플2 키 누른 후___________________________________

                    x2_change = 0



        gamepad.fill(BLACK)#게임패드에 검은색 화면 채우기



        x += x_change #플1 키움직임에 따라 좌표값 수정

        x2 += x2_change #플2 키움직임에 따라 좌표값 수정______________________________________________________________



        #비행기 화면밖으로 나가지 않게

        if x < 0:

            x = 0

        elif x > pad_width - fight_width:

            x = pad_width - fight_width



        # 게이머 전투기가 적과 충돌했는지 체크

        if y < enemy_y + enemy_height: #적이 비행기를 지나갔을때?

            if (enemy_x > x and enemy_x < x + fight_width) or \

                    (enemy_x + enemy_width > x and enemy_x + enemy_width < x + fight_width):

                crash()



        drawObject(fighter, x, y)

        drawObject(fighter2, x2, y2) #플레이어2 객체 생성___________________________________________________________



        # 전투기 무기 발사 구현

        if len(bullet_xy) != 0:

            for i, bxy in enumerate(bullet_xy): #i=index

                bxy[1] -= 10 #총알 올라가게 y값 좌표 변경

                bullet_xy[i][1] = bxy[1] #i번째 인덱스의 값리스트 1번째(by) 변화시킴



                # 총알이 적과 부딪혔을때

                if bxy[1] < enemy_y:

                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:

                        bullet_xy.remove(bxy)

                        isShot = True

                        shotcount += 1

                # 총알이 화면밖으로 갈때

                if bxy[1] <= 0:

                    try:

                        bullet_xy.remove(bxy)

                    except:

                        pass



        if len(bullet2_xy) != 0: #플레이어2가 발사하는 총알 구현 _______________________________________________________________

            for i, bxy in enumerate(bullet2_xy): #i=index

                bxy[1] -= 10 #총알 올라가게 y값 좌표 변경

                bullet2_xy[i][1] = bxy[1] #i번째 인덱스의 값리스트 1번째(by) 변화시킴



                # 총알이 적과 부딪혔을때

                if bxy[1] < enemy_y:

                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:

                        bullet2_xy.remove(bxy)

                        isShot = True

                        shotcount += 1

                # 총알이 화면밖으로 갈때

                if bxy[1] <= 0:

                    try:

                        bullet2_xy.remove(bxy)

                    except:

                        pass #________________________________________________________________________여기까지



        if len(bullet_xy) != 0: #bullet_xy = [[bx,by]]d

            for bx, by in bullet_xy:

                drawObject(bullet, bx, by) #총알 객체 그림



        if len(bullet2_xy) != 0: #bullet2_xy = [[bx,by]]  #총알2 객체____________________________________________

            for bx, by in bullet2_xy:

                drawObject(bullet2, bx, by) #총알 객체 그림



        drawScore(shotcount)



        # 적 구현

        enemy_y += enemy_speed



        if enemy_y > pad_height: #적이 화면 밖으로 지나갔으면

            enemy_x = random.randrange(0, pad_width - enemy_width)

            enemy_y = 0

            enemypassed += 1



        #지나간 적이 3명이면 게임오버

        if enemypassed == 3:

            gameover()



        drawPassed(enemypassed)



        if isShot: #적을맞췄을때 스피드 증가

            enemy_speed += 1

            if enemy_speed >= 10:

                enemy_speed = 10



            enemy_x = random.randrange(0, pad_width - enemy_width)

            enemy_y = 0

            isShot = False



        drawObject(enemy, enemy_x, enemy_y)



        pygame.display.update() #3. 게임 상태 업데이트

        clock.tick(60) #60FPS 맞추기 위한 딜레이 추가



    pygame.quit() #5. 라이브러리 종료



#1. 라이브러리 초기화 함수

def initGame():

    global gamepad, fighter, clock, fighter2

    global bullet, enemy, bullet2

    pygame.font.init() #font 초기화

    pygame.init() #pygame 초기화



    gamepad = pygame.display.set_mode((pad_width, pad_height)) #화면 객체 설정

    pygame.display.set_caption('MyGalaga') #타이틀바의 텍스트 설정

    #각 변수에 맞는 이미지 로드

    fighter = pygame.image.load('fighter.png')

    fighter2 = pygame.image.load('fighter2.png') #플레이어2 이미지______________________________________________

    enemy = pygame.image.load('enemy.png')

    bullet = pygame.image.load('bullet.png')

    bullet2 = pygame.image.load('bullet2.png') #플레이어2 총알 이미지____________________________________________



    clock = pygame.time.Clock()





initGame()

runGame()
