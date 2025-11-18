import tkinter as tk
import random
import os

# Load jokes from file (setup? punchline)
def load_jokes():
    jokes = []
    with open("randomjokes.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline))
    return jokes

jokes_list = load_jokes()
current_joke = None


# Fade-in animation for label text
def fade_in(label, text, delay=30, step=0):
    if step == 0:
        label.config(text="")
        label.opacity_text = ""

    if step < len(text):
        label.opacity_text += text[step]
        label.config(text=label.opacity_text)
        root.after(delay, fade_in, label, text, delay, step + 1)


# Slide-in animation for punchline
def slide_in(label, text, y_start=40, step=0):
    if step == 0:
        label.place_configure(y=y_start)
        label.config(text=text)

    if y_start > 0:
        y_start -= 3
        label.place_configure(y=y_start)
        root.after(10, slide_in, label, text, y_start, step + 1)


def show_joke():
    global current_joke
    current_joke = random.choice(jokes_list)
    punchline_label.config(text="")
    punchline_label.place_configure(y=200)

    fade_in(setup_label, current_joke[0], delay=30)

def show_punchline():
    if current_joke:
        slide_in(punchline_label, current_joke[1])


# GUI Setup
root = tk.Tk()
root.title("Alexa tell me a Joke")
root.geometry("600x350")
root.configure(bg="#181818")


# Window fade-in effect
def window_fade(step=0):
    if step <= 1:
        root.attributes("-alpha", step)
        root.after(20, window_fade, step + 0.05)
window_fade()


# Setup display labels
setup_label = tk.Label(root, text="", fg="white", bg="#181818",
                       font=("Arial", 18, "bold"), wraplength=550, justify="center")
setup_label.pack(pady=20)

punchline_label = tk.Label(root, text="", fg="#00ffaa", bg="#181818",
                           font=("Arial", 14, "italic"), wraplength=550, justify="center")
punchline_label.place(x=50, y=200)


# Button Styling + Hover effect
def on_enter(e):
    e.widget["bg"] = "#00ffaa"
    e.widget["fg"] = "#000000"

def on_leave(e):
    e.widget["bg"] = "#303030"
    e.widget["fg"] = "#ffffff"

button_frame = tk.Frame(root, bg="#181818")
button_frame.pack(pady=25)

def make_button(text, command, width):
    btn = tk.Button(button_frame, text=text, command=command, width=width,
                    font=("Arial", 12, "bold"), bg="#303030", fg="white",
                    activebackground="#00ffaa", activeforeground="black",
                    relief="flat", bd=0, padx=5, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


btn_joke = make_button("Alexa tell me a Joke", show_joke, 20)
btn_joke.grid(row=0, column=0, padx=10)

btn_punchline = make_button("Show Punchline", show_punchline, 15)
btn_punchline.grid(row=0, column=1, padx=10)

btn_next = make_button("Next Joke", show_joke, 12)
btn_next.grid(row=0, column=2, padx=10)


btn_quit = tk.Button(root, text="Quit", command=root.quit, width=10,
                     font=("Arial", 12, "bold"), bg="#660000", fg="white", relief="flat")
btn_quit.pack(pady=10)


# Start GUI loop
root.mainloop()
