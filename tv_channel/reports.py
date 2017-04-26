# -*- coding: utf-8 -*-

from openerp import tools
from openerp import models, fields


class ChannelsVSPartners(models.Model):
    _name = "channels.vs.partners"
    _auto = False
    channel = fields.Many2one('tv.channel', string='Channel', readonly=True)
    partner = fields.Char(string='Partners', readonly=True)
    # qty = fields.Integer(string='Quantity', readonly=True)
    language = fields.Many2one('res.lang', 'Language')
    genre = fields.Char(string='Genre')
    type = fields.Char(string='Type')
    format = fields.Char(string='Format')
    technology = fields.Char(string='Technology')
    country = fields.Char(string='Country')

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'channels_vs_partners')
        cr.execute("""
            create or replace view channels_vs_partners as (
           	SELECT 
		        row_number() over (order by p.name nulls last) as id,
                r.tv_channel_id as channel, 
                p.name as partner, 
                t.language,
                t.genre,
                t.type,
                t.format,
                t.technology,
                c.name as country
            FROM res_partner_tv_channel_rel as r
            LEFT JOIN res_partner p ON (r.res_partner_id = p.id)
            LEFT JOIN tv_channel t ON (r.tv_channel_id = t.id)
            LEFT JOIN res_country c ON (t.country = c.id)
           order by channel
            )
        """)
