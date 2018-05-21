//singapore - exploded bom
frappe.ui.form.on("Quotation", {
    set_bom_amount: function (frm) {
        return frappe.call({
            method: "set_items_amount",
            doc: frm.doc,
            callback: function (r, rt) {
                refresh_field("items");
            }
        });
    },
    ignore_pricing_rule: function (frm) {
        return frappe.call({
            method: "set_items",
            doc: frm.doc,
            callback: function (r, rt) {
                refresh_field("quotation_detail_item");
                // frm.doc.set_bom_amount.click();
                refresh_field("items");
            }
        });
    }
});
//singapore - exploded bom
frappe.ui.form.on("Quotation Item", {
    //singapore - exploded bom

    before_items_remove: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        var child_tbl = frm.doc.quotation_detail_item || [];
        var child_tbl_len = child_tbl.length;

        while (child_tbl_len--) {
            if ((child_tbl[child_tbl_len].bom_id == row.idx)) {
                cur_frm.get_field("quotation_detail_item").grid.grid_rows[child_tbl_len].remove();

            }
        }
        cur_frm.refresh();
    },
    items_remove: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        return frappe.call({
            method: "set_items",
            doc: frm.doc,
            changed_qty: 0,
            callback: function (r, rt) {
                refresh_field("quotation_detail_item");
            }
        });
    },


    item_code: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        return frappe.call({
            method: "set_items",
            doc: frm.doc,
            changed_qty: 0,
            callback: function (r, rt) {
                refresh_field("quotation_detail_item");
            }
        });
    },
    qty: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        return frappe.call({
            method: "set_items",
            doc: frm.doc,
            changed_qty: 1,
            callback: function (r, rt) {
                refresh_field("quotation_detail_item");
            }
        });
    }
    //singapore - exploded bom

});