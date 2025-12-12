# __init__.py
# Provide custom color palettes, seaborn/matplotlib config and helper func
# import form palettes modules
from .palettes import (
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_RED,
    PALETTE_ORANGE, PALETTE_BLUE_GREEN, PALETTE_PURPLE,
    DIVERGING_PALETTES, SEQUENTIAL_PALETTES,
    CATEGORICAL_PALETTES, CMAP_PALETTE_00, CMAP_PALETTE_01,
    CMAP_PALETTE_02, MIXED_PALETTE
)
# import from styles
from .styles import (
    sns_config,
    plt_config,
    set_palette,
    preview_all_palettes
)
#  auto-config default settings
sns_config()
plt_config()

# define 'from utils.dataviz_utils import *'
__all__ = [
    # Palettes
    "PALETTE_BLUE", "PALETTE_GREEN", "PALETTE_RED",
    "PALETTE_ORANGE", "PALETTE_BLUE_GREEN", "PALETTE_PURPLE",
    "DIVERGING_PALETTES", "SEQUENTIAL_PALETTES",
    "CATEGORICAL_PALETTES", "CMAP_PALETTE_00", "CMAP_PALETTE_01",
    "CMAP_PALETTE_02", "MIXED_PALETTE",
    # Func
    "sns_config", "plt_config", "set_palette", "preview_all_palettes"
]
# version info
__version__ = "1.0.0"
__author__ = "@Rackkoun"
__date__ = "07.12.2025"