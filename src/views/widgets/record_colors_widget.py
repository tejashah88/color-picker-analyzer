from string import ascii_uppercase
from kink import inject

from PySide6.QtWidgets import *

from pynput import keyboard, mouse

from src.services.screen_grabber import ScreenGrabber
from src.services.data_store import DataStore
from src.services.config_store import ConfigStore

from src.views.qutils import WidgetDataUpdateMixin

@inject
class RecordColorsWidget(QWidget, WidgetDataUpdateMixin):
    def __init__(self, config_store: ConfigStore, screen_grabber: ScreenGrabber, data_store: DataStore):
        super().__init__()

        self.config_store = config_store
        self.screen_grabber = screen_grabber
        self.data_store = data_store

        self.keyboard_listener = None
        self.mouse_listener = None

        # Setup UI
        self._build_gui()
        self._update_gui_with_data()

        # Activate listeners
        self.config_store.listen('colorspace', lambda value: self._update_gui_with_data())

    '''
    GUI building
    '''

    def _build_gui(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.cbox_select_group = QComboBox(parent=self)
        self.cbox_select_group.addItems([f'Group {letter}' for letter in ascii_uppercase[:self.config_store.get('max_groups')]])
        self.cbox_select_group.currentIndexChanged.connect(self._click_selected_group)
        self._layout.addWidget(self.cbox_select_group)


        self._layout.addWidget(QLabel('Statistics', parent=self))

        self.lst_stats_view = QListWidget(parent=self)
        self.lst_stats_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.lst_stats_view.setSortingEnabled(False)
        self._layout.addWidget(self.lst_stats_view)


        self._layout.addWidget(QLabel('Raw Data', parent=self))

        self.lst_raw_points_view = QListWidget(parent=self)
        self.lst_raw_points_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.lst_raw_points_view.setSortingEnabled(False)
        self._layout.addWidget(self.lst_raw_points_view)

        self.btn_record_points = QPushButton('Start Recording', parent=self)
        self.btn_record_points.setFixedHeight(40)
        self.btn_record_points.clicked.connect(self._click_record_colors)
        self._layout.addWidget(self.btn_record_points)

        self.btn_clear_data = QPushButton('Clear Data', parent=self)
        self.btn_clear_data.setFixedHeight(40)
        self.btn_clear_data.clicked.connect(self._click_clear_data)
        self._layout.addWidget(self.btn_clear_data)


    def _update_gui_with_data(self):
        colorspace = self.config_store.get('colorspace')
        current_group = self.data_store.active_group

        if current_group.size() > 0:
            points_avg   = tuple(current_group.color_mean(colorspace).round(decimals=4))
            points_stdev = tuple(current_group.color_stdev(colorspace).round(decimals=4))
        else:
            points_avg   = (0, 0, 0)
            points_stdev = (0, 0, 0)

        self.lst_stats_view.clear()
        self.lst_stats_view.addItems([
            f'Number of points: {current_group.size()}',
            f'Color space: {colorspace}',
            f'Average: {points_avg}',
            f'Standard Deviation: {points_stdev}'
        ])

        self.lst_raw_points_view.clear()
        self.lst_raw_points_view.addItems([str(color) for color in current_group.colors])


    def _start_input_listeners(self):
        self.keyboard_listener = keyboard.Listener(on_release = self._event_on_key_esc_release)
        self.mouse_listener = mouse.Listener(on_click = self._event_on_mouse_click)

        self.keyboard_listener.start()
        self.mouse_listener.start()


    def _stop_input_listeners(self):
        if self.mouse_listener is not None and self.mouse_listener.running:
            self.mouse_listener.stop()

        if self.keyboard_listener is not None and self.keyboard_listener.running:
            self.keyboard_listener.stop()

    '''
    Event handlers
    '''

    def _click_selected_group(self, index):
        self.data_store.switch_group(index)
        self._update_gui_with_data()


    def _click_record_colors(self):
        self.btn_record_points.setText('Recording! Press ` (tilde key) to stop recording...')
        self.btn_record_points.setEnabled(False)
        self._start_input_listeners()


    def _click_clear_data(self):
        self._stop_input_listeners()

        self.btn_record_points.setText('Start Recording')
        self.btn_record_points.setEnabled(True)

        self.data_store.active_group.clear()
        self._update_gui_with_data()


    def _event_on_mouse_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            color_pixel = self.screen_grabber.grab_color_pixel(x, y)
            self.data_store.active_group.add_color_pixel(color_pixel)
            self._update_gui_with_data()


    def _event_on_key_esc_release(self, key):
        if key == keyboard.KeyCode.from_char('`'):
            self.mouse_listener.stop()
            self.keyboard_listener.stop()

            self.btn_record_points.setText('Start Recording')
            self.btn_record_points.setEnabled(True)
            return False


    # NOTE: Overriding default handler from QWidget
    def closeEvent(self, event):
        # Check if mouse and keyboard listeners are initialized and running, and stop them if necessary
        self._stop_input_listeners()
        event.accept()