# encoding: utf-8

from typing import Any, Dict

import ckan.plugins as p
from ckan.types import Context
from ckan.common import CKANConfig


ignore_empty = p.toolkit.get_validator('ignore_empty')
unicode_safe = p.toolkit.get_validator('unicode_safe')

DEFAULT_VIDEO_FORMATS = 'mp4 ogg webm'


class VideoView(p.SingletonPlugin):
    '''This plugin makes views of video resources, using a <video> tag'''

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)

    def update_config(self, config: CKANConfig):
        p.toolkit.add_template_directory(config, 'theme/templates')
        self.formats = config.get(
            'ckan.preview.video_formats',
            DEFAULT_VIDEO_FORMATS).split()

    def info(self) -> Dict[str, Any]:
        return {'name': 'video_view',
                'title': p.toolkit._('Video'),
                'icon': 'file-video-o',
                'schema': {'video_url': [ignore_empty, unicode_safe],
                           'poster_url': [ignore_empty, unicode_safe]},
                'iframed': False,
                'always_available': True,
                'default_title': p.toolkit._('Video'),
                }

    def can_view(self, data_dict: Dict[str, Any]):
        return (data_dict['resource'].get('format', '').lower()
                in self.formats)

    def view_template(self, context: Context, data_dict: Dict[str, Any]):
        return 'video_view.html'

    def form_template(self, context: Context, data_dict: Dict[str, Any]):
        return 'video_form.html'
