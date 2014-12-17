define(function (require) {
    var $ = require('jquery'),
        Provider= require('./providers/activity')
        $elt = $('.js-stats-container');

    var provider = new Provider();

    // append the path where the main modules are at.
    var loadMe = ('./' + $elt.data('load').replace(',', ',./'));
    var modules = loadMe.split(',');

    require(modules, function(){
        var simulations = [];
        $.each(arguments, function(i, Simulation){
            var demo = new Simulation($elt);
            demo.init();

            simulations.push(demo);
        })

        provider.requestData()
            .done(function(data){
                simulations.forEach(function(s){ s.update(data); });
            });
    });

});
