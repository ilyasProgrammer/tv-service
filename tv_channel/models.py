# -*- coding: utf-8 -*-

from openerp import models, fields, api
from os.path import expanduser
import csv
from Tkinter import Tk
from tkFileDialog import askopenfilename
import logging

_logger = logging.getLogger(__name__)


class TVChannel(models.Model):
    _name = 'tv.channel'

    name = fields.Char()
    # free = fields.Boolean('Free channel', default=True)
    # hd = fields.Boolean('HD channel', default=True)
    language = fields.Many2one('res.lang', 'Language')
    genre = fields.Selection([('sport', 'Sport'),
                              ('music', 'Music'),
                              ('movie', 'Movie'),
                              ('games', 'Games'),
                              ('family', 'Family'),
                              ('kids', 'Kids'),
                              ('religious', 'Religious'),
                              ('drama', 'Drama'),
                              ('news', 'News')], 'Genre')
    type = fields.Selection([('fta', 'FTA'),
                             ('pay', 'Pay')], 'Channel Type')
    format = fields.Selection([('sd', 'SD'), ('hd', 'HD')], 'Format')
    technology = fields.Selection([('analog', 'Analog'), ('iptv', 'IPTV')], 'Technology')
    country = fields.Many2one('res.country', 'Country')


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
    total_ch = fields.Integer('Total Channels', compute='_count_channels', store=True, help='Number of tv channels under the customer account')
    paid_ch = fields.Integer('Pay Channels', compute='_count_channels', store=True, help='How many pay channel')
    free_ch = fields.Integer('Free Channels', compute='_count_channels', store=True, help='How many free to air channels')

    @api.one
    @api.depends('channel_ids')
    def _count_channels(self):
        self.total_ch = len(self.channel_ids)
        self.paid_ch = len(filter(lambda x: x.type == 'pay', self.channel_ids))
        self.free_ch = len(filter(lambda x: x.type == 'fta', self.channel_ids))

    @api.one
    def load_channels(self):
        root = Tk()
        root.withdraw()
        home = expanduser("~")
        channels = self.env['tv.channel']
        filename = askopenfilename(initialdir=home)
        root.destroy()
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for ind, row in enumerate(spamreader):
                if ind == 0:
                    continue
                found = channels.search([('name', '=', row[0].strip())], limit=1)
                if len(found):
                    self.channel_ids += found
                else:
                    language = self.env['res.lang'].search([('name', '=', row[1].strip())])
                    country = self.env['res.country'].search([('name', '=', row[5].strip())])
                    vals = {'name': row[0].strip(),
                            'language': language.id if language else None,
                            'genre': row[2].strip().lower(),
                            'type': row[3].strip().lower(),
                            'format': row[4].strip().lower(),
                            'technology': row[6].strip().lower(),
                            'country': country.id if country else None,
                            }
                    try:
                        new_ch = channels.create(vals)
                        self.channel_ids += new_ch
                        _logger.info("New channel created: %s", new_ch.name)
                    except:
                        _logger.error("Wrong line %s in file", ind)
