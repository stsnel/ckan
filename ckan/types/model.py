# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from typing_extensions import TypeAlias

from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.orm import Query

if TYPE_CHECKING:
    import ckan.model as _model  # noqa


AlchemySession = ScopedSession
Query = Query
Model: TypeAlias = "_model"
