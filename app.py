import argparse
from kink import di

from src.services.config_store import ConfigStore
from src.services.screen_grabber import ScreenGrabber
from src.services.data_store import DataStore

from PySide6.QtWidgets import QApplication
from src.views.main_window import MainWindow

if __name__ == '__main__':
    # Parse args
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-g', '--groups', type=int, default=3, help='Number of groups')

    args = arg_parser.parse_args()
    num_groups = args.groups

    # Initialize services
    di['config_store'] = lambda di: ConfigStore({
        'colorspace': 'RGB',
        'max_groups': num_groups,
        'selected_group': 0
    })
    di['screen_grabber'] = lambda di: ScreenGrabber()
    di['data_store'] = lambda di: DataStore(max_groups = di['config_store'].get('max_groups'))


    # Start new QT application
    app = QApplication([])

    # Build main GUI and show it
    window = MainWindow()
    window.show()

    # Start event loop
    app.exec()