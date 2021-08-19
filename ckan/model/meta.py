# encoding: utf-8

from typing import Any, Optional

"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
import sqlalchemy.orm as orm
from sqlalchemy.orm.session import SessionExtension  # type: ignore
from sqlalchemy.engine import Engine

import ckan.model.extension as extension
from ckan.types import AlchemySession

__all__ = ['Session', 'engine_is_sqlite', 'engine_is_pg']


class CkanSessionExtension(SessionExtension):  # type: ignore

    def before_flush(self, session: Any, flush_context: Any, instances: Any):
        if not hasattr(session, '_object_cache'):
            session._object_cache= {'new': set(),
                                    'deleted': set(),
                                    'changed': set()}

        changed = [obj for obj in session.dirty if
            session.is_modified(obj, include_collections=False, passive=True)]

        session._object_cache['new'].update(session.new)
        session._object_cache['deleted'].update(session.deleted)
        session._object_cache['changed'].update(changed)


    def before_commit(self, session: Any):
        session.flush()
        try:
            obj_cache = session._object_cache
        except AttributeError:
            return

    def after_commit(self, session: Any):
        if hasattr(session, '_object_cache'):
            del session._object_cache

    def after_rollback(self, session: Any):
        if hasattr(session, '_object_cache'):
            del session._object_cache

# __all__ = ['Session', 'engine', 'metadata', 'mapper']

# SQLAlchemy database engine. Updated by model.init_model()
engine: Optional[Engine] = None

Session: AlchemySession = orm.scoped_session(orm.sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    extension=[CkanSessionExtension(),
               extension.PluginSessionExtension(),
    ],
))

create_local_session = orm.sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    extension=[CkanSessionExtension(),
               extension.PluginSessionExtension(),
    ],
)

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
