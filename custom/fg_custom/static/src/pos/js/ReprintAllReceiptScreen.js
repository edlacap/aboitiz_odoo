odoo.define('point_of_sale.ReprintAllReceiptScreen', function (require) {
    'use strict';

    const AbstractReceiptScreen = require('point_of_sale.AbstractReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const ReprintAllReceiptScreen = (AbstractReceiptScreen) => {
        class ReprintAllReceiptScreen extends AbstractReceiptScreen {
            mounted() {
                this.printReceipt();
            }
            confirm() {
                this.showScreen('TicketScreen', { reuseSavedUIState: true });
            }
            async printReceipt() {
                if(this.env.pos.proxy.printer && this.env.pos.config.iface_print_skip_screen) {
                    let result = await this._printReceipt();
                    if(result)
                        this.showScreen('TicketScreen', { reuseSavedUIState: true });
                }
            }
            async tryReprint() {
                await this._printReceipt();
            }
            async DownloadTxtFile() {
                if($('.pos-receipt-container').length > 0){
                     const link = document.createElement("a");
                     var content = $('.pos-receipt-container')[0].innerText;
                     content = content.replaceAll("\n\n\n\n", "\n\n");
                     content = content.replaceAll("\n@\n", " @ ");
                     content = content.replaceAll("-----\n------------", "-----------------");
                     content = content.replaceAll("Item(s)\n", "Item(s)  ");
                     content = content.replaceAll("TOTAL DUE\n", "TOTAL DUE  ");
                     content = content.replaceAll("Cash\n", "Cash  ");
                     content = content.replaceAll("Change Amount\n", "Change Amount  ");
                     content = content.replaceAll("VAT-Exempt (E)\n", "VAT-Exempt (E)  ");
                     content = content.replaceAll("VAT Zero-Rated (Z)\n", "VAT Zero-Rated (Z)  ");
                     content = content.replaceAll("VATable (V)\n", "VATable (V)  ");
                     content = content.replaceAll("VAT\n", "VAT  ");
                     content = content.replaceAll("Cust Name:\n", "Cust Name:");
                     content = content.replaceAll("Address:\n", "Address:");
                     content = content.replaceAll("TIN:\n", "TIN:");
                     content = content.replaceAll("Bus Style:\n", "Bus Style:");
                     const file = new Blob([content], { type: 'text/plain' });
                     link.href = URL.createObjectURL(file);
                     link.download = "pos-receipt.txt";
                     link.click();
                     URL.revokeObjectURL(link.href);
                     $(link).remove();
                }
            }
        }
        ReprintAllReceiptScreen.template = 'ReprintAllReceiptScreen';
        return ReprintAllReceiptScreen;
    };
    Registries.Component.addByExtending(ReprintAllReceiptScreen, AbstractReceiptScreen);

    return ReprintAllReceiptScreen;
});
