// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  Application, IPlugin
} from '@phosphor/application';

import {
  Widget
} from '@phosphor/widgets';

import {
  IJupyterWidgetRegistry
 } from '@jupyter-widgets/base';

import {
  AstroImageModel, AstroImageView
} from './ipyfits';

import {
  EXTENSION_SPEC_VERSION
} from './version';


const EXTENSION_ID = 'jupyter.extensions.ipyfits';


/**
 * The example plugin.
 */
const ipyfitsPlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default ipyfitsPlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: 'ipyfits',
    version: EXTENSION_SPEC_VERSION,
    exports: {
      AstroImageModel: AstroImageModel,
      AstroImageView: AstroImageView
    }
  });
}
