from dataclasses import dataclass, field
from typing import List

import numpy as np

from src.models.color_pixel import ColorPixel


@dataclass
class ColorPixelGroup:
    POSSIBLE_CSPACES = ['RGB', 'HSV', 'LAB']
    colors: List[List[int]] = field(default_factory=list)


    def add_color_pixel(self, color: ColorPixel):
        self.colors += [color]


    def size(self):
        return len(self.colors)


    def fetch_pos_points(self):
        return [color.POS for color in self.colors]


    def fetch_color_points(self, cspace):
        if cspace not in self.POSSIBLE_CSPACES:
            raise Exception(f'Invalid colorspace specified: {val}')

        return [getattr(color, cspace) for color in self.colors]


    def pos_mean(self) -> List[float]:
        raw_pos = self.fetch_pos_points()
        return np.array(raw_pos).mean(axis=0)


    def pos_stdev(self) -> List[float]:
        raw_pos = self.fetch_pos_points()
        return np.array(raw_pos).std(axis=0)


    def color_mean(self, cspace) -> List[float]:
        raw_colors = self.fetch_color_points(cspace)
        return np.array(raw_colors).mean(axis=0)


    def color_stdev(self, cspace) -> List[float]:
        raw_colors = self.fetch_color_points(cspace)
        return np.array(raw_colors).std(axis=0)


    def clear(self):
        self.colors.clear()
