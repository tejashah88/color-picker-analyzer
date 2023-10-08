# Modified from https://github.com/tejashah88/image-clusterduck/blob/archived/src/components/plot_3d.py

from pyqtgraph.Qt import QtGui
import pyqtgraph.opengl as gl

from src.views.components.colored_gl_axis_item import ColoredGLAxisItem
from src.views.components.gl_3d_grid_item import GL3DGridItem

DEFAULT_AXIS_LENGTH = 4
DEFAULT_GRID_LENGTH = 4
DEFAULT_GRID_SPACING = 0.25

class Plot3D(gl.GLViewWidget):
    def __init__(self, plot=None, enable_grid=True, enable_axes=True, grid_length=DEFAULT_GRID_LENGTH, axis_length=DEFAULT_AXIS_LENGTH, *args, **kwargs):
        # Create and initialize 3D plotting widget
        super().__init__(*args, **kwargs)

        # Create vars for the grid, axes and 3d plot items
        self.grid_item = None
        self.axes_item = None
        self.plt_item = None
        self.cplt_item = None

        if enable_grid:
            self.enable_grid(grid_length)

        if enable_axes:
            self.enable_axes(axis_length)

        if plot is not None:
            self.set_plot(plot)

        self.setBackgroundColor('white')


    def set_plot(self, plot):
        if self.plt_item is not None:
            self.plt_item.setData(pos=plot.pos, color=plot.color)
        else:
            self.plt_item = plot
            self.addItem(self.plt_item)


    def enable_axes(self, axis_length=DEFAULT_AXIS_LENGTH):
        if self.axes_item is None:
            # x = blue, y = yellow, z = green
            self.axes_item = ColoredGLAxisItem(size=QtGui.QVector3D(1, 1, 1) * axis_length)
            self.addItem(self.axes_item)


    def set_axis_length(self, axis_length):
        if self.axes_item is not None:
            self.axes_item.setSize(x=axis_length, y=axis_length, z=axis_length)


    def disable_axes(self):
        if self.axes_item is not None:
            self.removeItem(self.axes_item)
            self.axes_item = None


    def enable_grid(self, grid_axis_length=DEFAULT_GRID_LENGTH, grid_spacing=DEFAULT_GRID_SPACING):
        if self.grid_item is None:
            self.grid_item = GL3DGridItem()
            self.grid_item.setSize(x=grid_axis_length, y=grid_axis_length, z=grid_axis_length)
            self.grid_item.setSpacing(x=grid_spacing, y=grid_spacing, z=grid_spacing)
            self.addItem(self.grid_item)


    def set_grid_length(self, grid_axis_length):
        if self.grid_item is not None:
            self.grid_item.setSize(x=grid_axis_length, y=grid_axis_length, z=grid_axis_length)


    def set_grid_spacing(self, grid_spacing):
        if self.grid_item is not None:
            self.grid_item.setSpacing(x=grid_spacing, y=grid_spacing, z=grid_spacing)


    def disable_grid(self):
        if self.grid_item is not None:
            self.removeItem(self.grid_item)
            self.grid_item = None
