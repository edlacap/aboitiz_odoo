odoo.define("fg_backend_custom.ir_options", function (require) {
    "use strict";
    var rpc = require("web.rpc");

    return rpc.query({
        model: "ir.config_parameter",
        method: "get_web_m2x_options",
    });
});
