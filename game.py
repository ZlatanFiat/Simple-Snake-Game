# Program in Python to create a Snake Game

from tkinter import *
import random

# Initialization of Dimensions and Constants
WIDTH = 720
HEIGHT = 640
INITIAL_SPEED = 120  # Slightly relaxed starting speed
SPEED = INITIAL_SPEED
SPACE_SIZE = 20
BODY_SIZE = 3

# Cyberpunk / Neon Color Palette
SNAKE_HEAD = "#FFFF00"      # Yellow for the head
SNAKE = "#00FF66"           # Neon Green for the body
SNAKE_BORDER = "#002208"
FOOD = "#FF00FF"            # Neon Magenta for food
BACKGROUND = "#09090E"      # Deep space-like dark background
GRID_COLOR = "#12121F"      # Discreet tech grid

game_started = False
can_change_direction = True

class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        # Create initial coordinates
        for i in range(0, BODY_SIZE):
            self.coordinates.append([WIDTH // 2, HEIGHT // 2]) # Starts at center

        # Draw the initial body
        for index, (x, y) in enumerate(self.coordinates):
            color = SNAKE_HEAD if index == 0 else SNAKE
            
            # Shrinking effect: the tail is slightly smaller than the head
            offset = min(index, 4) 
            
            square = canvas.create_oval(
                x + 1 + offset, y + 1 + offset, 
                x + SPACE_SIZE - 1 - offset, y + SPACE_SIZE - 1 - offset,
                fill=color, outline=SNAKE_BORDER, width=1, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self):
        # Prevent food from spawning exactly on the outer edges
        x = random.randint(1, (WIDTH // SPACE_SIZE) - 2) * SPACE_SIZE
        y = random.randint(1, (HEIGHT // SPACE_SIZE) - 2) * SPACE_SIZE
        self.coordinates = [x, y]
        
        # Neon circular food
        canvas.create_oval(
            x + 2, y + 2, 
            x + SPACE_SIZE - 2, y + SPACE_SIZE - 2, 
            fill=FOOD, outline="#FFFFFF", width=1, tag="food"
        )

def next_turn(snake, food):
    global can_change_direction, SPEED
    
    if not game_started:
        window.after(SPEED, next_turn, snake, food)
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert new head
    snake.coordinates.insert(0, (x, y))

    # Update body: turn the old Yellow head into a Green body segment
    if len(snake.squares) > 0:
        canvas.itemconfig(snake.squares[0], fill=SNAKE, outline=SNAKE_BORDER)

    # Draw new Yellow head
    square = canvas.create_oval(
        x + 1, y + 1, x + SPACE_SIZE - 1, y + SPACE_SIZE - 1,
        fill=SNAKE_HEAD, outline=SNAKE_BORDER, width=1, tag="snake"
    )
    snake.squares.insert(0, square)

    # Check if snake ate food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Points: {}  |  Speed: {}%".format(score, int((INITIAL_SPEED/SPEED)*100)))
        canvas.delete("food")
        food = Food()
        
        # --- INCREASING SPEED LOGIC ---
        if score % 3 == 0 and SPEED > 45:
            SPEED -= 10
            
    else:
        # Remove the last segment if not eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Apply progressive shrinking effect to the entire body
    for index, square_id in enumerate(snake.squares):
        if index > 0:
            offset = min(index // 2, 4)
            cx, cy = snake.coordinates[index]
            canvas.coords(
                square_id, 
                cx + 1 + offset, cy + 1 + offset, 
                cx + SPACE_SIZE - 1 - offset, cy + SPACE_SIZE - 1 - offset
            )

    if check_collisions(snake):
        game_over()
    else:
        can_change_direction = True
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction, can_change_direction
    
    if not can_change_direction:
        return
        
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
        can_change_direction = False
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
        can_change_direction = False
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
        can_change_direction = False
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction
        can_change_direction = False

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#050508")
    
    canvas.create_text(WIDTH/2, HEIGHT/2 - 30,
                       font=('consolas', 65, 'bold'), text="GAME OVER", 
                       fill="#FF0055", tag="gameover")
    
    canvas.create_text(WIDTH/2, HEIGHT/2 + 50,
                       font=('consolas', 22), text="Final Score: {}".format(score), 
                       fill="white", tag="gameover")

def start_game(event):
    global game_started
    if not game_started:
        canvas.delete("start_text")
        game_started = True

def draw_grid():
    for x in range(0, WIDTH, SPACE_SIZE):
        canvas.create_line(x, 0, x, HEIGHT, fill=GRID_COLOR, width=1)
    for y in range(0, HEIGHT, SPACE_SIZE):
        canvas.create_line(0, y, WIDTH, y, fill=GRID_COLOR, width=1)

# Window Setup
window = Tk()
window.title("SNAKE Game Pro")
window.configure(bg=BACKGROUND)
window.resizable(False, False)

score = 0
direction = 'right'

# Label for Score and Speed
label = Label(window, text="Points: 0  |  Speed: 100%",
            font=('consolas', 18, 'bold'), fg="#00FFCC", bg=BACKGROUND, pady=10)
label.pack()

canvas = Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH, highlightthickness=0)
canvas.pack()

draw_grid()
window.update()

# Window Centering
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Key Bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', start_game)

snake = Snake()
food = Food()

canvas.create_text(WIDTH/2, HEIGHT/2, text="Press 'Return' to play",
                  fill="#FFFF00", font=('consolas', 28, 'bold'), tag="start_text")

next_turn(snake, food)
window.mainloop()
