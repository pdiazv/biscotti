define(function (require) {
    var $ = require('jquery'),
        Demo = require('./demo'),
        Provider= require('./providers/activity')
        $elt = $('.js-stats');

    var demo = new Demo($elt),
        provider = new Provider();

    demo.init();

    provider.requestData()
        .done(function(data){
            demo.update(data);
        });
});
