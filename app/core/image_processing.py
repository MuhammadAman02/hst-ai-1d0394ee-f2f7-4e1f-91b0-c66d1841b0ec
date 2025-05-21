import cv2
import numpy as np
from PIL import Image
from skimage import color
from typing import Tuple, List

def analyze_skin_tone(image: Image.Image) -> str:
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Convert to LAB color space
    lab_image = color.rgb2lab(img_array)
    
    # Extract the A and B channels
    a_channel = lab_image[:,:,1]
    b_channel = lab_image[:,:,2]
    
    # Calculate average A and B values
    avg_a = np.mean(a_channel)
    avg_b = np.mean(b_channel)
    
    # Determine skin tone based on A and B values
    if avg_a < 0 and avg_b < 0:
        return "Cool"
    elif avg_a > 0 and avg_b > 0:
        return "Warm"
    else:
        return "Neutral"

def suggest_colors(skin_tone: str) -> List[Tuple[int, int, int]]:
    color_suggestions = {
        "Cool": [
            (70, 130, 180),   # Steel Blue
            (0, 128, 128),    # Teal
            (216, 191, 216),  # Thistle
            (255, 182, 193),  # Light Pink
            (230, 230, 250)   # Lavender
        ],
        "Warm": [
            (255, 165, 0),    # Orange
            (255, 69, 0),     # Red-Orange
            (255, 215, 0),    # Gold
            (50, 205, 50),    # Lime Green
            (255, 127, 80)    # Coral
        ],
        "Neutral": [
            (0, 0, 0),        # Black
            (255, 255, 255),  # White
            (128, 128, 128),  # Gray
            (0, 0, 128),      # Navy
            (101, 67, 33)     # Brown
        ]
    }
    return color_suggestions.get(skin_tone, [])

def change_skin_tone(image: Image.Image, target_tone: Tuple[int, int, int]) -> Image.Image:
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Convert to LAB color space
    lab_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
    
    # Split the LAB image into L, A, and B channels
    l_channel, a_channel, b_channel = cv2.split(lab_image)
    
    # Calculate the difference between target tone and current average
    current_avg = np.mean(lab_image, axis=(0, 1))
    diff = np.array(target_tone) - current_avg
    
    # Apply the difference to all pixels
    l_channel = np.clip(l_channel + diff[0], 0, 255).astype(np.uint8)
    a_channel = np.clip(a_channel + diff[1], 0, 255).astype(np.uint8)
    b_channel = np.clip(b_channel + diff[2], 0, 255).astype(np.uint8)
    
    # Merge the channels back
    adjusted_lab = cv2.merge((l_channel, a_channel, b_channel))
    
    # Convert back to RGB
    adjusted_rgb = cv2.cvtColor(adjusted_lab, cv2.COLOR_LAB2RGB)
    
    return Image.fromarray(adjusted_rgb)