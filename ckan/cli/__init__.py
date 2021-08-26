# encoding: utf-8

import os
from typing import Any, Dict, Optional, cast

import click
import logging
from logging.config import fileConfig as loggingFileConfig
from configparser import ConfigParser

from ckan.exceptions import CkanConfigurationException
from ckan.types import Config

log = logging.getLogger(__name__)


class CKANConfigLoader(object):
    config: Config
    config_file: str
    parser: ConfigParser
    section: str

    def __init__(self, filename: str) -> None:
        self.config_file = filename.strip()
        self.config = dict()
        self.parser = ConfigParser()
        # Preserve case in config keys
        self.parser.optionxform = lambda optionstr: str(optionstr)
        self.section = u'app:main'
        defaults = dict(
            (k, v) for k, v in os.environ.items()
            if k.startswith("CKAN_"))
        defaults['__file__'] = os.path.abspath(self.config_file)
        self._update_defaults(defaults)
        self._create_config_object()

    def _update_defaults(self, new_defaults: Dict[str, Any]) -> None:
        for key, value in new_defaults.items():
            # type_ignore_reason: using implementation details
            self.parser._defaults[key] = value  # type: ignore

    def _read_config_file(self, filename: str) -> None:
        defaults = {u'here': os.path.dirname(os.path.abspath(filename))}
        self._update_defaults(defaults)
        self.parser.read(filename)

    def _update_config(self) -> None:
        options = self.parser.options(self.section)
        for option in options:
            if option not in self.config or option in self.parser.defaults():
                value = self.parser.get(self.section, option)
                self.config[option] = value
                if option in self.parser.defaults():
                    global_conf = self.config[u'global_conf']
                    assert isinstance(global_conf, dict)
                    global_conf[option] = value

    def _create_config_object(self) -> None:
        use_config_path = self.config_file
        self._read_config_file(use_config_path)

        # # The global_config key is to keep compatibility with Pylons.
        # # It can be safely removed when the Flask migration is completed.
        self.config[u'global_conf'] = cast(
            Dict[str, Any], self.parser.defaults()).copy()

        self._update_config()

        loaded_files = [use_config_path]

        while True:
            schema, path = self.parser.get(self.section, u'use').split(u':')
            if schema == u'config':
                use_config_path = os.path.join(
                    os.path.dirname(os.path.abspath(use_config_path)), path)
                # Avoid circular references
                if use_config_path in loaded_files:
                    chain = ' -> '.join(loaded_files + [use_config_path])
                    raise CkanConfigurationException(
                        'Circular dependency located in '
                        f'the configuration chain: {chain}'
                    )
                loaded_files.append(use_config_path)

                self._read_config_file(use_config_path)
                self._update_config()
            else:
                break
        log.debug(
            u'Loaded configuration from the following files: %s',
            loaded_files
        )

    def get_config(self) -> Config:
        return self.config.copy()


def error_shout(exception: Any) -> None:
    click.secho(str(exception), fg=u'red', err=True)


def load_config(ini_path: Optional[str] = None) -> Config:
    if ini_path:
        if ini_path.startswith(u'~'):
            ini_path = os.path.expanduser(ini_path)
        filename: Optional[str] = os.path.abspath(ini_path)
        config_source = [u'-c parameter']
    elif os.environ.get(u'CKAN_INI'):
        filename = os.environ[u'CKAN_INI']
        config_source = [u'$CKAN_INI']
    else:
        # deprecated method since CKAN 2.9
        default_filenames = [u'ckan.ini', u'development.ini']
        config_source = default_filenames
        filename = None
        for default_filename in default_filenames:
            check_file = os.path.join(os.getcwd(), default_filename)
            if os.path.exists(check_file):
                filename = check_file
                break
        if not filename:
            # give really clear error message for this common situation
            msg = u'''
ERROR: You need to specify the CKAN config (.ini) file path.

Use the --config parameter or set environment variable CKAN_INI
or have one of {} in the current directory.'''
            msg = msg.format(u', '.join(default_filenames))
            raise CkanConfigurationException(msg)

    if not filename or not os.path.exists(filename):
        msg = u'Config file not found: %s' % filename
        msg += u'\n(Given by: %s)' % config_source
        raise CkanConfigurationException(msg)

    config_loader = CKANConfigLoader(filename)
    loggingFileConfig(filename)
    log.info(u'Using configuration file {}'.format(filename))

    return config_loader.get_config()
