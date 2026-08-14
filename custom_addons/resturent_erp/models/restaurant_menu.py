from odoo import models, fields 

class RestaurantMenuItem(models.Model):
    _name = "restaurant.menu.item"
    _description = "Restaurant Menu Item"

    name = fields.Char(string='Item Name', required=True)
    category = fields.Selection([
        ('starter', 'Starter'), 
        ('main_course', 'Main Course'), 
        ('fast_food', 'Fast Food'), 
        ('dessert', 'Dessert'), 
        ('beverage', 'Beverage')
    ], string='Category', required=True, default='main_course')
    price = fields.Float(string='Price', required=True)
    available = fields.Boolean(string="Available", default=True)
