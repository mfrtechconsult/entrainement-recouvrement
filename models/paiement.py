from odoo import models, fields

class Paiement(models.Model):
    _name = 'recouvrement.paiement'
    _description = 'Paiement de recouvrement'

    name = fields.Char(string='Référence de paiement', required=True)
    dossier_id = fields.Many2one('recouvrement.dossier', string='Dossier', required=True)
    montant = fields.Float(string='Montant', required=True)
    date_paiement = fields.Date(string='Date de paiement', default=fields.Date.today)
    moyen_paiement = fields.Selection([('agency', 'A l\'agence'), ('creditor', 'Au créancier')], required=True)
