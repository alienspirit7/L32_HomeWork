"""
FFT and IFFT operations for frequency domain processing.
"""

import cv2
import numpy as np


def apply_fft(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Apply Fast Fourier Transform to an image.
    
    Args:
        img: Greyscale input image
        
    Returns:
        Tuple of (shifted FFT complex data, magnitude spectrum)
    """
    # Convert to float32 for DFT
    img_float = np.float32(img)
    
    # Apply DFT
    dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)
    
    # Shift zero frequency to center
    dft_shifted = np.fft.fftshift(dft)
    
    # Calculate magnitude spectrum
    magnitude = cv2.magnitude(dft_shifted[:, :, 0], dft_shifted[:, :, 1])
    
    return dft_shifted, magnitude


def scale_for_display(magnitude: np.ndarray) -> np.ndarray:
    """
    Apply logarithmic scaling for frequency visualization.
    
    Uses formula: 20 * log(1 + magnitude)
    
    Args:
        magnitude: Magnitude spectrum from FFT
        
    Returns:
        Scaled magnitude suitable for display (0-255)
    """
    # Apply logarithmic scaling
    magnitude_log = 20 * np.log(1 + magnitude)
    
    # Normalize to 0-255 range
    magnitude_normalized = cv2.normalize(
        magnitude_log, None, 0, 255, cv2.NORM_MINMAX
    )
    
    return np.uint8(magnitude_normalized)


def apply_ifft(fft_shifted: np.ndarray) -> np.ndarray:
    """
    Apply Inverse Fast Fourier Transform.
    
    Args:
        fft_shifted: Shifted FFT complex data
        
    Returns:
        Reconstructed spatial domain image
    """
    # Shift back
    fft_unshifted = np.fft.ifftshift(fft_shifted)
    
    # Apply inverse DFT
    img_back = cv2.idft(fft_unshifted)
    
    # Get magnitude (reconstruct from complex)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    
    return img_back


def normalize_to_255(img: np.ndarray) -> np.ndarray:
    """
    Normalize image to 0-255 range.
    
    Args:
        img: Input image with any value range
        
    Returns:
        Image normalized to uint8 (0-255)
    """
    normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(normalized)
