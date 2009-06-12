"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm, schema, types, func
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_, select
from wattman.model import meta
#all elixer stuff below - might change - using bel-epa.com guide
import elixir


Session = elixir.session = meta.Session
metadata = elixir.metadata

elixir.options_defaults.update(dict(shortnames=True, inheritance='multi', polymorphic=True))

from entities import *

# this will be called in config/environment.py
def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    elixir.session.configure(bind=engine)
    metadata.bind = engine

    if elixir.options_defaults.get('autoload', False) and not metadata.is_bound():
        elixir.delay_setup = True

    if not elixir.options_defaults.get('autoload', False):
        elixir.setup_all(True)

