from tkinter import *
import random
GAME_WIDTH = 700
GAME_HEIGHT = 600
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
PADDING_CELLS = 0
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        start_x = ((GAME_WIDTH // 2) // SPACE_SIZE) * SPACE_SIZE
        start_y = ((GAME_HEIGHT // 2) // SPACE_SIZE) * SPACE_SIZE
        for i in range(BODY_PARTS):
            self.coordinates.append([start_x - i * SPACE_SIZE, start_y])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                             fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                           fill=FOOD_COLOR, tag="food")
def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score:{score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions_premature(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)
def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction
def check_collisions_premature(snake):
    """
    Premature collision: shrink the allowed play area inward by PADDING_CELLS grid cells
    on every side. Hitting that inner border counts as a collision.
    """
    x, y = snake.coordinates[0]
    min_x = PADDING_CELLS * SPACE_SIZE
    min_y = PADDING_CELLS * SPACE_SIZE
    max_x = GAME_WIDTH - (PADDING_CELLS + 1) * SPACE_SIZE
    max_y = GAME_HEIGHT - (PADDING_CELLS + 1) * SPACE_SIZE
    if x < min_x or x > max_x:
        return True
    if y < min_y or y > max_y:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
window = Tk()
window.title("Snake game (Premature wall collisions)")
window.resizable(False, False)
score = 0
direction = 'right'
label = Label(window, text=f"Score:{score}", font=('consolas', 40))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
window.update_idletasks()
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('a', lambda event: change_direction('left'))
window.bind('d', lambda event: change_direction('right'))
window.bind('w', lambda event: change_direction('up'))
window.bind('s', lambda event: change_direction('down'))
snake = Snake()
food = Food()
next_turn(snake, food)
window.mainloop()