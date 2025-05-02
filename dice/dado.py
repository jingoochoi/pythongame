import tkinter as tk
import random
from PIL import Image, ImageTk

# 윈도우 설정
root = tk.Tk()
root.title("🎲 애니메이션 주사위")
root.geometry("200x200")

# 주사위 이미지 로드 (dice1.png ~ dice6.png)
dice_images = [ImageTk.PhotoImage(Image.open(f"dice/dice{i}.png").resize((100, 100))) for i in range(1, 7)]

# 주사위 이미지 라벨
dice_label = tk.Label(root, image=dice_images[0])
dice_label.pack(pady=10)

rolling = False
roll_count = 0
max_rolls = 50  # 10ms * 50회 = 약 0.5초

def animate_roll():
    global roll_count, rolling
    if roll_count < max_rolls:
        num = random.randint(1, 6)
        dice_label.config(image=dice_images[num - 1])
        dice_label.image = dice_images[num - 1]
        roll_count += 1
        root.after(10, animate_roll)
    else:
        # 마지막 굴린 값 표시
        final = random.randint(1, 6)
        dice_label.config(image=dice_images[final - 1])
        dice_label.image = dice_images[final - 1]
        rolling = False

def start_roll():
    global roll_count, rolling
    if not rolling:
        roll_count = 0
        rolling = True
        animate_roll()

# 굴리기 버튼
btn = tk.Button(root, text="roll", command=start_roll,cursor='hand2')
btn.pack(pady=5)

root.mainloop()
