import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Watermark")
        self.root.geometry("1000x600")
        
        # Initialize variables
        self.original_image = None
        self.watermark_image = None
        self.displayed_image = None
        self.watermark_text = tk.StringVar(value="Your Watermark")
        self.watermark_opacity = tk.IntVar(value=50)
        self.watermark_size = tk.IntVar(value=36)
        self.watermark_color = "#000000"
        self.watermark_position = tk.StringVar(value="bottom-right")
        self.watermark_type = tk.StringVar(value="text")  # "text" or "image"
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Image display area
        self.image_label = ttk.Label(main_frame, text="No image selected")
        self.image_label.grid(row=0, column=0, rowspan=8, padx=10, pady=10)
        
        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Watermark Controls", padding="10")
        controls_frame.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=10)
        
        # Upload image button
        ttk.Button(controls_frame, text="Upload Image", command=self.upload_image).grid(row=0, column=0, pady=5, sticky=tk.W)
        
        # Watermark type selection
        ttk.Label(controls_frame, text="Watermark Type:").grid(row=1, column=0, pady=5, sticky=tk.W)
        ttk.Radiobutton(controls_frame, text="Text", variable=self.watermark_type, value="text",
                       command=self.toggle_watermark_controls).grid(row=2, column=0, pady=2, sticky=tk.W)
        ttk.Radiobutton(controls_frame, text="Image", variable=self.watermark_type, value="image",
                       command=self.toggle_watermark_controls).grid(row=2, column=1, pady=2, sticky=tk.W)
        
        # Text watermark frame
        self.text_frame = ttk.Frame(controls_frame)
        self.text_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(self.text_frame, text="Watermark Text:").pack(anchor=tk.W, pady=5)
        ttk.Entry(self.text_frame, textvariable=self.watermark_text).pack(anchor=tk.W, pady=5)
        ttk.Button(self.text_frame, text="Choose Color", command=self.choose_color).pack(anchor=tk.W, pady=5)
        
        # Image watermark frame
        self.image_frame = ttk.Frame(controls_frame)
        self.image_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Button(self.image_frame, text="Upload Watermark Image", 
                  command=self.upload_watermark_image).pack(anchor=tk.W, pady=5)
        self.watermark_preview = ttk.Label(self.image_frame, text="No watermark image")
        self.watermark_preview.pack(anchor=tk.W, pady=5)
        
        # Common controls
        ttk.Label(controls_frame, text="Opacity:").grid(row=4, column=0, pady=5, sticky=tk.W)
        ttk.Scale(controls_frame, from_=0, to=100, variable=self.watermark_opacity,
                 command=lambda _: self.update_watermark()).grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(controls_frame, text="Size:").grid(row=6, column=0, pady=5, sticky=tk.W)
        ttk.Scale(controls_frame, from_=10, to=100, variable=self.watermark_size,
                 command=lambda _: self.update_watermark()).grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
        
        # Position selection
        ttk.Label(controls_frame, text="Position:").grid(row=8, column=0, pady=5, sticky=tk.W)
        positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
        position_menu = ttk.OptionMenu(controls_frame, self.watermark_position, positions[0], *positions,
                                     command=lambda _: self.update_watermark())
        position_menu.grid(row=9, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        # Save button
        ttk.Button(controls_frame, text="Save Image", command=self.save_image).grid(row=10, column=0, columnspan=2, pady=20, sticky=tk.W)
        
        # Initialize watermark type display
        self.toggle_watermark_controls()
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")]
        )
        if file_path:
            self.original_image = Image.open(file_path)
            if self.original_image.mode != 'RGBA':
                self.original_image = self.original_image.convert('RGBA')
            self.update_watermark()
    
    def choose_color(self):
        color = colorchooser.askcolor(color=self.watermark_color)
        if color[1]:
            self.watermark_color = color[1]
            self.update_watermark()
    
    def toggle_watermark_controls(self):
        if self.watermark_type.get() == "text":
            self.text_frame.grid()
            self.image_frame.grid_remove()
        else:
            self.text_frame.grid_remove()
            self.image_frame.grid()
        self.update_watermark()
    
    def upload_watermark_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png")]
        )
        if file_path:
            self.watermark_image = Image.open(file_path)
            if self.watermark_image.mode != 'RGBA':
                self.watermark_image = self.watermark_image.convert('RGBA')
            
            # Create preview
            preview_size = (100, 100)
            preview = self.watermark_image.copy()
            preview.thumbnail(preview_size, Image.Resampling.LANCZOS)
            self.watermark_preview_img = ImageTk.PhotoImage(preview)
            self.watermark_preview.config(image=self.watermark_preview_img)
            
            self.update_watermark()
    
    def calculate_position(self, img_width, img_height, watermark_width, watermark_height):
        position = self.watermark_position.get()
        if position == "top-left":
            return (10, 10)
        elif position == "top-right":
            return (img_width - watermark_width - 10, 10)
        elif position == "bottom-left":
            return (10, img_height - watermark_height - 10)
        elif position == "bottom-right":
            return (img_width - watermark_width - 10, img_height - watermark_height - 10)
        else:  # center
            return ((img_width - watermark_width) // 2, (img_height - watermark_height) // 2)
    
    def apply_watermark(self, img, for_display=True):
        if img is None:
            return None
            
        img = img.copy()
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        opacity = self.watermark_opacity.get() / 100
        
        if self.watermark_type.get() == "text":
            # Text watermark
            watermark_draw = ImageDraw.Draw(watermark)
            font_size = self.watermark_size.get()
            try:
                font = ImageFont.truetype("Arial", font_size)
            except:
                font = ImageFont.load_default()
            
            text = self.watermark_text.get()
            text_bbox = watermark_draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            pos = self.calculate_position(img.width, img.height, text_width, text_height)
            watermark_draw.text(pos, text, font=font,
                              fill=(*tuple(int(self.watermark_color[i:i+2], 16) for i in (1, 3, 5)), int(255 * opacity)))
        
        elif self.watermark_type.get() == "image" and self.watermark_image:
            # Image watermark
            scale_factor = self.watermark_size.get() / 50.0  # Convert slider value to scale
            w_width = int(self.watermark_image.width * scale_factor)
            w_height = int(self.watermark_image.height * scale_factor)
            
            watermark_resized = self.watermark_image.resize((w_width, w_height), Image.Resampling.LANCZOS)
            pos = self.calculate_position(img.width, img.height, w_width, w_height)
            
            # Apply opacity to the watermark image
            watermark_array = watermark_resized.split()
            if len(watermark_array) == 4:  # If the image has an alpha channel
                r, g, b, a = watermark_array
                a = a.point(lambda x: x * opacity)
                watermark_resized = Image.merge('RGBA', (r, g, b, a))
            
            watermark.paste(watermark_resized, pos, watermark_resized)
        
        img = Image.alpha_composite(img, watermark)
        
        if for_display:
            # Resize for display
            display_size = (800, 500)
            img.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        return img
    
    def update_watermark(self):
        if self.original_image is None:
            return
        
        img = self.apply_watermark(self.original_image, for_display=True)
        if img:
            self.displayed_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.displayed_image)
    
    def save_image(self):
        if self.original_image is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            img = self.apply_watermark(self.original_image, for_display=False)
            if img:
                img.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
