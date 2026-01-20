"""
Histogram analysis and binary thresholding utilities.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_histogram(img: np.ndarray) -> None:
    """
    Display histogram of pixel value distribution (per pixel value basis).
    
    Args:
        img: Greyscale image
    """
    plt.figure(figsize=(12, 6))
    plt.hist(img.ravel(), bins=256, range=(0, 256), color='steelblue', 
             edgecolor='none', alpha=0.7)
    plt.title('Pixel Value Distribution (0-255)')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.xticks(range(0, 256, 25))  # Show ticks every 25 values
    plt.tight_layout()
    plt.show()


def get_threshold_from_user() -> int:
    """Prompt user to input a threshold value."""
    print("\n--- Threshold Selection ---")
    print("TIP: Look at the histogram peaks. Choose a value that separates")
    print("     the edges (high values) from the background (low values).")
    print("     Pixels BELOW threshold -> BLACK (255)")
    print("     Pixels ABOVE threshold -> WHITE (0)")
    
    while True:
        try:
            threshold = int(input("\nEnter threshold value (0-255): "))
            if 0 <= threshold <= 255:
                return threshold
            print("ERROR: Threshold must be between 0 and 255.")
        except ValueError:
            print("ERROR: Please enter a valid integer.")


def apply_binary_threshold(img: np.ndarray, threshold: int) -> np.ndarray:
    """
    Convert image to binary based on threshold.
    
    Pixels above threshold -> 0 (white)
    Pixels below threshold -> 255 (black)
    """
    print(f"\n[LOG] Applying binary threshold: {threshold}")
    print(f"[LOG] Pixels below {threshold} will become BLACK (255)")
    print(f"[LOG] Pixels above {threshold} will become WHITE (0)")
    
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Count pixels
    black_pixels = np.sum(binary == 255)
    white_pixels = np.sum(binary == 0)
    total_pixels = binary.size
    
    print(f"[LOG] Binary image created:")
    print(f"      - Black pixels: {black_pixels} ({100*black_pixels/total_pixels:.1f}%)")
    print(f"      - White pixels: {white_pixels} ({100*white_pixels/total_pixels:.1f}%)")
    
    return binary


def get_user_approval(img: np.ndarray, window_name: str = "Binary Image") -> bool:
    """Display image and ask user for approval."""
    print("\n[LOG] Displaying binary image preview...")
    cv2.imshow(window_name, img)
    cv2.waitKey(1)
    
    while True:
        response = input("Is the output good? (yes/no): ").strip().lower()
        if response in ('yes', 'y'):
            print("[LOG] User approved the binary image.")
            cv2.destroyAllWindows()
            return True
        elif response in ('no', 'n'):
            print("[LOG] User rejected the binary image. Trying again...")
            cv2.destroyAllWindows()
            return False
        print("Please enter 'yes' or 'no'.")


def interactive_threshold_loop(img: np.ndarray) -> np.ndarray:
    """
    Interactive loop for threshold selection.
    Repeats until user approves.
    """
    print("\n" + "="*50)
    print("=== Binary Threshold Selection ===")
    print("="*50)
    print("\n[LOG] Displaying pixel value histogram...")
    print("[LOG] Close the histogram window to continue.")
    
    show_histogram(img)
    
    while True:
        threshold = get_threshold_from_user()
        binary_img = apply_binary_threshold(img, threshold)
        
        if get_user_approval(binary_img):
            print(f"\n[LOG] Final threshold: {threshold}")
            return binary_img
        
        print("\n[LOG] Let's try a different threshold.")

