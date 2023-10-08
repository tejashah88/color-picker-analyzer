from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QAbstractScrollArea, QListWidget

# Modified from source: https://stackoverflow.com/a/63502112
class AlwaysShowListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def minimumSizeHint(self):
        # NOTE: We want to ensure that the contents are always shown since it'll all be underneath a parent scroll area
        return self.viewportSizeHint()

    def viewportSizeHint(self):
        if self.model().rowCount() == 0:
            return QSize(self.width(), 0)

        # NOTE: Adding a padding of 5 pixels to disable the scroll bar from showing
        height = sum(self.sizeHintForRow(i) for i in range(self.count()) if not self.item(i).isHidden()) + 5
        width = super().viewportSizeHint().width()
        return QSize(width, height)