from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, comma_and, cint

#start singapore - exploded bom
def get_bom_items_as_tree_order(bom,qty):
    bom_list = []
    def _get_children(bom):
        # bom_list.append(bom)
        child_boms = frappe.db.sql("""select
                bom_item.item_code,
                item.item_code,
                item.item_name,
                item.default_bom,
                bom_item.bom_no as value,
                bom_item.qty * %(qty)s as qty,
                (select item from `tabBOM` where name = bom_item.parent ) as parent,
                bom_item.bom_no as child, 
                bom_item.rate,
                if(ifnull(bom_item.bom_no, "")!="", 1, 0) as expandable,
                item.image,
                item.description
                from `tabBOM Item` bom_item, tabItem item
                where bom_item.parent=%(bom)s
                and bom_item.item_code = item.name
                order by bom_item.idx
                """, {"qty": qty,"bom": bom }, as_dict=True)
        for child_bom in child_boms:
            if child_bom["expandable"] == 1:
                _get_children(child_bom["value"])
            else:
                bom_list.append(child_bom)

    _get_children(bom)

    return bom_list

@frappe.whitelist()
def set_missing_item_details(self, for_validate=False):
    force_item_fields = ("item_group", "barcode", "brand", "stock_uom")

    """set missing item values"""
    from erpnext.stock.get_item_details import get_item_details
    from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos

    if self.doctype == "Quotation":
        child_bom_table="quotation_detail_item"
    elif self.doctype == "Sales Order":
        child_bom_table="sales_order_detail_item"


    if hasattr(self, child_bom_table):
        parent_dict = {}
        for fieldname in self.meta.get_valid_columns():
            parent_dict[fieldname] = self.get(fieldname)

        if self.doctype in ["Quotation", "Sales Order"]:
            document_type = "{} Item".format(self.doctype)
            parent_dict.update({"document_type": document_type})

        for item in self.get(child_bom_table):
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

    if self.doctype == "Quotation":
        child_bom_table="quotation_detail_item"
    elif self.doctype == "Sales Order":
        child_bom_table="sales_order_detail_item"

    for i in self.get('items'):
        if i.item_code:
            amount=0
            bom_no = get_default_bom_item(i.item_code)
            if bom_no:
                i.rate=0
                i.amount=0

                for j in self.get(child_bom_table):
                    if j.bom_id==i.idx:
                        amount=amount+j.amount
                i.rate=amount/i.qty	
                i.amount=amount	



@frappe.whitelist()
def set_items(self,change_qty=0):

    if self.doctype == "Quotation":
        child_bom_table="quotation_detail_item"
    elif self.doctype == "Sales Order":
        child_bom_table="sales_order_detail_item"

    print("set_items")
    self.set(child_bom_table,[])
    for i in self.get('items'):
        if i.item_code:
            if i.qty==0:
                i.qty=1
            bom_no = get_default_bom_item(i.item_code)
            print(bom_no)
            if bom_no:
                i.detail_id=i.idx
                item_dict = get_bom_items_as_tree_order(bom_no,qty=i.qty)
                for item in item_dict:
                    # if item.idx is None:
                    #     items_parent=bom_no+":"+item.item_name
                    # else:
                    items_parent=item.item_name
                    self.append(child_bom_table, {
                        'bom_id':i.idx,
                        'display_name':items_parent,
                        'parent_bom':item.parent,
                        'parent_qty':i.qty,
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
