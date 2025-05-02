odoo.define('todo_list.todo_list', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var Dialog = require('web.Dialog');
    var QWeb = core.qweb;

    var TodoWidget = Widget.extend({
        template: 'todo_list.todo_widget',
        events: {
            'click .o_todo_start': '_onStart',
            'click .o_todo_done': '_onDone',
            'click .o_todo_cancel': '_onCancel',
            'click .o_todo_reset': '_onReset',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.todo = options.todo;
        },

        start: function () {
            this.$el.find('.o_progressbar').progressbar({
                value: this.todo.progress,
                max: 100
            });
        },

        _onStart: function () {
            this._rpc({
                model: 'todo.todo',
                method: 'action_start',
                args: [[this.todo.id]]
            });
        },

        _onDone: function () {
            this._rpc({
                model: 'todo.todo',
                method: 'action_done',
                args: [[this.todo.id]]
            });
        },

        _onCancel: function () {
            this._rpc({
                model: 'todo.todo',
                method: 'action_cancel',
                args: [[this.todo.id]]
            });
        },

        _onReset: function () {
            this._rpc({
                model: 'todo.todo',
                method: 'action_reset',
                args: [[this.todo.id]]
            });
        },
    });

    core.action_registry.add('todo_list', TodoWidget);

    return {
        TodoWidget: TodoWidget,
    };
}); 