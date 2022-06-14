# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-11-07
#    Author : Fabio Colognesi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError


class AddPickingToDdt(models.TransientModel):
    _inherit = "add.pickings.to.ddt"

    @property
    def lock_on_payment_terms(self):
        return self.env['res.config.settings'].lock_on_payment_terms()

    ##### Overriding standard methods ###

    @api.multi
    def add_to_ddt(self):
        pickings = self.env['stock.picking'].browse(
            self.env.context['active_ids']
        )

        if self.lock_on_payment_terms:
            sale_orders = {
                picking.sale_id
                for picking in (pickings + self.ddt_id.picking_ids)
            }
            payment_terms = {
                sale_order.payment_term_id for sale_order in sale_orders
            }
            if len(payment_terms) > 1:
                raise UserError(
                    'Impossibile create DDT da movimenti di magazzino relativi'
                    ' a ordini di vendita con Termini di Pagamento diversi'
                )
            # end if

        for picking in pickings:
            # check if picking is already linked to a DDT
            self.env['stock.picking.package.preparation'].check_linked_picking(
                picking
            )
            current_ddt_shipping_partner = picking.get_ddt_shipping_partner()
            if picking.ddt_ids and self.ddt_id.id in [
                d.id for d in picking.ddt_ids
            ]:
                raise UserError(_("Picking %s already in TD") % picking.name)
            elif (
                current_ddt_shipping_partner != self.ddt_id.partner_shipping_id
            ):
                raise UserError(
                    _("Selected Picking %s have" " different Partner")
                    % picking.name
                )
            if picking.sale_id:
                if (
                    picking.sale_id.carriage_condition_id
                    and picking.sale_id.carriage_condition_id
                    != self.ddt_id.carriage_condition_id
                ):
                    raise UserError(
                        _(
                            "Sale order %s and DDT %s have"
                            " different carriage condition"
                        )
                        % (
                            picking.sale_id.display_name,
                            self.ddt_id.display_name,
                        )
                    )
                elif (
                    picking.sale_id.goods_description_id
                    and picking.sale_id.goods_description_id
                    != self.ddt_id.goods_description_id
                ):
                    raise UserError(
                        _(
                            "Sale order %s and DDT %s have "
                            "different goods description"
                        )
                        % (
                            picking.sale_id.display_name,
                            self.ddt_id.display_name,
                        )
                    )
                elif (
                    picking.sale_id.transportation_reason_id
                    and picking.sale_id.transportation_reason_id
                    != self.ddt_id.transportation_reason_id
                ):
                    raise UserError(
                        _(
                            "Sale order %s and DDT %s have"
                            " different transportation reason"
                        )
                        % (
                            picking.sale_id.display_name,
                            self.ddt_id.display_name,
                        )
                    )
                elif (
                    picking.sale_id.transportation_method_id
                    and picking.sale_id.transportation_method_id
                    != self.ddt_id.transportation_method_id
                ):
                    raise UserError(
                        _(
                            "Sale order %s and DDT %s have"
                            " different transportation method"
                        )
                        % (
                            picking.sale_id.display_name,
                            self.ddt_id.display_name,
                        )
                    )
            self.ddt_id.picking_ids = [(4, picking.id)]
        ir_model_data = self.env['ir.model.data']
        form_res = ir_model_data.get_object_reference(
            'stock_picking_package_preparation',
            'stock_picking_package_preparation_form',
        )
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(
            'stock_picking_package_preparation',
            'stock_picking_package_preparation_tree',
        )
        tree_id = tree_res and tree_res[1] or False
        return {
            'name': _('TD'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'stock.picking.package.preparation',
            'res_id': self.ddt_id.id,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }


##### Overriding standard methods ###