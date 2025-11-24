import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# Colors
BG_COLOR = "#F0F4F8"       # main background
BTN_COLOR = "#4DCCBD"     # turquoise buttons
BTN_TEXT = "white"
OUTPUT_BG = "#FFFFFF"
TITLE_COLOR = "#333"

class Student:
    def __init__(self, sid, name, c1, c2, c3, exam):
        self.sid = sid
        self.name = name
        self.c1 = int(c1)
        self.c2 = int(c2)
        self.c3 = int(c3)
        self.exam = int(exam)

    def coursework_total(self):
        return self.c1 + self.c2 + self.c3

    def overall_total(self):
        return self.coursework_total() + self.exam

    def percentage(self):
        return (self.overall_total() / 160) * 100

    def grade(self):
        p = self.percentage()
        if p >= 70:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 40:
            return "D"
        else:
            return "F"

    def summary(self):
        return (
            f"Name: {self.name}\n"
            f"Student Number: {self.sid}\n"
            f"Coursework Total: {self.coursework_total()}/60\n"
            f"Exam Mark: {self.exam}/100\n"
            f"Overall %: {self.percentage():.2f}%\n"
            f"Grade: {self.grade()}\n"
            f"{'-'*40}\n"
        )


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.configure(bg=BG_COLOR)

        self.students = []
        self.load_data()

        # ======= Layout Frames =======
        left_frame = tk.Frame(root, bg=BG_COLOR)
        left_frame.pack(side="left", fill="y", padx=15, pady=15)

        right_frame = tk.Frame(root, bg=BG_COLOR)
        right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # ======= Title =======
        tk.Label(left_frame, text="Student Manager", font=("Arial", 18, "bold"),
                 bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=10)

        # ======= Buttons =======
        def create_button(text, command):
            return tk.Button(
                left_frame,
                text=text,
                width=25,
                height=2,
                bg=BTN_COLOR,
                fg=BTN_TEXT,
                font=("Arial", 11, "bold"),
                relief="flat",
                command=command
            )

        create_button("📄 View All Students", self.view_all).pack(pady=5)
        create_button("🔍 View Individual", self.view_individual).pack(pady=5)
        create_button("🏆 Highest Score", self.highest_mark).pack(pady=5)
        create_button("⬇ Lowest Score", self.lowest_mark).pack(pady=5)
        create_button("➕ Add Student", self.add_student).pack(pady=5)
        create_button("✏ Update Student", self.update_student).pack(pady=5)
        create_button("🗑 Delete Student", self.delete_student).pack(pady=5)

        # ======= Output Box (Right Side) =======
        self.output = scrolledtext.ScrolledText(
            right_frame,
            width=60,
            height=25,
            bg=OUTPUT_BG,
            fg="#222",
            font=("Consolas", 11),
            relief="ridge",
            borderwidth=2
        )
        self.output.pack(fill="both", expand=True)

    # ============ Data Handling ============
    def load_data(self):
        try:
            with open("studentMarks.txt", "r") as f:
                lines = f.read().strip().split("\n")
                count = int(lines[0])

                for line in lines[1:]:
                    sid, name, c1, c2, c3, exam = line.split(",")
                    self.students.append(Student(sid, name, c1, c2, c3, exam))

        except FileNotFoundError:
            messagebox.showerror("Error", "studentMarks.txt not found.")
            exit()

    def save_data(self):
        with open("studentMarks.txt", "w") as f:
            f.write(str(len(self.students)) + "\n")
            for s in self.students:
                f.write(f"{s.sid},{s.name},{s.c1},{s.c2},{s.c3},{s.exam}\n")

    def clear_output(self):
        self.output.delete(1.0, tk.END)

    # ========= Core Features =========
    def view_all(self):
        self.clear_output()
        total_percentage = 0

        for student in self.students:
            self.output.insert(tk.END, student.summary())
            total_percentage += student.percentage()

        avg = total_percentage / len(self.students)
        self.output.insert(tk.END, f"\nTotal Students: {len(self.students)}\n")
        self.output.insert(tk.END, f"Class Average: {avg:.2f}%\n")

    def view_individual(self):
        query = simpledialog.askstring("Search", "Enter student number or name:")
        if not query:
            return

        query = query.lower()
        found = None

        for s in self.students:
            if query == s.sid.lower() or query in s.name.lower():
                found = s
                break

        self.clear_output()
        if found:
            self.output.insert(tk.END, found.summary())
        else:
            self.output.insert(tk.END, "❌ Student not found.\n")

    def highest_mark(self):
        top = max(self.students, key=lambda s: s.overall_total())
        self.clear_output()
        self.output.insert(tk.END, "🏆 Highest Scoring Student:\n")
        self.output.insert(tk.END, top.summary())

    def lowest_mark(self):
        low = min(self.students, key=lambda s: s.overall_total())
        self.clear_output()
        self.output.insert(tk.END, "⬇ Lowest Scoring Student:\n")
        self.output.insert(tk.END, low.summary())

    # ===== Add Student =====
    def add_student(self):
        sid = simpledialog.askstring("Add Student", "Enter Student ID:")
        name = simpledialog.askstring("Add Student", "Enter Student Name:")
        c1 = simpledialog.askstring("Add Student", "Coursework 1:")
        c2 = simpledialog.askstring("Add Student", "Coursework 2:")
        c3 = simpledialog.askstring("Add Student", "Coursework 3:")
        exam = simpledialog.askstring("Add Student", "Exam Mark:")

        if None in (sid, name, c1, c2, c3, exam):
            return

        new_stu = Student(sid, name, c1, c2, c3, exam)
        self.students.append(new_stu)
        self.save_data()

        messagebox.showinfo("Success", "Student Added Successfully!")

    # ===== Update Student =====
    def update_student(self):
        sid = simpledialog.askstring("Update", "Enter Student ID to update:")
        if not sid:
            return

        target = None
        for s in self.students:
            if s.sid == sid:
                target = s
                break

        if not target:
            messagebox.showerror("Error", "Student not found!")
            return

        new_name = simpledialog.askstring("Update", "New name:", initialvalue=target.name)
        new_c1 = simpledialog.askstring("Update", "Coursework 1:", initialvalue=target.c1)
        new_c2 = simpledialog.askstring("Update", "Coursework 2:", initialvalue=target.c2)
        new_c3 = simpledialog.askstring("Update", "Coursework 3:", initialvalue=target.c3)
        new_exam = simpledialog.askstring("Update", "Exam Mark:", initialvalue=target.exam)

        target.name = new_name
        target.c1 = int(new_c1)
        target.c2 = int(new_c2)
        target.c3 = int(new_c3)
        target.exam = int(new_exam)

        self.save_data()
        messagebox.showinfo("Success", "Student Updated Successfully!")

    # ===== Delete Student =====
    def delete_student(self):
        sid = simpledialog.askstring("Delete", "Enter Student ID to delete:")
        if not sid:
            return

        for s in self.students:
            if s.sid == sid:
                self.students.remove(s)
                self.save_data()
                messagebox.showinfo("Deleted", "Student Deleted Successfully!")
                return

        messagebox.showerror("Error", "Student not found!")


# Run
root = tk.Tk()
app = StudentManagerApp(root)
root.mainloop()
