import tkinter as tk
from tkinter import messagebox
import random

levels = [
    ("cat", "+", "fish", "catfish"),
    ("sun", "-", "s", "un"),
    ("butter", "+", "fly", "butterfly"),
    ("dog", "+", "house", "doghouse"),
    ("rain", "-", "r", "ain"),
    ("star", "+", "fish", "starfish"),
]

dot_patterns = {
    "catfish": [(100,150),(150,100),(200,120),(220,180),(180,220),(140,200),(120,170)],
    "un": [(150,150),(180,120),(210,150),(210,190),(180,210),(150,180)],
    "butterfly": [(100,180),(130,130),(170,120),(210,150),(230,200),(200,230),(150,220),(120,190)],
    "doghouse": [(100,200),(140,150),(190,150),(230,180),(220,220),(180,240),(130,230)],
    "ain": [(160,160),(200,140),(230,170),(230,210),(200,230),(160,200)],
    "starfish": [(110,150),(150,110),(190,140),(180,190),(140,220),(110,180),(160,180)],
}

colors = {
    "catfish": "orange",
    "un": "purple",
    "butterfly": "yellow",
    "doghouse": "brown",
    "ain": "blue",
    "starfish": "cyan",
}

class Game:
    def __init__(self, master):
        self.master = master
        master.title("Word Equation Dot Connect Game")
        master.configure(bg="#a4d4c8")

        self.level_index = 0
        self.diamonds = 0
        self.hints_used = 0

        self.top_frame = tk.Frame(master, bg="#a4d4c8")
        self.top_frame.pack(pady=10)

        self.equation_label = tk.Label(self.top_frame, text="", font=("Arial", 24, "bold"), fg="navy", bg="#a4d4c8")
        self.equation_label.pack(side="left", padx=20)

        self.diamond_label = tk.Label(self.top_frame, text=f"Blue Diamonds: {self.diamonds}", font=("Arial", 18), fg="navy", bg="#a4d4c8")
        self.diamond_label.pack(side="right", padx=20)

        self.canvas = tk.Canvas(master, width=400, height=300, bg="#a4d4c8", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.btn_frame = tk.Frame(master, bg="#a4d4c8")
        self.btn_frame.pack()

        self.hint_btn = tk.Button(self.btn_frame, text="❓", font=("Arial", 18, "bold"), command=self.show_hint)
        self.hint_btn.grid(row=0, column=0, padx=10)

        self.submit_btn = tk.Button(self.btn_frame, text="Submit", font=("Arial", 18), command=self.submit)
        self.submit_btn.grid(row=0, column=1, padx=10)

        self.next_btn = tk.Button(self.btn_frame, text="Next Level", font=("Arial", 18), state="disabled", command=self.next_level)
        self.next_btn.grid(row=0, column=2, padx=10)

        self.info_label = tk.Label(master, text="Draw lines connecting the dots to form the object/animal.", font=("Arial", 14), fg="navy", bg="#a4d4c8")
        self.info_label.pack(pady=5)

        self.lines = []
        self.current_line = None
        self.last_dot = None

        self.load_level()

        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)

    def load_level(self):
        self.canvas.delete("all")
        self.lines.clear()
        self.current_line = None
        self.last_dot = None
        self.next_btn.config(state="disabled")
        self.connected_pairs = set()

        self.current_level = levels[self.level_index]
        word1, op, word2, answer = self.current_level

        eq_text = f"{word1} {op} {word2}"
        self.equation_label.config(text=eq_text)

        self.dots = []
        self.dot_ids = []
        self.dot_positions = dot_patterns[answer]
        self.dot_color = colors.get(answer, "black")

        for (x,y) in self.dot_positions:
            dot = self.canvas.create_oval(x-7, y-7, x+7, y+7, fill=self.dot_color, outline="")
            self.dots.append((x,y))
            self.dot_ids.append(dot)

    def start_line(self, event):
        dot_index = self.get_closest_dot(event.x, event.y)
        if dot_index is not None:
            self.last_dot = dot_index
            x, y = self.dots[dot_index]
            self.current_line = self.canvas.create_line(x, y, event.x, event.y, fill=self.dot_color, width=3)

    def draw_line(self, event):
        if self.current_line is not None:
            x1, y1 = self.dots[self.last_dot]
            self.canvas.coords(self.current_line, x1, y1, event.x, event.y)

    def end_line(self, event):
        if self.current_line is None or self.last_dot is None:
            return

        dot_index = self.get_closest_dot(event.x, event.y)
        if dot_index is not None and dot_index != self.last_dot:
            x1, y1 = self.dots[self.last_dot]
            x2, y2 = self.dots[dot_index]
            self.canvas.coords(self.current_line, x1, y1, x2, y2)
            pair = frozenset({self.last_dot, dot_index})
            if pair not in self.connected_pairs:
                self.connected_pairs.add(pair)
            else:
                # Already connected, remove line
                self.canvas.delete(self.current_line)
            self.lines.append(self.current_line)
        else:
            self.canvas.delete(self.current_line)

        self.current_line = None
        self.last_dot = None

    def get_closest_dot(self, x, y):
        for i, (dx, dy) in enumerate(self.dots):
            if abs(dx - x) <= 15 and abs(dy - y) <= 15:
                return i
        return None

    def show_hint(self):
        if self.hints_used < 3:
            messagebox.showinfo("Hint", f"The answer is: {self.current_level[3]}")
            self.hints_used += 1
        else:
            if self.diamonds >= 5:
                self.diamonds -= 5
                self.diamond_label.config(text=f"Blue Diamonds: {self.diamonds}")
                messagebox.showinfo("Hint", f"The answer is: {self.current_level[3]}")
                self.hints_used += 1
            else:
                messagebox.showwarning("Not enough diamonds", "You need 5 blue diamonds to get a hint.")

    def submit(self):
        required_connections = set()
        for i in range(len(self.dots)-1):
            required_connections.add(frozenset({i, i+1}))

        if required_connections.issubset(self.connected_pairs):
            messagebox.showinfo("Success", "Correct! You earned 20 blue diamonds.")
            self.diamonds += 20
            self.diamond_label.config(text=f"Blue Diamonds: {self.diamonds}")
            self.next_btn.config(state="normal")
        else:
            messagebox.showerror("Incorrect", "Connections not correct. Try again!")

    def next_level(self):
        self.level_index = (self.level_index + 1) % len(levels)
        self.load_level()

root = tk.Tk()
game = Game(root)
root.mainloop()
