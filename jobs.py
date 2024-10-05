import tkinter as tk
import random
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk

class Ameba:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай число")
        self.root.configure(bg='black')
        self.min_value = 1
        self.max_value = 100
        self.secret_number = random.randint(self.min_value, self.max_value)
        self.tries = 0
        self.last_guess = None
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text=f"Угадайте число от {self.min_value} до {self.max_value}:",
                              bg='black', fg='orange', font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, bg='black', fg='orange', font=("Arial", 12))
        self.entry.pack(pady=5)

        self.check_button = tk.Button(self.root, text="Чекнуть", command=self.check_guess,
                                      bg='black', fg='orange', font=("Arial", 12))
        self.check_button.pack(pady=5)

        self.result_label = tk.Label(self.root, text="", bg='black', fg='orange', font=("Arial", 12))
        self.result_label.pack(pady=10)

    def check_guess(self):
        guess = self.entry.get()
        if not guess.isdigit():
            messagebox.showwarning("Ошибка", "Пожалуйста, введите число.")
            return
        guess = int(guess)
        self.tries += 1

        prompt = self.get_prompt(guess)
        if guess < self.secret_number:
            self.result_label.config(text=f"{prompt} Загаданное число больше.")
        elif guess > self.secret_number:
            self.result_label.config(text=f"{prompt} Загаданное число меньше.")
        else:
            self.show_celebration()
            self.reset_game()

        self.last_guess = guess

    def get_prompt(self, guess):
        distance = abs(guess - self.secret_number)
        
        if distance == 0:
            return ""
        elif distance <= 1:
            return "Ты такой горячий!!!"
        elif distance <= 3:
            return "Еще чуть-чуть!"
        elif distance <= 5:
            return "Очень горячо!"
        elif distance <= 12:
            return "Горячо!"
        elif distance <= 20:
            return "Тепло!"
        elif distance <= 30:
            return "Прохладно!"
        elif distance <= 50:
            return "Холодно!"
        else:
            return "Очень холодно!"

    def show_celebration(self):
        celebration_window = Toplevel(self.root)
        celebration_window.title("ГОЙДА!")
        celebration_window.configure(bg='black')

        label = tk.Label(celebration_window, text="ГОЙДА!", font=("Arial", 24), fg='orange', bg='black')
        label.pack(pady=10)

        self.load_gif(celebration_window)

    def load_gif(self, window):
        gif_path = "russiaflag.gif"
        img = Image.open(gif_path)
        frames = []
        num_frames = img.n_frames 
        for frame_index in range(num_frames):
            img.seek(frame_index)
            frame = ImageTk.PhotoImage(img.copy())  
            frames.append(frame)

        gif_label = tk.Label(window, bg='black')
        gif_label.pack()

        def update_frame(index):
            gif_label.config(image=frames[index]) 
            index = (index + 1) % num_frames 
            window.after(100, update_frame, index) 

        window.after(0, update_frame, 0)


    def reset_game(self):
        self.secret_number = random.randint(self.min_value, self.max_value)
        self.tries = 0
        self.last_guess = None
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = Ameba(root)
    root.mainloop()
