"""
Frequency domain filters: low pass, high pass, and band pass.
"""

import numpy as np


def create_low_pass_mask(shape: tuple, radius: int) -> np.ndarray:
    """
    Create a circular low pass filter mask.
    
    Passes frequencies inside the circle, blocks outside.
    
    Args:
        shape: Shape of the mask (rows, cols)
        radius: Radius of the circular mask
        
    Returns:
        Binary mask with 1s inside circle, 0s outside
    """
    rows, cols = shape
    center_row, center_col = rows // 2, cols // 2
    
    # Create coordinate grids
    y, x = np.ogrid[:rows, :cols]
    
    # Calculate distance from center
    distance = np.sqrt((x - center_col) ** 2 + (y - center_row) ** 2)
    
    # Create mask: 1 inside circle, 0 outside
    mask = (distance <= radius).astype(np.float32)
    
    return mask


def create_high_pass_mask(shape: tuple, radius: int) -> np.ndarray:
    """
    Create a circular high pass filter mask.
    
    Passes frequencies outside the circle, blocks inside.
    
    Args:
        shape: Shape of the mask (rows, cols)
        radius: Radius of the circular mask
        
    Returns:
        Binary mask with 0s inside circle, 1s outside
    """
    return 1 - create_low_pass_mask(shape, radius)


def create_band_pass_mask(
    shape: tuple, radius_low: int, radius_high: int
) -> np.ndarray:
    """
    Create a ring-shaped band pass filter mask.
    
    Passes frequencies between inner and outer radius.
    
    Args:
        shape: Shape of the mask (rows, cols)
        radius_low: Inner radius (low cutoff)
        radius_high: Outer radius (high cutoff)
        
    Returns:
        Binary mask with 1s in the ring, 0s elsewhere
    """
    low_mask = create_low_pass_mask(shape, radius_high)
    high_mask = create_high_pass_mask(shape, radius_low)
    
    # Band pass = intersection of low pass (outer) and high pass (inner)
    return low_mask * high_mask


def apply_filter(fft_shifted: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Apply a frequency domain filter to FFT data.
    
    Args:
        fft_shifted: Shifted FFT complex data (2 channels)
        mask: Filter mask to apply
        
    Returns:
        Filtered FFT data
    """
    # Expand mask to 2 channels for complex multiplication
    mask_2ch = np.dstack([mask, mask])
    
    # Apply mask
    filtered = fft_shifted * mask_2ch
    
    return filtered


def get_default_radii(shape: tuple) -> dict:
    """
    Calculate default filter radii based on image size.
    
    Args:
        shape: Image shape (rows, cols)
        
    Returns:
        Dictionary with low, high, band_low, band_high radii
    """
    min_dim = min(shape)
    
    return {
        "low_pass": min_dim // 10,      # ~10% of min dimension
        "high_pass": min_dim // 10,     # ~10% of min dimension  
        "band_low": min_dim // 20,      # ~5% of min dimension
        "band_high": min_dim // 5,      # ~20% of min dimension
    }
