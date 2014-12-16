define(function (require) {
    var $ = require('jquery'),
        Demo = require('./demo'),
        Dynamic = require('./dynamic'),
        Provider= require('./providers/activity')
        $elt = $('.js-stats');

    var pointChart = new Demo($elt),
        dynamic = new Dynamic($elt),
        provider = new Provider();

    pointChart.init();
    dynamic.init();

    provider.requestData()
        .done(function(data){
            pointChart.update(data);
            dynamic.update(data);
        });
});
