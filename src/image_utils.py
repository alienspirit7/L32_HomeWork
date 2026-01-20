"""
Image utility functions for loading, converting, and saving images.
"""

import os
import cv2
import numpy as np

# Constants
OUTPUT_DIR = "output_images"
INPUT_DIR = "input_image"


def create_output_dirs() -> None:
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def load_image(path: str) -> np.ndarray:
    """
    Load an image from the given path.
    
    Args:
        path: Path to the image file
        
    Returns:
        Loaded image as numpy array
        
    Raises:
        FileNotFoundError: If image file doesn't exist
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Failed to load image: {path}")
    
    return img


def ensure_greyscale(img: np.ndarray) -> np.ndarray:
    """
    Convert image to greyscale if it's not already.
    
    Args:
        img: Input image (BGR or greyscale)
        
    Returns:
        Greyscale image
    """
    if len(img.shape) == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def save_image(img: np.ndarray, filename: str) -> str:
    """
    Save image to the output directory.
    
    Args:
        img: Image to save
        filename: Output filename (without path)
        
    Returns:
        Full path to saved image
    """
    create_output_dirs()
    output_path = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(output_path, img)
    print(f"Saved: {output_path}")
    return output_path


def display_image(img: np.ndarray, window_name: str = "Image") -> None:
    """
    Display image in a window and wait for key press.
    
    Args:
        img: Image to display
        window_name: Name of the display window
    """
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
