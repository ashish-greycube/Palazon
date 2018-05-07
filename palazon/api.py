from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, comma_and, cint

#start singapore - exploded bom
@frappe.whitelist()
def set_missing_item_details(self, for_validate=False):
    force_item_fields = ("item_group", "barcode", "brand", "stock_uom")

    """set missing item values"""
    from erpnext.stock.get_item_details import get_item_details
    from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos

    if hasattr(self, "sales_order_detail_item"):
        parent_dict = {}
        for fieldname in self.meta.get_valid_columns():
            parent_dict[fieldname] = self.get(fieldname)

        if self.doctype in ["Quotation", "Sales Order"]:
            document_type = "{} Item".format(self.doctype)
            parent_dict.update({"document_type": document_type})

        for item in self.get("sales_order_detail_item"):
            if item.get("item_code"):
                args = parent_dict.copy()
                args.update(item.as_dict())

                args["doctype"] = self.doctype
                args["name"] = self.name

                if not args.get("transaction_date"):
                    args["transaction_date"] = args.get("posting_date")

                if self.get("is_subcontracted"):
                    args["is_subcontracted"] = self.is_subcontracted
                ret = get_item_details(args)

                for fieldname, value in ret.items():
                    if item.meta.get_field(fieldname) and value is not None:
                        item.set(fieldname, value)
                        if (item.get(fieldname) is None or fieldname in force_item_fields):
                            item.set(fieldname, value)
                        elif fieldname in ['cost_center', 'conversion_factor'] and not item.get(fieldname):
                            item.set(fieldname, value)
                        elif fieldname == "serial_no":
                            stock_qty = item.get("stock_qty") * -1 if item.get("stock_qty") < 0 else item.get("stock_qty")
                            if stock_qty != len(get_serial_nos(item.get('serial_no'))):
                                item.set(fieldname, value)

                if ret.get("pricing_rule"):
                    # if user changed the discount percentage then set user's discount percentage ?
                    item.set("discount_percentage", ret.get("discount_percentage"))
                    if ret.get("pricing_rule_for") == "Price":
                        item.set("pricing_list_rate", ret.get("pricing_list_rate"))

                    if item.price_list_rate:
                        item.rate = flt(item.price_list_rate *
                            (1.0 - (flt(item.discount_percentage) / 100.0)), item.precision("rate"))

                else:
                    if item.price_list_rate:
                        item.set("discount_percentage", ret.get("discount_percentage"))
                        item.rate = flt(item.price_list_rate *
                            (1.0 - (flt(item.discount_percentage) / 100.0)), item.precision("rate"))

                item.amount = flt(item.rate * item.qty,	item.precision("amount"))

@frappe.whitelist()
def set_items_amount(self):
    for i in self.get('items'):
        if i.item_code:
            amount=0
            bom_no = get_default_bom_item(i.item_code)
            if bom_no:
                i.rate=0
                i.amount=0

                for j in self.get('sales_order_detail_item'):
                    if j.bom_id==i.idx:
                        amount=amount+j.amount
                i.rate=amount/i.qty	
                i.amount=amount	



@frappe.whitelist()
def set_items(self,change_qty=0):
    self.set("sales_order_detail_item",[])
    for i in self.get('items'):
        if i.item_code:
            if i.qty==0:
                i.qty=1
            bom_no = get_default_bom_item(i.item_code)
            if bom_no:
                i.detail_id=i.idx
                from erpnext.manufacturing.doctype.bom.bom import get_bom_items_as_dict
                item_dict = get_bom_items_as_dict(bom_no, self.company, qty=i.qty,fetch_exploded = 1)
                
                # for item in sorted(item_dict.values(), key=lambda d: d['idx']):
                for item in item_dict.values():
                    if item.idx is None:
                        items_parent=bom_no+":"+item.item_name
                    else:
                        items_parent=item.item_name


                    self.append('sales_order_detail_item', {
                        'bom_id':i.idx,
                        'display_name':items_parent,
                        'bom_code':i.item_code,
                        'item_code': item.item_code,
                        'item_name': item.item_name,
                        'description': item.description,
                        'qty': item.qty,
                        'rate':item.rate,
                        'amount':item.amount,
                        'uom':item.stock_uom,
                        'conversion_factor':'1'						
                    })
            self.set_missing_item_details()
#end singapore - exploded bom

def get_default_bom_item(item_code):
	bom = frappe.get_all('BOM', dict(item=item_code, is_active=True),
			order_by='is_default desc')
	bom = bom[0].name if bom else None

	return bom					
