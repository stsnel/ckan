# encoding: utf-8


import ckan.plugins as p
from ckan.config.declaration import Declaration, Key


ignore_empty = p.toolkit.get_validator('ignore_empty')
unicode_safe = p.toolkit.get_validator('unicode_safe')


class VideoView(p.SingletonPlugin):
    '''This plugin makes views of video resources, using a <video> tag'''

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.IConfigDeclaration)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'theme/templates')
        self.formats = config.get_value('ckan.preview.video_formats').split()

    def info(self):
        return {'name': 'video_view',
                'title': p.toolkit._('Video'),
                'icon': 'file-video-o',
                'schema': {'video_url': [ignore_empty, unicode_safe],
                           'poster_url': [ignore_empty, unicode_safe]},
                'iframed': False,
                'always_available': True,
                'default_title': p.toolkit._('Video'),
                }

    def can_view(self, data_dict):
        return (data_dict['resource'].get('format', '').lower()
                in self.formats)

    def view_template(self, context, data_dict):
        return 'video_view.html'

    def form_template(self, context, data_dict):
        return 'video_form.html'

    # IConfigDeclaration

    def declare_config_options(self, declaration: Declaration, key: Key):
        declaration.annotate("video_view settings")
        declaration.declare(key.ckan.preview.video_formats, "mp4 ogg webm")
