from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Todo Name', required=True, tracking=True)
    tags = fields.Many2many('todo.tags', string='Tags', tracking=True)
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', required=True, tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete')
    ], string='Status', default='draft', tracking=True)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='Assigned To', default=lambda self: self.env.user)
    
    todo_item_ids = fields.One2many(
        'todo.item',
        'todo_list_id',
        string='Todo Items'
    )
    
    participant_ids = fields.Many2many(
        'res.users',
        string='Participants',
        tracking=True
    )
    
    is_locked = fields.Boolean(
        string='Locked',
        compute='_compute_is_locked',
        store=True
    )
    
    all_items_done = fields.Boolean(
        string='All Items Done',
        compute='_compute_all_items_done',
        store=True
    )

    progress = fields.Float(
        string='Progress',
        compute='_compute_progress',
        store=True,
        group_operator='avg'
    )

    color = fields.Integer(
        string='Color Index',
        compute='_compute_color'
    )

    todo_item_count = fields.Integer(
        string='Todo Items',
        compute='_compute_todo_item_count'
    )

    completed_item_count = fields.Integer(
        string='Completed Items',
        compute='_compute_completed_item_count'
    )
    
    @api.depends('status')
    def _compute_is_locked(self):
        for record in self:
            record.is_locked = record.status == 'complete'
    
    @api.depends('todo_item_ids.is_done')
    def _compute_all_items_done(self):
        for record in self:
            record.all_items_done = all(item.is_done for item in record.todo_item_ids) if record.todo_item_ids else False

    @api.depends('todo_item_ids.is_done')
    def _compute_progress(self):
        for record in self:
            if record.todo_item_ids:
                done_items = sum(1 for item in record.todo_item_ids if item.is_done)
                total_items = len(record.todo_item_ids)
                record.progress = (done_items / total_items) * 100
            else:
                record.progress = 0.0

    def _compute_color(self):
        for record in self:
            if record.status == 'draft':
                record.color = 0  # Default color
            elif record.status == 'in_progress':
                record.color = 2  # Blue
            elif record.status == 'complete':
                record.color = 10  # Green

    def _compute_todo_item_count(self):
        for record in self:
            record.todo_item_count = len(record.todo_item_ids)

    def _compute_completed_item_count(self):
        for record in self:
            record.completed_item_count = sum(1 for item in record.todo_item_ids if item.is_done)
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date < record.start_date:
                    raise ValidationError(_('End date must be greater than start date!'))
    
    def action_start_progress(self):
        self.write({'status': 'in_progress'})
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            user_id=self.user_id.id,
            note=_('Todo List has started. Please complete the tasks.')
        )
    
    def action_complete(self):
        if self.all_items_done:
            self.write({'status': 'complete'})
            self.activity_feedback(['mail.mail_activity_data_todo'])
        else:
            raise ValidationError(_('All items must be completed before marking the list as complete'))
    
    def write(self, vals):
        for record in self:
            if record.is_locked:
                raise ValidationError(_('Cannot modify a completed todo list'))
        return super(TodoList, self).write(vals)
    
    def unlink(self):
        for record in self:
            if record.is_locked:
                raise ValidationError(_('Cannot delete a completed todo list'))
        return super(TodoList, self).unlink()

    def action_view_todo_items(self):
        self.ensure_one()
        return {
            'name': _('Todo Items'),
            'type': 'ir.actions.act_window',
            'res_model': 'todo.item',
            'view_mode': 'tree,form',
            'domain': [('todo_list_id', '=', self.id)],
            'context': {'default_todo_list_id': self.id},
        }

class TodoTags(models.Model):
    _name = 'todo.tags'
    _description = 'Todo Tags'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color Index') 