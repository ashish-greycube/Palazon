## Palazon

get BOM Item Rate based on summation of their individual line item

#### License

MIT

#### How to do bench update
~/frappe-bench/apps/erpnext$ git status
		modified:   erpnext/selling/doctype/sales_order/sales_order.py
~/frappe-bench/apps/erpnext$ git stash

Once update, is done i.e.
~/frappe-bench$ bench update

Revert the stash changes back
~/frappe-bench/apps/erpnext$ git stash pop

#### Changes to be done apps/erpnext/erpnext/selling/doctype/sales_order.py

class SalesOrder(SellingController):
	def __init__(self, *args, **kwargs):
		super(SalesOrder, self).__init__(*args, **kwargs)

	#start singapore - exploded bom
	from palazon.api import set_missing_item_details, set_items_amount, set_items
	#end singapore - exploded bom
	
	def validate(self):

#### Changes to be done apps/erpnext/erpnext/selling/doctype/quotation.py


class Quotation(SellingController):

	#start singapore - exploded bom
	from palazon.api import set_missing_item_details, set_items_amount, set_items
	#end singapore - exploded bom
		
	def set_indicator(self):