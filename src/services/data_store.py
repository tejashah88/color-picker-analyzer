from kink import inject

from src.models.color_pixel_group import ColorPixelGroup

@inject
class DataStore:
    def __init__(self, max_groups):
        self._groups = []
        self.active_group_index = 0

        for i in range(max_groups):
            self._groups += [ColorPixelGroup()]


    def num_groups(self):
        return len(self._groups)


    def switch_group(self, index):
        self.active_group_index = index


    @property
    def active_group(self):
        return self._groups[self.active_group_index]


    @property
    def all_groups(self):
        return self._groups

