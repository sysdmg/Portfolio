import tkinter as tk
from tkinter import messagebox
import time
import random

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3333")  # Dark gray background

        # Define color scheme
        self.colors = {
            'bg': '#2C3333',  # Dark gray
            'text': '#E7F6F2',  # Light blue-white
            'button': '#395B64',  # Blue-gray
            'entry_bg': '#395B64',  # Blue-gray
            'entry_fg': '#E7F6F2'  # Light blue-white
        }

        # Sample texts for typing test
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "To be or not to be, that is the question.",
            "All that glitters is not gold.",
            "Practice makes perfect.",
            "A journey of a thousand miles begins with a single step."
        ]
        
        self.current_text = ""
        self.start_time = None
        self.typing = False

        # Create and pack widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Instructions
        self.instructions = tk.Label(
            self.root,
            text="Type the text below as fast as you can!",
            font=("Helvetica", 28),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            pady=10
        )
        self.instructions.pack()

        # Text to type (display area)
        self.text_display = tk.Text(
            self.root,
            height=3,
            width=60,
            wrap=tk.WORD,
            font=("Helvetica", 24),
            state='disabled',
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg']
        )
        self.text_display.pack(pady=20)

        # Entry field for typing
        self.type_entry = tk.Text(
            self.root,
            height=3,
            width=60,
            wrap=tk.WORD,
            font=("Helvetica", 24),
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg']
        )
        self.type_entry.pack(pady=20)
        self.type_entry.bind('<KeyPress>', self.on_key_press)

        # Results display
        self.result_label = tk.Label(
            self.root,
            text="WPM: 0 | Accuracy: 0%",
            font=("Helvetica", 28),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.result_label.pack(pady=20)

        # Reset button
        self.reset_button = tk.Button(
            self.root,
            text="Reset",
            command=self.reset_test,
            font=("Helvetica", 24),
            bg=self.colors['button'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        self.reset_button.pack(pady=20)

        # Initialize the test
        self.reset_test()

    def reset_test(self):
        # Reset all variables and UI elements
        self.current_text = random.choice(self.sample_texts)
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.current_text)
        self.text_display.config(state='disabled')
        
        self.type_entry.delete(1.0, tk.END)
        self.start_time = None
        self.typing = False
        self.result_label.config(text="WPM: 0 | Accuracy: 0%")
        self.type_entry.focus()

    def on_key_press(self, event):
        # Start timer on first keystroke
        if not self.typing and event.char:
            self.start_time = time.time()
            self.typing = True

        # Calculate results when Enter is pressed
        if event.keysym == 'Return':
            self.calculate_results()
            return 'break'  # Prevents adding a new line
        
    def calculate_results(self):
        if not self.start_time:
            return
            
        # Calculate time elapsed
        end_time = time.time()
        time_elapsed = end_time - self.start_time
        
        # Get typed text
        typed_text = self.type_entry.get(1.0, 'end-1c')
        
        # Calculate WPM
        # WPM = (characters typed / 5) / minutes elapsed
        words = len(typed_text) / 5
        minutes = time_elapsed / 60
        wpm = round(words / minutes)

        # Calculate accuracy
        correct_chars = sum(1 for i, j in zip(self.current_text, typed_text) if i == j)
        accuracy = round((correct_chars / len(self.current_text)) * 100)

        # Update result label
        self.result_label.config(text=f"WPM: {wpm} | Accuracy: {accuracy}%")
        
        # Show completion message
        messagebox.showinfo("Test Complete", 
                          f"Test completed!\nWPM: {wpm}\nAccuracy: {accuracy}%\n\n"
                          "Click Reset to try again!")

def main():
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
