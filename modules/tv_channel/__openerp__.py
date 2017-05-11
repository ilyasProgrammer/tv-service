# -*- coding: utf-8 -*-
{
    'name': "tv_channel",
    'summary': """TV service""",
    'description': """TV service""",
    'author': "Ilyas",
    'website': "https://github.com/ilyasProgrammer",
    'category': 'Custom',
    'version': '1.1',
    'depends': ['contacts'],
    'external_dependencies': {"python": ['Tkinter']},
    # sudo apt-get install python-tk
    'data': [
        # 'data.xml',
        'views/channel.xml',
        'views/contacts_view_alter.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
