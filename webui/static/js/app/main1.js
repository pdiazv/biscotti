define(function (require) {
    var $ = require('jquery'),
        Demo = require('./demo'),
        Dynamic = require('./dynamic'),
        Provider= require('./providers/activity')
        $elt = $('.js-stats');

    var demo = new Demo($elt),
        dynamic = new Dynamic($elt),
        provider = new Provider();

    demo.init();
    dynamic.init();

    provider.requestData()
        .done(function(data){
            demo.update(data);
            dynamic.update(data);
        });
});
