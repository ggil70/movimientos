# -*- coding: utf-8 -*-

#from odoo.osv import fields, osv, orm
from odoo import api, fields, models

class reportes_movDeta(report_sxw.rml_parse):
	def __init__(self,cr,uid,name,context):
		super(reportes_movDeta,self).__init__(cr,uid,name,context)

class reporte_formato(models.AbstractModel):
	_name="report.movimientos.detalle_mov"	
	_inherit="report.abstract_report"
	_template="movimientos.detalle_mov"
	_wrapped_report_class=reportes_movDeta
