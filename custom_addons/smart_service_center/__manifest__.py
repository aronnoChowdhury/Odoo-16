{
    'name': 'Smart Service Center Management System', 
    'version': '16.0.1.0.0', 
    'category': 'Services/Service Center', 
    'summary': 'Next Gen-Service Center, Repair Tracking, Diagnostics, Automated Inventory & Invoicing', 
    'description': """
Smart Service Center Management System
======================================
An enterprise-grade, comprehensive repair and service management platform for Odoo 16.

Key Capabilities:
-----------------
* **Job Sheet / Service Order Lifecycle**:
  - Full repair lifecycle: Draft -> Diagnosing -> Quotation -> In Progress -> QC -> Ready -> Delivered.
  - Device Brand, Model, Serial/IMEI tracking, and Warranty validation.
* **Diagnostics & Quality Control (QC)**:
  - Technical diagnostic checklist and post-repair quality assurance verification.
* **Inventory & Spare Parts Automation**:
  - Track parts consumed during repair with automated warehouse stock depletion.
* **1-Click Smart Invoicing**:
  - Seamless generation of Customer Invoices (account.move) combining spare parts and labor charges.
* **Customer Transparency**:
  - Order tracking tokens and communication via Odoo Chatter (mail.thread).
""", 
'author': 'Aronno Chowdhury', 
'website': 'https://github.com/aronnoChowdhury', 
'license': 'LGPL-3', 
'depends': [
    'base', 'mail', 'product', 'stock', 'account',
], 

'data': [
    'security/ir.model.access.csv', 
    'views/service_device_brand_view.xml', 
    'views/service_menus.xml',
],
'demo':[], 
'installable': True, 
'application': True, 
'auto_install': False,
}