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
    type = fields.Selection([('1', '1'),
                             ('2', '2'),
                             ('3', '3')], 'Channel Type')
    format = fields.Selection([('pal', 'PAL'), ('ntsc', 'NTSC')], 'Format')


class PartnerTVChannels(models.Model):
    _inherit = 'res.partner'

    channel_ids = fields.Many2many('tv.channel')
    service_type = fields.Selection([('direct_reception', 'Direct reception'),
                                     ('IPTV', 'IPTV'),
                                     ('OTT', 'OTT')], 'Service Type')
    customer_type = fields.Selection([('hotel', 'Hotel'),
                             ('resort', 'Resort'),
                             ('hospital', 'Hospital'),
                             ('clinic', 'Clinic'),
                             ('IPTV', 'IPTV operator'),
                             ('OTT', 'OTT operator'),
                             ('compound', 'Compound '),
                             ('private_enterprise', 'Private enterprise'),
                             ('public_organization', 'Public organization'),
                             ('MDU', 'MDU')], 'Customer Type', default='hotel')
