# FFT Image Processing & Triangle Detection

A Python-based image processing pipeline that demonstrates Fourier Transform techniques for frequency domain filtering and advanced triangle edge detection using Hough Line Transform.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Test Runs](#test-runs)
- [Processing Flow](#processing-flow)
- [Theoretical Background](#theoretical-background)
- [Output Images](#output-images)

---

## Overview

This project implements a complete image processing workflow using OpenCV:

1. **Basic Mode**: Converts images to frequency domain using FFT, applies various filters, and reconstructs the image
2. **Advanced Mode**: Detects triangle edges using binary thresholding and Hough Line Transform

---

## Project Structure

```
L32_HomeWork/
├── input_image/              # Place input images here
├── output_images/            # Generated output images (created automatically)
├── src/                      # Source modules
│   ├── __init__.py          # Package init (1 line)
│   ├── image_utils.py       # Image I/O operations (86 lines)
│   ├── fft_operations.py    # FFT/IFFT functions (90 lines)
│   ├── filters.py           # Frequency domain filters (112 lines)
│   ├── histogram_utils.py   # Histogram & thresholding (114 lines)
│   └── triangle_detector.py # Hough transform detection (174 lines)
├── main.py                   # Entry point (123 lines)
├── requirements.txt          # Python dependencies
├── PRD.md                    # Product Requirements Document
├── prompts.md               # Development prompts log
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

> **Note**: All Python files are designed to be under **175 lines** for maintainability and readability. Total codebase: ~700 lines.

---

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd L32_HomeWork

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

- `opencv-python` >= 4.8.0
- `numpy` >= 1.24.0
- `matplotlib` >= 3.7.0

---

## Usage

### Basic Mode (Steps 0-3)

Processes an image through FFT, applies frequency filters, and reconstructs using IFFT:

```bash
python main.py input_image/your_image.png
```

### Advanced Mode (Triangle Detection)

Includes interactive threshold selection and Hough Line Transform for triangle detection:

```bash
python main.py input_image/triangle.png --advanced
```

---

## Test Runs

Three test runs were performed to validate the pipeline functionality.

### Test Run 1: Simple Run (City Image - Basic Mode)

A complex city scene image processed through the basic FFT pipeline to demonstrate frequency filtering effects.

**Input Image:**

![City input image](simple%20run/input_image/city_image.png)

**FFT Magnitude Spectrum:**

![FFT spectrum](simple%20run/output_images/step1_fft.png)

*The bright center represents low frequencies (smooth areas), while the patterns radiating outward represent high frequencies (edges and details).*

**High Pass Filter Result (Edge Detection):**

![High pass result](simple%20run/output_images/step3_high_pass_filter_after_ifft.png)

*High pass filtering reveals only the edges - building outlines, windows, and structural details are preserved while smooth areas become black.*

---

### Test Run 2: Simple Triangle (Advanced Mode)

A clean triangle image with clear edges - ideal case for triangle detection.

**Input Image:**

![Triangle input](simple%20triangle%20run/input_image/triangle.png)

**Final Triangle Detection:**

![Triangle detected](simple%20triangle%20run/output_images/final_triangle_image.png)

*The algorithm successfully detected all 3 vertices (red dots) and drew the triangle edges (green lines) accurately matching the original shape.*

---

### Test Run 3: Hard Triangle (Advanced Mode)

A challenging image with a 3D triangle on a complex cosmic background - tests the robustness of edge detection.

**Input Image:**

![Hard triangle input](hard%20triangle%20run/input_image/hard_triangle.png)

**Binary Image (After Thresholding):**

![Binary result](hard%20triangle%20run/output_images/binary_image.png)

*The high pass filter + thresholding successfully isolated the triangle edges from the complex background.*

**Final Triangle Detection:**

![Hard triangle detected](hard%20triangle%20run/output_images/final_triangle_image.png)

*Despite the challenging input, the algorithm correctly detected all 3 vertices and drew the triangle outline, demonstrating the effectiveness of the line merging and vertex selection algorithms.*

---

### Threshold Selection Guide

The threshold selection process is interactive and relies on analyzing the pixel value distribution histogram.

#### Step 1: Analyze the Histogram

When advanced mode starts, the program displays a histogram showing the distribution of pixel values (0-255) in the high-pass filtered image:

**Example Histogram (Hard Triangle):**

![Histogram hard triangle](playing%20with%20threshold/Screenshot%202026-01-20%20at%2020.40.37.png)

**Example Histogram (Simple Triangle):**

![Histogram simple triangle](playing%20with%20threshold/Screenshot%202026-01-20%20at%2021.33.13.png)

**How to read the histogram:**
- **X-axis**: Pixel values from 0 (black) to 255 (white)
- **Y-axis**: Frequency (count of pixels with that value)
- **Large peak near 0**: Background pixels (black/dark areas after high-pass filter)
- **Smaller values in higher range**: Edge pixels (the triangle edges we want to detect)

**Choosing a good threshold:**
- Look for where the main peak (background) ends
- Choose a value just after the peak drops off
- Typical range: 10-50 for well-defined edges, higher for noisy images

#### Step 2: Interactive Threshold Testing

The program shows logs and lets you test different thresholds:

**Terminal Log Example:**

![Terminal logs](playing%20with%20threshold/Screenshot%202026-01-20%20at%2020.33.52.png)

![More terminal logs](playing%20with%20threshold/Screenshot%202026-01-20%20at%2020.34.40.png)

**Key information in logs:**
- **Threshold value**: The cutoff you selected
- **Black pixels %**: Edges (should be ~95-99% for clean detection)
- **White pixels %**: Background (should be ~1-5%)

#### Step 3: Evaluate Binary Image Output

**Threshold too low (noisy):**

![Too much noise](playing%20with%20threshold/Screenshot%202026-01-20%20at%2020.31.56.png)

*Too many black pixels - the background noise is being captured along with edges.*

**Threshold just right (clean edges):**

![Good threshold](playing%20with%20threshold/Screenshot%202026-01-20%20at%2020.32.33.png)

*Clean triangle edges with minimal noise - ideal for Hough Line detection.*

**Threshold too high (losing edges):**

![Threshold too high](playing%20with%20threshold/Screenshot%202026-01-20%20at%2020.32.46.png)

*Very clean but may lose some edge detail - still acceptable.*

#### Threshold Selection Summary

| Threshold Value | Effect | When to Use |
|-----------------|--------|-------------|
| Low (5-15) | More black pixels, may include noise | Simple images with clear contrast |
| Medium (20-50) | Balanced edge detection | Most images |
| High (60-100+) | Fewer edges, cleaner but may miss details | Noisy or complex backgrounds |

---

## Processing Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BASIC MODE (Steps 0-3)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │ Input Image  │───▶│  Greyscale   │───▶│    Apply FFT         │  │
│  │              │    │  Conversion  │    │  + Log Scaling       │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                                                  │                   │
│                      ┌───────────────────────────┼───────────────┐  │
│                      │                           │               │  │
│                      ▼                           ▼               ▼  │
│              ┌──────────────┐          ┌──────────────┐ ┌──────────┐│
│              │  Low Pass    │          │  Band Pass   │ │High Pass ││
│              │   Filter     │          │   Filter     │ │ Filter   ││
│              └──────────────┘          └──────────────┘ └──────────┘│
│                      │                           │               │  │
│                      ▼                           ▼               ▼  │
│              ┌──────────────┐          ┌──────────────┐ ┌──────────┐│
│              │    IFFT      │          │    IFFT      │ │  IFFT    ││
│              │  + Scale     │          │  + Scale     │ │ + Scale  ││
│              └──────────────┘          └──────────────┘ └──────────┘│
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (if --advanced)
┌─────────────────────────────────────────────────────────────────────┐
│                      ADVANCED MODE (Triangle Detection)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │ High Pass    │───▶│  Histogram   │───▶│ User Selects         │  │
│  │ IFFT Result  │    │  (256 bins)  │    │ Threshold Value      │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                                                  │                   │
│                                                  ▼                   │
│                                          ┌──────────────┐           │
│                              ┌───────────│ Binary Image │◀──┐       │
│                              │           └──────────────┘   │       │
│                              ▼                              │       │
│                      ┌──────────────┐              ┌────────┴─────┐ │
│                      │ User Approves│──── No ─────▶│ Try Different│ │
│                      │   Image?     │              │  Threshold   │ │
│                      └──────────────┘              └──────────────┘ │
│                              │ Yes                                   │
│                              ▼                                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │ Hough Line   │───▶│ Find Line    │───▶│  Draw Triangle       │  │
│  │  Transform   │    │ Intersections│    │  on Image            │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Theoretical Background

### Step 0: Greyscale Conversion

**Purpose**: Simplify the image to a single channel for frequency analysis.

**Theory**: Color images have 3 channels (RGB). FFT analysis is simpler on single-channel greyscale images where each pixel is a single intensity value (0-255).

**Formula**: `Grey = 0.299*R + 0.587*G + 0.114*B`

---

### Step 1: Fast Fourier Transform (FFT)

**Purpose**: Convert the image from spatial domain to frequency domain.

**Theory**: The Fourier Transform decomposes an image into its constituent frequencies. Low frequencies represent smooth areas (gradual changes), while high frequencies represent edges and fine details (rapid changes).

**Key Operations**:
- `cv2.dft()` - Compute the Discrete Fourier Transform
- `np.fft.fftshift()` - Shift zero-frequency component to center
- Logarithmic scaling: `20 * log(1 + magnitude)` - Makes the wide range of frequency magnitudes visible

**Visual Result**: A spectrum where:
- **Center** = Low frequencies (brightness, smooth gradients)
- **Edges** = High frequencies (edges, textures, noise)

---

### Step 2: Frequency Domain Filters

#### Low Pass Filter

**Purpose**: Keep low frequencies, remove high frequencies.

**Effect**: Blurs the image by removing sharp edges and fine details. Useful for noise reduction.

**Implementation**: Circular mask centered at origin; passes frequencies inside the circle.

#### High Pass Filter

**Purpose**: Keep high frequencies, remove low frequencies.

**Effect**: Enhances edges and details while removing smooth areas. Useful for edge detection.

**Implementation**: Inverse of low pass mask; passes frequencies outside the circle.

#### Band Pass Filter

**Purpose**: Keep mid-range frequencies, remove both low and high.

**Effect**: Isolates specific frequency components. Useful for texture analysis.

**Implementation**: Ring-shaped mask between inner and outer radius.

---

### Step 3: Inverse FFT (IFFT)

**Purpose**: Convert filtered frequency data back to spatial domain.

**Theory**: After applying filters in frequency domain, IFFT reconstructs the image showing the effect of the filter.

**Key Operations**:
- `np.fft.ifftshift()` - Reverse the shift
- `cv2.idft()` - Inverse Discrete Fourier Transform
- Normalize to 0-255 range for display

---

### Advanced Step 1: Histogram Analysis

**Purpose**: Visualize pixel value distribution to choose optimal threshold.

**Theory**: The histogram shows how many pixels have each intensity value (0-255). Peaks indicate common values; valleys indicate natural separation points for thresholding.

---

### Advanced Step 2: Binary Thresholding

**Purpose**: Convert greyscale image to binary (black and white only).

**Theory**: Separates foreground (edges) from background based on intensity threshold.

**Logic**:
- Pixels **above** threshold → 0 (white/background)
- Pixels **below** threshold → 255 (black/edges)

---

### Advanced Step 3: Hough Line Transform

**Purpose**: Detect straight lines in the binary image.

**Theory**: The Hough Transform converts points in image space to curves in parameter space (ρ, θ). Lines appear as intersections of curves.

**Key Algorithms**:
1. **Line Detection**: `cv2.HoughLinesP()` finds line segments
2. **Line Merging**: Groups similar-angle lines, keeps longest from each group
3. **Border Filtering**: Removes lines near image edges
4. **Intersection Finding**: Calculates where lines cross
5. **Vertex Selection**: Picks 3 vertices closest to line centroid

---

## Output Images

| Step | Filename | Description |
|------|----------|-------------|
| 0 | `prep_step_greyscale.png` | Greyscale input image |
| 1 | `step1_fft.png` | FFT magnitude spectrum |
| 2a | `step2_low_pass_filter.png` | Low pass filtered spectrum |
| 2b | `step2_band_pass_filter.png` | Band pass filtered spectrum |
| 2c | `step2_high_pass_filter.png` | High pass filtered spectrum |
| 3a | `step3_low_pass_filter_after_ifft.png` | Reconstructed (blurred) |
| 3b | `step3_band_pass_filter_after_ifft.png` | Reconstructed (mid-freq) |
| 3c | `step3_high_pass_filter_after_ifft.png` | Reconstructed (edges) |
| Adv | `binary_image.png` | Thresholded binary image |
| Adv | `final_triangle_image.png` | Detected triangle overlay |

---

## License

This project is for educational purposes.
