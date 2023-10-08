from dataclasses import dataclass
from typing import List

@dataclass
class ColorPixel:
    POS: List[int]
    RGB: List[int]
    HSV: List[int]
    LAB: List[int]
