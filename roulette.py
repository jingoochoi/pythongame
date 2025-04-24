import pygame
import random
import math

# 게임 초기화
pygame.init()

# 상수 설정
WIDTH, HEIGHT = 800, 600
RADIUS = 200
CENTER = (WIDTH // 2, HEIGHT // 2)
NUM_SECTORS = 37  # 0, 00, 1-36
SECTOR_ANGLE = 360 / NUM_SECTORS
BALL_RADIUS = 15
FONT = pygame.font.SysFont('Arial', 30)

# 색상
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY=(100,100,100)

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("룰렛 게임")

# 룰렛 원판 그리기
def draw_roulette(rotation_angle):
    screen.fill(WHITE)
    ROULETTE_NUMBERS = ["0", "28", "9", "26", "30", "11", "7", "20", "32", "17", "5",
                    "22", "34", "15", "3", "24", "36", "13", "1", "00", "27", "10", 
                    "25", "29", "12", "8", "19", "31", "18", "6", "21", "33", "16", 
                    "4", "23", "35", "14", "2"]
    for i, num in enumerate(ROULETTE_NUMBERS):
        angle_start = i * SECTOR_ANGLE + rotation_angle
        angle_end = (i + 1) * SECTOR_ANGLE + rotation_angle
        angle_mid = (angle_start + angle_end) / 2

        # 색상 선택
        if num in ["0", "00"]:
            color = GREEN
        elif i % 2 == 0:
            color = RED
        else:
            color = BLACK

        # 섹터 그리기
        start_rad = math.radians(angle_start)
        end_rad = math.radians(angle_end)
        points = [CENTER]
        for angle in range(int(angle_start), int(angle_end)+1):
            rad = math.radians(angle)
            x = CENTER[0] + RADIUS * math.cos(rad)
            y = CENTER[1] + RADIUS * math.sin(rad)
            points.append((x, y))
        pygame.draw.polygon(screen, color, points)


        # 번호 그리기 (각도에 맞춰 회전)
        text_angle = math.radians(angle_mid)
        tx = CENTER[0] + (RADIUS - 40) * math.cos(text_angle)
        ty = CENTER[1] + (RADIUS - 40) * math.sin(text_angle)
        text = FONT.render(str(num), True, WHITE if color != WHITE else BLACK)
        rotated_text = pygame.transform.rotate(text, -angle_mid + 90)  # +90은 글씨를 바깥으로 정렬
        text_rect = rotated_text.get_rect(center=(tx, ty))
        screen.blit(rotated_text, text_rect)

# 구슬 그리기
def draw_ball(ball_angle):
    ball_x = CENTER[0] + (RADIUS + 10) * math.cos(math.radians(ball_angle))
    ball_y = CENTER[1] + (RADIUS + 10) * math.sin(math.radians(ball_angle))
    pygame.draw.circle(screen, GRAY, (int(ball_x), int(ball_y)), BALL_RADIUS)

# 게임 루프
def main():
    running = True
    rotation_angle = 0  # 회전 각도
    ball_angle = random.randint(0, NUM_SECTORS - 1) * SECTOR_ANGLE+SECTOR_ANGLE      # 구슬의 초기 각도
    ball_speed = 5      # 구슬의 속도 (회전 속도)
    ball_rotating = False  # 구슬이 회전 중인지 여부
    stop_angle = random.randint(0, NUM_SECTORS - 1) * SECTOR_ANGLE  # 구슬 멈출 위치
    clock = pygame.time.Clock()
    rotation_speed = 10
    while running:
        delta_time = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 스페이스바로 회전 시작
                    ball_rotating = True
                    ball_speed = 10  # 속도 설정
                    rotation_speed=10
                    stop_index = random.randint(0, NUM_SECTORS - 1)
                    stop_angle = stop_index * SECTOR_ANGLE + SECTOR_ANGLE / 2

        if ball_rotating:
            # 원판 회전
            rotation_angle += rotation_speed  
            ball_angle -= ball_speed
            if abs(ball_angle - stop_angle) < 1:  # 차이가 1도 이내면 멈춤
                ball_rotating = False
                ball_angle = stop_angle  # 정확히 목표 각도에 멈춤
                ball_speed = 0
                rotation_speed = 0
            if abs(ball_angle - stop_angle) > 1:  # 목표 각도와 차이가 있을 때만 감속
                ball_speed *= 0.99
                rotation_speed*=0.99
            if ball_speed < 0.05:
                ball_rotating = False
                ball_speed = 0
                rotation_speed = 0
        draw_roulette(rotation_angle)  # 원판 그리기
        draw_ball(ball_angle)  # 구슬 그리기

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 FPS로 제한

    pygame.quit()

if __name__ == "__main__":
    main()
