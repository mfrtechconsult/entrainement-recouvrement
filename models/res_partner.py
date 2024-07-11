from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    dossier_crediteur_ids = fields.One2many('recouvrement.dossier', 'crediteur_id', string='Dossiers de recouvrement (Créditeur)')
    dossier_debiteur_ids = fields.One2many('recouvrement.dossier', 'debiteur_id', string='Dossiers de recouvrement (Débiteur)')
    dossier_ids = fields.Many2many('recouvrement.dossier', string='Dossiers de recouvrement', compute='_compute_dossier_ids')

    def _compute_dossier_ids(self):
        for partner in self:
            dossiers = self.env['recouvrement.dossier'].search([
                '|',
                ('crediteur_id', '=', partner.id),
                ('debiteur_id', '=', partner.id)
            ])
            partner.dossier_ids = dossiers
