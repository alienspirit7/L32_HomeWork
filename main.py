"""
FFT Image Processing & Triangle Detection

Main entry point for the application.
Usage: python main.py <input_image> [--advanced]
"""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.image_utils import load_image, ensure_greyscale, save_image
from src.fft_operations import apply_fft, scale_for_display, apply_ifft, normalize_to_255
from src.filters import (
    create_low_pass_mask, create_high_pass_mask, 
    create_band_pass_mask, apply_filter, get_default_radii
)
from src.histogram_utils import interactive_threshold_loop
from src.triangle_detector import detect_lines, find_triangle_vertices, draw_triangle


def run_basic_pipeline(input_path: str) -> dict:
    """
    Execute Steps 0-3: greyscale, FFT, filters, IFFT.
    
    Returns:
        Dictionary with paths and data for advanced mode
    """
    print("=== Step 0: Loading and converting to greyscale ===")
    img = load_image(input_path)
    grey_img = ensure_greyscale(img)
    save_image(grey_img, "prep_step_greyscale.png")
    
    print("\n=== Step 1: Applying FFT ===")
    fft_shifted, magnitude = apply_fft(grey_img)
    fft_display = scale_for_display(magnitude)
    save_image(fft_display, "step1_fft.png")
    
    print("\n=== Step 2: Applying frequency filters ===")
    shape = grey_img.shape
    radii = get_default_radii(shape)
    
    # Low pass filter
    low_mask = create_low_pass_mask(shape, radii["low_pass"])
    low_filtered = apply_filter(fft_shifted, low_mask)
    low_mag = scale_for_display(
        __import__('cv2').magnitude(low_filtered[:, :, 0], low_filtered[:, :, 1])
    )
    save_image(low_mag, "step2_low_pass_filter.png")
    
    # Band pass filter
    band_mask = create_band_pass_mask(shape, radii["band_low"], radii["band_high"])
    band_filtered = apply_filter(fft_shifted, band_mask)
    band_mag = scale_for_display(
        __import__('cv2').magnitude(band_filtered[:, :, 0], band_filtered[:, :, 1])
    )
    save_image(band_mag, "step2_band_pass_filter.png")
    
    # High pass filter
    high_mask = create_high_pass_mask(shape, radii["high_pass"])
    high_filtered = apply_filter(fft_shifted, high_mask)
    high_mag = scale_for_display(
        __import__('cv2').magnitude(high_filtered[:, :, 0], high_filtered[:, :, 1])
    )
    save_image(high_mag, "step2_high_pass_filter.png")
    
    print("\n=== Step 3: Applying IFFT ===")
    # IFFT for each filter
    low_ifft = normalize_to_255(apply_ifft(low_filtered))
    save_image(low_ifft, "step3_low_pass_filter_after_ifft.png")
    
    band_ifft = normalize_to_255(apply_ifft(band_filtered))
    save_image(band_ifft, "step3_band_pass_filter_after_ifft.png")
    
    high_ifft = normalize_to_255(apply_ifft(high_filtered))
    save_image(high_ifft, "step3_high_pass_filter_after_ifft.png")
    
    print("\n=== Basic pipeline complete ===")
    return {"high_pass_ifft": high_ifft}


def run_advanced_pipeline(high_pass_img) -> None:
    """Execute Advanced Steps: histogram, threshold, Hough transform."""
    print("\n=== Advanced Mode: Triangle Detection ===")
    
    # Step 1 & 2: Interactive threshold selection
    binary_img = interactive_threshold_loop(high_pass_img)
    save_image(binary_img, "binary_image.png")
    
    # Step 3: Hough Line Transform
    print("\n=== Detecting triangle lines ===")
    lines = detect_lines(binary_img)
    print(f"Detected {len(lines)} lines")
    
    vertices = find_triangle_vertices(lines, binary_img.shape)
    print(f"Found {len(vertices)} vertices")
    
    final_img = draw_triangle(binary_img, vertices)
    save_image(final_img, "final_triangle_image.png")
    
    print("\n=== Advanced pipeline complete ===")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="FFT Image Processing & Triangle Detection")
    parser.add_argument("input_image", help="Path to input image")
    parser.add_argument("--advanced", action="store_true", help="Enable advanced triangle detection")
    
    args = parser.parse_args()
    
    # Run basic pipeline
    result = run_basic_pipeline(args.input_image)
    
    if args.advanced:
        run_advanced_pipeline(result["high_pass_ifft"])


if __name__ == "__main__":
    main()
