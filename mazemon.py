import tkinter as tk
import numpy as np
import random
from dataclasses import dataclass

TILE_SIZE = 40
MAZE_SIZE = 10

@dataclass
class Player:
    x: int
    y: int

@dataclass
class Monster:
    x: int
    y: int

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("미로 탈출 게임")
        self.canvas = tk.Canvas(root, width=MAZE_SIZE * TILE_SIZE, height=MAZE_SIZE * TILE_SIZE)
        self.canvas.pack()
        self.player = Player(1, 1)
        self.monster = Monster(MAZE_SIZE - 2, MAZE_SIZE - 3)
        self.maze = self.generate_maze()
        self.game_over = False
        self.root.bind("<Key>", self.handle_key)
        self.draw_maze()

    def generate_maze(self):
        maze = np.full((MAZE_SIZE, MAZE_SIZE), '#', dtype=str)

    # 내부 공간 무작위로 벽과 통로 생성
        for y in range(1, MAZE_SIZE - 1):
            for x in range(1, MAZE_SIZE - 1):
                maze[y, x] = '.' if random.random() > 0.25 else '#'

    # 시작 위치, 몬스터 위치, 출구는 반드시 통로
        maze[1, 1] = '.'  # Player start
        maze[MAZE_SIZE - 2, MAZE_SIZE - 3] = '.'  # Monster start
        maze[MAZE_SIZE - 2, MAZE_SIZE - 2] = 'E'  # Exit
    
        return maze


    def draw_maze(self):
        self.canvas.delete("all")
        for y in range(MAZE_SIZE):
            for x in range(MAZE_SIZE):
                tile = self.maze[y, x]
                color = {
                    '#': 'gray',
                    '.': 'white',
                    'E': 'blue'
                }.get(tile, 'white')
                if self.player.x == x and self.player.y == y:
                    color = 'green'
                elif self.monster.x == x and self.monster.y == y:
                    color = 'red'
                self.canvas.create_rectangle(
                    x * TILE_SIZE, y * TILE_SIZE,
                    (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE,
                    fill=color, outline='black'
                )
        
        

    def handle_key(self, event):
        if self.game_over:
            return

        key = event.keysym
        dx, dy = 0, 0
        if key == 'Up': dy = -1
        elif key == 'Down': dy = 1
        elif key == 'Left': dx = -1
        elif key == 'Right': dx = 1

        new_x = self.player.x + dx
        new_y = self.player.y + dy
        if 0 <= new_x < MAZE_SIZE and 0 <= new_y < MAZE_SIZE:
            if self.maze[new_y, new_x] != '#':
                self.player.x = new_x
                self.player.y = new_y
        if self.maze[self.player.y, self.player.x] == 'E':
            self.game_over = True
            self.draw_maze()
            self.canvas.create_text(MAZE_SIZE * TILE_SIZE // 2, MAZE_SIZE *     TILE_SIZE // 2,
                                    text="🎉 탈출 성공!", font=("Arial",    24), fill="green")
            return

    # 2. 몬스터 이동
        self.move_monster()

    # 3. 충돌 체크
        if self.player.x == self.monster.x and self.player.y == self.monster.y:
            self.game_over = True
            self.draw_maze()
            self.canvas.create_text(MAZE_SIZE * TILE_SIZE // 2, MAZE_SIZE *     TILE_SIZE // 2,
                                    text="💀 게임 오버 💀", font=("Arial",  24), fill="red")
            return
        self.draw_maze()

    def move_monster(self):
        if self.game_over:
            return

        # 몬스터가 랜덤으로 상하좌우로 한 칸 이동
        direction = random.choice(['Up', 'Down', 'Left', 'Right'])
        dx, dy = 0, 0
        if direction == 'Up': dy = -1
        elif direction == 'Down': dy = 1
        elif direction == 'Left': dx = -1
        elif direction == 'Right': dx = 1

        new_x = self.monster.x + dx
        new_y = self.monster.y + dy
        if 0 <= new_x < MAZE_SIZE and 0 <= new_y < MAZE_SIZE:
            if self.maze[new_y, new_x] != '#':
                self.monster.x = new_x
                self.monster.y = new_y

    def check_collision(self):
        if self.player.x == self.monster.x and self.player.y == self.monster.y:
            self.game_over = True
            self.canvas.create_text(MAZE_SIZE * TILE_SIZE // 2, MAZE_SIZE * TILE_SIZE // 2,
                                    text="💀 게임 오버 💀", font=("Arial", 24), fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()
