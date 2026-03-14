#!/usr/bin/env python3
"""
Convert a PNG/JPG image to a lithophane STL file.

Usage:
    python3 image_to_lithophane.py <input_image> [output.stl]

A lithophane is a 3D relief where thin areas let more light through,
reproducing the image when backlit. Bright pixels → thin (recessed),
dark pixels → thick (raised).
"""

import sys
import numpy as np
from PIL import Image
from stl import mesh

# --- Configuration ---
MAX_WIDTH_PX = 200       # Downsample to this width (height scaled proportionally)
BASE_THICKNESS_MM = 0.8  # Minimum wall thickness (bright areas)
MAX_THICKNESS_MM = 3.0   # Maximum wall thickness (dark areas)
PIXEL_SIZE_MM = 0.4      # Physical size of each pixel cell in mm
# ---------------------


def image_to_heightmap(image_path: str) -> np.ndarray:
    img = Image.open(image_path).convert("L")  # grayscale

    # Resize so width = MAX_WIDTH_PX
    w, h = img.size
    new_w = MAX_WIDTH_PX
    new_h = int(h * new_w / w)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    pixels = np.array(img, dtype=np.float32) / 255.0  # 0=black, 1=white

    # Lithophane: invert so dark areas are thicker
    depth = 1.0 - pixels
    return BASE_THICKNESS_MM + depth * (MAX_THICKNESS_MM - BASE_THICKNESS_MM)


def heightmap_to_stl(heightmap: np.ndarray, output_path: str) -> None:
    rows, cols = heightmap.shape
    ps = PIXEL_SIZE_MM  # pixel size in mm

    # Each grid cell produces 2 triangles for the top face
    # plus side walls and a flat bottom face.
    # Total faces = top(2*rows*cols) + bottom(2*rows*cols) + sides
    # For simplicity we build top + bottom + perimeter walls.

    triangles = []

    def quad(a, b, c, d):
        """Add two triangles forming a quad (a,b,c,d in order)."""
        triangles.append((a, b, c))
        triangles.append((a, c, d))

    # Top surface (z = height at each corner, bilinear quad)
    for r in range(rows - 1):
        for c in range(cols - 1):
            x0, y0 = c * ps, r * ps
            x1, y1 = (c + 1) * ps, (r + 1) * ps
            z00 = heightmap[r,     c]
            z10 = heightmap[r,     c + 1]
            z01 = heightmap[r + 1, c]
            z11 = heightmap[r + 1, c + 1]
            quad(
                (x0, y0, z00),
                (x1, y0, z10),
                (x1, y1, z11),
                (x0, y1, z01),
            )

    # Bottom face (flat at z=0)
    for r in range(rows - 1):
        for c in range(cols - 1):
            x0, y0 = c * ps, r * ps
            x1, y1 = (c + 1) * ps, (r + 1) * ps
            quad(
                (x0, y1, 0),
                (x1, y1, 0),
                (x1, y0, 0),
                (x0, y0, 0),
            )

    # Side walls (4 edges)
    def wall_strip(edge_r, edge_c, next_r, next_c):
        for i in range(len(edge_r) - 1):
            r0, c0 = edge_r[i],     edge_c[i]
            r1, c1 = edge_r[i + 1], edge_c[i + 1]
            x0, y0, z0 = c0 * ps, r0 * ps, heightmap[r0, c0]
            x1, y1, z1 = c1 * ps, r1 * ps, heightmap[r1, c1]
            quad((x0, y0, 0), (x1, y1, 0), (x1, y1, z1), (x0, y0, z0))

    # Left edge (c=0)
    wall_strip(list(range(rows)), [0] * rows,
               list(range(rows)), [0] * rows)
    # Right edge (c=cols-1)
    r_idx = list(range(rows - 1, -1, -1))
    wall_strip(r_idx, [cols - 1] * rows, r_idx, [cols - 1] * rows)
    # Top edge (r=0)
    c_idx = list(range(cols - 1, -1, -1))
    wall_strip([0] * cols, c_idx, [0] * cols, c_idx)
    # Bottom edge (r=rows-1)
    wall_strip([rows - 1] * cols, list(range(cols)),
               [rows - 1] * cols, list(range(cols)))

    # Build numpy-stl mesh
    tri_array = np.array(triangles, dtype=np.float32)  # (N, 3, 3)
    solid = mesh.Mesh(np.zeros(len(tri_array), dtype=mesh.Mesh.dtype))
    for i, t in enumerate(tri_array):
        solid.vectors[i] = t

    solid.save(output_path)
    print(f"Saved {output_path}  ({len(tri_array)} triangles)")
    w_mm = (cols - 1) * ps
    h_mm = (rows - 1) * ps
    print(f"Dimensions: {w_mm:.1f} mm x {h_mm:.1f} mm x "
          f"{MAX_THICKNESS_MM:.1f} mm (max depth)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.rsplit(".", 1)[0] + ".stl"

    print(f"Loading {input_path} ...")
    heightmap = image_to_heightmap(input_path)
    print(f"Grid: {heightmap.shape[1]} x {heightmap.shape[0]} cells")
    print("Building mesh ...")
    heightmap_to_stl(heightmap, output_path)


if __name__ == "__main__":
    main()
