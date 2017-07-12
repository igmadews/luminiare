# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    delivery_type = fields.Selection([
                       ('led_strip','LED Strip Delivery Order'),
                       ('led_attach','LED Attachments Delivery Order')
                     ],string="Delivery Type")
    crm_lead_id = fields.Many2one('crm.lead','Project')
    attention = fields.Char("Attention")
    
    
    def get_order_line(self,obj):
    	sale_order_pool = self.env['sale.order']
    	sale_order_ids = sale_order_pool.search([('name','=',obj.origin)])
    	order_line_list = []
    	if sale_order_ids:
    		for line in sale_order_ids.order_line:
    			order_line_list.append(line)
		return order_line_list
    
    @api.model
    def create(self, vals):
        sale_order_pool = self.env['sale.order']
        if vals.get('origin'):
        	sale_order_obj = sale_order_pool.search([('name','=',vals.get('origin'))])
        	if sale_order_obj:
        		vals.update({
        			'crm_lead_id': sale_order_obj.crm_lead_id and sale_order_obj.crm_lead_id.id or False,
        			'attention': sale_order_obj.attention,
        			'delivery_type': sale_order_obj.quote_type,
        		})
        stock_picking_obj = super(StockPicking, self).create(vals)
        return stock_picking_obj