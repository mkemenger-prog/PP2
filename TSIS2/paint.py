"""
Practice 12 – Paint Application (Extended)
New features added on top of Practice 10–11:
  1. Freehand pencil tool (continuous draw while mouse held)
  2. Straight line tool with live preview
  3. Three brush size levels (2 / 5 / 10 px) — keyboard 1/2/3 or buttons
  4. Flood-fill tool (iterative BFS pixel fill)
  5. Ctrl+S saves canvas as timestamped .png
  6. Text tool — click to place, type, Enter to confirm, Escape to cancel
  7. All existing shapes respect active brush size
"""

import pygame
import sys
import math
from datetime import datetime

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────
SCREEN_W  = 1000
SCREEN_H  = 680
TOOLBAR_W = 170
CANVAS_X  = TOOLBAR_W
CANVAS_W  = SCREEN_W - TOOLBAR_W
CANVAS_H  = SCREEN_H

# Colours
WHITE        = (255, 255, 255)
BLACK        = (0,   0,   0)
BG_TOOLBAR   = (28,  30,  40)
BG_CANVAS    = (255, 255, 255)
HIGHLIGHT    = (99,  179, 237)
HIGHLIGHT_DK = (49,  130, 180)
TEXT_COLOUR  = (200, 210, 220)
SECTION_COL  = (55,  58,  75)
GRID_COLOUR  = (235, 235, 240)
STATUS_BG    = (18,  20,  28)

# Palette
PALETTE = [
    (0,   0,   0),
    (255, 255, 255),
    (220, 40,  40),
    (30,  120, 255),
    (50,  200, 80),
    (255, 220, 0),
    (255, 140, 0),
    (180, 60,  200),
    (0,   200, 200),
    (255, 105, 180),
    (139, 90,  43),
    (128, 128, 128),
]

# Brush sizes — (display label, pixel width)
BRUSH_SIZES = [(2, "S"), (5, "M"), (10, "L")]

# Tool IDs
TOOL_PENCIL     = "pencil"
TOOL_LINE       = "line"
TOOL_RECT       = "rect"
TOOL_SQUARE     = "square"
TOOL_CIRCLE     = "circle"
TOOL_RTRIANGLE  = "right_tri"
TOOL_EQTRIANGLE = "eq_tri"
TOOL_RHOMBUS    = "rhombus"
TOOL_FILL       = "fill"
TOOL_TEXT       = "text"
TOOL_ERASER     = "eraser"

TOOL_LABELS = {
    TOOL_PENCIL:     "✏  Pencil",
    TOOL_LINE:       "╱  Line",
    TOOL_RECT:       "▭  Rectangle",
    TOOL_SQUARE:     "■  Square",
    TOOL_CIRCLE:     "○  Circle",
    TOOL_RTRIANGLE:  "◺  R-Triangle",
    TOOL_EQTRIANGLE: "△  Eq-Triangle",
    TOOL_RHOMBUS:    "◇  Rhombus",
    TOOL_FILL:       "🪣  Fill",
    TOOL_TEXT:       "T  Text",
    TOOL_ERASER:     "⬜  Eraser",
}

TOOL_ORDER = [
    TOOL_PENCIL,   TOOL_LINE,
    TOOL_RECT,     TOOL_SQUARE,
    TOOL_CIRCLE,
    TOOL_RTRIANGLE, TOOL_EQTRIANGLE,
    TOOL_RHOMBUS,
    TOOL_FILL,     TOOL_TEXT,
    TOOL_ERASER,
]

# Keyboard shortcuts for brush sizes
SIZE_KEYS = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}


# ──────────────────────────────────────────────
# GEOMETRY HELPERS
# ──────────────────────────────────────────────

def points_right_triangle(x1, y1, x2, y2):
    """Right-angle at bottom-left corner."""
    return [(x1, y1), (x1, y2), (x2, y2)]


def points_equilateral_triangle(x1, y1, x2, y2):
    """Equilateral triangle: base from x1→x2 at lower y, apex centred above."""
    bx1 = min(x1, x2);  bx2 = max(x1, x2)
    by  = max(y1, y2)
    cx  = (bx1 + bx2) / 2
    side   = bx2 - bx1
    height = side * math.sqrt(3) / 2
    ay  = by - height
    return [(cx, ay), (bx1, by), (bx2, by)]


def points_rhombus(x1, y1, x2, y2):
    """Diamond inscribed in bounding box."""
    lx = min(x1, x2); rx = max(x1, x2)
    ty = min(y1, y2); by = max(y1, y2)
    cx = (lx + rx) / 2;  cy = (ty + by) / 2
    return [(cx, ty), (rx, cy), (cx, by), (lx, cy)]


def flood_fill(surface, pos, fill_colour):
    """
    Iterative BFS flood fill.
    Fills all connected pixels matching the colour at `pos` with `fill_colour`.
    """
    target = surface.get_at(pos)[:3]
    if target == tuple(fill_colour):
        return
    w, h = surface.get_size()
    stack = [pos]
    visited = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        if not (0 <= x < w and 0 <= y < h):
            continue
        if surface.get_at((x, y))[:3] != target:
            continue
        surface.set_at((x, y), fill_colour)
        visited.add((x, y))
        stack += [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]


# ──────────────────────────────────────────────
# TOOLBAR
# ──────────────────────────────────────────────

class Toolbar:
    """Left-side toolbar: tools, palette, brush size, clear button."""

    BTN_H   = 32
    BTN_PAD = 3

    def __init__(self, small_font, tiny_font):
        self.small_font = small_font
        self.tiny_font  = tiny_font

        # ── Tool buttons ──
        self.tool_rects = {}
        y = 32
        for tool in TOOL_ORDER:
            r = pygame.Rect(6, y, TOOLBAR_W - 12, self.BTN_H)
            self.tool_rects[tool] = r
            y += self.BTN_H + self.BTN_PAD
        self._tools_bottom = y + 8

        # ── Palette swatches ──
        self.palette_rects = []
        px, py = 8, self._tools_bottom + 22
        SW = 26
        for i, col in enumerate(PALETTE):
            ci = i % 4;  ri = i // 4
            r = pygame.Rect(px + ci*(SW+3), py + ri*(SW+3), SW, SW)
            self.palette_rects.append((r, col))
        self._palette_bottom = py + (len(PALETTE)//4 + 1)*(SW+3) + 8

        # ── Brush size buttons ──
        self.size_rects = []
        sx = 8;  sy = self._palette_bottom + 22
        BW = (TOOLBAR_W - 16 - 8) // 3
        for i, (sz, lbl) in enumerate(BRUSH_SIZES):
            r = pygame.Rect(sx + i*(BW+4), sy, BW, 30)
            self.size_rects.append((r, sz, lbl))
        self._sizes_bottom = sy + 34

        # ── Clear button ──
        self.clear_rect = pygame.Rect(8, self._sizes_bottom + 10, TOOLBAR_W-16, 30)

    # ── Drawing ────────────────────────────────

    def draw(self, surface, active_tool, active_colour, active_size):
        # Background
        pygame.draw.rect(surface, BG_TOOLBAR, (0, 0, TOOLBAR_W, SCREEN_H))
        pygame.draw.line(surface, SECTION_COL, (TOOLBAR_W-1, 0), (TOOLBAR_W-1, SCREEN_H), 2)

        # Title
        t = self.small_font.render("PAINT", True, HIGHLIGHT)
        surface.blit(t, (TOOLBAR_W//2 - t.get_width()//2, 8))

        # Tool buttons
        for tool, rect in self.tool_rects.items():
            selected = (tool == active_tool)
            bg = HIGHLIGHT_DK if selected else (50, 52, 65)
            pygame.draw.rect(surface, bg, rect, border_radius=5)
            if selected:
                pygame.draw.rect(surface, HIGHLIGHT, rect, 2, border_radius=5)
            lbl = self.tiny_font.render(TOOL_LABELS[tool], True, WHITE if selected else TEXT_COLOUR)
            surface.blit(lbl, lbl.get_rect(center=rect.center))

        # Palette header
        ph = self.tiny_font.render("COLOUR", True, TEXT_COLOUR)
        surface.blit(ph, (TOOLBAR_W//2 - ph.get_width()//2, self._tools_bottom + 6))
        # Swatches
        for rect, col in self.palette_rects:
            pygame.draw.rect(surface, col, rect, border_radius=3)
            if col == active_colour:
                pygame.draw.rect(surface, WHITE, rect, 2, border_radius=3)
            else:
                pygame.draw.rect(surface, (80,80,90), rect, 1, border_radius=3)

        # Size header
        sh = self.tiny_font.render("BRUSH  (keys 1/2/3)", True, TEXT_COLOUR)
        surface.blit(sh, (TOOLBAR_W//2 - sh.get_width()//2, self._palette_bottom + 6))
        # Size buttons
        for rect, sz, lbl in self.size_rects:
            sel = (sz == active_size)
            bg  = HIGHLIGHT_DK if sel else (50, 52, 65)
            pygame.draw.rect(surface, bg, rect, border_radius=4)
            if sel:
                pygame.draw.rect(surface, HIGHLIGHT, rect, 2, border_radius=4)
            # Visual dot + label
            dot_r = min(sz//2, 8)
            pygame.draw.circle(surface, WHITE, (rect.centerx - 10, rect.centery), dot_r)
            lt = self.tiny_font.render(lbl, True, WHITE if sel else TEXT_COLOUR)
            surface.blit(lt, lt.get_rect(midleft=(rect.centerx - 2, rect.centery)))

        # Clear button
        pygame.draw.rect(surface, (160, 40, 40), self.clear_rect, border_radius=5)
        ct = self.tiny_font.render("🗑  Clear Canvas", True, WHITE)
        surface.blit(ct, ct.get_rect(center=self.clear_rect.center))

    # ── Click handling ──────────────────────────

    def handle_click(self, pos, active_tool, active_colour, active_size):
        new_tool   = active_tool
        new_colour = active_colour
        new_size   = active_size
        clear      = False

        for tool, rect in self.tool_rects.items():
            if rect.collidepoint(pos):
                new_tool = tool
        for rect, col in self.palette_rects:
            if rect.collidepoint(pos):
                new_colour = col
        for rect, sz, lbl in self.size_rects:
            if rect.collidepoint(pos):
                new_size = sz
        if self.clear_rect.collidepoint(pos):
            clear = True

        return new_tool, new_colour, new_size, clear


# ──────────────────────────────────────────────
# TEXT INPUT STATE
# ──────────────────────────────────────────────

class TextInput:
    """Manages an active text-placement session."""

    def __init__(self, canvas_pos, font, colour):
        self.pos    = canvas_pos   # (x, y) on canvas
        self.text   = ""
        self.font   = font
        self.colour = colour
        self.active = True
        # Blinking cursor timer
        self.cursor_timer = 0

    def add_char(self, char):
        self.text += char

    def backspace(self):
        self.text = self.text[:-1]

    def render_preview(self, canvas_surf):
        """Draw the current typed text + blinking cursor onto a temp surface copy."""
        display_text = self.text
        self.cursor_timer += 1
        # Blink every 30 frames
        if (self.cursor_timer // 30) % 2 == 0:
            display_text += "|"
        surf = self.font.render(display_text, True, self.colour)
        canvas_surf.blit(surf, self.pos)

    def commit(self, canvas_surf):
        """Permanently draw text onto the canvas."""
        if self.text:
            surf = self.font.render(self.text, True, self.colour)
            canvas_surf.blit(surf, self.pos)
        self.active = False


# ──────────────────────────────────────────────
# SHAPE DRAWING HELPER
# ──────────────────────────────────────────────

def draw_shape(surface, tool, p1, p2, colour, size, offset_x=0):
    """
    Draw a shape onto `surface`.
    offset_x is added to all x coords (used for screen-space preview).
    """
    x1, y1 = p1[0] + offset_x, p1[1]
    x2, y2 = p2[0] + offset_x, p2[1]
    w = max(1, size)

    if tool == TOOL_LINE:
        pygame.draw.line(surface, colour, (x1,y1), (x2,y2), w)

    elif tool == TOOL_RECT:
        rx = min(x1,x2); ry = min(y1,y2)
        rw = abs(x2-x1); rh = abs(y2-y1)
        pygame.draw.rect(surface, colour, (rx,ry,rw,rh), w)

    elif tool == TOOL_SQUARE:
        side = min(abs(x2-x1), abs(y2-y1))
        sx   = x1 if x2 >= x1 else x1 - side
        sy   = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, colour, (sx,sy,side,side), w)

    elif tool == TOOL_CIRCLE:
        cx = (x1+x2)//2; cy = (y1+y2)//2
        rad = max(1, int(math.hypot(x2-x1, y2-y1)//2))
        pygame.draw.circle(surface, colour, (cx,cy), rad, w)

    elif tool == TOOL_RTRIANGLE:
        pts = points_right_triangle(x1,y1,x2,y2)
        pygame.draw.polygon(surface, colour, [(int(a),int(b)) for a,b in pts], w)

    elif tool == TOOL_EQTRIANGLE:
        pts = points_equilateral_triangle(x1,y1,x2,y2)
        pygame.draw.polygon(surface, colour, [(int(a),int(b)) for a,b in pts], w)

    elif tool == TOOL_RHOMBUS:
        pts = points_rhombus(x1,y1,x2,y2)
        pygame.draw.polygon(surface, colour, [(int(a),int(b)) for a,b in pts], w)


SHAPE_TOOLS = {TOOL_LINE, TOOL_RECT, TOOL_SQUARE, TOOL_CIRCLE,
               TOOL_RTRIANGLE, TOOL_EQTRIANGLE, TOOL_RHOMBUS}


# ──────────────────────────────────────────────
# MAIN APPLICATION
# ──────────────────────────────────────────────

class PaintApp:

    def __init__(self):
        pygame.init()
        self.screen     = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Paint – Practice 12")
        self.clock      = pygame.time.Clock()

        # Fonts
        self.font       = pygame.font.SysFont("segoeui", 18, bold=True)
        self.small_font = pygame.font.SysFont("segoeui", 14, bold=True)
        self.tiny_font  = pygame.font.SysFont("segoeui", 12)
        self.text_font  = pygame.font.SysFont("segoeui", 22)  # for text tool

        # Canvas
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(BG_CANVAS)

        # Toolbar
        self.toolbar = Toolbar(self.small_font, self.tiny_font)

        # Active state
        self.active_tool   = TOOL_PENCIL
        self.active_colour = BLACK
        self.active_size   = BRUSH_SIZES[1][0]  # medium (5px)

        # Drag state
        self.drawing   = False
        self.start_pos = None
        self.last_pos  = None

        # Text input session
        self.text_input: TextInput | None = None

        self.running = True

    # ── Helpers ────────────────────────────────

    def to_canvas(self, pos):
        return (pos[0] - CANVAS_X, pos[1])

    def on_canvas(self, pos):
        return pos[0] >= CANVAS_X

    # ── Main loop ──────────────────────────────

    def run(self):
        while self.running:
            self.clock.tick(60)
            self._handle_events()
            self._draw()
        pygame.quit()
        sys.exit()

    # ── Events ─────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():

            # ── Quit ──
            if event.type == pygame.QUIT:
                self.running = False

            # ── Key down ──
            elif event.type == pygame.KEYDOWN:

                # Text tool active: intercept all typing
                if self.text_input and self.text_input.active:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.text_input.commit(self.canvas)
                        self.text_input = None
                    elif event.key == pygame.K_ESCAPE:
                        self.text_input = None
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_input.backspace()
                    else:
                        ch = event.unicode
                        if ch and ch.isprintable():
                            self.text_input.add_char(ch)
                    return   # don't process other shortcuts while typing

                # Escape → quit
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Delete → clear canvas
                if event.key == pygame.K_DELETE:
                    self.canvas.fill(BG_CANVAS)

                # Ctrl+S → save canvas
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    self._save_canvas()

                # 1/2/3 → brush size shortcut
                if event.key in SIZE_KEYS:
                    idx = SIZE_KEYS[event.key]
                    self.active_size = BRUSH_SIZES[idx][0]

            # ── Mouse button DOWN ──
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if not self.on_canvas(pos):
                    # Toolbar click
                    r = self.toolbar.handle_click(
                        pos, self.active_tool, self.active_colour, self.active_size)
                    self.active_tool, self.active_colour, self.active_size, clear = r
                    if clear:
                        self.canvas.fill(BG_CANVAS)
                        self.text_input = None
                else:
                    cp = self.to_canvas(pos)

                    # ── Text tool: start new text session ──
                    if self.active_tool == TOOL_TEXT:
                        # Commit any existing session first
                        if self.text_input and self.text_input.active:
                            self.text_input.commit(self.canvas)
                        self.text_input = TextInput(cp, self.text_font, self.active_colour)
                        return

                    # Cancel text session if another tool clicked on canvas
                    if self.text_input and self.text_input.active:
                        self.text_input.commit(self.canvas)
                        self.text_input = None

                    # ── Fill tool ──
                    if self.active_tool == TOOL_FILL:
                        flood_fill(self.canvas, cp, self.active_colour)
                        return

                    # ── Begin draw session ──
                    self.drawing   = True
                    self.start_pos = cp
                    self.last_pos  = cp

                    # Pencil/eraser: dot at click point
                    if self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                        col = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                        pygame.draw.circle(self.canvas, col, cp, self.active_size // 2)

            # ── Mouse MOTION ──
            elif event.type == pygame.MOUSEMOTION and self.drawing:
                pos = event.pos
                if self.on_canvas(pos):
                    cp = self.to_canvas(pos)
                    if self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                        col = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                        pygame.draw.line(self.canvas, col, self.last_pos, cp, self.active_size)
                        self.last_pos = cp
                    # Shape tools: preview handled in _draw()

            # ── Mouse button UP ──
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.drawing:
                    pos = event.pos
                    if self.on_canvas(pos):
                        cp = self.to_canvas(pos)
                        if self.active_tool in SHAPE_TOOLS:
                            draw_shape(self.canvas, self.active_tool,
                                       self.start_pos, cp,
                                       self.active_colour, self.active_size)
                    self.drawing   = False
                    self.start_pos = None

    # ── Save ───────────────────────────────────

    def _save_canvas(self):
        """Save canvas as a timestamped PNG."""
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"canvas_{ts}.png"
        pygame.image.save(self.canvas, path)
        # Brief flash feedback stored for status bar
        self._last_save = path
        self._save_flash = 120   # frames to show message

    # ── Rendering ──────────────────────────────

    def _draw(self):
        self.screen.fill((20, 22, 30))

        # ── Canvas ──
        self.screen.blit(self.canvas, (CANVAS_X, 0))

        # ── Text tool preview ──
        if self.text_input and self.text_input.active:
            # Draw on a temp copy so cursor blink doesn't modify canvas
            tmp = self.canvas.copy()
            self.text_input.render_preview(tmp)
            self.screen.blit(tmp, (CANVAS_X, 0))

        # ── Shape preview while dragging ──
        if self.drawing and self.start_pos and self.active_tool in SHAPE_TOOLS:
            mc = self.to_canvas(pygame.mouse.get_pos())
            draw_shape(self.screen, self.active_tool,
                       self.start_pos, mc,
                       self.active_colour, self.active_size,
                       offset_x=CANVAS_X)

        # ── Toolbar ──
        self.toolbar.draw(self.screen, self.active_tool, self.active_colour, self.active_size)

        # ── Status bar (bottom of toolbar) ──
        mx, my = pygame.mouse.get_pos()
        cx, cy = self.to_canvas((mx, my))
        pygame.draw.rect(self.screen, STATUS_BG, (0, SCREEN_H-20, TOOLBAR_W, 20))

        # Save flash message
        if hasattr(self, '_save_flash') and self._save_flash > 0:
            msg = self.tiny_font.render(f"Saved: {self._last_save}", True, (100, 220, 100))
            self._save_flash -= 1
        else:
            tool_lbl = TOOL_LABELS.get(self.active_tool, "")
            msg = self.tiny_font.render(
                f"{tool_lbl}  ({max(0,cx)},{max(0,cy)})  sz:{self.active_size}", True, TEXT_COLOUR)

        self.screen.blit(msg, (4, SCREEN_H - 17))

        # ── Text-mode indicator overlay ──
        if self.text_input and self.text_input.active:
            banner = self.tiny_font.render(
                "TEXT MODE — Type text, Enter to confirm, Esc to cancel", True, (255, 230, 100))
            bx = CANVAS_X + (CANVAS_W - banner.get_width()) // 2
            pygame.draw.rect(self.screen, (30, 30, 20),
                             (bx-6, 4, banner.get_width()+12, 20), border_radius=4)
            self.screen.blit(banner, (bx, 6))

        # ── Keyboard hint ──
        hint = self.tiny_font.render("Ctrl+S: Save  |  Del: Clear  |  1/2/3: Brush size", True, (70,75,90))
        self.screen.blit(hint, (CANVAS_X + 6, SCREEN_H - 17))

        pygame.display.flip()


# ──────────────────────────────────────────────
if __name__ == "__main__":
    PaintApp().run()