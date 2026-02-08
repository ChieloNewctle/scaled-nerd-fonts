from pathlib import Path

import fontforge
import psMat

BASE_DIR = Path(__file__).parent
INPUT_FONT = str(BASE_DIR / "SymbolsNerdFont-Regular.ttf")

SCALE = 0.95
SHIFT_Y = 65


RANGES = [
    (0x2190, 0x21FF),  # Arrows
    (0x2300, 0x23FF),  # Misc technical
    (0x2460, 0x24FF),  # Enclosed alphanumerics
    (0x25A0, 0x25FF),  # Geometric shapes
    (0x2600, 0x26FF),  # Misc symbols
    (0x2700, 0x27BF),  # Dingbats
    (0x2B00, 0x2BFF),  # Arrows & symbols
    (0xE000, 0xF8FF),  # PUA (BMP)
    (0xF0000, 0xFFFFD),  # PUA (Supplementary)
]


def scale_glyph(glyph, scale):
    if glyph.isWorthOutputting() is False:
        return

    bbox = glyph.boundingBox()
    if bbox is None:
        return

    # em = glyph.font.em
    # cx = em / 2
    # cy = (glyph.font.ascent - glyph.font.descent) / 2

    xmin, ymin, xmax, ymax = bbox
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2

    mat = psMat.translate(-cx, -cy)
    mat = psMat.compose(mat, psMat.scale(scale))
    mat = psMat.compose(mat, psMat.translate(cx, cy))
    mat = psMat.compose(mat, psMat.translate(0, SHIFT_Y))

    old_width = glyph.width
    glyph.transform(mat)
    glyph.width = old_width


def gen_font(is_bold, is_italic):
    font = fontforge.open(INPUT_FONT)

    font.familyname = "Symbols Nerd Font Scaled"

    suffix = {
        (False, False): "Regular",
        (True, False): "Bold",
        (False, True): "Italic",
        (True, True): "BoldItalic",
    }[(is_bold, is_italic)]
    font.fontname = f"SymbolsNerdFontScaled-{suffix}"
    font.fullname = f"Symbols Nerd Font Scaled {suffix}"

    font.appendSFNTName(0x409, 2, suffix)

    style_map = 0

    if is_bold:
        font.os2_weight = 700
        font.weight = "Bold"
        style_map |= 32

    if is_italic:
        font.italicangle = 0
        style_map |= 1

    if style_map:
        font.os2_stylemap = style_map

    mac_style = 0
    if is_bold:
        mac_style |= 1
    if is_italic:
        mac_style |= 2
    font.macstyle = mac_style

    count = 0
    for start, end in RANGES:
        font.selection.select(("ranges",), start, end)
        for g in font.selection.byGlyphs:
            scale_glyph(g, SCALE)
            count += 1

    print(f"Scaled {count} glyphs")

    typo_ascent = font.ascent
    typo_descent = font.descent
    font.os2_typoascent = typo_ascent
    font.os2_typodescent = -typo_descent
    font.os2_typolinegap = 0
    font.os2_winascent = typo_ascent
    font.os2_windescent = typo_descent

    output_font = str(BASE_DIR / f"SymbolsNerdFontScaled-{suffix}.ttf")
    font.generate(output_font)
    print(f"Generated {output_font}")
    font.close()


for bold in [False, True]:
    for italic in [False, True]:
        gen_font(bold, italic)
