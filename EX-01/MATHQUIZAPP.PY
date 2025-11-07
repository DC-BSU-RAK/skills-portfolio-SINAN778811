import tkinter as tk
from tkinter import messagebox
import random

def displayMenu():
    clear_window()
    root.configure(bg="#222831")  # dark background

    tk.Label(root, text="🎯 MATHS QUIZ 🎯", font=("Comic Sans MS", 22, "bold"), fg="#FFD369", bg="#222831").pack(pady=15)
    tk.Label(root, text="Select Difficulty Level", font=("Poppins", 14, "bold"), fg="white", bg="#222831").pack(pady=10)

    make_button("1️⃣ Easy (1-digit numbers)", "#00ADB5", lambda: start_quiz("easy"))
    make_button("2️⃣ Moderate (2-digit numbers)", "#393E46", lambda: start_quiz("moderate"))
    make_button("3️⃣ Advanced (4-digit numbers)", "#FFD369", lambda: start_quiz("advanced"))
    make_button("❌ Quit", "#FF5722", root.destroy)


def make_button(text, color, command):
    """Create a custom styled button."""
    button = tk.Button(root,
                       text=text,
                       font=("Poppins", 12, "bold"),
                       bg=color,
                       fg="white" if color != "#FFD369" else "black",
                       width=28,
                       relief="flat",
                       command=command,
                       activebackground="#EEEEEE")
    button.pack(pady=8)


def randomInt(level):
    """Return two random numbers based on difficulty."""
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    elif level == "advanced":
        return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation():
    """Randomly decide between addition or subtraction."""
    return random.choice(['+', '-'])


def displayProblem():
    """Show the next question or results."""
    global current_question, num1, num2, operation, attempt

    if current_question >= 10:
        displayResults()
        return

    clear_window()
    root.configure(bg="#393E46")

    attempt = 1
    num1, num2 = randomInt(difficulty)
    operation = decideOperation()

    tk.Label(root, text=f"Question {current_question + 1} of 10",
             font=("Poppins", 13, "italic"), fg="#FFD369", bg="#393E46").pack(pady=5)

    question_label.config(text=f"{num1} {operation} {num2} = ?", font=("Consolas", 22, "bold"),
                          fg="white", bg="#393E46")
    question_label.pack(pady=15)

    # Entry box
    answer_entry.config(bg="#EEEEEE", fg="#222831", font=("Courier New", 16),
                        relief="flat", justify="center")
    answer_entry.pack(ipady=5, ipadx=10)

    # Submit button
    submit_button.config(text="Submit Answer", bg="#00ADB5", fg="white",
                         font=("Poppins", 12, "bold"), relief="flat", command=isCorrect)
    submit_button.pack(pady=15)

    feedback_label.config(bg="#393E46", fg="white", font=("Poppins", 12))
    feedback_label.pack()

    # Score indicator
    score_label = tk.Label(root,
                           text=f"🏆 Score: {score} | Question: {current_question+1}/10",
                           bg="#393E46", fg="#FFD369", font=("Poppins", 11, "italic"))
    score_label.pack(side="bottom", pady=10)

    answer_entry.delete(0, tk.END)


def isCorrect():
    """Check if the user's answer is correct and handle scoring logic."""
    global score, current_question, attempt

    user_answer = answer_entry.get().strip()

    # Validation
    if not user_answer.lstrip('-').isdigit():
        feedback_label.config(text="⚠️ Please enter a valid number!", fg="#FF5722")
        return

    user_answer = int(user_answer)
    correct_answer = num1 + num2 if operation == '+' else num1 - num2

    # Correct on first or second attempt
    if user_answer == correct_answer:
        if attempt == 1:
            score += 10
            feedback_label.config(text="✅ Correct! +10 points", fg="#4CAF50")
        else:
            score += 5
            feedback_label.config(text="✅ Correct (2nd try)! +5 points", fg="#8BC34A")

        current_question += 1
        root.after(1200, displayProblem)

    else:
        # Wrong on first try → give another chance
        if attempt == 1:
            feedback_label.config(text="❌ Wrong, try again!", fg="#FF5722")
            attempt += 1
            answer_entry.delete(0, tk.END)
        else:
            # Wrong on second try → move to next question, 0 points
            feedback_label.config(text=f"❌ Wrong again! Correct: {correct_answer}", fg="#FF5722")
            current_question += 1
            root.after(1500, displayProblem)


def displayResults():
    """Show final score and grade."""
    clear_window()
    root.configure(bg="#222831")

    # Grade system
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "F"

    tk.Label(root, text="🎉 QUIZ COMPLETE! 🎉", font=("Comic Sans MS", 20, "bold"),
             fg="#FFD369", bg="#222831").pack(pady=15)
    tk.Label(root, text=f"Final Score: {score}/100", font=("Poppins", 16, "bold"),
             fg="white", bg="#222831").pack(pady=5)
    tk.Label(root, text=f"Your Grade: {grade}", font=("Poppins", 14),
             fg="#00ADB5", bg="#222831").pack(pady=5)

    make_button("🔁 Play Again", "#00ADB5", displayMenu)
    make_button("❌ Quit", "#FF5722", root.destroy)


def clear_window():
    """Remove all widgets from the window."""
    for widget in root.winfo_children():
        widget.pack_forget()


def start_quiz(level):
    """Initialize game variables and begin quiz."""
    global difficulty, score, current_question
    difficulty = level
    score = 0
    current_question = 0
    displayProblem()


root = tk.Tk()
root.title("🧮 Maths Quiz Game")
root.geometry("420x400")
root.resizable(False, False)

question_label = tk.Label(root)
answer_entry = tk.Entry(root)
submit_button = tk.Button(root)
feedback_label = tk.Label(root)

displayMenu()
root.mainloop()
