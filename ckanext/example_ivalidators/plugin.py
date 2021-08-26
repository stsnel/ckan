# encoding: utf-8

from typing import Any, Dict
from ckan.types import Validator
import six


from ckan.plugins.toolkit import Invalid
from ckan import plugins


class ExampleIValidatorsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IValidators)

    def get_validators(self) -> Dict[str, Validator]:
        return {
            u'equals_fortytwo': equals_fortytwo,
            u'negate': negate,
            u'unicode_only': unicode_please,
        }


def equals_fortytwo(value: Any):
    if value != 42:
        raise Invalid(u'not 42')
    return value


def negate(value: Any):
    return -value


def unicode_please(value: Any):
    if isinstance(value, bytes):
        try:
            return six.ensure_text(value)
        except UnicodeDecodeError:
            return value.decode(u'cp1252')
    return str(value)
