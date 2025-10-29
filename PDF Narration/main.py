import PyPDF2
import pyttsx3
import tkinter as tk
from tkinter import filedialog, ttk
import os

class PDFNarrator:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.pdf_text = ""
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("PDF Narrator")
        self.root.geometry("600x400")
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # File selection
        select_frame = ttk.Frame(self.root)
        select_frame.pack(pady=20, padx=20, fill='x')
        
        self.file_label = ttk.Label(select_frame, text="No file selected")
        self.file_label.pack(side='left', expand=True)
        
        select_btn = ttk.Button(select_frame, text="Select PDF", command=self.select_pdf)
        select_btn.pack(side='right')
        
        # Voice controls
        control_frame = ttk.LabelFrame(self.root, text="Voice Controls")
        control_frame.pack(pady=20, padx=20, fill='x')
        
        # Rate control
        rate_frame = ttk.Frame(control_frame)
        rate_frame.pack(pady=10, fill='x')
        ttk.Label(rate_frame, text="Rate:").pack(side='left')
        self.rate_scale = ttk.Scale(rate_frame, from_=50, to=300, orient='horizontal')
        self.rate_scale.set(175)  # Default rate
        self.rate_scale.pack(side='left', fill='x', expand=True, padx=10)
        
        # Volume control
        volume_frame = ttk.Frame(control_frame)
        volume_frame.pack(pady=10, fill='x')
        ttk.Label(volume_frame, text="Volume:").pack(side='left')
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=1, orient='horizontal')
        self.volume_scale.set(1)  # Default volume
        self.volume_scale.pack(side='left', fill='x', expand=True, padx=10)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.play_btn = ttk.Button(button_frame, text="Play", command=self.play_pdf)
        self.play_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_speech)
        self.stop_btn.pack(side='left', padx=5)
        self.stop_btn['state'] = 'disabled'
        
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.file_label.config(text=os.path.basename(file_path))
            self.extract_text(file_path)
    
    def extract_text(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                self.pdf_text = ""
                
                for page in reader.pages:
                    self.pdf_text += page.extract_text() + "\n"
                
            if self.pdf_text.strip():
                self.play_btn['state'] = 'normal'
            else:
                self.file_label.config(text="No readable text found in PDF")
                self.play_btn['state'] = 'disabled'
                
        except Exception as e:
            self.file_label.config(text=f"Error: {str(e)}")
            self.play_btn['state'] = 'disabled'
    
    def play_pdf(self):
        if not self.pdf_text:
            return
        
        # Update button states
        self.play_btn['state'] = 'disabled'
        self.stop_btn['state'] = 'normal'
        
        # Configure speech engine
        self.engine.setProperty('rate', self.rate_scale.get())
        self.engine.setProperty('volume', self.volume_scale.get())
        
        # Start speaking in a separate thread
        self.engine.say(self.pdf_text)
        self.engine.startLoop(False)
        self.engine.iterate()
    
    def stop_speech(self):
        self.engine.stop()
        self.engine.endLoop()
        
        # Reset button states
        self.play_btn['state'] = 'normal'
        self.stop_btn['state'] = 'disabled'
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFNarrator()
    app.run()
