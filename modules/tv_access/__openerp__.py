# -*- coding: utf-8 -*-
{
    'name': "tv_access",
    'summary': """acces groups and rules for all needed models""",
    'description': """tv_access""",
    'author': "Ilyas",
    'website': "https://github.com/ilyasProgrammer",
    'category': 'Custom',
    'version': '1.1',
    'depends': ['tv_channel',
                'sale',
                'project',
                'purchase',
                'hr',
                ],
    'external_dependencies': {},
    'data': [
        'security/tv_security.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
