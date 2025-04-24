import pygame
import random
import math
import time

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("룰렛 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 룰렛 원판 파라미터
RADIUS = 250
CENTER = (WIDTH // 2, HEIGHT // 2)
NUMBERS = ['00', '0'] + [str(i) for i in range(1, 37)]

# 구슬 파라미터
BALL_RADIUS = 10
ball_angle = random.uniform(0, 360)  # 구슬의 초기 각도
ball_speed = random.uniform(10, 15)  # 구슬 속도

# 회전 상태
spin_speed = random.uniform(15, 20)  # 회전 속도
spin_angle = 0                        # 회전 각도 초기화

# 승리 번호
winning_number = None

# 폰트
font = pygame.font.Font(None, 36)

def draw_roulette():
    """룰렛 원판 그리기"""
    pygame.draw.circle(screen, BLACK, CENTER, RADIUS)  # 원판 배경
    for i, num in enumerate(NUMBERS):
        angle = math.radians(i * (360 / len(NUMBERS)))
        x = CENTER[0] + math.cos(angle) * (RADIUS - 40)
        y = CENTER[1] + math.sin(angle) * (RADIUS - 40)
        text = font.render(num, True, RED if i % 2 == 0 else GREEN)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

def draw_ball():
    """구슬 그리기"""
    global ball_angle
    ball_x = CENTER[0] + math.cos(math.radians(ball_angle)) * (RADIUS - 20)
    ball_y = CENTER[1] + math.sin(math.radians(ball_angle)) * (RADIUS - 20)
    pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), BALL_RADIUS)

def spin_wheel():
    """회전하는 룰렛 애니메이션"""
    global spin_angle, ball_angle, ball_speed, winning_number
    
    # 원판 회전
    spin_angle += spin_speed
    if spin_angle > 360:
        spin_angle -= 360

    # 구슬 이동
    ball_angle += ball_speed
    if ball_angle > 360:
        ball_angle -= 360
    
    # 구슬의 현재 위치 계산
    draw_ball()

    # 회전 멈춤 처리
    if spin_angle % 360 < 5:  # 회전이 거의 멈출 때
        winning_number = NUMBERS[int((ball_angle / 360) * len(NUMBERS))]
        print("Winning number:", winning_number)

def game_loop():
    global winning_number

    running = True
    while running:
        screen.fill(WHITE)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 룰렛 원판 그리기
        draw_roulette()

        # 룰렛 원판 회전 및 구슬 이동
        spin_wheel()

        # 승리 번호 표시
        if winning_number:
            winning_text = font.render(f"Winning Number: {winning_number}", True, (0, 0, 255))
            screen.blit(winning_text, (WIDTH // 2 - winning_text.get_width() // 2, HEIGHT - 50))

        # 화면 업데이트
        pygame.display.flip()

        # 게임 루프 속도 조절
        time.sleep(0.02)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
