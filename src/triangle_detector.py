"""
Triangle detection using Hough Line Transform with improved line merging.
"""

import cv2
import numpy as np
from itertools import combinations
from typing import Optional, List, Tuple


def detect_lines(binary_img: np.ndarray) -> List[Tuple]:
    """Detect lines using Probabilistic Hough Transform."""
    edges = cv2.Canny(binary_img, 50, 150)
    lines = cv2.HoughLinesP(
        edges, rho=1, theta=np.pi / 180,
        threshold=30, minLineLength=20, maxLineGap=15
    )
    if lines is None:
        return []
    return [tuple(line[0]) for line in lines]


def get_line_length(line: tuple) -> float:
    """Calculate length of a line segment."""
    x1, y1, x2, y2 = line
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_line_angle(line: tuple) -> float:
    """Get angle of line in degrees (0-180)."""
    x1, y1, x2, y2 = line
    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    return angle % 180  # Normalize to 0-180


def merge_similar_lines(lines: List[Tuple], angle_thresh: float = 15) -> List[Tuple]:
    """
    Merge lines with similar angles into representative lines.
    Returns longest line from each angle group.
    """
    if not lines:
        return []
    
    # Sort by length (longest first)
    sorted_lines = sorted(lines, key=get_line_length, reverse=True)
    
    merged = []
    used = [False] * len(sorted_lines)
    
    for i, line in enumerate(sorted_lines):
        if used[i]:
            continue
        
        angle = get_line_angle(line)
        group = [line]
        used[i] = True
        
        # Find lines with similar angle
        for j, other in enumerate(sorted_lines[i+1:], i+1):
            if used[j]:
                continue
            other_angle = get_line_angle(other)
            angle_diff = min(abs(angle - other_angle), 180 - abs(angle - other_angle))
            if angle_diff < angle_thresh:
                group.append(other)
                used[j] = True
        
        # Keep the longest line from this group
        merged.append(max(group, key=get_line_length))
    
    return merged


def find_line_intersection(line1: tuple, line2: tuple) -> Optional[Tuple]:
    """Find intersection point of two lines (extended infinitely)."""
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-10:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    return (int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1)))


def find_triangle_vertices(lines: list, img_shape: tuple) -> list:
    """Find triangle vertices from detected lines using improved algorithm."""
    print(f"[LOG] Processing {len(lines)} raw lines...")
    
    height, width = img_shape[:2]
    border_margin = int(min(height, width) * 0.05)  # Ignore lines near border
    
    # Step 1: Filter out border lines
    filtered_lines = []
    for line in lines:
        x1, y1, x2, y2 = line
        # Skip if both endpoints are near border
        near_border = (
            (x1 < border_margin or x1 > width - border_margin or 
             y1 < border_margin or y1 > height - border_margin) and
            (x2 < border_margin or x2 > width - border_margin or 
             y2 < border_margin or y2 > height - border_margin)
        )
        if not near_border:
            filtered_lines.append(line)
    
    print(f"[LOG] After filtering border lines: {len(filtered_lines)} lines")
    
    # Step 2: Sort by length and merge
    sorted_lines = sorted(filtered_lines, key=get_line_length, reverse=True)
    print(f"[LOG] Top 5 line lengths: {[int(get_line_length(l)) for l in sorted_lines[:5]]}")
    
    merged_lines = merge_similar_lines(sorted_lines[:50])
    print(f"[LOG] After merging similar angles: {len(merged_lines)} unique lines")
    
    if len(merged_lines) < 3:
        print("[LOG] Not enough unique lines for triangle")
        return []
    
    # Step 3: Calculate centroid of lines (center of triangle area)
    all_points = []
    for line in merged_lines[:6]:
        x1, y1, x2, y2 = line
        all_points.extend([(x1, y1), (x2, y2)])
    centroid_x = sum(p[0] for p in all_points) / len(all_points)
    centroid_y = sum(p[1] for p in all_points) / len(all_points)
    print(f"[LOG] Line centroid: ({int(centroid_x)}, {int(centroid_y)})")
    
    # Step 4: Find intersections (only inside image with small margin)
    vertices = []
    margin = border_margin * 2
    
    for line1, line2 in combinations(merged_lines[:10], 2):
        intersection = find_line_intersection(line1, line2)
        if intersection is None:
            continue
        x, y = intersection
        # Only keep if inside image (with small margin, not outside)
        if margin <= x <= width - margin and margin <= y <= height - margin:
            dist_to_center = np.sqrt((x - centroid_x)**2 + (y - centroid_y)**2)
            vertices.append((intersection, dist_to_center))
    
    # Step 5: Sort by distance to centroid and remove duplicates
    vertices.sort(key=lambda v: v[1])  # Closest to center first
    
    unique = []
    tolerance = int(min(height, width) * 0.03)
    for v, dist in vertices:
        is_dup = any(abs(v[0]-u[0]) < tolerance and abs(v[1]-u[1]) < tolerance for u in unique)
        if not is_dup:
            unique.append(v)
    
    print(f"[LOG] Found {len(unique)} unique vertices inside image")
    return unique[:3]


def draw_triangle(img: np.ndarray, vertices: list) -> np.ndarray:
    """Draw triangle lines between vertices."""
    result = img.copy()
    if len(result.shape) == 2:
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    if len(vertices) < 3:
        print(f"Warning: Only {len(vertices)} vertices found, need 3 for triangle")
        for v in vertices:
            cv2.circle(result, v, 8, (0, 0, 255), -1)
        return result
    
    # Draw triangle
    for i in range(3):
        pt1, pt2 = vertices[i], vertices[(i + 1) % 3]
        cv2.line(result, pt1, pt2, (0, 255, 0), 2)
        cv2.circle(result, pt1, 8, (0, 0, 255), -1)
    
    return result
