import re
from odoo import models, fields, api

class Dossier(models.Model):
    _name = 'recouvrement.dossier'
    _description = 'Dossier de recouvrement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Référence', required=True)
    crediteur_id = fields.Many2one('res.partner', string='Créditeur', required=True, domain=[('is_company', '=', True)])
    debiteur_id = fields.Many2one('res.partner', string='Débiteur', required=True)
    montant = fields.Float(string='Montant total dû', compute='_compute_montant_total', store=True)
    montant_recouvre = fields.Float(string='Montant recouvré', compute='_compute_montant_recouvre', store=True)
    date_creation = fields.Date(string='Date de création', default=fields.Date.today)
    date_cloture = fields.Date(string='Date de clôture')
    status = fields.Selection([('open', 'Ouvert'), ('closed', 'Fermé')], string='Statut', default='open')
    factures_ids = fields.One2many('recouvrement.facture', 'dossier_id', string='Factures')
    paiements_ids = fields.One2many('recouvrement.paiement', 'dossier_id', string='Paiements')
    next_action_date = fields.Date(string='Date de la prochaine action')
    active = fields.Boolean(string='Active', default=True)

    @api.depends('factures_ids.montant')
    def _compute_montant_total(self):
        for dossier in self:
            dossier.montant = sum(facture.montant for facture in dossier.factures_ids)

    @api.depends('paiements_ids.montant')
    def _compute_montant_recouvre(self):
        for dossier in self:
            dossier.montant_recouvre = sum(paiement.montant for paiement in dossier.paiements_ids)

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """Extract the dossier ID from the subject and attach the email to the correct dossier"""
        subject = msg_dict.get('subject', '')
        match = re.search(r'\[#(\d+)\]', subject)
        if match:
            dossier_id = int(match.group(1))
            dossier = self.browse(dossier_id)
            if dossier:
                msg_dict['model'] = 'recouvrement.dossier'
                msg_dict['res_id'] = dossier.id
        return super(Dossier, self).message_new(msg_dict, custom_values)


class Action(models.Model):
    _name = 'recouvrement.action'
    _description = 'Action de recouvrement'

    dossier_id = fields.Many2one('recouvrement.dossier', string='Dossier', required=True, ondelete='cascade')
    date_action = fields.Date(string='Date de l\'action', default=fields.Date.today)
    description = fields.Text(string='Description de l\'action')
    type_action = fields.Selection([('call', 'Appel téléphonique'), ('email', 'Email'), ('visit', 'Visite'), ('other', 'Autre')], string='Type d\'action', required=True)
    next_action_date = fields.Date(string='Date de la prochaine action')

    @api.model
    def create(self, vals):
        res = super(Action, self).create(vals)
        if 'next_action_date' in vals:
            dossier = self.env['recouvrement.dossier'].browse(vals['dossier_id'])
            dossier.next_action_date = vals['next_action_date']
            dossier.save()
        return res
