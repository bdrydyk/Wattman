"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
from pylons import config
from pylons.error import handle_mako_error

import wattman.lib.app_globals as app_globals
import wattman.lib.helpers
from wattman.config.routing import make_map

from sqlalchemy import engine_from_config
from wattman.model import init_model
import wattman.model as model
import elixir as elixir

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='wattman', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = wattman.lib.helpers

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    # Setup Elixir

    engine = engine_from_config(config, 'sqlalchemy.')
    if model.elixir.options_defaults.get('autoload'):
        # Reflected tables
        model.elixir.bind = engine
        model.metadata.bind = engine
        model.elixir.setup_all()
    else:
        # Non-reflected tables
        model.init_model(engine)


