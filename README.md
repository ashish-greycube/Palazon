# GreyCube Technologies Ltd.

## App Name - Palazon
**Description** - Get BOM Item Rate based on summation of their individual line item for Sales Order and Quotation. Custom Print format which shows sub bom leaf items.

## How to install app
- [ ] Go to bench directory i.e  /home/ubuntu/frappe-bench
- [ ] ~/frappe-bench$   bench get-app palazon https://github.com/ashish-greycube/palazon
- [ ] ~/frappe-bench$   bench --site site1.local install-app palazon
- [ ] ~/frappe-bench$   bench --site site1.local migrate
- [ ] ~/frappe-bench$   bench clear-cache
- [ ] ~/frappe-bench$   bench restart

#### Edit sales_order.py and quotation.py
Following line is to be added to sales_order.py and quotation.py

```
	#start singapore - exploded bom
	from palazon.api import set_missing_item_details, set_items_amount, set_items
	#end singapore - exploded bom

```
[a] apps/erpnext/selling/doctype/sales_order/sales_order.py

sales_order.py before changes
![Image](before_so.png)

sales_order.py after changes
![Image](after_so.png)
```
class SalesOrder(SellingController):
	def __init__(self, *args, **kwargs):
		super(SalesOrder, self).__init__(*args, **kwargs)

	#start singapore - exploded bom
	from palazon.api import set_missing_item_details, set_items_amount, set_items
	#end singapore - exploded bom
	
	def validate(self):
		super(SalesOrder, self).validate()

```
[b] apps/erpnext/erpnext/selling/doctype/quotation.py

quotation.py before changes
![Image](before_qo.png)

quotation.py after changes
![Image](after_qo.png)
```
class Quotation(SellingController):

	#start singapore - exploded bom
	from palazon.api import set_missing_item_details, set_items_amount, set_items
	#end singapore - exploded bom
		
	def set_indicator(self):

```

## How to do bench update for future
- [ ] ~/frappe-bench/apps/erpnext$ git status
		modified:   erpnext/selling/doctype/sales_order/sales_order.py
		modified:   erpnext/selling/doctype/quotation/quotation.py

- [ ] ~/frappe-bench/apps/erpnext$ git stash

- [ ] Once update, is done i.e. ~/frappe-bench$ bench update
- [ ] Revert the stash changes back ~/frappe-bench/apps/erpnext$ git stash pop

#### License
MIT