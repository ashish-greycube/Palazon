## Palazon

get BOM Item Rate based on summation of their individual line item

#### License

MIT

#### Changes to be done apps/erpnext/erpnext/selling/doctype/sales_order.py

class SalesOrder(SellingController):
	def __init__(self, *args, **kwargs):
		super(SalesOrder, self).__init__(*args, **kwargs)

	#start singapore - exploded bom
	from palazon.api import set_missing_item_details, set_items_amount, set_items
	#end singapore - exploded bom
	
	def validate(self):