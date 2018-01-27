// Copyright (c) Matt Craig.
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView
} from '@jupyter-widgets/base';

import {
  ImageModel, ImageView
} from '@jupyter-widgets/controls';

import {
  JUPYTER_EXTENSION_VERSION
} from './version';


export
class AstroImageModel extends ImageModel {
  defaults() {
    return {...super.defaults(),
      _model_name: AstroImageModel.model_name,
      _model_module: AstroImageModel.model_module,
      _model_module_version: AstroImageModel.model_module_version,
      _view_name: AstroImageModel.view_name,
      _view_module: AstroImageModel.view_module,
      _view_module_version: AstroImageModel.view_module_version,
    };
  }

  static serializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'AstroImageModel';
  static model_module = 'ipyfits';
  static model_module_version = JUPYTER_EXTENSION_VERSION;
  static view_name = 'AstroImageView';  // Set to null if no view
  static view_module = 'ipyfits';   // Set to null if no view
  static view_module_version = JUPYTER_EXTENSION_VERSION;
}


export
class AstroImageView extends ImageView {
  render() {
    super.render()
    this.update()
  }

  _click_location_original_image(event: MouseEvent) {
      // Calculate the location in image units.
      // Works for ipywidgets.Image
      var pad_left = parseInt(this.el.style.paddingLeft || '') || 0;
      var border_left = parseInt(this.el.style.borderLeft || '') || 0;
      var pad_top = parseInt(this.el.style.paddingTop || '') || 0;
      var border_top = parseInt(this.el.style.borderTop || '') || 0;

      var bounding_rect = this.el.getBoundingClientRect();
      var y_offset = bounding_rect.top;
      var x_offset = bounding_rect.left;
      var relativeX = Math.round(event.clientX - x_offset)
      var relativeY = Math.round(event.clientY - y_offset)

      var relative_click_x = relativeX - border_left - pad_left;
      var relative_click_y = relativeY - border_top - pad_top;
      var image_x = Math.round(relative_click_x / this.el.width * this.el.naturalWidth);
      var image_y = Math.round(relative_click_y / this.el.height * this.el.naturalHeight);
      return {x: image_x, y: image_y}
  }

  _array_xy(event: MouseEvent) {
    console.log('I am in ipyfits _array_xy')
    return this._click_location_original_image(event)
  }
}
