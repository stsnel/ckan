# encoding: utf-8

"""SQLAlchemy Metadata and Session object"""
from typing import Any, Optional
from sqlalchemy import MetaData, event
import sqlalchemy.orm as orm
from sqlalchemy.engine import Engine

import ckan.model.extension as extension
from ckan.types import AlchemySession

__all__ = ['Session', 'engine_is_sqlite', 'engine_is_pg']


# SQLAlchemy database engine. Updated by model.init_model()
engine: Optional[Engine] = None


Session: AlchemySession = orm.scoped_session(orm.sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    extension=[extension.PluginSessionExtension(),],
))


create_local_session = orm.sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    extension=[extension.PluginSessionExtension(),],
)


@event.listens_for(create_local_session, 'before_flush')
@event.listens_for(Session, 'before_flush')
def ckan_before_flush(session: Any, flush_context: Any, instances: Any):
    """ Create a new _object_cache in the Session object.

    _object_cache is used in DomainObjectModificationExtension to trigger
    notifications on changes. e.g: re-indexing a package in solr upon update.
    """
    if not hasattr(session, '_object_cache'):
        session._object_cache= {'new': set(),
                                'deleted': set(),
                                'changed': set()}

    changed = [obj for obj in session.dirty if
        session.is_modified(obj, include_collections=False, passive=True)]

    session._object_cache['new'].update(session.new)
    session._object_cache['deleted'].update(session.deleted)
    session._object_cache['changed'].update(changed)

@event.listens_for(create_local_session, 'after_commit')
@event.listens_for(Session, 'after_commit')
def ckan_after_commit(session: Any):
    """ Cleans our custom _object_cache attribute after commiting.
    """
    if hasattr(session, '_object_cache'):
        del session._object_cache

@event.listens_for(create_local_session, 'before_commit')
@event.listens_for(Session, 'before_commit')
def ckan_before_commit(session: Any):
    session.flush()
    try:
        session._object_cache
    except AttributeError:
        return

@event.listens_for(create_local_session, 'after_rollback')
@event.listens_for(Session, 'after_rollback')
def ckan_after_rollback(session: Any):
    """ Cleans our custom _object_cache attribute after rollback.
    """
    if hasattr(session, '_object_cache'):
        del session._object_cache


#mapper = Session.mapper
mapper = orm.mapper

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()


def engine_is_sqlite(sa_engine: Optional[Engine]=None) -> bool:
    # Returns true iff the engine is connected to a sqlite database.
    e = sa_engine or engine
    assert e
    return e.engine.url.drivername == 'sqlite'


def engine_is_pg(sa_engine: Optional[Engine]=None) -> bool:
    # Returns true iff the engine is connected to a postgresql database.
    # According to http://docs.sqlalchemy.org/en/latest/core/engines.html#postgresql
    # all Postgres driver names start with `postgres`
    e = sa_engine or engine
    assert e
    return e.engine.url.drivername.startswith('postgres')
