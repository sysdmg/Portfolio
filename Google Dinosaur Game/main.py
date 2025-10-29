import pyautogui
import time
import cv2
import numpy as np
from PIL import ImageGrab
import sys

# Disable PyAutoGUI safety feature
pyautogui.FAILSAFE = False

class DinoGame:
    def __init__(self):
        # Default game region (will be updated during calibration)
        self.game_width = 600
        self.game_height = 150
        self.GAME_REGION = (0, 0, self.game_width, self.game_height)
        self.calibrated = False
        
    def calibrate(self):
        """Calibrate the game region by finding the dinosaur."""
        print("Please open Chrome's dinosaur game (chrome://dino)")
        print("Make sure the game window is visible")
        print("Position your mouse at the top-left corner of the game area")
        input("Press Enter when ready...")
        
        top_left = pyautogui.position()
        print("Now position your mouse at the bottom-right corner of the game area")
        input("Press Enter when ready...")
        bottom_right = pyautogui.position()
        
        # Update game region based on user input
        x1, y1 = min(top_left.x, bottom_right.x), min(top_left.y, bottom_right.y)
        x2, y2 = max(top_left.x, bottom_right.x), max(top_left.y, bottom_right.y)
        
        width = x2 - x1
        height = y2 - y1
        
        # Validate the region size
        if width < 100 or height < 100:
            print("Error: Selected region is too small. Please try again.")
            return self.calibrate()
            
        self.GAME_REGION = (x1, y1, width, height)
        self.calibrated = True
        print(f"Calibration complete! Game region: {self.GAME_REGION}")
        print(f"Region size: {width}x{height} pixels")
        
    def get_game_region(self):
        """Take a screenshot of the game region."""
        try:
            screenshot = ImageGrab.grab(bbox=self.GAME_REGION)
            return np.array(screenshot)
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def detect_obstacle(self, image):
        """Detect if there's an obstacle in front of the dinosaur."""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate detection region dimensions
        height = image.shape[0]
        width = image.shape[1]
        
        # Define region to check for obstacles
        obstacle_y1 = int(height * 0.5)  # Start from middle of screen
        obstacle_y2 = int(height * 0.7)  # Check until 70% of screen height
        obstacle_x1 = int(width * 0.2)   # Start checking from 20% of screen width
        obstacle_x2 = int(width * 0.4)   # Check until 40% of screen width
        
        obstacle_region = gray[obstacle_y1:obstacle_y2, obstacle_x1:obstacle_x2]
        
        # Check if there are any dark pixels (obstacles) in the region
        return np.min(obstacle_region) < 100  # Threshold for dark pixels
    
    def play(self):
        """Main game loop."""
        if not self.calibrated:
            self.calibrate()
        
        print("Starting game in 3 seconds...")
        print("Press Ctrl+C to stop the game")
        time.sleep(3)
        
        # Press space to start game
        pyautogui.press('space')
        
        while True:
            try:
                # Get game screen
                screen = self.get_game_region()
                
                if screen is None:
                    print("Failed to get game screen. Retrying...")
                    time.sleep(0.5)
                    continue
                
                # Check for obstacles
                if self.detect_obstacle(screen):
                    # Jump
                    pyautogui.press('space')
                    # Small delay to prevent multiple jumps
                    time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\nGame stopped by user")
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                print("If the game area was not correctly selected, please restart the program.")
                break

if __name__ == "__main__":
    # Create and start game
    game = DinoGame()
    game.play()