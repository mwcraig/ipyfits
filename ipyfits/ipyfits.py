#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Matt Craig.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import Image, VBox, HTML
from astropy.coordinates import Angle
import numpy as np

module_name = "ipyfits"


class AstroImageWidget(VBox):
    """
    Display an astronomical image in as a Jupyter widget.
    """

    def __init__(self, *args, **kwargs):
        # Check for widget-specific arguments
        backend = kwargs.pop('backend', 'ginga')
        fits_specifier = kwargs.pop('fits_specifier', None)
        show_cursor_location = kwargs.pop('show_cursor_location', True)

        # then call super
        super().__init__(*args, **kwargs)

        # This should always be defined.
        self._ginga_viewer = None

        if backend == 'ginga':
            from ginga.web.jupyterw.ImageViewJpw import EnhancedCanvasView
            v1 = EnhancedCanvasView()
            # ginga insists that a width and height be set, so make sure we
            # have one.
            self._image = Image()
            children = [self._image]

            self._image.width = self._image.width or '500'
            self._image.height = self._image.height or '500'

            # set our linkage between the jupyter widget at ginga
            v1.set_widget(self._image)

            # enable all possible keyboard and pointer operations
            bd = v1.get_bindings()
            bd.enable_all(True)
            v1.load_fits(fits_specifier)
            self._ginga_viewer = v1
            self._file = fits_specifier

            if show_cursor_location:
                self._coord_display = HTML(value='Cursor position')
                children.append(self._coord_display)
                self._ginga_viewer.add_callback('cursor-changed',
                                                self._update_cursor_display)
            self.children = children

    @property
    def ginga_viewer(self):
        return self._ginga_viewer

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._ginga_viewer.load_fits(value)

    def show(self):
        return self._ginga_viewer.show()

    def _update_cursor_display(self, viewer, button, data_x, data_y):
        image = viewer.get_image()
        if image is not None:
            ra, dec = image.pixtoradec(data_x, data_y)
            display = f'({data_x:.2f}, {data_y:.2f}) px'
            if 'WCSAXES' in image.get_header():
                world_display = f'({ra:.5f}, {dec:.5f}) degrees'
                display += ', ' + world_display
                ra_d = Angle(ra, unit='degree')
                dec_d = Angle(dec, unit='degree')
                world_d = f'({ra_d.to_string(unit="hour", precision=2)}, '
                world_d += f'{dec_d.to_string(precision=2)})'
                display += ', ' + world_d
            # Get the pixel value
            pixel_value = image.get_data_xy(int(np.round(data_x)),
                                            int(np.round(data_y)))
            display += f' Value: {pixel_value:.2f}'
            self._coord_display.value = display
        else:
            self._coord_display.value = 'WTF'
