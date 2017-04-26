# -*- coding: utf-8 -*-

from openerp import tools
from openerp import models, fields


class ChannelsVSPartners(models.Model):
    _name = "channels.vs.partners"
    _auto = False
    channel = fields.Many2one('tv.channel', string='channel', readonly=True)
    language = fields.Many2one('res.lang', string='language', readonly=True)
    partner = fields.Many2one('res.partner', string='partner', readonly=True)
    hd = fields.Boolean(string='hd', readonly=True)
    # partner = fields.Char(string='partner', readonly=True)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'channels_vs_partners')
        cr.execute("""
            create or replace view channels_vs_partners as (
            SELECT t.language, t.hd, r.tv_channel_id as id, r.tv_channel_id as channel, p.id as partner
            FROM res_partner_tv_channel_rel as r
            LEFT JOIN res_partner p ON (r.res_partner_id = p.id)
            LEFT JOIN tv_channel t ON (r.tv_channel_id = t.id)
            )
        """)
