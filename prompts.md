# Development Prompts Log

This file tracks all prompts used during the development of this project and the actions taken by the LLM.

---

## Prompt 1: Initial PRD Creation

**Date:** 2026-01-20

**Prompt:**
> Create PRD.md file for the following project (Use open CV library):
> 0) Get the image, make sure it's greyscale image (if not, make it grey scale), save the email calling prep_step_greyscale.
> 1) Apply on it FFT, apply scaling and view, so Frequency domain can be actually seen on the output image (frequencies should be seen). Save the output image calling it step1_fft.
> 2) Then we apply 3 different filters on the step1_fft (only one filter at a time): 
> - once on step1_fft image we apply low pass filter and save the output image, calling it step2_low_pass_filter
> - once on step1_fft image we apply band pass filter and save the output image, calling it step2_band_pass_filter
> - once on step1_fft image we apply high pass filter and save the output image, calling it step2_high_pass_filter
> 3) Then on each of the above output images (step2_low_pass_filter, step2_band_pass_filter, step2_high_pass_filter) apply IFFT and do scaling and view again such, we can see the full imaga again. The scale should be 0-255 (values of pixel). Save the output images of the step 3, calling them step3_low_pass_filter_after_ifft, step3_band_pass_filter_after_ifft, step3_high_pass_filter_after_ifft
> All images should be saved in the same output images folder. Input image will be stored in input image folder.
> 
> Next steps are for the advanced usage of the project.
> The input image that will be provided is going to contain the triangle figure. After the first 3 steps, where we apply specifically low pass filter, we should be able to see the triangle edges. What we do next (advanced mode):
> 1) In addition to the output image of low pass filter after ifft, we see the pixle values distribution (bins of 26). This should help us to decide on the threshold. The program asks user to input the desired threshold.
> 2) Once user chose the threshold, the program should convert the image to binary image (make pixels above the threshold as 255 (fully black), below the threshold as 0 (fully white)). Program shows the user the output image, calling it binary_image and asks to confirm if output is good or bad. If output is good - keep the saved image, if output is bad, the program asks user again on the threshold and create a new binary image, overwriting the old one.
> 3) On binary_image we apply Hough Line Transform to find the triangle lines and draw them, but only until the cross with the other line. The output we save as final_triangle_image.

**Action Taken:**
Created comprehensive `PRD.md` file containing:
- Project overview and structure
- Core workflow (Steps 0-3): greyscale conversion, FFT, filtering, IFFT
- Advanced mode workflow: histogram analysis, binary thresholding, Hough transform
- Output images summary table
- Technical requirements and OpenCV functions
- Mermaid flowchart of the entire process
- Acceptance criteria checklist

---

## Prompt 2: Modular Structure Review

**Date:** 2026-01-20

**Prompt:**
> Now review the PRD and make sure it can be developed with python files of less than 150 lines

**Action Taken:**
Updated `PRD.md` with modular architecture:
- Added `src/` folder with 5 specialized modules
- `image_utils.py` (~40 lines): Image loading, greyscale conversion, saving
- `fft_operations.py` (~50 lines): FFT, IFFT, and scaling functions
- `filters.py` (~60 lines): Low, band, high pass filter masks
- `histogram_utils.py` (~45 lines): Histogram display and threshold logic
- `triangle_detector.py` (~70 lines): Hough transform and line intersection
- `main.py` (~80 lines): Entry point and pipeline orchestration
- Added detailed Module Specifications section with function signatures
- Added `requirements.txt` to project structure

---

## Prompt 3: Prompts Log Creation

**Date:** 2026-01-20

**Prompt:**
> Create prompts.md file and add exact prompts from the beginning of this session and short description of what was done by LLM after the prompt. Keep updating this file with all the prompts used while developing the project.

**Action Taken:**
Created this `prompts.md` file to track all development prompts and LLM actions.

---

## Prompt 4: Implementation

**Date:** 2026-01-20

**Prompt:**
> Yes, proceed with implementation. Make sure all python scripts are under 150 lines and code is written with the best practices of good architecture.

**Action Taken:**
Created complete modular Python codebase:
- `src/image_utils.py` (86 lines): Image loading, greyscale conversion, saving, display
- `src/fft_operations.py` (90 lines): FFT, IFFT, logarithmic scaling, normalization
- `src/filters.py` (112 lines): Low/high/band pass filter mask creation and application
- `src/histogram_utils.py` (114 lines): Histogram display, threshold input, binary conversion
- `src/triangle_detector.py` (117 lines): Hough line detection, intersection finding, triangle drawing
- `main.py` (124 lines): Entry point with basic and advanced pipeline orchestration
- `requirements.txt`: opencv-python, numpy, matplotlib
- `src/__init__.py`: Package init

All files verified under 150 lines with proper docstrings, type hints, and single responsibility.

---

## Prompt 5: Python 3.9 Compatibility Fix

**Date:** 2026-01-20

**Prompt:**
> fix the issue
> (Error: `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`)

**Action Taken:**
Fixed Python 3.9 compatibility in `src/triangle_detector.py`:
- Added `from typing import Optional, List, Tuple` import
- Changed `tuple | None` to `Optional[Tuple]` (union syntax requires Python 3.10+)
- Changed `list` to `List[Tuple]` for proper type hints

---

## Prompt 6: Change Advanced Mode to High Pass Filter

**Date:** 2026-01-20

**Prompt:**
> Change the advance to start with 3 steps where the filter applied on the second step is high pass filter

**Action Taken:**
Modified `main.py` to use high pass filter for advanced mode:
- Changed `run_basic_pipeline()` return value from `low_pass_ifft` to `high_pass_ifft`
- Updated `run_advanced_pipeline()` parameter from `low_pass_img` to `high_pass_img`
- High pass filter is better for edge detection as it preserves edges and removes smooth areas

---

## Prompt 7: Invert Binary Threshold Logic

**Date:** 2026-01-20

**Prompt:**
> Change the logic of binary image creation to be, if above the threshold - make it 0, if below the threshold - make it 255.

**Action Taken:**
Modified `src/histogram_utils.py`:
- Changed `cv2.THRESH_BINARY` to `cv2.THRESH_BINARY_INV`
- Updated docstring to reflect: above threshold → 0 (white), below threshold → 255 (black)

---

## Prompt 8: Histogram & Logging Improvements

**Date:** 2026-01-20

**Prompt:**
> Change Histogram to be on per pixel value basis, not bins. Add message to the user on threshold choice. Add some logs to print on the screen while creating binary image

**Action Taken:**
Updated `src/histogram_utils.py`:
- Changed histogram from 26 bins to 256 bins (per pixel value 0-255)
- Added threshold selection guidance with tips about histogram peaks
- Added `[LOG]` messages throughout:
  - When displaying histogram
  - When applying threshold with pixel counts and percentages
  - When user approves/rejects binary image
  - When finalizing threshold selection

---

## Prompt 9: Triangle Detection Investigation

**Date:** 2026-01-20

**Prompt:**
> Why Hough Line Transform doesn't succeed in capturing current binary image lines?

**Action Taken:**
Analyzed the code and identified issues:
- Only checking first 6 lines (best lines might be further)
- HoughLinesP returns segments, not infinite lines
- Many noisy/fragmented lines from high pass filter
- Intersections far outside the actual triangle

Proposed solutions: merge similar lines, sort by length, improve vertex selection.

---

## Prompt 10: Improved Triangle Detection Algorithm

**Date:** 2026-01-20

**Prompt:**
> Could it be a mix of approaches?

**Action Taken:**
Rewrote `src/triangle_detector.py` with combined improvements:
- Sort lines by length (longest first)
- Merge similar-angle lines (±15°), keep longest from each group
- Filter out border/frame edges (5% margin)
- Calculate centroid of detected lines
- Find intersections only inside image bounds
- Sort vertices by distance to centroid
- Dynamic tolerances based on image size

---

## Prompt 11: Documentation Creation

**Date:** 2026-01-20

**Prompt:**
> Add gitignore file. Create detailed ReadMe with project structure and mention python files length. ReadMe should also include clear flow schema and explanation (theoretical) of each step in the process and what it does.

**Action Taken:**
Created:
- `.gitignore` - Standard Python ignores + output_images/
- `README.md` - Comprehensive documentation including:
  - Project structure with all file line counts
  - Installation and usage instructions
  - ASCII art flow diagrams for basic and advanced modes
  - Theoretical explanations of FFT, filters, IFFT, thresholding, and Hough Transform
  - Output images summary table

---

*This file will be updated with each new prompt during the development process.*
