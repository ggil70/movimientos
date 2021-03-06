# -*- coding: utf-8 -*-
##############################################################################
#
#    odoo, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# Generated by the Odoo plugin for Dia !
from odoo.osv import fields, osv, orm
from odoo import api, fields, models
from odoo.osv.orm import except_orm
from odoo.exceptions import ValidationError,except_orm, Warning, RedirectWarning

#Importamos la libreria logger
import logging
#Definimos la Variable Global
_logger = logging.getLogger(__name__)  
global res, cod_movi
res = 0

#****************Tipos de Movimientos*******************#
class movimiento(models.Model):
    """Registra los Tipos movimientos de bienes"""
    _name = 'movimiento'
    _rec_name = 'nom_mov'
    nom_mov = fields.Char('Nombre del Movimiento',size=100,required=True, help='Registra el Nombre del Movimiento')
    cod_mov = fields.Char('Codigo del Movimiento',size=100,required=True, help='Registra el Codigo del Movimiento ')
    sw_desin = fields.Boolean ('Desincorporado', help='Registra si el bien fue Desincorporado')
    _sql_constraints = [('nom_mov', 'unique(nom_mov)', 'El Nombre del Movimiento debe ser Unico!')]  



#****************Enten Externos a quien se le Envian Bienes*******************#

class ente_externo(models.Model):
    """Registra los Entes Externos"""
    _name = 'ente_externo'
    _rec_name = 'ente_externo_nombre'
    ente_externo_rif = fields.Char('Rif' ,help='Registra el Rif del Ente Externo')
    ente_externo_cedula = fields.Char('Cedula del Funcionario Responsable' ,help='Registra la Cedula  Funcionario Responsable del Ente Externo')
    ente_externo_nombre = fields.Char('Nombre del Funcionario Responsable',size=200,required=True, help='Registra el Nombre del Funcionario Responsable del Ente Externo')
    ente_externo_telf   = fields.Char('Telefono del Funcionario Responsable',size=100,required=True, help='Registra el Numero de telefono del Funcionario Responsabledel Ente Externo')
    ente_externo_correo = fields.Char('Correo del Funcionario Responsable',size=200,required=True, help='Registra el Correo del Funcionario Responsable del Ente Externo')


#****************Pesonal que Autoriza los Movimientos*******************#

# class mov_autoriza(models.Model):  
#     _name = 'mov_autoriza'
#     _rec_name = 'autoriza_persona'
#     autoriza_grupo = fields.Many2one('grupo_bien','Grupo del bienes al que Autorizan',required=True,store = True)
#     autoriza_persona = fields.Many2one('personas','Persona que  Autoriza',required=True,store = True)
                


#****************Detalle de los  Movimientos*******************#
class mov_deta(models.Model):
    #_inherit ='bienes'
    """Registra el detalle de los movimientos"""
    _name = 'mov_deta'
    _rec_name = 'movimiento_id'
    global res
    res = ()
  
    bienes_ids = fields.Many2many('bienes','bienes_numbien', help='Registra el Numero de Bien')
    bi_nombre = fields.Char('Descripcion del Bien', help='Descripcion del Bien')
    bi_fecha_inv = fields.Date('Fecha del Ultimo Movimiento del Bien')
    #bi_oficina_cedente = fields.Many2one('oficinas','Oficina Cedente',domain = "[('oficinas','=','bienes_id.oficinas_id')]")
    bi_oficina_cedente = fields.Many2one('oficinas','Oficina Cedente')
    #bi_resp_uso_cedente = fields.Many2one('personas','Responsable de Uso Cedente', domain = "[('personas','=','bienes_id.resp_uso_id')]")
    bi_resp_uso_cedente = fields.Many2one('personas','Responsable de Uso Cedente',domain="[('oficinas_id','=',bi_oficina_cedente)]")
    movimiento_id = fields.Many2one('movimiento','Nombre del Movimiento',required=True, help='Registra el codigo de Vinculacion con los Tipos de Movimientos ')
    movimiento_codigo = fields.Char(string='Codigo',related='movimiento_id.cod_mov', store= False)
    ofi_receptora = fields.Many2one('oficinas','Oficina Receptora',size=2, help='Registra la Oficina Receptora del Bien')
    resp_uso_receptor = fields.Many2one('personas','Responsable de uso Receptor',domain="[('oficinas_id','=',ofi_receptora)]",help='Registra el Responsable de uso Cedente del Bien')
    fecha_mov = fields.Date(string='Fecha del Movimiento',size=8,required=True, help='Registra la Fecha del Movimiento')    
    analista_bienes = fields.Many2one('personas','Analista de Bienes',domain="[('oficinas_id','=',12)]",required=True, help='Registra el Analista que realizo el Movimiento')
    nro_acta = fields.Text('Acta del Movimiento',help='Registra Acta del Movimiento')
    fecha_acta = fields.Date(string='Fecha del Acta',help='Registra la Fecha del Acta del Movimiento')
    ente_externo_id = fields.Many2one('ente_externo','Ente Externo',help='Registra el codigo de Vinculacion con los Entes Externos')
    observacion = fields.Text('Observacion', help='Observaciones')
    state = fields.Selection([('1','Registrado'),('2','Realizar Movimiento'),('3','Movimiento Realizado ')],'Estado')
  
    
  



    # @api.one 
    # @api.onchange('movimiento_id')
    # def generar_movimiento_compra(self):
    #     #cod_movi == self.movimiento_id.cod_mov
    #     if self.movimiento_id.cod_mov == '01':
    #        self.bi_oficina_cedente = 13
    #        self.ofi_receptora = 23
       
       
   


    @api.one 
    @api.onchange('fecha_mov')
    def validar_fecha(self):
       if  self.fecha_mov < self.bi_fecha_inv:
            raise ValidationError (
                "Error ! No puedes crear registros en donde la fecha del movimiento %s sea menor a la fecha del inventario" % (self.fecha_mov)
            )

         
   
    _defaults = { 
        'state': '1', }



    # @api.multi
    # @api.onchange('bi_oficina_cedente')
    # def generar_bien(self):
    #      self.bi_nombre = self.bienes_id.bienes_nombre
    #      self.bi_oficina_cedente = self.bienes_id.oficinas_id
    #      self.bi_resp_uso_cedente  = self.bienes_id.resp_uso_id
    #      self.bi_fecha_inv = self.bienes_id.fech_inventario
    
    
    # @api.multi
    # def mover(self):
    #      if self.movimiento_id.cod_mov < '05' or self.movimiento_id.cod_mov <='10':
    #         recep = self.env['bienes'].search([('id','=',self.bienes_ids.id)])
    #         recep.oficinas_id = self.bi_ofi_receptora
    #         recep.resp_uso_id = self.resp_uso_receptor
         
    #      if self.movimiento_id.cod_mov >= '01' or self.movimiento_id.cod_mov <='09':
    #         recep.sw_desin = True

    #      self.state ="3"
        #write({'oficinas_id':ofi_re,'resp_uso_id':res_uso})


        #bienes_id.search([('bienes_id.bienes.id','=','mov_deta.bienes_id')])
        
        #bienes_id.write({'bienes_id.oficinas_id':'mov_deta.ofi_receptora'},{'bienes_id.resp_uso_id':'mov_deta. resp_uso_receptor'})




       #var = super(self, mov_deta)
 #       raise Warning("Esta Seguro de realizar el movimiento!")
 
 #       return False
        #return  {'warning': {'title': 'Advertencia', 'message': 'Esta Seguro de realizar el movimiento!'},}
 
######################################################################
