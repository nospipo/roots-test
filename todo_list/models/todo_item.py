from odoo import models, fields, api

class TodoItem(models.Model):
    _name = 'todo.item'
    _description = 'Todo Item'
    _order = 'sequence, id'

    name = fields.Char(string='Item Name', required=True)
    description = fields.Text(string='Description')
    is_done = fields.Boolean(string='Done')
    sequence = fields.Integer(string='Sequence', default=10)
    todo_list_id = fields.Many2one(
        'todo.list',
        string='Todo List',
        required=True,
        ondelete='cascade'
    )
    todo_list_status = fields.Selection(related='todo_list_id.status', store=True)
    
    @api.onchange('is_done')
    def _onchange_is_done(self):
        if self.is_done and self.todo_list_id.status != 'in_progress':
            self.is_done = False
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Items can only be marked as done when the list is in progress'
                }
            } 