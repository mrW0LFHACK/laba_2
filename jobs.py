import tkinter as tk
import random
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import time

class Ameba:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай число")
        self.root.configure(bg='black')
        self.min_value = 1
        self.max_value = 100
        self.secret_number = random.randint(self.min_value, self.max_value)
        self.tries = 0
        self.max_tries = 6  # Default for mode 1
        self.mode = 1  # Default game mode
        self.last_guess = None
        self.start_time = None  # Used for mode 2
        self.create_widgets()

    def create_widgets(self):
        # Choose game mode
        self.mode_label = tk.Label(self.root, text="Выберите режим игры:",
                                   bg='black', fg='orange', font=("Arial", 14))
        self.mode_label.pack(pady=10)

        self.mode1_button = tk.Button(self.root, text="Режим 1: Угадай за 6 попыток",
                                      command=lambda: self.set_mode(1),
                                      bg='black', fg='orange', font=("Arial", 12))
        self.mode1_button.pack(pady=5)

        self.mode2_button = tk.Button(self.root, text="Режим 2: Угадай за 20 секунд и 3 попытки",
                                      command=lambda: self.set_mode(2),
                                      bg='black', fg='orange', font=("Arial", 12))
        self.mode2_button.pack(pady=5)

        self.mode3_button = tk.Button(self.root, text="Режим 3: Угадай с 1 попытки",
                                      command=lambda: self.set_mode(3),
                                      bg='black', fg='orange', font=("Arial", 12))
        self.mode3_button.pack(pady=5)

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

    def set_mode(self, mode):
        """Установить режим игры"""
        self.mode = mode
        if mode == 1:
            self.max_tries = 6
            self.result_label.config(text="Режим 1: Угадай за 6 попыток")
        elif mode == 2:
            self.max_tries = 3
            self.start_time = time.time()  # Начало отсчета времени
            self.result_label.config(text="Режим 2: Угадай за 20 секунд и 3 попытки")
        elif mode == 3:
            self.max_tries = 1
            self.result_label.config(text="Режим 3: Угадай с 1 попытки")
        self.reset_game()

    def check_guess(self):
        guess = self.entry.get()
        if not guess.isdigit():
            messagebox.showwarning("Ошибка", "Пожалуйста, введите число.")
            return
        guess = int(guess)
        self.tries += 1

        # Проверка времени для режима 2
        if self.mode == 2:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 20:
                messagebox.showinfo("Время вышло!", "Вы не успели за 20 секунд.")
                self.reset_game()
                return

        if self.tries > self.max_tries:
            messagebox.showinfo("Попытки кончились", "Вы исчерпали все попытки!")
            self.reset_game()
            return

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
            return "КАПЕЦ ТЫ ЛОХ!!! "
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
        """Отображение окна с гифкой и сообщением 'ГОЙДА'"""
        celebration_window = Toplevel(self.root)
        celebration_window.title("ГОЙДА!")
        celebration_window.configure(bg='black')

        # Надпись ГОЙДА
        label = tk.Label(celebration_window, text="ГОЙДА!", font=("Arial", 24), fg='orange', bg='black')
        label.pack(pady=10)

        # Загрузка и отображение гифки
        self.load_gif(celebration_window)

    def load_gif(self, window):
        """Загружает и отображает гифку"""
        gif_path = "russiaflag.gif"  # Путь к гифке
        img = Image.open(gif_path)

        num_frames = img.n_frames
        frames = [ImageTk.PhotoImage(img.copy().convert('RGBA')) for _ in range(num_frames)]

        gif_label = tk.Label(window, bg='black')
        gif_label.pack()

        def update_frame(index):
            gif_label.config(image=frames[index])
            index = (index + 1) % num_frames
            window.after(100, update_frame, index)

        # Запуск анимации
        window.after(0, update_frame, 0)

    def reset_game(self):
        """Сброс игры после победы или проигрыша"""
        self.secret_number = random.randint(self.min_value, self.max_value)
        self.tries = 0
        self.last_guess = None
        self.entry.delete(0, tk.END)
        if self.mode == 2:
            self.start_time = time.time()  # Обновление времени для режима 2

if __name__ == "__main__":
    root = tk.Tk()
    game = Ameba(root)
    root.mainloop()
