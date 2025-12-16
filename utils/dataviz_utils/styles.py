# styles.py
# author: @Rackkoun
# date: 07.12.25 - 16:50
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

# import palettes
from utils.dataviz_utils.palettes import (
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_RED,
    PALETTE_ORANGE, PALETTE_BLUE_GREEN, PALETTE_PURPLE,
    DIVERGING_PALETTES, SEQUENTIAL_PALETTES,
    CATEGORICAL_PALETTES, CMAP_PALETTE_00, CMAP_PALETTE_01,
    CMAP_PALETTE_02, MIXED_PALETTE
)
# Seaborn Config
def sns_config(style="darkgrid", context="notebook"):
    """Custom settings for data viz with seaborn"""
    sns.set_theme(
        context=context,
        style=style,
        rc={
            "axes.edgecolor": "0.3",
            "axes.linewidth": 1.1,
            "grid.color": "0.85",
            "grid.linewidth": 0.8,
            "figure.figsize": (15, 10),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": True,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "figure.titlesize": 16,
        }
    )
    print(f"[^v^] Seaborn configured with style: '{style}', context: '{context}'")

def plt_config():
    """Custom setting for matplotlib rcParams"""
    rcParams.update({
        'figure.figsize': (12, 6),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        'figure.constrained_layout.use': True,
        'font.family': 'DejaVu Sans',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linewidth': 0.8,
    })
    print("[°-°] Matplotlib rcParams configured")

# helper func
def set_palette(palette_name, n_colors=6):
    """Set seaborn color palette by name"""
    if palette_name in SEQUENTIAL_PALETTES:
        palette = SEQUENTIAL_PALETTES[palette_name]
    elif palette_name in DIVERGING_PALETTES:
        palette = DIVERGING_PALETTES[palette_name]
    elif palette_name in CATEGORICAL_PALETTES:
        palette = CATEGORICAL_PALETTES[palette_name]
    else:
        # palette name does not exit
        print(f"Palette '{palette_name}' not found [`^´]")
    
    if palette:
        colors = palette[:n_colors] if len(palette) > n_colors else palette
        sns.set_palette(colors)
        print(f"[°v^] Palette set: '{palette_name}' with {len(colors)} colors")
        return colors
    else:
        print(f"[-_-]  Palette '{palette_name}' not found. Using default.")
        return None

# preview palettes
def preview_all_palettes():
    """Display all available palettes"""
    fig, axes = plt.subplots(13, 1, figsize=(12, 6))
    
    palettes = [
        ("PALETTE_BLUE", PALETTE_BLUE),
        ("PALETTE_BLUE_GREEN", PALETTE_BLUE_GREEN),
        ("PALETTE_GREEN", PALETTE_GREEN),
        ("PALETTE_RED", PALETTE_RED),
        ("PALETTE_PURPLE", PALETTE_PURPLE),
        ("PALETTE_ORANGE", PALETTE_ORANGE),
        ("CATEGORICAL_set1", CATEGORICAL_PALETTES['set1']),
        ("CATEGORICAL_set2", CATEGORICAL_PALETTES['set2']),
        ("CATEGORICAL_paired", CATEGORICAL_PALETTES['paired']),
        ("CMAP_00", CMAP_PALETTE_00),
        ("CMAP_01", CMAP_PALETTE_01),
        ("CMAP_02", CMAP_PALETTE_02),
        ("ALL MIXED", MIXED_PALETTE),
    ]
    
    for ax, (name, palette) in zip(axes, palettes):
        for i, color in enumerate(palette):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        ax.set_xlim(0, len(palette))
        ax.set_ylim(0, 1)
        ax.set_title(name, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
    
    # plt.tight_layout()
    plt.show()