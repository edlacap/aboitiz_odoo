odoo.define('fg_custom.ReceiptScreen', function(require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');

    const { useRef, useContext } = owl.hooks;
    const { useErrorHandlers, onChangeOrder } = require('point_of_sale.custom_hooks');

    const _super_posmodel = models.PosModel.prototype;
    const PosResReceiptScreen = ReceiptScreen =>
        class extends ReceiptScreen {
            /**
             * @override
             */
             async mounted() {
                var self = this;
                const order = self.currentOrder;
                var old_name = order.name
                const data = await self._getSiTransSequence(old_name);
                if(data){
                    order.pos_trans_reference = data.pos_trans_reference;
                    order.pos_si_trans_reference = data.pos_si_trans_reference;
                    order.pos_refund_si_reference = data.pos_refund_si_reference;
                    order.pos_refunded_id = data.pos_refunded_id;
                    self.render();
                }
                setTimeout(async () => {
                    let images = this.orderReceipt.el.getElementsByTagName('img');
                    for(let image of images) {
                        await image.decode();
                    }
                    await this.handleAutoPrint();
                }, 300);
            }

            async _getSiTransSequence(name) {
                var self = this;
                const data = await this.rpc({
                    model: 'pos.order',
                    method: 'get_si_trans_sequence_number',
                    args: [0, name],
                });
                return data;
            }

            async printReceipt() {
                var isPrinted = await super._printReceipt();
                this.currentOrder._printed = false;
                if(isPrinted && !this.currentOrder.x_receipt_printed){
                    this.currentOrder.x_receipt_printed = true;
                    this.currentOrder.trigger('change', this.currentOrder); // needed so that export_to_JSON gets triggered
                    this.currentOrder.x_receipt_printed_date = new Date();
                    this.render();
                    this.currentOrder.save_to_db();
                    this.env.pos.push_orders(this.currentOrder, {});
                }
            }
        };

    Registries.Component.extend(ReceiptScreen, PosResReceiptScreen);

    return ReceiptScreen;
});


