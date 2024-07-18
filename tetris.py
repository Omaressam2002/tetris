import tkinter as tk
import random

# Define the shapes of the Tetrominoes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 1, 0]]  # T shape (different orientation)
]

# Game dimensions
WIDTH = 10
HEIGHT = 20
CELL_SIZE = 30  # Size of each cell in pixels

# Define the colors for different Tetrominoes
COLORS = [
    "cyan",  # I shape
    "purple",  # T shape
    "yellow",  # O shape
    "green",  # S shape
    "red",  # Z shape
    "orange",  # L shape
    "blue"  # J shape
]

class TetrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris")
        self.canvas = tk.Canvas(root, width=WIDTH*CELL_SIZE, height=HEIGHT*CELL_SIZE, bg="black")
        self.canvas.pack()
        self.score = 0
        self.current_piece = None
        self.current_color = None
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.setup_ui()
        self.new_piece()
        self.update_game()
        # Bind keys for user control
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Up>", self.rotate_piece)
        self.root.mainloop()

    def setup_ui(self):
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(pady=10)
        self.game_over_label = tk.Label(self.root, text="", font=("Helvetica", 24))
        self.game_over_label.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    self.canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill=COLORS[self.board[y][x]-1])

        # Draw the current piece
        shape = self.current_shape
        offset = self.current_offset
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    self.canvas.create_rectangle(
                        (x + offset[0]) * CELL_SIZE,
                        (y + offset[1]) * CELL_SIZE,
                        (x + offset[0] + 1) * CELL_SIZE,
                        (y + offset[1] + 1) * CELL_SIZE,
                        fill=self.current_color
                    )

    def check_collision(self, shape, offset):
        shape_height = len(shape)
        shape_width = len(shape[0])
        for y in range(shape_height):
            for x in range(shape_width):
                if shape[y][x] and (y + offset[1] >= HEIGHT or
                                    x + offset[0] < 0 or
                                    x + offset[0] >= WIDTH or
                                    self.board[y + offset[1]][x + offset[0]]):
                    return True
        return False

    def merge_piece(self, shape, offset):
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    self.board[y + offset[1]][x + offset[0]] = self.current_piece

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = HEIGHT - len(new_board)
        self.score += lines_cleared * 100
        self.board = [[0] * WIDTH for _ in range(lines_cleared)] + new_board
        self.score_label.config(text=f"Score: {self.score}")

    def get_random_shape(self):
        shape_index = random.randint(0, len(SHAPES) - 1)
        self.current_piece = shape_index + 1
        self.current_color = COLORS[shape_index]
        return SHAPES[shape_index]

    def new_piece(self):
        self.current_shape = self.get_random_shape()
        self.current_offset = [WIDTH // 2 - len(self.current_shape[0]) // 2, 0]
        if self.check_collision(self.current_shape, self.current_offset):
            self.game_over()

    def game_over(self):
        self.game_over_label.config(text=f"Game Over! Score: {self.score}")

    def drop_piece(self):
        if not self.check_collision(self.current_shape, [self.current_offset[0], self.current_offset[1] + 1]):
            self.current_offset[1] += 1
        else:
            self.merge_piece(self.current_shape, self.current_offset)
            self.clear_lines()
            self.new_piece()
    
    def update_game(self):
        if not self.game_over_label.cget("text"):
            self.drop_piece()
            self.draw_board()
            self.root.after(300, self.update_game) 

    def move_left(self, event):
        # Move the piece left
        if not self.check_collision(self.current_shape, [self.current_offset[0] - 1, self.current_offset[1]]):
            self.current_offset[0] -= 1

    def move_right(self, event):
        # Move the piece right
        if not self.check_collision(self.current_shape, [self.current_offset[0] + 1, self.current_offset[1]]):
            self.current_offset[0] += 1

    def move_down(self, event):
        # Move the piece down
        if not self.check_collision(self.current_shape, [self.current_offset[0], self.current_offset[1] + 1]):
            self.current_offset[1] += 1
        else:
            self.merge_piece(self.current_shape, self.current_offset)
            self.clear_lines()
            self.new_piece()

    def rotate_piece(self, event):
        # Rotate the piece
        new_shape = list(zip(*self.current_shape[::-1]))
        if not self.check_collision(new_shape, self.current_offset):
            self.current_shape = new_shape


if __name__ == "__main__":
    root = tk.Tk()
    TetrisGame(root)
