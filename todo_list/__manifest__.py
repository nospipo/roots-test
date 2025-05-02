{
    'name': 'Todo List',
    'version': '1.0',
    'category': 'Productivity',
    'summary': 'Manage your todo lists',
    'description': """
        This module allows you to manage your todo lists with the following features:
        - Create and manage todo items
        - Assign tags to todos
        - Track status (draft, in progress, complete)
        - Set start and end dates
        - Assign to users
        - Add todo items with inline editing
        - Mark items as done when in progress
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/todo_tags_data.xml',
        'views/todo_list_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 