# encoding: utf-8
from __future__ import annotations

import os
import logging
from typing import Any, Optional

from ckan.common import config
from jinja2.exceptions import TemplateNotFound

log = logging.getLogger(__name__)

_template_info_cache: dict[str, Any] = {}


def reset_template_info_cache() -> None:
    '''Reset the template cache'''
    _template_info_cache.clear()


def find_template(template_name: str) -> Optional[str]:
    ''' looks through the possible template paths to find a template
    returns the full path is it exists. '''
    template_paths = config['computed_template_paths']
    for path in template_paths:
        if os.path.exists(os.path.join(path, template_name.encode('utf-8'))):
            return os.path.join(path, template_name)
    return None


def template_type(template_path: str) -> str:
    return 'jinja2'


def template_info(template_name: str) -> tuple[str, str]:
    ''' Returns the path and type for a template '''

    if template_name in _template_info_cache:
        t_data = _template_info_cache[template_name]
        return t_data['template_path'], t_data['template_type']

    template_path = find_template(template_name)
    if not template_path:
        raise TemplateNotFound(
            template_path,
            'Template %s cannot be found' % template_name)
    t_type = template_type(template_path)

    # if in debug mode we always want to search for templates so we
    # don't want to store it.
    if not config.get('debug', False):
        t_data = {'template_path': template_path,
                  'template_type': t_type}
        _template_info_cache[template_name] = t_data
    return template_path, t_type
