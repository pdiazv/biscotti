define(function (require) {
    var $ = require('jquery'),
        Chart = require('./controller/chart'),
        DataProvider = require('./providers/activity'),
        PointModifier = require('./modifiers/pointmodifier'),
        InfoModifier = require('./modifiers/infomodifier'),
        InfoCards = require('./controller/infocards');


    function Demo(elt){
        this.$elt = $(elt);
    };

    Demo.prototype = {
        init: function(){
            var paddingLeft = 100;
            this.cards = new InfoCards(this.$elt);
            this.chart = new Chart();
            this.chart.init({
                width: this.$elt.width() - paddingLeft,
                containerSelector: '.js-chart-container',
                weeklySelector: '.js-weekly-indicator'
            });
        },

        update: function(data){
            var values = PointModifier.modify(data),
                info = InfoModifier.modify(data);

            this.chart.render(info, values)
            this.cards.render(info);
        }
    }

    return Demo;
});
