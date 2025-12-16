# palettes.py
# author: @Rackkoun
# date: 07.12.25 - 16:40

# Color Palettes
PALETTE_BLUE = [
    "#061c5c", "#112770", "#1c3384", "#054fb9", "#0461cf",
    "#2918ac", "#3924c5", "#4930df", "#948ceb", "#b9b4f4",
    "#0073e6", "#589ef4", "#8babf1", "#b3c7f7", "#8086ae",
    "#adb1cd"
]
PALETTE_BLUE_GREEN = [
    
    "#23a17d", "#31b791", "#3fcda6", "#3fcda6",
    "#72d390", "#99e1c9", "#ade5bc", "#a5dc4e",
    "#c8eaa0", "#b9ebd9", "#99e1c9",
    "#005a86", "#42bfd3", "#a1c4f9", "#98d8e6", "#829ab4"
]
PALETTE_GREEN = [
    "#015d1f", "#02712e", "#03863d", "#00806a", "#03863d",
    "#03863d", "#2a7a01", "#388f00", "#599887", "#89b593",
    "#47cd0f", "#5ee417", "#74fb1f", "#b3fd9a", "#cbfebb",
    "#898600", "#aeb300", "#cdd090", "#93ba8b", 
    "#89b593", "#86b1a5",
]
PALETTE_RED = [
    "#820107", "#9a0308", "#b20408", "#b1233b", "#c9324d",
    "#e2405f", "#cf8686", "#ef97a3", "#e1b0b0", "#f6bac2",
    "#dbafbc", "#c58499", "#a30456", "#8c0244", "#750132", 
]
PALETTE_PURPLE = [
    "#680482", "#84099d", "#a20fb9","#9a39e9", "#da39d1",
    "#d066e5", "#c389d2", "#d8b2e3",
]
PALETTE_ORANGE = [
    "#cb574f", "#e46c61", "#fc8175", "#f17944", "#f1c307"
]

# Specialized palettes for different plot types
SEQUENTIAL_PALETTES = {
    'blue_seq': PALETTE_BLUE,
    'green_seq': PALETTE_GREEN,
    'red_seq': PALETTE_RED,
    'purple_seq': PALETTE_PURPLE
}

DIVERGING_PALETTES = {
    'blue_green': PALETTE_BLUE_GREEN,
    'red_green': PALETTE_RED[:5] + PALETTE_GREEN[:5],
    'purple_green': PALETTE_PURPLE[:5] + PALETTE_GREEN[:5]
}

CATEGORICAL_PALETTES = {
    'set1': PALETTE_BLUE[:3] + PALETTE_GREEN[:3] + PALETTE_RED[:3],
    'set2': PALETTE_PURPLE[:3] + PALETTE_ORANGE[:3] + PALETTE_BLUE_GREEN[:3],
    'paired': [PALETTE_BLUE[0], PALETTE_BLUE[2], 
               PALETTE_GREEN[0], PALETTE_GREEN[2],
               PALETTE_RED[0], PALETTE_RED[2]]
}

# Heatmap and pairplot:
CMAP_PALETTE_00 = [
    "#D73027", "#F46D43", "#FDAE61", "#FEE08B", 
    "#FFFFBF", "#D9EF8B", "#A6D96A", "#66BD63", "#1A9850"
]
CMAP_PALETTE_01 = [
    "#3A7C7E", "#5A96A6", "#8BB4B4", "#E6B8A2", 
    "#C17767", "#F77189", "#A0453A"
]
CMAP_PALETTE_02 = [
    "#2C5F7A", "#4A8AA6", "#8BB4B4","#F5F5F5",
    "#E6B8A2", "#C17767", "#A0453A"
]
# MIXED
MIXED_PALETTE = [
    "#44AF69",  # Fresh green
    "#C73E1D",  # Earth red
    "#F18F01",  # Warm orange
    "#2E86AB",  # Professional blue
    "#A23B72",  # Muted purple
    "#3B8EA5",  # Teal blue
    "#6D597A",  # Dusty purple
    "#FF6B6B",  # Coral
    "#5D5C61",  # Charcoal
    "#F9C74F",  # Gold
    "#577590",  # Steel blue
    "#F3722C",  # Burnt orange
    "#43AA8B",  # Sage green
    "#BC4749",  # Brick red
    "#6A4C93"   # Amethyst
]