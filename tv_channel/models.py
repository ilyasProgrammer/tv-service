# -*- coding: utf-8 -*-

from openerp import models, fields, api


class TVChannel(models.Model):
    _name = 'tv.channel'

    name = fields.Char()
    language = fields.Many2one('res.lang', 'Language')
    genre = fields.Selection([('sport', 'Sport'),
                              ('music', 'Music'),
                              ('movie', 'Movie'),
                              ('games', 'Games'),
                              ('news', 'News')], 'Genre')
    type = fields.Selection([('1', '1'), ('2', '2')], 'Type')
    format = fields.Selection([('pal', 'PAL'), ('ntsc', 'NTSC')], 'Format')
