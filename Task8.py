import tkinter as tk
import random
import time
class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.start_time = 0
        self.is_running = False
        self.texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is a powerful programming language.",
            "Coding is not just about syntax, it is about logic.",
            "Artificial Intelligence is the future of technology.",
            "Practice makes perfect when learning to type.",
            "Tkinter is the standard GUI library for Python.",
            "Consistency is key to mastering any skill."
        ]
        self.create_widgets()
        self.reset_game()
    def create_widgets(self):
        self.title_label = tk.Label(
            self.root, 
            text="Typing Speed Test", 
            font=("Helvetica", 24, "bold"), 
            bg="#f0f0f0", 
            fg="#333"
        )
        self.title_label.pack(pady=20)
        self.instruction_label = tk.Label(
            self.root, 
            text="Type the sentence below and press ENTER to finish.", 
            font=("Helvetica", 12), 
            bg="#f0f0f0", 
            fg="#666"
        )
        self.instruction_label.pack(pady=5)
        self.sample_label = tk.Label(
            self.root, 
            text="", 
            font=("Courier New", 16), 
            bg="white", 
            fg="black",
            wraplength=700, 
            relief="solid", 
            padx=20, 
            pady=20
        )
        self.sample_label.pack(pady=20, padx=50, fill="x")
        self.input_entry = tk.Entry(
            self.root, 
            font=("Courier New", 16)
        )
        self.input_entry.pack(pady=10, padx=50, fill="x")
        self.input_entry.bind("<KeyPress>", self.start_timer)
        self.input_entry.bind("<Return>", self.calculate_result)
        self.result_label = tk.Label(
            self.root, 
            text="WPM: 0 | Accuracy: 0%", 
            font=("Helvetica", 18, "bold"), 
            bg="#f0f0f0", 
            fg="#007acc"
        )
        self.result_label.pack(pady=20)
        self.reset_btn = tk.Button(
            self.root, 
            text="Reset / New Sentence", 
            command=self.reset_game, 
            font=("Helvetica", 12), 
            bg="#ff5722", 
            fg="white", 
            padx=20, 
            pady=10
        )
        self.reset_btn.pack(pady=10)
    def start_timer(self, event):
        """Starts the timer on the first keypress."""
        if not self.is_running:
            if event.keysym in ["Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"]:
                return
            self.start_time = time.time()
            self.is_running = True
    def calculate_result(self, event):
        """Calculates WPM and Accuracy when Enter is pressed."""
        if not self.is_running:
            return
        end_time = time.time()
        time_taken = end_time - self.start_time
        if time_taken == 0:
            time_taken = 0.001
        typed_text = self.input_entry.get()
        target_text = self.sample_label.cget("text")
        character_count = len(typed_text)
        wpm = (character_count / 5) / (time_taken / 60)
        correct_chars = 0
        for i in range(min(len(typed_text), len(target_text))):
            if typed_text[i] == target_text[i]:
                correct_chars += 1
        try:
            accuracy = (correct_chars / len(target_text)) * 100
        except ZeroDivisionError:
            accuracy = 0
        self.result_label.config(
            text=f"WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}% | Time: {time_taken:.1f}s"
        )
        self.is_running = False
        self.input_entry.config(state="disabled")
    def reset_game(self):
        """Resets variables and picks a new sentence."""
        self.is_running = False
        self.start_time = 0
        new_text = random.choice(self.texts)
        self.sample_label.config(text=new_text)
        self.input_entry.config(state="normal")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()
        self.result_label.config(text="WPM: 0 | Accuracy: 0%")
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()