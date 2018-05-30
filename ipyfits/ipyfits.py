#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Matt Craig.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import Image
from traitlets import Unicode
from ._version import EXTENSION_SPEC_VERSION

module_name = "ipyfits"


class AstroImageWidget(Image):
    """TODO: Add docstring here
    """
    # _model_name = Unicode('AstroImageModel').tag(sync=True)
    # _model_module = Unicode(module_name).tag(sync=True)
    # _model_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)
    # _view_name = Unicode('AstroImageView').tag(sync=True)
    # _view_module = Unicode(module_name).tag(sync=True)
    # _view_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)

    def __init__(self, *args, **kwargs):
        # Check for widget-specific arguments
        backend = kwargs.pop('backend', 'ginga')
        fits_specifier = kwargs.pop('fits_specifier', None)

        # then call super
        super().__init__(*args, **kwargs)

        if backend == 'ginga':
            from ginga.misc.log import get_logger
            logger = get_logger("my viewer", log_stderr=False, log_file='/tmp/ginga.log', level=0)

            from ginga.web.jupyterw.ImageViewJpw import EnhancedCanvasView
            v1 = EnhancedCanvasView(logger=logger)
            # ginga insists that a width and height be set, so make sure we
            # have one.
            self.width = self.width or '500'
            self.height = self.height or '500'

            # set our linkage between the jupyter widget at ginga
            v1.set_widget(self)

            # enable all possible keyboard and pointer operations
            bd = v1.get_bindings()
            bd.enable_all(True)
            v1.load_fits(fits_specifier)
