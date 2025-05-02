from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Todo(models.Model):
    _name = 'todo.todo'
    _description = 'Todo Item'
    _order = 'priority desc, sequence, create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    user_id = fields.Many2one('res.users', string='Assigned To', default=lambda self: self.env.user, tracking=True)
    tag_ids = fields.Many2many('todo.tag', string='Tags')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string='Priority', default='1', tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
    progress = fields.Float(string='Progress', default=0.0)
    due_date = fields.Date(string='Due Date', tracking=True)
    color = fields.Integer(string='Color Index')
    create_date = fields.Datetime(string='Created On', readonly=True)
    write_date = fields.Datetime(string='Last Updated On', readonly=True)
    
    # New fields for collaboration
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    message_ids = fields.One2many('mail.message', 'res_id', string='Messages')
    activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities')
    follower_ids = fields.Many2many('res.partner', string='Followers')
    
    # New fields for recurring tasks
    is_recurring = fields.Boolean(string='Recurring Task')
    recurrence_rule = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], string='Recurrence')
    recurrence_interval = fields.Integer(string='Interval', default=1)
    next_recurrence_date = fields.Date(string='Next Recurrence Date')
    
    # New fields for calendar integration
    calendar_event_id = fields.Many2one('calendar.event', string='Calendar Event')
    is_all_day = fields.Boolean(string='All Day')
    start_datetime = fields.Datetime(string='Start Date/Time')
    end_datetime = fields.Datetime(string='End Date/Time')

    @api.constrains('progress')
    def _check_progress(self):
        for record in self:
            if record.progress < 0 or record.progress > 100:
                raise ValidationError(_('Progress must be between 0 and 100'))

    def action_start(self):
        self.write({'status': 'in_progress'})
        self._send_notification('started')

    def action_done(self):
        self.write({
            'status': 'done',
            'progress': 100
        })
        self._send_notification('completed')

    def action_cancel(self):
        self.write({'status': 'cancelled'})
        self._send_notification('cancelled')

    def action_reset(self):
        self.write({
            'status': 'draft',
            'progress': 0
        })
        self._send_notification('reset')

    def _send_notification(self, action):
        """Send notification to followers when task status changes"""
        message = {
            'started': _('Task has been started'),
            'completed': _('Task has been completed'),
            'cancelled': _('Task has been cancelled'),
            'reset': _('Task has been reset')
        }
        self.message_post(
            body=message.get(action, _('Task status has been updated')),
            message_type='notification',
            subtype_xmlid='mail.mt_comment'
        )

    def create_calendar_event(self):
        """Create calendar event for the task"""
        if not self.calendar_event_id:
            event = self.env['calendar.event'].create({
                'name': self.name,
                'start': self.start_datetime or fields.Datetime.now(),
                'stop': self.end_datetime or (fields.Datetime.now() + timedelta(hours=1)),
                'allday': self.is_all_day,
                'description': self.description,
                'user_id': self.user_id.id,
                'partner_ids': [(4, partner.id) for partner in self.follower_ids],
            })
            self.calendar_event_id = event.id

    def generate_recurring_task(self):
        """Generate next recurring task"""
        if self.is_recurring and self.next_recurrence_date:
            new_task = self.copy({
                'status': 'draft',
                'progress': 0,
                'create_date': fields.Datetime.now(),
                'write_date': fields.Datetime.now(),
            })
            
            # Calculate next recurrence date
            if self.recurrence_rule == 'daily':
                delta = timedelta(days=self.recurrence_interval)
            elif self.recurrence_rule == 'weekly':
                delta = timedelta(weeks=self.recurrence_interval)
            elif self.recurrence_rule == 'monthly':
                delta = timedelta(days=30 * self.recurrence_interval)
            else:  # yearly
                delta = timedelta(days=365 * self.recurrence_interval)
                
            self.next_recurrence_date = self.next_recurrence_date + delta
            new_task.next_recurrence_date = self.next_recurrence_date

class TodoTag(models.Model):
    _name = 'todo.tag'
    _description = 'Todo Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color Index')
    todo_ids = fields.Many2many('todo.todo', string='Todos') 