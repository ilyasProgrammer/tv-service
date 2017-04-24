# -*- coding: utf-8 -*-

from openerp import models, fields, api
from os.path import expanduser
import csv
from Tkinter import Tk
from tkFileDialog import askopenfilename


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

    @api.one
    def load_channels(self):
        root = Tk()
        root.withdraw()
        home = expanduser("~")
        channels = self.env['tv.channel']
        filename = askopenfilename(initialdir=home)
        root.destroy()
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar=',')
            for row in spamreader:
                found = channels.search([('name', '=', row[0].strip())], limit=1)
                if len(found):
                    self.channel_ids += found
