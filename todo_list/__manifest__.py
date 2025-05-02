{
    'name': 'Todo List',
    'version': '1.0',
    'category': 'Productivity',
    'summary': 'A simple and effective todo list management system',
    'description': """
        This module provides a comprehensive todo list management system with the following features:
        - Create, read, update, and delete todo items
        - Track task status and progress
        - Set priorities and due dates
        - Organize tasks with tags
        - Color coding for better visualization
        - Kanban view for task management
        - Notifications and collaboration
        - Recurring tasks
        - Calendar integration
        - File attachments
        - Multi-language support
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'web', 'mail', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_views.xml',
        'views/todo_menu.xml',
        'views/todo_templates.xml',
        'data/todo_data.xml',
        'reports/todo_reports.xml',
        'reports/todo_report_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'todo_list/static/src/js/todo_list.js',
            'todo_list/static/src/css/todo_list.css',
        ],
    },
} 