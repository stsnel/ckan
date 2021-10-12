# encoding: utf-8
from __future__ import annotations

from typing import Any

import ckan.plugins as p
from ckan.types import Context, DataDict
from ckan.common import CKANConfig


ignore_empty = p.toolkit.get_validator('ignore_empty')
unicode_safe = p.toolkit.get_validator('unicode_safe')

DEFAULT_AUDIO_FORMATS: str = 'wav ogg mp3'


class AudioView(p.SingletonPlugin):
    '''This plugin makes views of audio resources, using an <audio> tag'''

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)

    def update_config(self, config: CKANConfig):
        p.toolkit.add_template_directory(config, 'theme/templates')
        self.formats = config.get(
            'ckan.preview.audio_formats',
            DEFAULT_AUDIO_FORMATS).split()

    def info(self) -> dict[str, Any]:
        return {'name': 'audio_view',
                'title': p.toolkit._('Audio'),
                'icon': 'file-audio-o',
                'schema': {'audio_url': [ignore_empty, unicode_safe]},
                'iframed': False,
                'always_available': True,
                'default_title': p.toolkit._('Audio'),
                }

    def can_view(self, data_dict: DataDict) -> bool:
        return (data_dict['resource'].get('format', '').lower()
                in self.formats)

    def view_template(self, context: Context, data_dict: DataDict) -> str:
        return 'audio_view.html'

    def form_template(self, context: Context, data_dict: DataDict) -> str:
        return 'audio_form.html'
