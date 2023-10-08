from pynput import keyboard, mouse

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *

import pyqtgraph as pg
from random import randint

from src.views.qutils import bind_menu_to_actions
from src.views.widgets.record_colors_widget import RecordColorsWidget
from src.views.widgets.visualize_data_widget import VisualizeDataWidget

from src.services.config_store import ConfigStore
from src.services.screen_grabber import ScreenGrabber
from src.services.data_store import DataStore

from kink import inject


@inject
class MainWindow(QMainWindow):
    def __init__(self, config_store: ConfigStore):
        super().__init__()

        self.config_store = config_store

        # Setup UI
        self.setWindowTitle('Color Picker Analyzer')
        self.setFixedSize(QSize(1200, 800))
        self.setStyleSheet('''
            * {
                font-size: 12pt;
            }

            QLabel {
                font-size: 18pt;
            }

            QPushButton {
                font-size: 28px;
            }

            QComboBox {
                font-size: 24px;
            }
        ''')

        tabs = self._build_all_tabs()
        self.setCentralWidget(tabs)

        menu_bar = self._build_menubar()
        self.setMenuBar(menu_bar)

        # Activate listeners
        self.config_store.listen('colorspace', lambda value: self.setWindowTitle(f'Color Picker Analyzer ({value} mode)'))
        self.config_store.refresh('colorspace')


    def _build_all_tabs(self):
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(False)

        tabs.addTab(RecordColorsWidget(), 'Record')
        tabs.addTab(VisualizeDataWidget(), 'Visualize')
        tabs.currentChanged.connect(lambda index: tabs.currentWidget()._update_gui_with_data())

        return tabs


    def _build_menubar(self):
        menu_bar = QMenuBar(parent=self)
        menu_settings = QMenu('Settings', parent=self)
        menu_bar.addMenu(menu_settings)

        submenu_change_colorspace = QMenu('Change Colorspace', parent=self)
        menu_settings.addMenu(submenu_change_colorspace)

        action_select_colorspace_rgb = QAction('RGB', parent=self)
        action_select_colorspace_rgb.toggled.connect(lambda checked: self.config_store.set('colorspace', 'RGB'))

        action_select_colorspace_hsv = QAction('HSV', parent=self)
        action_select_colorspace_hsv.toggled.connect(lambda checked: self.config_store.set('colorspace', 'HSV'))

        action_select_colorspace_lab = QAction('LAB', parent=self)
        action_select_colorspace_lab.toggled.connect(lambda checked: self.config_store.set('colorspace', 'LAB'))

        bind_menu_to_actions(
            menu = submenu_change_colorspace,
            actions = [
                action_select_colorspace_rgb,
                action_select_colorspace_hsv,
                action_select_colorspace_lab,
            ],
            single_select = True,
            selected_index = self.config_store.get('selected_group'),
            parent = self
        )


        return menu_bar

