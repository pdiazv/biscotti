define(function (require) {
    var $ = require('jquery'),
        Chart = require('./controller/chart'),
        DataProvider = require('./providers/activity'),
        PointModifier = require('./modifiers/pointmodifier'),
        InfoModifier = require('./modifiers/infomodifier');


    function Demo(elt){
        this.$elt = $(elt);
    };

    Demo.prototype = {
        init: function(){
            this.chart = new Chart();
            this.chart.init({
                width: this.$elt.width(),
                containerSelector: '.js-chart-container',
                weeklySelector: '.js-weekly-indicator'
            });
        },

        update: function(data){
            var values = PointModifier.modify(data),
                info = InfoModifier.modify(data);

            this.chart.render(info, values)
        }
    }

    return Demo;
});
