"""
tools.py – Geometry helpers and fill algorithm for Paint (Practice 12).
Imported by paint.py; can also be tested independently.
"""

import math
import pygame


# ──────────────────────────────────────────────
# GEOMETRY HELPERS
# ──────────────────────────────────────────────

def points_right_triangle(x1, y1, x2, y2):
    """
    Returns the 3 vertices of a right-angle triangle.
    The right angle is placed at the bottom-left corner.
      P0 = (x1, y1)  – top-left (opposite vertex)
      P1 = (x1, y2)  – bottom-left (RIGHT ANGLE)
      P2 = (x2, y2)  – bottom-right
    """
    return [(x1, y1), (x1, y2), (x2, y2)]


def points_equilateral_triangle(x1, y1, x2, y2):
    """
    Returns 3 vertices of an equilateral triangle.
    The base runs from x1 to x2 at the lower of y1/y2.
    The apex is centred horizontally above the base.
    Height = base_length * sqrt(3) / 2.
    """
    bx1  = min(x1, x2);  bx2 = max(x1, x2)
    by   = max(y1, y2)                         # base at bottom
    cx   = (bx1 + bx2) / 2
    side = bx2 - bx1
    h    = side * math.sqrt(3) / 2
    return [(cx, by - h), (bx1, by), (bx2, by)]


def points_rhombus(x1, y1, x2, y2):
    """
    Returns 4 vertices of a rhombus (diamond) inscribed in the bounding box
    (x1, y1) → (x2, y2).  Each vertex is at the midpoint of one bounding edge.
    """
    lx = min(x1, x2);  rx = max(x1, x2)
    ty = min(y1, y2);  by = max(y1, y2)
    cx = (lx + rx) / 2;  cy = (ty + by) / 2
    return [(cx, ty), (rx, cy), (cx, by), (lx, cy)]


# ──────────────────────────────────────────────
# FLOOD FILL
# ──────────────────────────────────────────────

def flood_fill(surface: pygame.Surface, pos: tuple, fill_colour: tuple) -> None:
    """
    Iterative (stack-based) flood fill.

    Starting from pixel `pos` on `surface`, replaces all orthogonally
    connected pixels whose colour matches the original colour at `pos`
    with `fill_colour`.

    Uses exact colour matching — no tolerance.  Ignores the alpha channel.

    Parameters
    ----------
    surface      : pygame.Surface  – the surface to paint on (modified in-place)
    pos          : (int, int)       – starting pixel coordinate (canvas-relative)
    fill_colour  : (R, G, B)        – target fill colour
    """
    target = surface.get_at(pos)[:3]          # original colour (RGB only)
    fill   = tuple(fill_colour[:3])

    if target == fill:
        return                                  # already the desired colour

    w, h    = surface.get_size()
    stack   = [pos]
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        if not (0 <= x < w and 0 <= y < h):    # out of bounds
            continue
        if surface.get_at((x, y))[:3] != target:  # different colour → boundary
            continue

        surface.set_at((x, y), fill)
        visited.add((x, y))

        # Push four orthogonal neighbours
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))


# ──────────────────────────────────────────────
# UNIFIED SHAPE DRAW FUNCTION
# ──────────────────────────────────────────────

# Tool ID constants (mirrors paint.py — kept here too for standalone use)
TOOL_LINE       = "line"
TOOL_RECT       = "rect"
TOOL_SQUARE     = "square"
TOOL_CIRCLE     = "circle"
TOOL_RTRIANGLE  = "right_tri"
TOOL_EQTRIANGLE = "eq_tri"
TOOL_RHOMBUS    = "rhombus"

SHAPE_TOOLS = {
    TOOL_LINE, TOOL_RECT, TOOL_SQUARE, TOOL_CIRCLE,
    TOOL_RTRIANGLE, TOOL_EQTRIANGLE, TOOL_RHOMBUS,
}


def draw_shape(surface: pygame.Surface,
               tool: str,
               p1: tuple, p2: tuple,
               colour: tuple,
               size: int,
               offset_x: int = 0) -> None:
    """
    Draw one geometric shape onto `surface`.

    Parameters
    ----------
    surface   : destination pygame.Surface
    tool      : one of the TOOL_* constants above
    p1        : (x, y) – drag start (canvas-relative)
    p2        : (x, y) – drag end   (canvas-relative)
    colour    : (R, G, B)
    size      : stroke width in pixels (≥ 1)
    offset_x  : horizontal offset added to all x coords — pass TOOLBAR_W
                when drawing a preview onto the full screen surface.
    """
    x1, y1 = p1[0] + offset_x, p1[1]
    x2, y2 = p2[0] + offset_x, p2[1]
    w      = max(1, size)

    if tool == TOOL_LINE:
        pygame.draw.line(surface, colour, (x1, y1), (x2, y2), w)

    elif tool == TOOL_RECT:
        rx = min(x1, x2);  ry = min(y1, y2)
        rw = abs(x2 - x1); rh = abs(y2 - y1)
        pygame.draw.rect(surface, colour, (rx, ry, rw, rh), w)

    elif tool == TOOL_SQUARE:
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx   = x1 if x2 >= x1 else x1 - side
        sy   = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, colour, (sx, sy, side, side), w)

    elif tool == TOOL_CIRCLE:
        cx  = (x1 + x2) // 2;  cy = (y1 + y2) // 2
        rad = max(1, int(math.hypot(x2 - x1, y2 - y1) / 2))
        pygame.draw.circle(surface, colour, (cx, cy), rad, w)

    elif tool == TOOL_RTRIANGLE:
        pts = points_right_triangle(x1, y1, x2, y2)
        pygame.draw.polygon(surface, colour, [(int(a), int(b)) for a, b in pts], w)

    elif tool == TOOL_EQTRIANGLE:
        pts = points_equilateral_triangle(x1, y1, x2, y2)
        pygame.draw.polygon(surface, colour, [(int(a), int(b)) for a, b in pts], w)

    elif tool == TOOL_RHOMBUS:
        pts = points_rhombus(x1, y1, x2, y2)
        pygame.draw.polygon(surface, colour, [(int(a), int(b)) for a, b in pts], w)