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
    language = fields.Many2one('res.lang', 'Language')
    genre = fields.Many2one('tv.genre', 'Genre')
    type = fields.Many2one('tv.type', 'Channel Type')
    format = fields.Many2one('tv.format', 'Format')
    technology = fields.Many2one('tv.technology', 'Signal Reception')
    country = fields.Many2one('res.country', 'Country')


class PartnerTVChannels(models.Model):
    _inherit = 'res.partner'

    channel_ids = fields.Many2many('tv.channel')
    service_type = fields.Many2one('partner_service_type', 'Service Type')
    total_ch = fields.Integer('Total Channels', compute='_count_channels', store=True, help='Number of tv channels under the customer account')
    paid_ch = fields.Integer('Pay Channels', compute='_count_channels', store=True, help='How many pay channel')
    free_ch = fields.Integer('Free Channels', compute='_count_channels', store=True, help='How many free to air channels')

    @api.one
    @api.depends('channel_ids')
    def _count_channels(self):
        self.total_ch = len(self.channel_ids)
        self.paid_ch = len(filter(lambda x: x.type.name.lower() == 'pay', self.channel_ids))
        self.free_ch = len(filter(lambda x: x.type.name.lower() == 'fta', self.channel_ids))

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
                    genre = self.env['tv.genre'].search([('name', '=', row[2].strip())])
                    tv_type = self.env['tv.type'].search([('name', '=', row[3].strip())])
                    tv_format = self.env['tv.format'].search([('name', '=', row[4].strip())])
                    technology = self.env['tv.technology'].search([('name', '=', row[6].strip())])
                    vals = {'name': row[0].strip(),
                            'language': language.id if language else None,
                            'genre':  genre.id if genre else None,
                            'type':  tv_type.id if tv_type else None,
                            'format':  tv_format.id if tv_format else None,
                            'technology':  technology.id if technology else None,
                            'country': country.id if country else None,
                            }
                    try:
                        new_ch = channels.create(vals)
                        self.channel_ids += new_ch
                        _logger.info("New channel created: %s", new_ch.name)
                    except:
                        _logger.error("Wrong line %s in file", ind)


class TvGenre(models.Model):
    _name = 'tv.genre'
    name = fields.Char()


class TvType(models.Model):
    _name = 'tv.type'
    name = fields.Char()


class TvFormat(models.Model):
    _name = 'tv.format'
    name = fields.Char()


class TvTechnology(models.Model):
    _name = 'tv.technology'
    name = fields.Char()


class ServiceType(models.Model):
    _name = 'partner_service_type'
    name = fields.Char()

