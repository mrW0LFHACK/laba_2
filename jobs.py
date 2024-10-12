import tkinter as tk
import random
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3")


class Ameba:
    def __init__(self, root, attempts=None):
        self.root = root
        self.root.title("Угадай число with AI")
        self.root.configure(bg='black')
        self.min_value = 1
        self.max_value = 100
        self.secret_number = random.randint(self.min_value, self.max_value)
        self.tries = 0
        self.last_guess = None
        self.max_attempts = attempts
        self.attempts_left = attempts
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

        if self.max_attempts is not None:
            self.attempts_frame = tk.Frame(self.root, bg='black')
            self.attempts_frame.pack(pady=10)
            self.attempts_labels = [tk.Label(self.attempts_frame, bg='red', width=4, height=2)
                                    for _ in range(self.max_attempts)]
            for label in self.attempts_labels:
                label.pack(side=tk.LEFT, padx=5)

    def check_guess(self):
        guess = self.entry.get()
        if not guess.isdigit():
            messagebox.showwarning("Ошибка", "Пожалуйста, введите число.")
            return
        guess = int(guess)
        self.tries += 1

        prompt = self.get_prompt(guess)
        if guess < self.secret_number:
            self.result_label.config(text=f"{prompt} (Больше)")
        elif guess > self.secret_number:
            self.result_label.config(text=f"{prompt} (Меньше)")
        else:
            self.show_celebration()
            self.reset_game()
            return

        if self.max_attempts is not None:
            self.update_attempts()

        self.last_guess = guess

    def get_prompt(self, guess):
        result = model.invoke(input=f"Мне загадали число {self.secret_number}, а я ввел{guess} Дай подсказку на русском языке, которая поможет мне приблизиться к верному числу (максимум 7 слов). Не называй загаданное число! И не давай подсказки, как 'прибвыьте 5', 'поделите на 4' и так далее. Можешь использовать фразы по типу 'Ваше число сильно меньше загаданого', 'Ваше число капельку больше чем загаданное'")
#       result = model.invoke(input=f"Мне загадали число {self.secret_number}, а я ввел{guess} Дай подсказку на русском языке, которая поможет мне приблизиться к верному числу (максимум 7 слов). Не раскрывай число, можешь использовать, 'ваше число меньше', 'ваше число сильно больше', и так далее")
        print(self.secret_number)
        return result

    def update_attempts(self):
        if self.attempts_left > 0:
            self.attempts_labels[self.attempts_left - 1].config(bg='black')
            self.attempts_left -= 1
        if self.attempts_left == 0:
            messagebox.showinfo("Конец игры", "Вы исчерпали все попытки!")
            self.reset_game()

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
        if self.max_attempts is not None:
            self.attempts_left = self.max_attempts
            for label in self.attempts_labels:
                label.config(bg='red')


def start_game(mode):
    game_window = tk.Toplevel()  
    if mode == "no_attempts":
        Ameba(game_window)
    elif mode == "three_attempts":
        Ameba(game_window, attempts=3)


def show_mode_selection():
    selection_window = tk.Tk()  
    selection_window.title("Выбор режима игры")
    selection_window.configure(bg='black')

    label = tk.Label(selection_window, text="Выберите режим игры:", bg='black', fg='orange', font=("Arial", 14))
    label.pack(pady=10)

    no_attempts_button = tk.Button(selection_window, text="Играть без попыток", 
                                   command=lambda: [selection_window.destroy(), start_game("no_attempts")],
                                   bg='black', fg='orange', font=("Arial", 12))
    no_attempts_button.pack(pady=5)

    three_attempts_button = tk.Button(selection_window, text="Играть с 3 попытками", 
                                      command=lambda: [selection_window.destroy(), start_game("three_attempts")],
                                      bg='black', fg='orange', font=("Arial", 12))
    three_attempts_button.pack(pady=5)

    selection_window.mainloop()


if __name__ == "__main__":
    show_mode_selection()
