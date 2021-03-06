from odoo import models, fields, _
from odoo.exceptions import UserError


class ChangeLockDate(models.TransientModel):
    _name = 'change.lock.date'
    _description = 'Change Lock Date'

    period_lock_date = fields.Date(string='Lock Date for Non-Advisers',
        default=lambda self: self.env.user.company_id.period_lock_date,
        help='Only users with the Adviser role can edit accounts prior to and inclusive of this date. '
             'Use it for period locking inside an open fiscal year, for example.')
    fiscalyear_lock_date = fields.Date(string='Lock Date for All Users',
        default=lambda self: self.env.user.company_id.fiscalyear_lock_date,
        help='No users, including Advisers, can edit accounts prior to and inclusive of this date. '
             'Use it for fiscal year locking for example.')

    def update_lock_date(self):
        if self.user_has_groups('account.group_account_manager'):
            self.env.user.company_id.sudo().write({
                'period_lock_date': self.period_lock_date,
                'fiscalyear_lock_date': self.fiscalyear_lock_date,
            })
        else:
            raise UserError(_('Only Billing Administrators are allowed to change lock dates!'))
        return {'type': 'ir.actions.act_window_close'}
