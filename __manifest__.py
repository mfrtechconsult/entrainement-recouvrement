# __manifest__.py
{
    'name': 'Recouvrement',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Gestion des dossiers de recouvrement pour des agences de recouvrement',
    'description': """
    Module de gestion pour les agences de recouvrement.
    """,
    'depends': ['base', 'contacts', 'mail', 'partner_autocomplete'],
    'data': [
        'security/ir.model.access.csv',
        'data/email_templates.xml',
        'views/recouvrement_views.xml',
        'views/facture_views.xml',
        'views/paiement_views.xml',
        'views/contact_views.xml',
        'data/activity_type_data.xml',
    ],
    'installable': True,
    'application': True,
}
