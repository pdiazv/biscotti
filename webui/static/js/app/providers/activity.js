
define(['jquery'], function($){

    function DataProvider($elt){
        this.$elt = $elt;
    };

    DataProvider.prototype = {
        requestData: function(){
            var data = {
                type: this.$elt.data('type') || 'global',
                group: this.$elt.data('group') || null,
            };

            return $.get('/stats_data', data);
        }
    };

    return DataProvider;
});
