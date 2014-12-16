define(function (require) {
    var $ = require('jquery'),
        lib = require('./lib'),
        Chart = require('./controller/chart'),
        DataProvider = require('./providers/activity'),
        PointModifier = require('./modifiers/pointmodifier'),
        InfoModifier = require('./modifiers/infomodifier');


    function Demo(elt){
        this.$elt = $(elt);
    };

    Demo.prototype = {
        run: function(){
            var provider = new DataProvider();
            this.chart = new Chart();
            this.chart.Init({
                width: this.$elt.width(),
                containerSelector: '.js-chart-selector'
            });

            var boundUpdate = this.update.bind(this);

            provider.requestData()
                .done(boundUpdate);
        },

        update: function(data){
            var values = PointModifier.modify(data),
                info = InfoModifier.modify(data);

            this.chart.render(info, values)
        }
    }

    return Demo;
});
