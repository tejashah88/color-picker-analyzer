from string import ascii_uppercase
from kink import inject

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *

import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

from src.views.qutils import WidgetDataUpdateMixin
from src.views.components.plot_3d import Plot3D
from src.views.components.always_show_list_widget import AlwaysShowListWidget

from src.services.config_store import ConfigStore
from src.services.data_store import DataStore

COLOR_3D_PLOT_AXIS_SCALE = 4


@inject
class VisualizeDataWidget(QWidget, WidgetDataUpdateMixin):
    def __init__(self, config_store: ConfigStore, data_store: DataStore):
        super().__init__()

        self.config_store = config_store
        self.data_store = data_store
        self.selected_group = -1

        # Setup UI
        self._build_gui()
        self._update_gui_with_data()

        # Activate listeners
        self.config_store.listen('colorspace', lambda value: self._update_gui_with_data())

    '''
    GUI building
    '''

    def _build_gui(self):
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)


        self.color_3d_plot = Plot3D(parent=self)
        self._layout.addWidget(self.color_3d_plot, stretch=2)


        self.group_stats_layout = QVBoxLayout()
        max_groups = self.config_store.get('max_groups')
        self.all_stats_views = []

        self.cbox_select_group = QComboBox(parent=self)
        self.cbox_select_group.addItems([f'Group {letter}' for letter in ascii_uppercase[:self.config_store.get('max_groups')]])
        self.cbox_select_group.addItems(['All groups'])
        self.cbox_select_group.currentIndexChanged.connect(self._click_selected_group)
        self.group_stats_layout.addWidget(self.cbox_select_group)

        for i in range(max_groups):
            group_layout = QVBoxLayout()

            group_letter = ascii_uppercase[i]
            group_layout.addWidget(QLabel(f'Group {group_letter}', parent=self))

            lst_stats_view = AlwaysShowListWidget(parent=self)
            lst_stats_view.setSelectionMode(QAbstractItemView.NoSelection)
            lst_stats_view.setSortingEnabled(False)
            self.all_stats_views += [lst_stats_view]
            group_layout.addWidget(lst_stats_view)

            self.group_stats_layout.addLayout(group_layout)

        self.ui_controls_widget = QWidget()
        self.ui_controls_widget.setLayout(self.group_stats_layout)

        self.ui_controls_scroll = QScrollArea(parent=self)
        self.ui_controls_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui_controls_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui_controls_scroll.setWidgetResizable(True)
        self.ui_controls_scroll.setWidget(self.ui_controls_widget)

        self._layout.addWidget(self.ui_controls_scroll, stretch=1)


    def _update_gui_with_data(self):
        colorspace = self.config_store.get('colorspace')

        for (i, group) in enumerate(self.data_store.all_groups):
            if group.size() > 0:
                points_avg   = tuple(group.color_mean(colorspace).round(decimals=4))
                points_stdev = tuple(group.color_stdev(colorspace).round(decimals=4))
            else:
                points_avg   = (0, 0, 0)
                points_stdev = (0, 0, 0)

            self.all_stats_views[i].clear()
            self.all_stats_views[i].addItems([
                f'Number of points: {group.size()}',
                f'Color space: {colorspace}',
                f'Average: {points_avg}',
                f'Standard Deviation: {points_stdev}'
            ])

        self.color_3d_plot.set_plot(plot=self._generate_color_3d_plot())


    def _click_selected_group(self, index):
        if index == self.data_store.num_groups():
            self.selected_group = -1
        else:
            self.selected_group = index

        self._update_gui_with_data()


    def _generate_color_3d_plot(self):
        colorspace = self.config_store.get('colorspace')

        if self.selected_group == -1:
            viewed_groups = self.data_store.all_groups
        else:
            viewed_groups = [self.data_store.all_groups[self.selected_group]]

        pos_list = []
        color_list = []
        for group in viewed_groups:
            pos_list += group.fetch_color_points(colorspace)
            color_list += group.fetch_color_points('RGB')

        if len(pos_list) == 0:
            pos_arr = np.array([[0, 0, 0]])
            color_arr = np.array([[0, 0, 0, 1]])
        else:
            pos_arr = np.array(pos_list) / 255 * COLOR_3D_PLOT_AXIS_SCALE
            color_arr = np.array(color_list) / 255

        return gl.GLScatterPlotItem(
            pos=pos_arr, color=color_arr,
            size=10, pxMode=True,
            glOptions='opaque'
        )
