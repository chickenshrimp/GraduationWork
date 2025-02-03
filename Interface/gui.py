import tkinter as tk
from tkinter import ttk
import subprocess
import os
from threading import Thread
import itertools

# Функция для анимации загрузки
def animate_loader():
    for frame in itertools.cycle(["◐", "◓", "◑", "◒"]):  # Символы анимации
        if not loading:
            loader_label.config(text="")
            break
        loader_label.config(text=frame)
        root.update_idletasks()
        root.after(150)

# Функция запуска генерации персонажа
def run_script():
    global loading
    prompt_text = input_field.get().strip()
    if not prompt_text:
        status_label.config(text="Enter character description", foreground="red")
        return

    status_label.config(text="Generation of 2d version...", foreground="black")
    loading = True
    Thread(target=animate_loader, daemon=True).start()

    def run_process():
        try:
            # Определяем пути
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            main_script_path = os.path.join(base_dir, "api", "main.py")
            images_dir = os.path.join(base_dir, "input", "images")

            # Запуск main.py
            result = subprocess.run(['python', main_script_path, prompt_text], capture_output=True, text=True)
            print(result.stdout)

            status_label.config(text="Generation of 3d version. Please, wait...")
            latest_image = sorted(os.listdir(images_dir))[-1]  # Получаем последнюю картинку

            optimizer_path = os.path.join(base_dir, "optimizer.py")
            output_path = os.path.join(base_dir, "output")

            optimizer_result = subprocess.run(
                ['python', optimizer_path, '--input', os.path.join(images_dir, latest_image), '--output', output_path], 
                capture_output=True, text=True, cwd=base_dir
            )

            print(optimizer_result.stdout)
            status_label.config(text="Completed!", foreground="green")

        except Exception as e:
            print(f"Ошибка: {e}")
            status_label.config(text="Error!", foreground="red")

        finally:
            global loading
            loading = False
            loader_label.config(text="")

    Thread(target=run_process, daemon=True).start()

root = tk.Tk()
root.title("Character Generator")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

FONT_MAIN = ("Arial", 12)
FONT_BOLD = ("Arial", 12, "bold")

title_label = tk.Label(root, text="Character Generator", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=5)

input_field = ttk.Entry(input_frame, width=40, font=FONT_MAIN)
input_field.pack(side="left", padx=5)

run_button = ttk.Button(root, text="Generate", command=run_script)
run_button.pack(pady=10)

# Лоадер (анимация)
loader_label = tk.Label(root, text="", font=("Arial", 20), bg="#f0f0f0", fg="blue")
loader_label.pack(pady=5)

status_label = tk.Label(root, text="", font=FONT_BOLD, bg="#f0f0f0")
status_label.pack(pady=5)

# Запуск интерфейса
root.mainloop()