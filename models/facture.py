from odoo import models, fields

class Facture(models.Model):
    _name = 'recouvrement.facture'
    _description = 'Facture de recouvrement'

    name = fields.Char(string='Référence de la facture', required=True)
    dossier_id = fields.Many2one('recouvrement.dossier', string='Dossier', required=True, ondelete='cascade')
    montant = fields.Float(string='Montant', required=True)
    date_facture = fields.Date(string='Date de la facture', default=fields.Date.today)
    date_echeance = fields.Date(string='Date d\'échéance', required=True)
    fichier = fields.Binary(string='Fichier de la facture')
    fichier_name = fields.Char(string='Nom du fichier')
